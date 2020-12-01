import inspect
import operator
from collections.abc import Sequence

from .bases import Pattern
from .random import RandomNumberGenerator


class Pbinop(Pattern):

    ### INITIALIZER ###

    def __init__(self, expr_one, operator, expr_two):
        self._expr_one = self._freeze_recursive(expr_one)
        self._expr_two = self._freeze_recursive(expr_two)
        self._operator = operator

    ### PRIVATE METHODS ###

    def _iterate(self, state=None):
        import supriya.patterns

        expr_one = self.expr_one
        if not isinstance(expr_one, Pattern):
            expr_one = supriya.patterns.Pseq([expr_one], None)
        expr_one = iter(expr_one)
        expr_two = self.expr_two
        if not isinstance(expr_two, Pattern):
            expr_two = supriya.patterns.Pseq([expr_two], None)
        expr_two = iter(expr_two)
        operator = self._string_to_operator()
        for one, two in zip(expr_one, expr_two):
            yield self._process_recursive(one, two, operator)

    def _string_to_operator(self):
        operators = {
            "+": operator.__add__,
            "-": operator.__sub__,
            "*": operator.__mul__,
            "**": operator.__pow__,
            "/": operator.__truediv__,
            "//": operator.__floordiv__,
        }
        return operators[self.operator]

    ### PUBLIC PROPERTIES ###

    @property
    def arity(self):
        return max(self._get_arity(x) for x in (self._expr_one, self._expr_two))

    @property
    def expr_one(self):
        return self._expr_one

    @property
    def expr_two(self):
        return self._expr_two

    @property
    def is_infinite(self):
        import supriya.patterns

        return (
            isinstance(self.expr_one, supriya.patterns.Pattern)
            and isinstance(self.expr_two, supriya.patterns.Pattern)
            and self.expr_one.is_infinite
            and self.expr_two.is_infinite
        )

    @property
    def operator(self):
        return self._operator


class Pseed(Pattern):

    ### CLASS VARIABLES ###

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


class Pseq(Pattern):
    """
    A sequence pattern.

    ::

        >>> pattern = supriya.patterns.Pseq([1, 2, 3])
        >>> for x in pattern:
        ...     x
        ...
        1
        2
        3

    ::

        >>> pattern = supriya.patterns.Pseq([1, 10, 100], repetitions=2)
        >>> list(pattern)
        [1, 10, 100, 1, 10, 100]

    ::

        >>> pattern = supriya.patterns.Pseq(
        ...     [
        ...         supriya.patterns.Pseq([1, 2, 3], repetitions=1),
        ...         supriya.patterns.Pseq([4, 5, 6], repetitions=1),
        ...     ],
        ...     repetitions=2,
        ... )
        >>> list(pattern)
        [1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6]

    """

    ### INITIALIZER ###

    def __init__(self, sequence, repetitions=1):
        assert isinstance(sequence, Sequence)
        self._sequence = self._freeze_recursive(sequence)
        if repetitions is not None:
            repetitions = int(repetitions)
            assert 0 < repetitions
        self._repetitions = repetitions

    ### PRIVATE METHODS ###

    def _iterate(self, state=None):
        should_stop = self.PatternState.CONTINUE
        for _ in self._loop(self._repetitions):
            for x in self._sequence:
                if not isinstance(x, Pattern):
                    should_stop = yield x
                else:
                    iterator = iter(x)
                    try:
                        y = next(iterator)
                        should_stop = yield y
                        while True:
                            y = iterator.send(should_stop)
                            should_stop = yield y
                    except StopIteration:
                        pass
                if should_stop:
                    return

    ### PUBLIC PROPERTIES ###

    @property
    def arity(self):
        """
        Gets arity of Pseq.

        ::

            >>> pattern = supriya.patterns.Pseq([1, 2, 3])
            >>> pattern.arity
            1

        ::

            >>> pattern = supriya.patterns.Pseq([[1, 2], 3, 4])
            >>> pattern.arity
            2

        ::

            >>> pattern = supriya.patterns.Pseq(
            ...     [supriya.patterns.Pseq([1, 2, 3]), supriya.patterns.Pseq([[1, 2], 3, 4]),]
            ... )
            >>> pattern.arity
            2

        Returns integer.
        """
        return max(self._get_arity(x) for x in self.sequence)

    @property
    def is_infinite(self):
        import supriya.patterns

        if self.repetitions is None:
            return True
        for x in self.sequence:
            if isinstance(x, supriya.patterns.Pattern) and x.is_infinite:
                return True
        return False

    @property
    def repetitions(self):
        return self._repetitions

    @property
    def sequence(self):
        return self._sequence


class Prand(Pseq):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def _iterate(self, state=None):
        rng = self._get_rng()
        for _ in self._loop(self._repetitions):
            index = int(next(rng) * 0x7FFFFFFF) % len(self.sequence)
            choice = self.sequence[index]
            if isinstance(choice, Pattern):
                yield from choice
            else:
                yield choice


class Pwhite(Pattern):

    ### INITIALIZER ###

    def __init__(self, minimum=0.0, maximum=1.0, repetitions=None):
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
            return (number * (maximum - minimum)) + minimum

        rng = self._get_rng()
        for _ in self._loop(self._repetitions):
            expr = self._process_recursive(self._minimum, self._maximum, procedure)
            should_stop = yield expr
            if should_stop:
                return

    ### PUBLIC PROPERTIES ###

    @property
    def arity(self):
        """
        Gets arity of Pwhite.

        ::

            >>> pattern = supriya.patterns.Pwhite(0.0, 1.0)
            >>> pattern.arity
            1

        ::

            >>> pattern = supriya.patterns.Pwhite([0.0, 0.1], 2)
            >>> pattern.arity
            2

        Returns integer.
        """
        return max(self._get_arity(x) for x in (self._minimum, self._maximum))

    @property
    def is_infinite(self):
        return self._repetitions is None

    @property
    def minimum(self):
        return self._minimum

    @property
    def maximum(self):
        return self._maximum

    @property
    def repetitions(self):
        return self._repetitions
