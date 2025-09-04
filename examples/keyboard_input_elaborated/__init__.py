"""
Keyboard input, elaborated.

Let's rewrite our keyboard example one more time, and make it into something
more polished.

We'll introduce limits on polyphony, craft a lusher-sounding instrumental
voice, add some effects and compression, and restructure our logic so it
starts to approach what a real musical application might look like.

Invoke with:

..  shell::
    :cwd: ..
    :rel: ..
    :user: josephine
    :host: laptop

    python -m examples.keyboard_input_elaborated --help

... to see complete options.

See the :doc:`example documentation </examples/keyboard_input_elaborated>` for a
complete explanation.
"""

import argparse
import asyncio
import dataclasses
import functools
import random
import signal
from typing import Literal

import rtmidi
import rtmidi.midiutil

import supriya

from ..keyboard_input import (
    InputHandler,
    MidiHandler,
    NoteOff,
    NoteOn,
    QwertyHandler,
)


def build_instrument_synthdef() -> supriya.SynthDef:
    """
    Build an instrument SynthDef.
    """
    with supriya.SynthDefBuilder(
        attack_time=0.1,
        bus=0,
        gain=0.0,
        gate=1,
        lowpass_frequency=5000.0,
        panning=0.0,
        pitch=69.0,
        pitch_detune=0.1,
    ) as builder:
        amplitude_envelope = (
            supriya.ugens.Linen.kr(
                attack_time=builder["attack_time"],
                done_action=supriya.DoneAction.FREE_SYNTH,
                gate=builder["gate"],
            )
            * builder["gain"].db_to_amplitude()
        )
        frequency_envelope = supriya.ugens.Linen.kr(
            attack_time=builder["attack_time"] * 2,
            gate=builder["gate"],
        ).scale(0.0, 1.0, 20.0, builder["lowpass_frequency"])
        source = supriya.ugens.Mix.new(
            [
                supriya.ugens.LFSaw.ar(
                    frequency=supriya.ugens.Vibrato.kr(
                        frequency=builder["pitch"].midi_to_hz(),
                        onset=0.5,
                    ),
                ),
                supriya.ugens.LFTri.ar(
                    frequency=(builder["pitch"] + builder["pitch_detune"]).midi_to_hz()
                ),
                supriya.ugens.LFTri.ar(
                    frequency=(builder["pitch"] - builder["pitch_detune"]).midi_to_hz()
                ),
            ]
        )
        source = supriya.ugens.RLPF.ar(
            frequency=frequency_envelope,
            reciprocal_of_q=0.5,
            source=source,
        )
        source = source.tanh()
        source *= (amplitude_envelope,)
        source = supriya.ugens.Pan2.ar(position=builder["panning"], source=source)
        supriya.ugens.Out.ar(
            bus=builder["bus"],
            source=source,
        )
    return builder.build(name="example:instrument")


def build_reverb_synthdef() -> supriya.SynthDef:
    """
    Build a reverb SynthDef with pitched-up granular halo feedback.
    """
    with supriya.SynthDefBuilder(bus=0, gate=1) as builder:
        bus = builder["bus"]
        source = supriya.ugens.LeakDC.ar(
            source=(
                supriya.ugens.In.ar(bus=bus, channel_count=2)
                + supriya.ugens.LocalIn.ar(channel_count=2)
            ).tanh()
        )
        reverb = supriya.ugens.FreeVerb.ar(
            damping=0.1,
            mix=1.0,
            room_size=0.99,
            source=source,
        )
        pitch_shifted_reverb = supriya.ugens.PitchShift.ar(
            pitch_dispersion=0.05,
            pitch_ratio=2.0,
            source=reverb,
            time_dispersion=0.25,
            window_size=0.25,
        )
        assert isinstance(pitch_shifted_reverb, supriya.ugens.UGenVector)
        feedback_source = supriya.ugens.LPF.ar(
            frequency=2500.0,
            source=supriya.ugens.FreqShift.ar(
                frequency=1.0,
                source=supriya.ugens.Rotate2.ar(
                    x=pitch_shifted_reverb[0],
                    y=pitch_shifted_reverb[1],
                    position=supriya.ugens.LFSaw.kr(frequency=5.0),
                ),
            ),
        )
        supriya.ugens.LocalOut.ar(source=feedback_source * -0.9)
        supriya.ugens.XOut.ar(
            bus=bus,
            crossfade=supriya.ugens.Linen.kr(
                done_action=supriya.DoneAction.FREE_SYNTH,
                gate=builder["gate"],
                release_time=0.25,
            )
            * 0.5,
            source=reverb,
        )
    return builder.build(name="example:reverb")


def build_compressor_synthdef() -> supriya.SynthDef:
    """
    Build a simple compressor SynthDef.
    """
    with supriya.SynthDefBuilder(bus=0, gate=1) as builder:
        bus = builder["bus"]
        supriya.ugens.XOut.ar(
            bus=bus,
            crossfade=supriya.ugens.Linen.kr(
                done_action=supriya.DoneAction.FREE_SYNTH,
                gate=builder["gate"],
                release_time=0.5,
            ),
            source=supriya.ugens.CompanderD.ar(
                slope_above=0.5,
                source=supriya.ugens.In.ar(bus=bus, channel_count=2),
                threshold=0.75,
            ),
        )
    return builder.build(name="example:compressor")


