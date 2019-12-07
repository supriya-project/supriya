import enum
from typing import Dict, List, Tuple

from supriya.clock import TempoClock, TimeUnit
from supriya.midi import NoteOffMessage, NoteOnMessage

from .devices import DeviceObject


class ChordEffect(DeviceObject):
    def __init__(self, name=None, uuid=None):
        DeviceObject.__init__(self, name=name, uuid=uuid)
        self._transpositions = []
        self._input_notes_to_output_notes: Dict[float, List[float]] = {}

    def _handle_note_off(self, moment, midi_message):
        result = []
        note_number = midi_message.note_number
        self._input_notes.remove(note_number)
        output_note_numbers = self._input_notes_to_output_notes.pop(note_number)
        for note_number in sorted(output_note_numbers):
            if note_number in self._output_notes:
                self._output_notes.remove(note_number)
                result.append(NoteOffMessage(note_number=note_number))
        return result

    def _handle_note_on(self, moment, midi_message):
        result = []
        note_number = midi_message.note_number
        if note_number in self._input_notes:
            result.extend(self._handle_note_off(moment, midi_message))
        transpositions = sorted(
            set(note_number + _ for _ in self._transpositions or [0])
        )
        self._input_notes.add(note_number)
        self._input_notes_to_output_notes[note_number] = transpositions
        for transposition in transpositions:
            if transposition in self._output_notes:
                result.append(NoteOffMessage(note_number=transposition))
            result.append(
                NoteOnMessage(note_number=transposition, velocity=midi_message.velocity)
            )
            self._output_notes.add(transposition)
        return result


class ArpeggiatorEffect(DeviceObject):

    ### CLASS VARIABLES ###

    class PatternStyle(enum.IntEnum):
        UP = 0
        DOWN = 1
        UP_DOWN = 2
        DOWN_UP = 3

    ### INITIALIZER ###

    def __init__(self, name=None, uuid=None):
        DeviceObject.__init__(self, name=name, uuid=uuid)
        self._input_notes_to_velocities: Dict[float, float] = {}
        self._pattern: List[Tuple[float, float]] = ()
        self._pattern_style = self.PatternStyle.UP
        self._current_index = 0
        self._duration_scale = 1.0
        self._octaves = 0
        self._quantization = "1/16"
        self._callback_id = None

    ### PRIVATE METHODS ###

    def _applicate(self, new_application):
        DeviceObject._applicate(self, new_application)
        new_application.transport._dependencies.add(self)

    def _deapplicate(self, old_application):
        DeviceObject._applicate(self, old_application)
        old_application.transport._dependencies.remove(self)

    def _handle_note_off(self, moment, midi_message):
        self._input_notes.remove(midi_message.note_number)
        self._input_notes_to_velocities.pop(midi_message.note_number)
        self._pattern = self._rebuild_pattern()
        return []

    def _handle_note_on(self, moment, midi_message):
        self._input_notes.add(midi_message.note_number)
        self._input_notes_to_velocities[
            midi_message.note_number
        ] = midi_message.velocity
        self._pattern = self._rebuild_pattern()
        return []

    def _rebuild_pattern(self):
        if not self._input_notes:
            return ()
        initial_pairs = sorted(self._input_notes_to_velocities.items())
        octave_pairs = []
        pattern_pairs = []
        for octave in range(self._octaves + 1):
            for note_number, velocity in initial_pairs:
                octave_pairs.append((note_number + (12 * octave), velocity))
        if self._pattern_style == self.PatternStyle.UP:
            pattern_pairs.extend(octave_pairs)
        elif self._pattern_style == self.PatternStyle.DOWN:
            pattern_pairs.extend(reversed(octave_pairs))
        elif self._pattern_style == self.PatternStyle.UP_DOWN:
            pattern_pairs.extend(octave_pairs)
            pattern_pairs.extend(reversed(octave_pairs))
        elif self._pattern_style == self.PatternStyle.DOWN_UP:
            pattern_pairs.extend(reversed(octave_pairs))
            pattern_pairs.extend(octave_pairs)
        else:
            raise ValueError(self._pattern_style)
        return tuple(pattern_pairs)

    def _start(self):
        self._debug_tree(self, "Starting")
        if self._callback_id is not None:
            return
        self._callback_id = self.transport.cue(
            self._transport_note_on_callback,
            event_type=2,
            quantization=self._quantization,
        )

    def _stop(self):
        self._debug_tree(self, "Stopping")
        if self._callback_id is not None:
            self.transport.cancel(self._callback_id)
        self._callback_id = None

    def _transport_note_on_callback(
        self, current_moment, desired_moment, event, **kwargs
    ):
        with self.lock([self], seconds=desired_moment.seconds):
            delta = TempoClock.quantization_to_beats(self._quantization)
            self._debug_tree(self, "Note On CB")
            if not len(self._pattern):
                return delta, TimeUnit.BEATS
            elif self._current_index >= len(self._pattern):
                self._current_index = 0
            note_number, velocity = self._pattern[self._current_index]
            self._current_index += 1
            midi_messages = []
            if note_number in self._output_notes:
                midi_messages.append(NoteOffMessage(note_number=note_number))
            self._output_notes.add(note_number)
            midi_messages.append(NoteOnMessage(note_number=note_number, velocity=velocity))
            self.transport.schedule(
                self._transport_note_off_callback,
                schedule_at=desired_moment.offset + (delta * self._duration_scale),
                args=(note_number,),
            )
            performer = self._next_performer()
            if performer is not None:
                self._perform_loop(desired_moment, performer, midi_messages)
        return delta, TimeUnit.BEATS

    def _transport_note_off_callback(
        self, current_moment, desired_moment, event, note_number, **kwargs
    ):
        with self.lock([self], seconds=desired_moment.seconds):
            self._debug_tree(self, "Note Off CB")
            if note_number not in self._output_notes:
                return
            self._output_notes.remove(note_number)
            midi_messages = [NoteOffMessage(note_number=note_number)]
            performer = self._next_performer()
            if performer is None:
                return
            self._perform_loop(desired_moment, performer, midi_messages)
