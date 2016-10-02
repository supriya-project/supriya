# -*- encoding: utf-8 -*-
from abjad import new
from supriya.tools.patterntools.EventPattern import EventPattern


class Pchain(EventPattern):
    """
    Chains patterns.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_patterns',
        )

    ### INITIALIZER ###

    def __init__(self, patterns):
        from supriya.tools import patterntools
        assert all(isinstance(_, patterntools.EventPattern) for _ in patterns)
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
