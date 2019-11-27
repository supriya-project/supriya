import enum
from typing import List, Sequence, Tuple

from supriya.clock import TempoClock
from supriya.commands import Request
from supriya.midi import MidiMessage, NoteOffMessage, NoteOnMessage

from .MidiDevice import MidiDevice


class ArpeggiatorDevice(MidiDevice):

    ### CLASS VARIABLES ###

    class Pattern(enum.IntEnum):
        UP = 0
        DOWN = 1
        UP_DOWN = 2
        DOWN_UP = 3

    ### INITIALIZER ###

    def __init__(self):
        MidiDevice.__init__(self)
        self._event_handlers.update(
            {NoteOnMessage: self._handle_note_on, NoteOffMessage: self._handle_note_off}
        )
        self._pattern: List[Tuple[float, float]] = ()
        self._pattern_style = self.Pattern.UP
        self._octaves = 0
        self._current_index = 0
        self._quantization = "1/4"

    ### PRIVATE METHODS ###

    def _handle_note_on(
        self, message: NoteOnMessage
    ) -> Tuple[Sequence[MidiMessage], Sequence[Request]]:
        self._input_note_numbers[message.note_number] = message.velocity
        self._pattern = self._rebuild_pattern()
        return (), ()

    def _handle_note_off(
        self, message: NoteOffMessage
    ) -> Tuple[Sequence[MidiMessage], Sequence[Request]]:
        self._input_note_numbers.pop(message.note_number, None)
        self._pattern = self._rebuild_pattern()
        return (), ()

    def _rebuild_pattern(self):
        if not self._input_note_numbers:
            return ()
        initial_pairs = sorted(self._input_note_numbers.items())
        octave_pairs = []
        pattern_pairs = []
        for octave in range(self._octaves + 1):
            for note_number, velocity in initial_pairs:
                octave_pairs.append((note_number + (12 * octave), velocity))
        if self._pattern_style == self.Pattern.UP:
            pattern_pairs.extend(octave_pairs)
        elif self._pattern_style == self.Pattern.DOWN:
            pattern_pairs.extend(reversed(octave_pairs))
        elif self._pattern_style == self.Pattern.UP_DOWN:
            pattern_pairs.extend(octave_pairs)
            pattern_pairs.extend(reversed(octave_pairs))
        elif self._pattern_style == self.Pattern.DOWN_UP:
            pattern_pairs.extend(reversed(octave_pairs))
            pattern_pairs.extend(octave_pairs)
        else:
            raise ValueError(self._pattern_style)
        return tuple(pattern_pairs)

    def _transport_note_on_callback(
        self, current_moment, desired_moment, event, **kwargs
    ):
        if not len(self._pattern):
            return
        elif self._current_index >= len(self._pattern):
            self._current_index = 0
        note_number, velocity = self._pattern[self._current_index]
        self._output_note_numbers[note_number] = velocity
        self._current_index += 1
        midi_messages = [NoteOnMessage(note_number=note_number, velocity=velocity)]
        for message in midi_messages:
            self._update_captures(desired_moment, message, "O")
        # check if note is already being played, and add note-off if so
        # schedule note off
        transport = self.transport
        if transport is not None:
            transport.clock.schedule(
                self._transport_note_off_callback,
                schedule_at=desired_moment.offset
                + (TempoClock.quantization_to_duration(self._quantization),),
                kwargs={"note_numbers": note_number},
            )
        performer = self.next_performer()
        if performer is None:
            return
        requests = self.perform_loop(desired_moment, performer, [midi_messages])
        self.application.send_requests(desired_moment, requests)

    def _transport_note_off_callback(
        self, current_moment, desired_moment, event, note_number=None, **kwargs
    ):
        if note_number not in self._output_note_numbers:
            return
        self._output_note_numbers.pop(note_number)
        midi_messages = [NoteOffMessage(note_number=note_number)]
        for message in midi_messages:
            self._update_captures(desired_moment, message, "O")
        performer = self.next_performer()
        if performer is None:
            return
        requests = self.perform_loop(desired_moment, performer, midi_messages)
        self.application.send_requests(desired_moment, requests)

    ### PUBLIC PROPERTIES ###

    @property
    def current_index(self):
        return self._current_index

    @property
    def pattern(self):
        return self._pattern
