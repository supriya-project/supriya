import dataclasses
from typing import Optional, Tuple

from supriya.time import TimespanCollection
from supriya.utils import iterate_nwise

from .Note import Note
from .NoteSelector import NoteSelector

# TODO: looping, loop start and end, clip start and end
# TODO: scheduling: this event, next event, clip stop, etc.
# TODO: global transport and clip playing


class Clip:
    """
    A clip.

    ::

        >>> from supriya.daw import Clip, Note

    ::

        >>> notes = [
        ...     Note(0, 1, pitch=0), Note(4, 5, pitch=0), Note(8, 9, pitch=0),
        ...     Note(0, 1, pitch=2), Note(4, 5, pitch=2), Note(8, 9, pitch=2),
        ...     Note(2, 6, pitch=7),
        ... ]

    ::

        >>> clip = Clip(notes=notes)

    ::

        >>> selector = (
        ...     clip.select()
        ...     .between_offsets(stop_offset=6)
        ...     .between_pitches(-2, 3)
        ... )
        >>> for note in selector:
        ...     note
        ...
        Note(start_offset=0, stop_offset=1, pitch=0, velocity=1.0)
        Note(start_offset=0, stop_offset=1, pitch=2, velocity=1.0)
        Note(start_offset=4, stop_offset=5, pitch=0, velocity=1.0)
        Note(start_offset=4, stop_offset=5, pitch=2, velocity=1.0)

    ::

        >>> selector.translate_offsets(stop_translation=4)

    ::

        >>> for note in clip:
        ...     note
        ...
        Note(start_offset=0, stop_offset=4, pitch=0, velocity=1.0)
        Note(start_offset=0, stop_offset=4, pitch=2, velocity=1.0)
        Note(start_offset=2, stop_offset=6, pitch=7, velocity=1.0)
        Note(start_offset=4, stop_offset=9, pitch=0, velocity=1.0)
        Note(start_offset=4, stop_offset=9, pitch=2, velocity=1.0)

    """

    @dataclasses.dataclass(frozen=True)
    class Moment:
        offset: float = 0.0
        local_offset: float = 0.0
        next_offset: Optional[float] = None
        start_notes: Optional[Tuple[Note]] = None
        stop_notes: Optional[Tuple[Note]] = None

    ### INITIALIZER ###

    def __init__(self, *, notes=None, duration=4, is_looping=True, parent=None):
        self._duration = duration
        self._is_looping = is_looping
        self._parent = parent
        self._notes = TimespanCollection()
        self.add_notes(notes)

    ### SPECIAL METHODS ###

    def __iter__(self):
        return iter(self._notes)

    def __len__(self):
        return len(self._notes)

    ### PRIVATE METHODS ###

    def _by_pitch(cls, notes):
        by_pitch = {}
        for note in sorted(notes):
            by_pitch.setdefault(note.pitch, []).append(note)
        return by_pitch

    def _notify_parent(self):
        if self.parent is None:
            return
        self.parent.notify()

    ### PUBLIC METHODS ###

    def add_notes(self, notes):
        new_notes_by_pitch = self._by_pitch(list(notes))
        old_notes_by_pitch = self._by_pitch(list(self))
        for pitch, new_notes in new_notes_by_pitch.items():
            note_one = new_notes[0]
            # simultaneous new note starts: longer note wins
            for note_two in tuple(new_notes[1:]):
                if note_one.start_offset == note_two.start_offset:
                    new_notes.remove(note_one)
            # new note overlaps: later notes masks earlier note
            for i, (note_one, note_two) in enumerate(tuple(iterate_nwise(new_notes))):
                if note_one.start_offset < note_two.start_offset < note_one.stop_offset:
                    new_notes[i] = dataclasses.replace(
                        note_one, stop_offset=note_two.start_offset
                    )
            # old note overlaps: new notes delete old notes
            # TODO: make this more efficient(use an iterator for the new notes)
            for old_note in tuple(old_notes_by_pitch.get(pitch, ())):
                for new_note in new_notes:
                    if (
                        new_note.start_offset
                        <= old_note.start_offset
                        < new_note.stop_offset
                    ):
                        self._notes.remove(old_note)

            self._notes.insert(new_notes)

    def at(self, offset, start_delta=0.0, force_stop=False):
        def get_nonstart_notes(simultaneity):
            stop_notes = [
                note for note in simultaneity.stop_timespans if note.start_offset >= 0
            ]
            overlap_notes = [
                note
                for note in simultaneity.overlap_timespans
                if note.start_offset >= 0
            ]
            return stop_notes, overlap_notes

        local_offset = offset - start_delta
        loop_delta = 0
        start_notes, stop_notes, overlap_notes = [], [], []
        next_offset = None
        if offset < start_delta:
            return self.Moment(
                offset=offset,
                local_offset=local_offset,
                next_offset=next_offset,
                start_notes=tuple(start_notes),
                stop_notes=tuple(stop_notes),
            )
        if self.is_looping:
            count, local_offset = divmod(local_offset, self.clip_stop)
            if not local_offset:  # at the loop boundary
                simultaneity = self._notes.get_simultaneity_at(local_offset)
                start_notes = simultaneity.start_timespans
                overlap_notes, stop_notes = [], []
                if count:  # at end of loop
                    simultaneity_two = self._notes.get_simultaneity_at(self.duration)
                    stops, overlaps = get_nonstart_notes(simultaneity_two)
                    stop_notes.extend(stops)
                    stop_notes.extend(overlaps)
            else:  # in the middle of the loop
                simultaneity = self._notes.get_simultaneity_at(local_offset)
                start_notes = simultaneity.start_timespans
                stop_notes, overlap_notes = get_nonstart_notes(simultaneity)
            loop_delta = count * self.duration
        else:  # non-looping
            simultaneity = self._notes.get_simultaneity_at(local_offset)
            start_notes = simultaneity.start_timespans
            stop_notes, overlap_notes = get_nonstart_notes(simultaneity)
        # next offset could be from a pre-zero timespan, but who cares?
        next_offset = self._notes.get_offset_after(local_offset)
        if next_offset is not None:
            if self.is_looping:
                next_offset = min([next_offset, self.duration])
            next_offset += start_delta + loop_delta
        if force_stop:
            start_notes[:] = []
            stop_notes.extend(overlap_notes)
            next_offset = None
        return self.Moment(
            offset=offset,
            local_offset=local_offset,
            next_offset=next_offset,
            start_notes=tuple(start_notes),
            stop_notes=tuple(stop_notes),
        )

    def fire(self):
        if not self._parent:
            raise RuntimeError("Parent cannot be null")
        self.parent.fire(self)

    def remove_notes(self, notes):
        notes = list(notes)
        self._notes.remove(notes)

    def select(self):
        return NoteSelector(self)

    ### PUBLIC PROPERTIES ###

    @property
    def clip_start(self):
        return 0.0

    @property
    def clip_stop(self):
        return self._duration if self.is_looping else self._notes.stop_offset

    @property
    def duration(self):
        return self._duration

    @property
    def is_looping(self):
        return self._is_looping
