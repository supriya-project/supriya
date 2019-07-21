from typing import List, Sequence, Tuple

from supriya.commands import Request
from supriya.midi import MidiMessage, NoteOffMessage, NoteOnMessage

from .MidiDevice import MidiDevice


class ChordDevice(MidiDevice):

    ### INITIALIZER ###

    def __init__(self):
        MidiDevice.__init__(self, name="chord")
        self._transpositions = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self._velocity_multipliers = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self._event_handlers.update(
            {NoteOnMessage: self._handle_note_on, NoteOffMessage: self._handle_note_off}
        )

    ### PRIVATE METHODS ###

    def _handle_note_on(
        self, message: NoteOnMessage
    ) -> Tuple[Sequence[MidiMessage], Sequence[Request]]:
        result: List[MidiMessage] = []
        if message.note_number in self._input_note_numbers:
            return result, ()
        for transposition, velocity_multiplier in zip(
            self._transpositions, self._velocity_multipliers
        ):
            if not velocity_multiplier:
                continue
            note_number = message.note_number + transposition
            velocity = message.velocity * velocity_multiplier
            self._input_note_numbers.setdefault(message.note_number, []).append(
                note_number
            )
            note_on_message = NoteOnMessage(
                channel_number=message.channel_number,
                note_number=note_number,
                velocity=velocity,
            )
            result.append(note_on_message)
        return result, ()

    def _handle_note_off(
        self, message: NoteOffMessage
    ) -> Tuple[Sequence[MidiMessage], Sequence[Request]]:
        result: List[MidiMessage] = []
        if message.note_number not in self._input_note_numbers:
            return result, ()
        active_note_numbers = self._input_note_numbers.pop(message.note_number)
        for note_number in active_note_numbers:
            if note_number in self._output_note_numbers:
                note_off_message = NoteOffMessage(
                    channel_number=message.channel_number,
                    note_number=note_number,
                    velocity=message.velocity,
                )
                result.append(note_off_message)
        return result, ()
