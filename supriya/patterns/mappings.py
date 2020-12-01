import uuid
from collections.abc import Sequence

from uqbar.objects import new

from supriya.patterns.bases import EventPattern


class Pbind(EventPattern):
    """
    A pattern binding.

    ::

        >>> pattern = supriya.patterns.Pbind(
        ...     pitch=supriya.patterns.Pseq([0, 3, 7]),
        ...     duration=supriya.patterns.Pseq([0.5, 0.25, 0.25, 0.125]),
        ...     foo=[1, 2],
        ...     bar=3,
        ... )

    ::

        >>> for event in pattern:
        ...     event
        ...
        NoteEvent(
            bar=3,
            delta=0.5,
            duration=0.5,
            foo=(1, 2),
            pitch=0,
            uuid=UUID('...'),
        )
        NoteEvent(
            bar=3,
            delta=0.25,
            duration=0.25,
            foo=(1, 2),
            pitch=3,
            uuid=UUID('...'),
        )
        NoteEvent(
            bar=3,
            delta=0.25,
            duration=0.25,
            foo=(1, 2),
            pitch=7,
            uuid=UUID('...'),
        )

    ::

        >>> pattern = supriya.patterns.Pseq(
        ...     [
        ...         supriya.patterns.Pbind(pitch=supriya.patterns.Pseq([1, 2, 3], 1),),
        ...         supriya.patterns.Pbind(pitch=supriya.patterns.Pseq([4, 5, 6], 1),),
        ...     ],
        ...     1,
        ... )

    ::

        >>> for event in pattern:
        ...     event
        ...
        NoteEvent(
            pitch=1,
            uuid=UUID('...'),
        )
        NoteEvent(
            pitch=2,
            uuid=UUID('...'),
        )
        NoteEvent(
            pitch=3,
            uuid=UUID('...'),
        )
        NoteEvent(
            pitch=4,
            uuid=UUID('...'),
        )
        NoteEvent(
            pitch=5,
            uuid=UUID('...'),
        )
        NoteEvent(
            pitch=6,
            uuid=UUID('...'),
        )

    """

    ### INITIALIZER ###

    def __init__(self, synthdef=None, **patterns):
        import supriya.patterns
        import supriya.synthdefs

        assert isinstance(
            synthdef, (supriya.synthdefs.SynthDef, supriya.patterns.Pattern, type(None))
        )
        self._synthdef = synthdef
        self._patterns = tuple(sorted(patterns.items()))

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        return self.patterns[item]

    ### PRIVATE METHODS ###

    def _coerce_pattern_pairs(self, patterns):
        import supriya.patterns

        patterns = dict(patterns)
        for name, pattern in sorted(patterns.items()):
            if not isinstance(pattern, supriya.patterns.Pattern):
                pattern = supriya.patterns.Pseq([pattern], None)
            patterns[name] = iter(pattern)
        synthdef = self.synthdef
        if not isinstance(synthdef, supriya.patterns.Pattern):
            synthdef = supriya.patterns.Pseq([synthdef], None)
        patterns["synthdef"] = iter(synthdef)
        return patterns

    def _iterate(self, state=None):
        patterns = self._coerce_pattern_pairs(self._patterns)
        while True:
            expr = {}
            for name, pattern in sorted(patterns.items()):
                try:
                    expr[name] = next(pattern)
                except StopIteration:
                    return
            expr = self._coerce_iterator_output(expr)
            should_stop = yield expr
            if should_stop:
                return

    ### PUBLIC PROPERTIES ###

    @property
    def arity(self):
        return max(self._get_arity(v) for _, v in self._patterns)

    @property
    def is_infinite(self):
        import supriya.patterns

        for _, value in self._patterns:
            if isinstance(value, supriya.patterns.Pattern) and not value.is_infinite:
                return False
            elif isinstance(value, Sequence):
                return False
        return True

    @property
    def patterns(self):
        return dict(self._patterns)

    @property
    def synthdef(self):
        return self._synthdef


class Pbindf(EventPattern):
    """
    Overwrites keys in an event pattern.
    """

    ### INITIALIZER ###

    def __init__(self, event_pattern=None, **patterns):
        import supriya.patterns

        assert isinstance(event_pattern, supriya.patterns.Pattern)
        self._event_pattern = event_pattern
        self._patterns = tuple(sorted(patterns.items()))

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        return self.patterns[item]

    ### PRIVATE METHODS ###

    def _coerce_pattern_pairs(self, patterns):
        import supriya.patterns

        patterns = dict(patterns)
        for name, pattern in sorted(patterns.items()):
            if not isinstance(pattern, supriya.patterns.Pattern):
                pattern = supriya.patterns.Pseq([pattern], None)
            patterns[name] = iter(pattern)
        return patterns

    def _iterate(self, state=None):
        should_stop = self.PatternState.CONTINUE
        event_iterator = iter(self._event_pattern)
        key_iterators = self._coerce_pattern_pairs(self._patterns)
        template_dict = {}
        while True:
            try:
                if not should_stop:
                    expr = next(event_iterator)
                else:
                    expr = event_iterator.send(True)
            except StopIteration:
                return
            expr = self._coerce_iterator_output(expr)
            for name, key_iterator in sorted(key_iterators.items()):
                try:
                    template_dict[name] = next(key_iterator)
                except StopIteration:
                    continue
            expr = new(expr, **template_dict)
            should_stop = yield expr

    ### PUBLIC PROPERTIES ###

    @property
    def arity(self):
        arity = max(self._get_arity(v) for _, v in self._patterns)
        return max([self._get_arity(self._event_pattern), arity])

    @property
    def event_pattern(self):
        return self._event_pattern

    @property
    def is_infinite(self):
        import supriya.patterns

        if not self._event_pattern.is_infinite:
            return False
        for _, value in self._patterns:
            if isinstance(value, supriya.patterns.Pattern) and not value.is_infinite:
                return False
            elif isinstance(value, Sequence):
                return False
        return True

    @property
    def patterns(self):
        return dict(self._patterns)


