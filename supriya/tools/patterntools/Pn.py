# -*- encoding: utf-8 -*-
from abjad import new
from supriya.tools.patterntools.Pattern import Pattern


class Pn(Pattern):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_key',
        '_repetitions',
        '_pattern',
        )

    ### INITIALIZER ###

    def __init__(self, pattern, repetitions=None, key=None):
        assert isinstance(pattern, Pattern)
        if repetitions is not None:
            repetitions = int(repetitions)
            assert 0 < repetitions
        self._repetitions = repetitions
        if key is not None:
            key = str(key)
        self._key = key

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
