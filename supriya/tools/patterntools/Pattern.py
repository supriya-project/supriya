# -*- encoding: utf-8 -*-
import abc
import collections
import inspect
import itertools
from supriya.tools.systemtools.SupriyaValueObject import SupriyaValueObject


class Pattern(SupriyaValueObject):
    """
    Pattern base class.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    _filename = __file__

    _rngs = {}

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    ### SPECIAL METHODS ###

    def __add__(self, expr):
        """
        Adds `expr` to pattern.

        ::

            >>> pattern = patterntools.Pseq([1, 2, 3])
            >>> expr = patterntools.Pseq([0, 10])
            >>> list(pattern + expr)
            [1, 12]

        ::

            >>> expr = 10
            >>> list(pattern + expr)
            [11, 12, 13]

        ::

            >>> expr = [10, [100, 1000]]
            >>> list(pattern + expr)
            [[11, [101, 1001]], [12, [102, 1002]], [13, [103, 1003]]]

        ::

            >>> pattern = patterntools.Pseq([[1, [2, 3]], [[4, 5], 6, 7]])
            >>> expr = [10, [100, 1000]]
            >>> for x in (pattern + expr):
            ...     x
            ...
            [11, [102, 1003]]
            [[14, 15], [106, 1006], 17]

        """
        from supriya.tools import patterntools
        return patterntools.Pbinop(self, '+', expr)

    def __div__(self, expr):
        from supriya.tools import patterntools
        return patterntools.Pbinop(self, '/', expr)

    def __mul__(self, expr):
        from supriya.tools import patterntools
        return patterntools.Pbinop(self, '*', expr)

    def __radd__(self, expr):
        from supriya.tools import patterntools
        return patterntools.Pbinop(expr, '+', self)

    def __rdiv__(self, expr):
        from supriya.tools import patterntools
        return patterntools.Pbinop(expr, '/', self)

    def __rmul__(self, expr):
        from supriya.tools import patterntools
        return patterntools.Pbinop(expr, '*', self)

    def __rsub__(self, expr):
        from supriya.tools import patterntools
        return patterntools.Pbinop(expr, '-', self)

    def __sub__(self, expr):
        from supriya.tools import patterntools
        return patterntools.Pbinop(self, '-', expr)

    def __iter__(self):
        yield_count = 0
        should_stop = False
        state = self._setup_state()
        iterator = self._iterate(state)
        try:
            expr = next(iterator)
            expr = self._coerce_iterator_output(expr, state)
        except StopIteration:
            return
        exprs = self._handle_first(expr, state)
        while len(exprs) > 1:
            expr = exprs.pop(0)
            should_stop = yield expr
            yield_count += 1
            if should_stop:
                iterator.send(True)
                exprs[:] = [exprs[0]]
                break
        if not should_stop:
            try:
                for expr in iterator:
                    expr = self._coerce_iterator_output(expr, state)
                    exprs.append(expr)
                    expr = exprs.pop(0)
                    should_stop = yield expr
                    if should_stop:
                        iterator.send(True)
                        break
            except StopIteration:
                pass
        exprs.extend(self._handle_last(exprs.pop(), state, yield_count))
        for expr in exprs:
            yield expr

    ### PRIVATE METHODS ###

    def _coerce_iterator_output(self, expr, state=None):
        return expr

    @classmethod
    def _coerce_floats(cls, value):
        if isinstance(value, collections.Sequence):
            value = tuple(float(_) for _ in value)
            assert value
        else:
            value = float(value)
        return value

    @classmethod
    def _freeze_recursive(cls, value):
        if (
            isinstance(value, collections.Sequence) and
            not isinstance(value, Pattern)
            ):
            return tuple(cls._freeze_recursive(_) for _ in value)
        return value

    @classmethod
    def _get_arity(cls, value):
        if isinstance(value, Pattern):
            return value.arity
        elif isinstance(value, collections.Sequence):
            return len(value)
        return 1

    @classmethod
    def _get_rng(cls, seed=None):
        from supriya.tools import patterntools
        identifier = None
        try:
            stack = inspect.stack()
            for frame_info in reversed(stack):
                if frame_info.filename != cls._filename:
                    continue
                elif frame_info.function != '__iter__':
                    continue
                identifier = id(frame_info.frame)
                break
        finally:
            del(frame_info)
            del(stack)
        if identifier in cls._rngs:
            rng = cls._rngs[identifier]
        elif identifier is None:
            rng = iter(patterntools.RandomNumberGenerator(seed or 1))
        else:
            rng = cls._rngs.setdefault(
                identifier,
                iter(patterntools.RandomNumberGenerator(seed or 1))
                )
        return rng, identifier

    def _handle_first(self, expr, state=None):
        return [expr]

    def _handle_last(self, expr, state=None, yield_count=0):
        return [expr]

    @abc.abstractmethod
    def _iterate(self, state=None):
        raise NotImplementedError

    @classmethod
    def _loop(cls, repetitions=None):
        if repetitions is None:
            while True:
                yield True
        else:
            for _ in range(repetitions):
                yield True

    @classmethod
    def _process_recursive(cls, one, two, procedure):
        if not isinstance(one, collections.Sequence) and \
            not isinstance(two, collections.Sequence):
            return procedure(one, two)
        if not isinstance(one, collections.Sequence):
            one = [one]
        if not isinstance(two, collections.Sequence):
            two = [two]
        length = max(len(one), len(two))
        if len(one) < length:
            cycle = itertools.cycle(one)
            one = (next(cycle) for _ in range(length))
        if len(two) < length:
            cycle = itertools.cycle(two)
            two = (next(cycle) for _ in range(length))
        result = []
        for one, two in zip(one, two):
            result.append(cls._process_recursive(one, two, procedure))
        return result

    def _setup_state(self):
        return None

    ### PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def arity(self):
        raise NotImplementedError

    @abc.abstractproperty
    def is_infinite(self):
        raise NotImplementedError
