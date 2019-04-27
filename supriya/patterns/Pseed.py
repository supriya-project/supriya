import inspect

from supriya.patterns.Pattern import Pattern
from supriya.patterns.RandomNumberGenerator import RandomNumberGenerator


class Pseed(Pattern):

    ### CLASS VARIABLES ###

    __slots__ = ("_pattern", "_seed")

    _file_path = __file__

    ### INITIALIZER ###

    def __init__(self, pattern, seed=0):
        assert isinstance(pattern, Pattern)
        self._pattern = pattern
        self._seed = int(seed)

    ### PRIVATE METHODS ###

    def _iterate(self, state=None):
        try:
            identifier = id(inspect.currentframe())
            rng = RandomNumberGenerator(seed=self.seed)
            Pattern._rngs[identifier] = iter(rng)
            yield from self._pattern
        finally:
            del Pattern._rngs[identifier]

    ### PUBLIC PROPERTIES ###

    @property
    def arity(self):
        return self._pattern.arity

    @property
    def is_infinite(self):
        return self._pattern.is_infinite

    @property
    def pattern(self):
        return self._pattern

    @property
    def seed(self):
        return self._seed
