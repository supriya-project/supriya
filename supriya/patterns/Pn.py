from supriya import utils
from supriya.patterns.EventPattern import EventPattern


class Pn(EventPattern):

    ### CLASS VARIABLES ###

    __slots__ = ('_key', '_repetitions', '_pattern')

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
                        x = utils.new(x, **{self.key: True})
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
