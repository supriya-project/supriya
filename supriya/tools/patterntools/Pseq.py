# -*- encoding: utf-8 -*-
import collections
from supriya.tools.patterntools.Pattern import Pattern


class Pseq(Pattern):
    '''
    A sequence pattern.

    ::

        >>> pattern = patterntools.Pseq([1, 2, 3])
        >>> for x in pattern:
        ...     x
        ...
        1
        2
        3

    ::

        >>> pattern = patterntools.Pseq([1, 10, 100], repetitions=2)
        >>> list(pattern)
        [1, 10, 100, 1, 10, 100]

    ::

        >>> pattern = patterntools.Pseq([
        ...     patterntools.Pseq([1, 2, 3], repetitions=1),
        ...     patterntools.Pseq([4, 5, 6], repetitions=1),
        ...     ], repetitions=2)
        >>> list(pattern)
        [1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6]

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_sequence',
        '_repetitions',
        )

    ### INITIALIZER ###

    def __init__(self, sequence, repetitions=1):
        assert isinstance(sequence, collections.Sequence)
        self._sequence = self._freeze_recursive(sequence)
        if repetitions is not None:
            repetitions = int(repetitions)
            assert 0 < repetitions
        self._repetitions = repetitions

    ### PRIVATE METHODS ###

    def _iterate(self, state=None):
        for _ in self._loop(self._repetitions):
            for x in self._sequence:
                if isinstance(x, Pattern):
                    yield from x
                else:
                    yield x

    ### PUBLIC PROPERTIES ###

    @property
    def arity(self):
        """
        Gets arity of Pseq.

        ::

            >>> pattern = patterntools.Pseq([1, 2, 3])
            >>> pattern.arity
            1

        ::

            >>> pattern = patterntools.Pseq([[1, 2], 3, 4])
            >>> pattern.arity
            2

        ::

            >>> pattern = patterntools.Pseq([
            ...     patterntools.Pseq([1, 2, 3]),
            ...     patterntools.Pseq([[1, 2], 3, 4]),
            ...     ])
            >>> pattern.arity
            2

        Returns integer.
        """
        return max(self._get_arity(x) for x in self.sequence)

    @property
    def is_infinite(self):
        from supriya.tools import patterntools
        if self.repetitions is None:
            return True
        for x in self.sequence:
            if isinstance(x, patterntools.Pattern) and x.is_infinite:
                return True
        return False

    @property
    def repetitions(self):
        return self._repetitions

    @property
    def sequence(self):
        return self._sequence
