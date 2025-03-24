import argparse
import asyncio
import time

import supriya

FREQUENCIES = [261.63, 329.63, 392.00]


def run_threaded() -> None:
    server = supriya.Server().boot()
    synths: list[supriya.Synth] = []
    with server.at():
        with server.add_synthdefs(supriya.default):
            for frequency in FREQUENCIES:
                synths.append(
                    server.add_synth(synthdef=supriya.default, frequency=frequency)
                )
    time.sleep(4)
    for synth in synths:
        synth.free()
    time.sleep(1)
    server.quit()


async def run_async() -> None:
    server = await supriya.AsyncServer().boot()
    synths: list[supriya.Synth] = []
    with server.at():
        with server.add_synthdefs(supriya.default):
            for frequency in FREQUENCIES:
                synths.append(
                    server.add_synth(synthdef=supriya.default, frequency=frequency)
                )
    await asyncio.sleep(4)
    for synth in synths:
        synth.free()
    await asyncio.sleep(1)
    await server.quit()


def run_nonrealtime() -> None:
    score = supriya.Score(output_bus_channel_count=2)
    synths: list[supriya.Synth] = []
    with score.at(0):
        with score.add_synthdefs(supriya.default):
            for frequency in FREQUENCIES:
                synths.append(
                    score.add_synth(synthdef=supriya.default, frequency=frequency)
                )
    with score.at(4):
        for synth in synths:
            synth.free()
    with score.at(5):
        score.do_nothing()
    supriya.play(score)


def parse_args(args: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="hello world!")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--realtime-threaded", action="store_true")
    group.add_argument("--realtime-async", action="store_true")
    group.add_argument("--nonrealtime", action="store_true")
    return parser.parse_args(args)


def main(args: list[str] | None = None) -> None:
    parsed_args = parse_args(args)
    if parsed_args.realtime_threaded:
        run_threaded()
    elif parsed_args.realtime_async:
        asyncio.run(run_async())
    else:
        run_nonrealtime()


if __name__ == "__main__":
    main()
