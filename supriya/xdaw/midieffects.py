from typing import Dict, List

from supriya.midi import NoteOffMessage, NoteOnMessage

from .devices import DeviceObject


class ChordEffect(DeviceObject):
    def __init__(self, name=None, uuid=None):
        DeviceObject.__init__(self, name=name, uuid=uuid)
        self._transpositions = []
        self._input_notes_to_output_notes: Dict[float, List[float]] = {}

    def _handle_note_off(self, moment, midi_message):
        print("D", midi_message)
        result = []
        note_number = midi_message.note_number
        self._input_notes.remove(note_number)
        output_note_numbers = self._input_notes_to_output_notes.pop(note_number)
        for note_number in sorted(output_note_numbers):
            if note_number in self._output_notes:
                self._output_notes.remove(note_number)
                result.append(NoteOffMessage(note_number=note_number))
        print("E", result)
        return result

    def _handle_note_on(self, moment, midi_message):
        print("D", midi_message)
        result = []
        note_number = midi_message.note_number
        if note_number in self._input_notes:
            result.extend(self._handle_note_off(moment, midi_message))
        transpositions = sorted(set(note_number + _ for _ in self._transpositions or [0]))
        self._input_notes.add(note_number)
        self._input_notes_to_output_notes[note_number] = transpositions
        for transposition in transpositions:
            if transposition in self._output_notes:
                result.append(NoteOffMessage(note_number=transposition))
            result.append(
                NoteOnMessage(
                    note_number=transposition, velocity=midi_message.velocity
                )
            )
            self._output_notes.add(transposition)
        print("E", result)
        return result
