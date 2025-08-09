"""
Keyboard input.

Let's play live with either a MIDI keyboard or our QWERTY keyboard.

Invoke with:

..  shell::
    :cwd: ..
    :rel: ..
    :user: josephine
    :host: laptop

    python -m examples.keyboard_input --help

... to see complete options.

See the :doc:`example documentation </examples/keyboard_input>` for a complete
explanation.
"""

import argparse
import concurrent.futures
import contextlib
import dataclasses
import functools
import random
import signal
import time
from typing import Callable, Generator

import pynput
import rtmidi
import rtmidi.midiconstants
import rtmidi.midiutil

import supriya


@dataclasses.dataclass
class NoteOn:
    """
    A note on event.
    """

    note_number: int
    velocity: int


@dataclasses.dataclass
class NoteOff:
    """
    A note off event.
    """

    note_number: int


@dataclasses.dataclass
class PolyphonyManager:
    """
    A polyphony manager.

    Translates :py:class:`NoteOn` or :py:class:`NoteOff` events into actions
    against a :py:class:`~supriya.contexts.core.Context`.
    """

    # the server to act on
    server: supriya.Context
    # a dictionary of MIDI note numbers to synths
    notes: dict[int, supriya.Synth] = dataclasses.field(default_factory=dict)
    # a synthdef to use when making new synths
    synthdef: supriya.SynthDef = dataclasses.field(default=supriya.default)
    # target node to add relative to
    target_node: supriya.Node | None = None
    # add action to use
    add_action: supriya.AddAction = supriya.AddAction.ADD_TO_HEAD

    def free_all(self) -> None:
        """
        Free all currently playing :py:class:`~supriya.contexts.entities.Synth`
        instances.
        """
        with self.server.at():
            for synth in self.notes.values():
                synth.free()

    def perform(self, event: NoteOn | NoteOff) -> None:
        """
        Perform a :py:class:`NoteOn` or :py:class:`NoteOff` event.
        """
        # if we're starting a note ...
        if isinstance(event, NoteOn):
            # bail if we already started this note
            if event.note_number in self.notes:
                return
            print(f"Performing {event}")
            # convert MIDI 0-127 to frequency in Hertz
            frequency = supriya.conversions.midi_note_number_to_frequency(
                event.note_number
            )
            # convert MIDI 0-127 to amplitude
            amplitude = supriya.conversions.midi_velocity_to_amplitude(event.velocity)
            # create a synth and store a reference by MIDI note number in the
            # dictionary ...
            self.notes[event.note_number] = self.server.add_synth(
                add_action=self.add_action,
                amplitude=amplitude,
                frequency=frequency,
                synthdef=self.synthdef,
                target_node=self.target_node,
            )
        # if we're stopping a note ...
        elif isinstance(event, NoteOff):
            # bail if we already stopped this note:
            if event.note_number not in self.notes:
                return
            print(f"Performing {event}")
            # pop the synth out of the dictionary and free it ...
            self.notes.pop(event.note_number).free()


@dataclasses.dataclass
class InputHandler:
    """
    Base class for input handlers.
    """

    @contextlib.contextmanager
    def listen(
        self, callback: Callable[[NoteOn | NoteOff], None]
    ) -> Generator[None, None, None]:
        # subclasses must implement this method!
        # 1) start the handler's listener
        # 2) yield to the with block body
        # 3) stop the handler's listener
        raise NotImplementedError


@dataclasses.dataclass
class MidiHandler(InputHandler):
    """
    A MIDI input handler.
    """

    port: int | str

    @contextlib.contextmanager
    def listen(
        self, callback: Callable[[NoteOn | NoteOff], None]
    ) -> Generator[None, None, None]:
        """
        Context manager for listening to MIDI input events.
        """
        self.midi_input = rtmidi.MidiIn()  # create the MIDI input
        # set the MIDI event callback to this class's __call__
        self.midi_input.set_callback(functools.partial(self.handle, callback))
        self.midi_input.open_port(self.port)  # open the port for listening
        print("Listening for MIDI keyboard events ...")  # let the user know
        yield  # yield to the with block body
        self.midi_input.close_port()  # close the port

    def handle(
        self,
        callback: Callable[[NoteOn | NoteOff], None],
        event: tuple[tuple[int, int, int], float],
        *args,
    ) -> None:
        """
        Handle a MIDI input event.
        """
        print(f"MIDI received: {event}")
        # the raw MIDI event is a 2-tuple of MIDI data and time delta, so
        # unpack it, keep the data and discard the time delta ...
        data, _ = event
        if data[0] == rtmidi.midiconstants.NOTE_ON:  # if we received a note-on ...
            # grab the note number and velocity
            _, note_number, velocity = data
            # perform a "note on" event
            callback(NoteOn(note_number=note_number, velocity=velocity))
        elif data[0] == rtmidi.midiconstants.NOTE_OFF:  # if we received a note-off ...
            # grab the note number
            _, note_number, _ = data
            # perform a "note off" event
            callback(NoteOff(note_number=note_number))


