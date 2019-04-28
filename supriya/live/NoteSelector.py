class NoteSelector:

    _valid_operators = frozenset(("==", "!=", "<", ">", "<=", ">="))

    def __init__(self, clip, filters=None):
        self._clip = clip
        self._filters = tuple(filters or ())

    def __iter__(self):
        source = iter(self._clip)
        for filter_ in self._filters:
            filter_name, filter_args = filter_[0], filter_[1:]
            filter_func = getattr(self, "_" + filter_name)
            source = filter_func(source, *filter_args)
        yield from source

    def __and__(self, selector):
        pass

    def __or__(self, selector):
        pass

    def __invert__(self):
        pass

    def __xor__(self):
        pass

    def _and_selector(self, source, selector):
        pass

    def _or_selector(self, source, selector):
        pass

    def _xor_selector(self, source, selector):
        pass

    def _invert(self, source):
        pass

    def _between_offsets(self, source, start_offset, stop_offset):
        if start_offset is None and stop_offset is not None:
            for note in source:
                if note.stop_offset <= stop_offset:
                    yield note
        elif start_offset is not None and stop_offset is None:
            for note in source:
                if start_offset <= note.start_offset:
                    yield note
        elif start_offset < stop_offset:
            for note in source:
                if (
                    start_offset <= note.start_offset
                    and note.stop_offset <= stop_offset
                ):
                    yield note
        elif stop_offset < start_offset:
            for note in source:
                if note.stop_offset <= stop_offset or start_offset <= note.start_offset:
                    yield note
        else:
            yield from source

    def _between_pitches(self, source, start_pitch, stop_pitch):
        if start_pitch is None and stop_pitch is not None:
            for note in source:
                if note.pitch <= stop_pitch:
                    yield note
        elif start_pitch is not None and stop_pitch is None:
            for note in source:
                if start_pitch <= note.pitch:
                    yield note
        elif start_pitch < stop_pitch:
            for note in source:
                if start_pitch <= note.pitch <= stop_pitch:
                    yield note
        elif stop_pitch < start_pitch:
            for note in source:
                if note.pitch <= stop_pitch or start_pitch <= note.pitch:
                    yield note
        else:
            yield from source

    def _with_durations(self, source, durations, operator):
        pass

    def _with_pitches(self, source, pitches, operator):
        pass

    def _with_pitch_classes(self, source, pitch_classes, operator):
        pass

    def between_offsets(self, start_offset=None, stop_offset=None):
        if start_offset is not None:
            start_offset = float(start_offset)
        if stop_offset is not None:
            stop_offset = float(stop_offset)
        filter_ = ("between_offsets", start_offset, stop_offset)
        filters = self._filters + (filter_,)
        return type(self)(self._clip, filters)

    def between_pitches(self, start_pitch=None, stop_pitch=None):
        if start_pitch is not None:
            start_pitch = float(start_pitch)
        if stop_pitch is not None:
            stop_pitch = float(stop_pitch)
        filter_ = ("between_pitches", start_pitch, stop_pitch)
        filters = self._filters + (filter_,)
        return type(self)(self._clip, filters)

    def with_durations(self, durations, operator="=="):
        pass

    def with_pitches(self, pitches, operator="=="):
        pass

    def with_pitch_classes(self, pitch_classes, operator="=="):
        pass

    def delete(self):
        self._clip.remove_notes(self)

    def replace(self, notes):
        self._clip.remove_notes(self)
        self._clip.add_notes(notes)

    def transpose(self, transposition):
        notes = list(self)
        self._clip.remove_notes(self)
        self._clip.add_notes([note.transpose(transposition) for note in notes])

    def translate(self, translation):
        notes = list(self)
        self._clip.remove_notes(self)
        self._clip.add_notes(
            [note.translate(translation, translation) for note in notes]
        )

    def translate_offsets(self, start_translation=None, stop_translation=None):
        notes = list(self)
        self._clip.remove_notes(self)
        self._clip.add_notes(
            [note.translate(start_translation, stop_translation) for note in notes]
        )