instrument_synthdef = build_instrument_synthdef()
reverb_synthdef = build_reverb_synthdef()
compressor_synthdef = build_compressor_synthdef()


# TODO: OK
#       Let's combine polyphonymanager into instrument
#       Handle monophonic instruments as first-class
#       And make an instrument that accepts:
#       - synthdef
#       - start note callable
#       - stop note callable
#       - update note callable (monophonic only)


@dataclasses.dataclass
class PolyphonyManager:
    """
    A polyphony manager.
    """

    polyphony_mode: Literal["oldest", "highest", "closest"] = "oldest"
    voice_count: int | None = None
    note_numbers: list[int] = dataclasses.field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        if self.voice_count is not None and self.voice_count < 1:
            raise ValueError("Voice count must be a None or a positive integer")

    def free_all(self) -> list[NoteOff]:
        events: list[NoteOff] = [
            NoteOff(note_number=note_number) for note_number in self.note_numbers
        ]
        self.note_numbers.clear()
        return events

    @functools.singledispatchmethod
    def __call__(self, event: NoteOn | NoteOff) -> list[NoteOn | NoteOff]:
        raise NotImplementedError

    @__call__.register
    def _(self, event: NoteOn) -> list[NoteOn | NoteOff]:
        events: list[NoteOn | NoteOff] = []
        old_note_number: int | None = None
        # already played, bail early
        if event.note_number in self.note_numbers:
            return events
        # make sure the NoteOn hits the instrument first
        # because this makes monophonic instruments simpler
        events.append(event)
        self.note_numbers.append(event.note_number)
        if self.voice_count and len(self.note_numbers) >= self.voice_count:
            print(f"Polyphony limit reached! {event.note_number} {self.note_numbers}")
            if self.polyphony_mode == "oldest":
                # drop the oldest note number
                old_note_number = self.note_numbers[0]
            elif self.polyphony_mode == "highest":
                # drop the highest note number
                old_note_number = sorted(self.note_numbers)[-1]
            elif self.polyphony_mode == "closest":
                # drop the note number closest to the new note number
                old_note_number = sorted(
                    self.note_numbers, key=lambda x: abs(event.note_number - x)
                )[0]
        if old_note_number is not None:
            self.note_numbers.remove(old_note_number)
            events.append(NoteOff(note_number=old_note_number))
        return events

    @__call__.register
    def _(self, event: NoteOff) -> list[NoteOn | NoteOff]:
        events: list[NoteOn | NoteOff] = []
        if event.note_number in self.note_numbers:
            self.note_numbers.remove(event.note_number)
            events.append(event)
        return events


@dataclasses.dataclass
class Instrument:
    """
    An instrument.
    """

    server: supriya.Context
    polyphony_manager: PolyphonyManager
    target_node: supriya.Node | None = None
    synthdef: supriya.SynthDef = dataclasses.field(
        default=instrument_synthdef, init=False
    )
    synths: dict[int, supriya.Synth] = dataclasses.field(
        default_factory=dict, init=False
    )

    @functools.singledispatchmethod
    def _handle_event(self, event) -> None:
        raise NotImplementedError

    @_handle_event.register
    def _(self, event: NoteOn) -> None:
        print(f"Performing {event}")
        self.synths[event.note_number] = self.server.add_synth(
            attack_time=((128 - event.velocity) / 127) ** 2.0,
            gain=supriya.conversions.midi_velocity_to_decibels(event.velocity),
            lowpass_frequency=((event.note_number + 12) / 127) * 10000.0,
            panning=(random.random() * 2.0) - 1.0,
            pitch=event.note_number,
            pitch_detune=random.random() * 0.5,
            synthdef=self.synthdef,
            target_node=self.target_node,
        )

    @_handle_event.register
    def _(self, event: NoteOff) -> None:
        print(f"Performing {event}")
        self.synths.pop(event.note_number).free()

    def __call__(self, event: NoteOn | NoteOff) -> None:
        with self.server.at():
            for event_ in self.polyphony_manager(event):
                self._handle_event(event_)

    def free_all(self) -> None:
        with self.server.at():
            for event_ in self.polyphony_manager.free_all():
                self._handle_event(event_)