@dataclasses.dataclass
class QwertyHandler(InputHandler):
    """
    A QWERTY input handler.
    """

    octave: int = 5
    presses_to_note_numbers: dict[str, int] = dataclasses.field(default_factory=dict)

    @contextlib.contextmanager
    def listen(
        self, callback: Callable[[NoteOn | NoteOff], None]
    ) -> Generator[None, None, None]:
        """
        Context manager for listening to QWERTY input events.
        """
        # setup the QWERTY keybord listener
        self.listener = pynput.keyboard.Listener(
            on_press=functools.partial(self.on_press, callback),
            on_release=functools.partial(self.on_release, callback),
        )
        self.listener.start()  # start the listener
        print("Listening for QWERTY keyboard events ...")  # let the user know
        yield  # yield to the with block body
        self.listener.stop()  # stop the listener

    @staticmethod
    def qwerty_key_to_pitch_number(key: str) -> int | None:
        """
        Translate a QWERTY key event into a pitch number.
        """
        # dict lookups are faster, but this is soooo much shorter
        try:
            return "awsedftgyhujkolp;'".index(key)
        except ValueError:
            return None

    def on_press(
        self,
        callback: Callable[[NoteOn | NoteOff], None],
        key: pynput.keyboard.Key | pynput.keyboard.KeyCode | None,
    ) -> None:
        """
        Handle a QWERTY key press.
        """
        if not isinstance(key, pynput.keyboard.KeyCode):
            return  # bail if we didn't get a keycode object
        print(f"QWERTY pressed: {key.char}")
        if key.char is None:
            return
        if key.char == "z":  # decrement our octave setting
            self.octave = max(self.octave - 1, 0)
            return
        if key.char == "x":  # increment our octave setting
            self.octave = min(self.octave + 1, 10)
            return
        if key in self.presses_to_note_numbers:
            return  # already pressed
        if (pitch := self.qwerty_key_to_pitch_number(key.char)) is None:
            return  # not a valid key, ignore it
        # calculate the note number from the pitch and octave
        note_number = pitch + self.octave * 12
        # QWERTY keyboards aren't pressure-sensitive, so let's create a random
        # velocity to simulate expressivity
        velocity = random.randint(32, 128)
        # stash the note number with the key for releasing later
        # so that changing the octave doesn't prevent releasing
        self.presses_to_note_numbers[key.char] = note_number
        # perform a "note on" event
        callback(NoteOn(note_number=note_number, velocity=velocity))

    def on_release(
        self,
        callback: Callable[[NoteOn | NoteOff], None],
        key: pynput.keyboard.Key | pynput.keyboard.KeyCode | None,
    ) -> None:
        """
        Handle a QWERTY key release.
        """
        if not isinstance(key, pynput.keyboard.KeyCode):
            return  # bail if we didn't get a keycode object
        print(f"QWERTY released: {key.char}")
        # bail if the key isn't currently held down
        if key.char not in self.presses_to_note_numbers:
            return
        # grab the note number out of the stash
        note_number = self.presses_to_note_numbers.pop(key.char)
        # perform a "note off" event
        callback(NoteOff(note_number=note_number))


def run(input_handler: InputHandler) -> None:
    """
    Run the script.
    """

    def on_boot(*args) -> None:  # run this during server.boot()
        server.add_synthdefs(polyphony.synthdef)  # add the polyphony's synthdef
        server.sync()  # wait for the synthdef to load before moving on

    def on_quitting(*args) -> None:  # run this during server.quit()
        polyphony.free_all()  # free all the synths
        time.sleep(0.5)  # wait for them to fade out before moving on

    def signal_handler(*args) -> None:
        exit_future.set_result(True)  # set the exit future flag

    def input_callback(event: NoteOn | NoteOff) -> None:
        # just play the event via polyphony directly
        polyphony.perform(event)

    # create a future we can wait on to quit the script
    exit_future: concurrent.futures.Future[bool] = concurrent.futures.Future()
    # create a server and polyphony manager
    server = supriya.Server()
    polyphony = PolyphonyManager(server=server)
    # setup lifecycle callbacks
    server.register_lifecycle_callback("BOOTED", on_boot)
    server.register_lifecycle_callback("QUITTING", on_quitting)
    # hook up Ctrl-C so we can gracefully shutdown the server
    signal.signal(signal.SIGINT, signal_handler)
    # boot the server and let the user know we're ready to play
    server.boot()
    print("Server online. Press Ctrl-C to exit.")
    # turn on the input handler and teach it to callback against the polyphony manager
    with input_handler.listen(callback=input_callback):
        exit_future.result()  # wait for Ctrl-C
    # stop the input handler and quit the server
    server.quit()


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    """
    Parse CLI arguments.
    """
    parser = argparse.ArgumentParser(
        description="Play notes via your QWERTY or MIDI keyboards"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--list-midi-inputs", action="store_true", help="list available MIDI inputs"
    )
    group.add_argument(
        "--use-midi", help="play via MIDI keyboard", type=int, metavar="PORT_NUMBER"
    )
    group.add_argument(
        "--use-qwerty", action="store_true", help="play via QWERTY keyboard"
    )
    return parser.parse_args(args)


def main(args: list[str] | None = None) -> None:
    """
    The example entry-point function.
    """
    parsed_args = parse_args(args)
    if parsed_args.list_midi_inputs:
        # print out available MIDI input ports
        rtmidi.midiutil.list_input_ports()
    elif parsed_args.use_midi is not None:
        run(MidiHandler(port=parsed_args.use_midi))
    elif parsed_args.use_qwerty:
        run(QwertyHandler())


if __name__ == "__main__":
    main()
