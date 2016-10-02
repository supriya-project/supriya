# -*- encoding: utf-8 -*-
from supriya.tools.patterntools.Pattern import Pattern


class Pwhite(Pattern):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_minimum',
        '_maximum',
        '_repetitions',
        )

    ### INITIALIZER ###

    def __init__(self, minimum=0., maximum=1., repetitions=None):
        if repetitions is not None:
            repetitions = int(repetitions)
            assert 0 < repetitions
        self._repetitions = repetitions
        self._minimum = self._freeze_recursive(minimum)
        self._maximum = self._freeze_recursive(maximum)

    ### PRIVATE METHODS ###

    def _iterate(self, state=None):
        def procedure(one, two):
            minimum, maximum = sorted([one, two])
            number = next(rng)
            return (number + minimum) * (maximum - minimum)
            #if isinstance(minimum, int) and isinstance(maximum, int):
            #    return random.randint(minimum, maximum)
            #return (random.random() + minimum) * (maximum - minimum)
        rng, identifier = self._get_rng()
        try:
            for _ in self._loop(self._repetitions):
                yield self._process_recursive(
                    self._minimum,
                    self._maximum,
                    procedure,
                    )
        finally:
            if identifier in Pattern._rngs:
                del(Pattern._rngs[identifier])
            print('DONE', identifier, Pattern._rngs)

    ### PUBLIC PROPERTIES ###

    @property
    def arity(self):
        """
        Gets arity of Pwhite.

        ::

            >>> pattern = patterntools.Pwhite(0.0, 1.0)
            >>> pattern.arity
            1

        ::

            >>> pattern = patterntools.Pwhite([0.0, 0.1], 2)
            >>> pattern.arity
            2

        Returns integer.
        """
        return max(self._get_arity(x) for x in (
            self._minimum, self._maximum))

    @property
    def is_infinite(self):
        return self.iterations is None

    @property
    def minimum(self):
        return self._minimum

    @property
    def maximum(self):
        return self._maximum
