import dataclasses
from typing import Optional, Tuple


@dataclasses.dataclass(frozen=True, order=True)
class Note:
    start_offset: Optional[float] = None
    stop_offset: Optional[float] = None
    pitch: float = 0.0
    velocity: float = 100.0

    def __post_init__(self):
        if self.start_offset >= self.stop_offset:
            raise ValueError

    def transpose(self, transposition):
        return dataclasses.replace(self, self.pitch + transposition)

    def translate(self, start_translation=None, stop_translation=None):
        start_offset = self.start_offset + (start_translation or 0)
        stop_offset = self.stop_offset + (stop_translation or 0)
        return dataclasses.replace(
            self, start_offset=start_offset, stop_offset=stop_offset
        )


@dataclasses.dataclass(frozen=True)
class NoteMoment:
    offset: float = 0.0
    local_offset: float = 0.0
    next_offset: Optional[float] = None
    start_notes: Optional[Tuple[Note]] = None
    stop_notes: Optional[Tuple[Note]] = None

    @property
    def note_on_messages(self):
        return [
            NoteOnMessage(note_number=note.pitch, velocity=note.velocity)
            for note in self.start_notes
        ]

    @property
    def note_off_messages(self):
        return [
            NoteOffMessage(note_number=note.pitch, velocity=note.velocity)
            for note in self.stop_notes
        ]