class Pchain(EventPattern):
    """
    Chains patterns.
    """

    ### INITIALIZER ###

    def __init__(self, patterns):
        import supriya.patterns

        assert all(isinstance(_, supriya.patterns.EventPattern) for _ in patterns)
        assert patterns
        self._patterns = tuple(patterns)

    ### PRIVATE METHODS ###

    def _iterate(self, state=None):
        patterns = [iter(_) for _ in self._patterns]
        while True:
            try:
                event = next(patterns[0])
            except StopIteration:
                return
            for pattern in patterns[1:]:
                try:
                    template_event = next(pattern)
                except StopIteration:
                    return
                template_dict = template_event.as_dict()
                for key, value in tuple(template_dict.items()):
                    if value is None:
                        template_dict.pop(key)
                event = new(event, **template_dict)
            yield event

    ### PUBLIC PROPERTIES ###

    @property
    def arity(self):
        return max(self._get_arity(_) for _ in self._patterns)

    @property
    def is_infinite(self):
        return all(_.is_infinite for _ in self._patterns)

    @property
    def patterns(self):
        return self._patterns


class Pmono(Pbind):
    """
    A monophonic pattern.

    ::

        >>> pattern = supriya.patterns.Pmono(
        ...     pitch=supriya.patterns.Pseq([0, 3, 7]),
        ...     duration=supriya.patterns.Pseq([0.5, 0.25, 0.25]),
        ... )

    ::

        >>> for event in pattern:
        ...     event
        ...
        NoteEvent(
            delta=0.5,
            duration=0.5,
            is_stop=False,
            pitch=0,
            uuid=UUID('...'),
        )
        NoteEvent(
            delta=0.25,
            duration=0.25,
            is_stop=False,
            pitch=3,
            uuid=UUID('...'),
        )
        NoteEvent(
            delta=0.25,
            duration=0.25,
            pitch=7,
            uuid=UUID('...'),
        )

    ::

        >>> pattern = supriya.patterns.Pseq(
        ...     [
        ...         supriya.patterns.Pmono(pitch=supriya.patterns.Pseq([1, 2, 3], 1),),
        ...         supriya.patterns.Pmono(pitch=supriya.patterns.Pseq([4, 5, 6], 1),),
        ...     ],
        ...     1,
        ... )

    ::

        >>> for event in pattern:
        ...     event
        ...
        NoteEvent(
            is_stop=False,
            pitch=1,
            uuid=UUID('...'),
        )
        NoteEvent(
            is_stop=False,
            pitch=2,
            uuid=UUID('...'),
        )
        NoteEvent(
            pitch=3,
            uuid=UUID('...'),
        )
        NoteEvent(
            is_stop=False,
            pitch=4,
            uuid=UUID('...'),
        )
        NoteEvent(
            is_stop=False,
            pitch=5,
            uuid=UUID('...'),
        )
        NoteEvent(
            pitch=6,
            uuid=UUID('...'),
        )

    """

    ### PRIVATE METHODS ###

    def _iterate(self, state=None):
        synth_uuid = uuid.uuid4()
        iterator = super(Pmono, self)._iterate(state=state)
        events = []
        try:
            events.append(next(iterator))
        except StopIteration:
            return
        for event in iterator:
            events.append(event)
            event = new(events.pop(0), uuid=synth_uuid, is_stop=False)
            should_stop = yield event
            if should_stop:
                return
        assert len(events) == 1
        if events:
            event = events.pop()
            event = new(event, uuid=synth_uuid, is_stop=True)
            yield event


class Pn(EventPattern):

    ### INITIALIZER ###

    def __init__(self, pattern, repetitions=None, key=None):
        assert isinstance(pattern, EventPattern)
        if repetitions is not None:
            repetitions = int(repetitions)
            assert 0 < repetitions
        self._repetitions = repetitions
        if key is not None:
            key = str(key)
        self._key = key
        self._pattern = pattern

    ### PRIVATE METHODS ###

    def _iterate(self, state=None):
        if self.key:
            for _ in self._loop(self._repetitions):
                for i, x in enumerate(self._pattern):
                    if i == 0:
                        x = new(x, **{self.key: True})
                    yield x
        else:
            for _ in self._loop(self._repetitions):
                yield from self._pattern

    ### PUBLIC PROPERTIES ###

    @property
    def arity(self):
        return self._pattern.arity

    @property
    def is_infinite(self):
        return self._pattern.is_infinite

    @property
    def key(self):
        return self._key

    @property
    def pattern(self):
        return self._pattern

    @property
    def repetitions(self):
        return self._repetitions
