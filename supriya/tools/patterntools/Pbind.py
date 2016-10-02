# -*- encoding: utf-8 -*-
import collections
from supriya.tools.patterntools.EventPattern import EventPattern


class Pbind(EventPattern):
    '''
    A pattern binding.

    ::

        >>> pattern = patterntools.Pbind(
        ...     pitch=patterntools.Pseq([0, 3, 7]),
        ...     duration=patterntools.Pseq([0.5, 0.25, 0.25, 0.125]),
        ...     foo=[1, 2],
        ...     bar=3,
        ...     )
        >>> print(format(pattern))
        supriya.tools.patterntools.Pbind(
            bar=3,
            duration=supriya.tools.patterntools.Pseq(
                (0.5, 0.25, 0.25, 0.125),
                repetitions=1,
                ),
            foo=[1, 2],
            pitch=supriya.tools.patterntools.Pseq(
                (0, 3, 7),
                repetitions=1,
                ),
            )

    ::

        >>> for event in pattern:
        ...     event
        ...
        NoteEvent(duration=0.5, uuid=UUID('...'), bar=3, foo=(1, 2), pitch=0)
        NoteEvent(duration=0.25, uuid=UUID('...'), bar=3, foo=(1, 2), pitch=3)
        NoteEvent(duration=0.25, uuid=UUID('...'), bar=3, foo=(1, 2), pitch=7)

    ::

        >>> pattern = patterntools.Pseq([
        ...     patterntools.Pbind(
        ...         pitch=patterntools.Pseq([1, 2, 3], 1),
        ...         ),
        ...     patterntools.Pbind(
        ...         pitch=patterntools.Pseq([4, 5, 6], 1),
        ...         ),
        ...     ], 1)

    ::

        >>> for event in pattern:
        ...     event
        ...
        NoteEvent(uuid=UUID('...'), pitch=1)
        NoteEvent(uuid=UUID('...'), pitch=2)
        NoteEvent(uuid=UUID('...'), pitch=3)
        NoteEvent(uuid=UUID('...'), pitch=4)
        NoteEvent(uuid=UUID('...'), pitch=5)
        NoteEvent(uuid=UUID('...'), pitch=6)

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_patterns',
        '_synthdef',
        )

    ### INITIALIZER ###

    def __init__(self, synthdef=None, **patterns):
        from supriya.tools import synthdeftools
        assert isinstance(synthdef, (
            synthdeftools.SynthDef,
            type(None),
            ))
        self._synthdef = synthdef
        self._patterns = tuple(sorted(patterns.items()))

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        return self.patterns[item]

    ### PRIVATE METHODS ###

    def _coerce_pattern_pairs(self, patterns):
        from supriya.tools import patterntools
        patterns = dict(patterns)
        for name, pattern in patterns.items():
            if not isinstance(pattern, patterntools.Pattern):
                pattern = patterntools.Pseq([pattern], None)
            patterns[name] = iter(pattern)
        return patterns

    def _get_format_specification(self):
        from abjad.tools import systemtools
        agent = systemtools.StorageFormatAgent(self)
        names = agent.signature_keyword_names
        names.extend(self.patterns)
        names.sort()
        return systemtools.FormatSpecification(
            client=self,
            storage_format_kwargs_names=names,
            template_names=names,
            )

    def _iterate(self, state=None):
        patterns = self._coerce_pattern_pairs(self._patterns)
        while True:
            event = {}
            for name, pattern in patterns.items():
                try:
                    event[name] = next(pattern)
                except StopIteration:
                    return
            yield event

    ### PUBLIC PROPERTIES ###

    @property
    def arity(self):
        return max(self._get_arity(v) for _, v in self._patterns)

    @property
    def is_infinite(self):
        from supriya.tools import patterntools
        for _, value in self._patterns:
            if (
                isinstance(value, patterntools.Pattern) and
                not value.is_infinite
                ):
                return False
            elif isinstance(value, collections.Sequence):
                return False
        return True

    @property
    def patterns(self):
        return dict(self._patterns)

    @property
    def synthdef(self):
        return self._synthdef