@dataclasses.dataclass
class Application:
    """
    A performance application.
    """

    loop: asyncio.AbstractEventLoop
    input_handler: InputHandler
    polyphony_mode: dataclasses.InitVar[Literal["oldest", "highest", "closest"]] = (
        "oldest"
    )
    voice_count: dataclasses.InitVar[int | None] = None
    exit_future: asyncio.Future[bool] = dataclasses.field(init=False)
    instrument: Instrument = dataclasses.field(init=False)
    queue: asyncio.Queue[NoteOn | NoteOff] = dataclasses.field(
        default_factory=asyncio.Queue, init=False
    )
    server: supriya.AsyncServer = dataclasses.field(default_factory=supriya.AsyncServer)
    synths: list[supriya.Synth] = dataclasses.field(default_factory=list, init=False)
    tasks: set[asyncio.Task] = dataclasses.field(default_factory=set, init=False)

    def __post_init__(
        self,
        polyphony_mode: Literal["oldest", "highest", "closest"],
        voice_count: int | None,
    ) -> None:
        self.exit_future = self.loop.create_future()
        self.instrument = Instrument(
            polyphony_manager=PolyphonyManager(
                polyphony_mode=polyphony_mode,
                voice_count=voice_count,
            ),
            server=self.server,
        )

    async def run(self) -> None:
        # setup callbacks
        self.server.register_lifecycle_callback("BOOTED", self.on_boot)
        self.server.register_lifecycle_callback("QUITTING", self.on_quitting)
        # setup the Ctrl-C signal handler
        self.loop.add_signal_handler(signal.SIGINT, self.signal_handler)
        # start the queue consumer and save it to a set of background tasks
        self.tasks.add(self.loop.create_task(self.queue_consumer()))
        await self.server.boot()
        print("Server online. Press Ctrl-C to exit.")
        # start listening for input
        with self.input_handler.listen(callback=self.input_callback):
            await self.exit_future  # wait for Ctrl-C
        while self.tasks:  # cancel all background tasks
            self.tasks.pop().cancel()
        await self.server.quit()

    async def on_boot(self, *args) -> None:  # run this during server.boot()
        with self.server.at():
            with self.server.add_synthdefs(
                self.instrument.synthdef,
                compressor_synthdef,
                reverb_synthdef,
            ):
                self.instrument.target_node = self.server.add_group()
                self.synths.extend(
                    [
                        self.server.add_synth(
                            add_action=supriya.AddAction.ADD_TO_TAIL,
                            synthdef=reverb_synthdef,
                        ),
                        self.server.add_synth(
                            add_action=supriya.AddAction.ADD_TO_TAIL,
                            synthdef=compressor_synthdef,
                        ),
                    ],
                )
        await self.server.sync()  # wait for the synthdef to load before moving on
        print("Ready to play!")

    async def on_quitting(self, *args) -> None:  # run this during server.quit()
        print("Quitting ...")
        with self.server.at():
            self.instrument.free_all()  # free all the instrument's synths
            for synth in self.synths:  # free the effect synths
                synth.free()
        await asyncio.sleep(0.5)  # wait for them to fade out before moving on
        print("... quit!")

    def signal_handler(self, *args) -> None:
        self.exit_future.set_result(True)  # set the exit future flag

    def input_callback(self, event: NoteOn | NoteOff) -> None:
        # drop the event onto the queue
        self.loop.call_soon_threadsafe(self.queue.put_nowait, event)

    async def queue_consumer(self) -> None:
        while True:  # run forever
            # grab an event off the queue and play it
            self.instrument(await self.queue.get())


async def run(
    input_handler: InputHandler,
    polyphony_mode: Literal["oldest", "highest", "closest"],
    voice_count: int | None,
) -> None:
    application = Application(
        input_handler=input_handler,
        loop=asyncio.get_event_loop(),
        polyphony_mode=polyphony_mode,
        voice_count=voice_count,
    )
    await application.run()


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    """
    Parse CLI arguments.
    """
    parser = argparse.ArgumentParser(
        description="Play notes via your QWERTY or MIDI keyboards"
    )
    subparsers = parser.add_subparsers(
        dest="command", help="command to run", required=True
    )
    subparsers.add_parser("list-midi-inputs", help="list available MIDI inputs")
    qwerty_parser = subparsers.add_parser("use-qwerty", help="play via QWERTY keyboard")
    midi_parser = subparsers.add_parser("use-midi", help="play via MIDI keyboard")
    for subparser in [midi_parser, qwerty_parser]:
        subparser.add_argument(
            "--polyphony-mode",
            choices=["oldest", "highest", "closest"],
            default="oldest",
            metavar="MODE",
        )
        subparser.add_argument("--voice-count", metavar="COUNT", type=int)
    midi_parser.add_argument("--port", metavar="PORT", required=True, type=int)
    return parser.parse_args(args)


def main(args: list[str] | None = None) -> None:
    """
    The example entry-point function.
    """
    parsed_args = parse_args(args)
    if parsed_args.command == "list-midi-inputs":
        rtmidi.midiutil.list_input_ports()
        return
    input_handler: InputHandler
    if parsed_args.command == "use-midi":
        input_handler = MidiHandler(port=parsed_args.port)
    elif parsed_args.command == "use-qwerty":
        input_handler = QwertyHandler()
    else:
        raise ValueError("How did we get here?")
    asyncio.run(
        run(
            input_handler=input_handler,
            polyphony_mode=parsed_args.polyphony_mode,
            voice_count=parsed_args.voice_count,
        )
    )


if __name__ == "__main__":
    main()
