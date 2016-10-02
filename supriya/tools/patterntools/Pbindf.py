# -*- encoding: utf-8 -*-
import collections
from abjad import new
from supriya.tools.patterntools.EventPattern import EventPattern


class Pbindf(EventPattern):
    """
    Overwrites keys in an event pattern.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_event_pattern',
        '_patterns',
        )

    ### INITIALIZER ###

    def __init__(self, event_pattern=None, **patterns):
        from supriya.tools import patterntools
        assert isinstance(event_pattern, patterntools.EventPattern)
        self._event_pattern = event_pattern
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
        event_pattern = iter(self._event_pattern)
        patterns = self._coerce_pattern_pairs(self._patterns)
        while True:
            try:
                event = next(event_pattern)
            except StopIteration:
                return
            template_dict = {}
            for name, pattern in patterns.items():
                try:
                    template_dict[name] = next(pattern)
                except StopIteration:
                    return
            yield new(event, **template_dict)

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
        from supriya.tools import patterntools
        if not self._event_pattern.is_infinite():
            return False
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
