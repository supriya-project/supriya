import asyncio
import monome
import signal
import supriya
import sys

from supriya import ugens


def build_synthdef():
    def signal_block(builder, source, state):
        count = 8
        varsaws = supriya.ugens.VarSaw.ar(
            frequency=[
                ugens.Vibrato.kr(
                    frequency=builder["frequency"],
                    rate=ugens.Rand.ir(minimum=1, maximum=10),
                    depth=ugens.Rand.ir(0.0, 0.02),
                )
                for _ in range(count)
            ],
        )
        splayed = ugens.Splay.ar(source=varsaws)
        linen = ugens.Linen.kr(
            attack_time=ugens.Rand.ir(1, 3),
            done_action=supriya.DoneAction.FREE_SYNTH,
            gate=builder["gate"],
            release_time=ugens.Rand.ir(2, 5),
            sustain_level=1.0,
        )
        low_pass = ugens.LPF.ar(
            source=splayed * linen,
            frequency=linen.range(
                ugens.Rand.ir(100, 500),
                ugens.Rand.ir(3000, 6000),
            ),
        )
        return low_pass.tanh() / count * builder["amplitude"]

    factory = (
        supriya.SynthDefFactory(amplitude=0.1, frequency=440.0, gate=1)
        .with_channel_count(2)
        .with_output()
        .with_signal_block(signal_block)
    )
    return factory.build()


synthdef = build_synthdef()


class App(monome.GridApp):
    def __init__(self, provider):
        monome.GridApp.__init__(self)
        self.provider = provider
        self.synths = {}

    def on_grid_key(self, x, y, s):
        print(f"Grid key at {x}, {y}, {s}")
        with self.provider.at():
            if not s:
                return
            if not x and not y:
                for key in tuple(self.synths):
                    self.synths.pop(key).free()
                self.grid.led_all(0)
                return
            synth = self.synths.pop(f"{x}-{y}", None)
            if synth is not None:
                synth.free()
                self.grid.led_level_set(x, y, 0)
            else:
                frequency = supriya.conversions.midi_note_number_to_frequency(
                    ((x / 2) + 72) - (y / 8),
                )
                self.synths[f"{x}-{y}"] = self.provider.add_synth(
                    frequency=frequency,
                    level=0.1,
                    synthdef=synthdef,
                )
                self.grid.led_level_set(x, y, 15)

    def on_grid_ready(self):
        self.grid.led_all(0)


async def initialize():
    def serialosc_device_added(id, type, port):
        print("Connecting to {} ({})".format(id, type))
        asyncio.ensure_future(app.grid.connect("127.0.0.1", port))

    provider = await supriya.Provider.realtime_async()
    app = App(provider)
    serialosc = monome.SerialOsc()
    serialosc.device_added_event.add_handler(serialosc_device_added)
    await serialosc.connect()


async def shutdown(signal, loop):
    print(f"Received exit signal {signal.name}...")
    tasks = [
        task for task in asyncio.all_tasks() if task is not
        asyncio.current_task()
    ]
    [task.cancel() for task in tasks]
    print("Cancelling outstanding tasks")
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()


def main():
    loop = asyncio.get_event_loop()
    signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
    for s in signals:
        loop.add_signal_handler(
            s, lambda s=s: asyncio.create_task(shutdown(s, loop)))
    try:
        loop.create_task(initialize())
        loop.run_forever()
    finally:
        print("Successfully shutdown service")
        loop.close()
        sys.exit()


if __name__ == "__main__":
    main()
