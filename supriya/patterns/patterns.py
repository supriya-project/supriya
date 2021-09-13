"""
The core pattern classes.
"""
import abc
import inspect
import itertools
import operator
import random
from collections.abc import Sequence
from typing import Dict, Iterator, Optional

from uqbar.objects import get_vars

from supriya.clocks import Clock, OfflineClock
from supriya.providers import NonrealtimeProvider, Provider

from .events import CompositeEvent
from .players import PatternPlayer


class Pattern(metaclass=abc.ABCMeta):

    ### CLASSMETHODS ###

    _rngs: Dict[int, Iterator[float]] = {}

    ### SPECIAL METHODS ###

    def __abs__(self):
        return UnaryOpPattern("abs", self)

    def __add__(self, expr):
        return BinaryOpPattern("+", self, expr)

    def __eq__(self, expr):
        self_values = type(self), get_vars(self)
        try:
            expr_values = type(expr), get_vars(expr)
        except AttributeError:
            expr_values = type(expr), expr
        return self_values == expr_values

    def __floordiv__(self, expr):
        return BinaryOpPattern("//", self, expr)

    def __invert__(self):
        return UnaryOpPattern("~", self)

    def __iter__(self):
        should_stop = False
        state: Optional[Dict] = self._setup_state()
        iterator = self._iterate(state)
        try:
            expr = self._adjust_recursive(next(iterator), state=state)
        except StopIteration:
            return
        start_event, stop_event = self._setup_peripherals(state)
        if start_event:
            should_stop = (yield start_event) or should_stop
        if not should_stop:
            should_stop = (yield expr) or should_stop
            while True:  # Exhaust iterator, even if scheduled to stop
                try:
                    expr = self._adjust_recursive(
                        iterator.send(should_stop), state=state
                    )
                    should_stop = (yield expr) or should_stop
                except StopIteration:
                    break
        if stop_event:
            yield stop_event

    def __mod__(self, expr):
        return BinaryOpPattern("%", self, expr)

    def __mul__(self, expr):
        return BinaryOpPattern("*", self, expr)

    def __neg__(self):
        return UnaryOpPattern("-", self)

    def __pos__(self):
        return UnaryOpPattern("+", self)

    def __pow__(self, expr):
        return BinaryOpPattern("**", self, expr)

    def __radd__(self, expr):
        return BinaryOpPattern("+", expr, self)

    def __rmod__(self, expr):
        return BinaryOpPattern("%", expr, self)

    def __rmul__(self, expr):
        return BinaryOpPattern("*", expr, self)

    def __rpow__(self, expr):
        return BinaryOpPattern("**", expr, self)

    def __rsub__(self, expr):
        return BinaryOpPattern("-", expr, self)

    def __rtruediv__(self, expr):
        return BinaryOpPattern("/", expr, self)

    def __rfloordiv__(self, expr):
        return BinaryOpPattern("//", expr, self)

    def __sub__(self, expr):
        return BinaryOpPattern("-", self, expr)

    def __truediv__(self, expr):
        return BinaryOpPattern("/", self, expr)

    ### PRIVATE METHODS ###

    def _adjust(self, expr, state=None):
        return expr

    def _adjust_recursive(self, expr, state=None):
        if isinstance(expr, CompositeEvent):
            return CompositeEvent(
                [self._adjust(event, state=state) for event in expr.events],
                delta=expr.delta,
            )
        return self._adjust(expr, state=state)

    def _apply_recursive(self, procedure, *exprs):
        if all(not isinstance(x, Sequence) for x in exprs):
            return procedure(*exprs)
        coerced_exprs = [
            expr if isinstance(expr, Sequence) else [expr] for expr in exprs
        ]
        max_length = max(len(expr) for expr in coerced_exprs)
        for i, expr in enumerate(coerced_exprs):
            if len(expr) < max_length:
                cycle = itertools.cycle(expr)
                coerced_exprs[i] = [next(cycle) for _ in range(max_length)]
        return tuple(
            self._apply_recursive(procedure, *items) for items in zip(*coerced_exprs)
        )

    def _freeze_recursive(self, value):
        if isinstance(value, str):
            return value
        elif isinstance(value, Sequence) and not isinstance(value, Pattern):
            return tuple(self._freeze_recursive(_) for _ in value)
        return value

    def _get_rng(self):
        identifier = None
        try:
            # Walk frames to find an enclosing SeedPattern._iterate()
            frame = inspect.currentframe()
            while frame is not None:
                if (
                    isinstance(frame.f_locals.get("self"), SeedPattern)
                    and frame.f_code.co_name == "_iterate"
                ):
                    identifier = id(frame)
                    break
                frame = frame.f_back
        finally:
            del frame
        if identifier in self._rngs:
            return self._rngs[identifier]
        return self._get_stdlib_rng()

    def _get_seeded_rng(self, seed: int = 1) -> Iterator[float]:
        while True:
            seed = (seed * 1_103_515_245 + 12345) & 0x7FFFFFFF
            yield float(seed) / 0x7FFFFFFF

    def _get_stdlib_rng(self) -> Iterator[float]:
        while True:
            yield random.random()

    @abc.abstractmethod
    def _iterate(self):
        raise NotImplementedError

    def _loop(self, iterations=None):
        if iterations is None:
            while True:
                yield True
        else:
            for _ in range(iterations):
                yield True

    def _setup_state(self) -> Optional[Dict]:
        return None

    def _setup_peripherals(self, state):
        return None, None

    ### PUBLIC METHODS ###

    def play(
        self,
        provider=None,
        *,
        at=None,
        clock=None,
        quantization=None,
        tempo=None,
        until=None,
    ):
        if provider is None:
            provider = Provider.realtime()
        elif not isinstance(provider, Provider):
            provider = Provider.from_context(provider)
        if isinstance(provider, NonrealtimeProvider):
            clock = OfflineClock()
            at = at or 0.0
        elif not clock:
            clock = Clock.default()
        player = PatternPlayer(pattern=self, provider=provider, clock=clock)
        player.play(quantization=quantization, at=at, until=until)
        return player

    ### PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def is_infinite(self):
        raise NotImplementedError


class BinaryOpPattern(Pattern):

    ### INITIALIZER ###

    def __init__(self, operator, expr_one, expr_two):
        self._operator = operator
        self._expr_one = self._freeze_recursive(expr_one)
        self._expr_two = self._freeze_recursive(expr_two)

    ### PRIVATE METHODS ###

    def _iterate(self, state=None):
        expr_one = self.expr_one
        if not isinstance(expr_one, Pattern):
            expr_one = SequencePattern([expr_one], None)
        expr_one = iter(expr_one)
        expr_two = self.expr_two
        if not isinstance(expr_two, Pattern):
            expr_two = SequencePattern([expr_two], None)
        expr_two = iter(expr_two)
        operator = self._string_to_operator()
        for item_one, item_two in zip(expr_one, expr_two):
            yield self._apply_recursive(operator, item_one, item_two)

    def _string_to_operator(self):
        operators = {
            "%": operator.__mod__,
            "*": operator.__mul__,
            "**": operator.__pow__,
            "+": operator.__add__,
            "-": operator.__sub__,
            "/": operator.__truediv__,
            "//": operator.__floordiv__,
        }
        return operators[self.operator]

    ### PUBLIC PROPERTIES ###

    @property
    def expr_one(self):
        return self._expr_one

    @property
    def expr_two(self):
        return self._expr_two

    @property
    def is_infinite(self):
        expr_one_is_infinite = (
            not isinstance(self.expr_one, Pattern) or self.expr_one.is_infinite
        )
        expr_two_is_infinite = (
            not isinstance(self.expr_two, Pattern) or self.expr_two.is_infinite
        )
        return expr_one_is_infinite and expr_two_is_infinite

    @property
    def operator(self):
        return self._operator


class UnaryOpPattern(Pattern):

    ### INITIALIZER ###

    def __init__(self, operator, expr):
        self._operator = operator
        self._expr = expr

    ### PRIVATE METHODS ###

    def _iterate(self, state=None):
        expr = self.expr
        if not isinstance(expr, Pattern):
            expr = SequencePattern([expr], None)
        expr = iter(expr)
        operator = self._string_to_operator()
        for item in expr:
            yield self._apply_recursive(operator, item)

    def _string_to_operator(self):
        operators = {
            "~": operator.invert,
            "-": operator.__neg__,
            "+": operator.__pos__,
            "abs": operator.abs,
        }
        return operators[self.operator]

    ### PUBLIC PROPERTIES ###

    @property
    def expr(self):
        return self._expr

    @property
    def is_infinite(self):
        return not isinstance(self.expr, Pattern) or self.expr.is_infinite

    @property
    def operator(self):
        return self._operator


class SeedPattern(Pattern):

    ### INITIALIZER ###

    def __init__(self, pattern, seed=0):
        if not isinstance(pattern, Pattern):
            raise ValueError(f"Must be pattern: {pattern!r}")
        self._pattern = pattern
        self._seed = int(seed)

    ### PRIVATE METHODS ###

    def _iterate(self, state=None):
        try:
            identifier = id(inspect.currentframe())
            rng = self._get_seeded_rng(seed=self.seed)
            self._rngs[identifier] = rng
            yield from self._pattern
        finally:
            del self._rngs[identifier]

    ### PUBLIC PROPERTIES ###

    @property
    def is_infinite(self):
        return self._pattern.is_infinite

    @property
    def pattern(self):
        return self._pattern

    @property
    def seed(self):
        return self._seed


class SequencePattern(Pattern):

    ### INITIALIZER ###

    def __init__(self, sequence, iterations=1):
        if not isinstance(sequence, Sequence):
            raise ValueError(f"Must be sequence: {sequence!r}")
        if iterations is not None:
            iterations = int(iterations)
            if iterations < 1:
                raise ValueError("Iterations must be null or greater than 0")
        self._sequence = self._freeze_recursive(sequence)
        self._iterations = iterations

    ### PRIVATE METHODS ###

    def _iterate(self, state=None):
        should_stop = False
        for _ in self._loop(self._iterations):
            for x in self._sequence:
                if not isinstance(x, Pattern):
                    should_stop = (yield x) or should_stop
                else:
                    iterator = iter(x)
                    try:
                        y = next(iterator)
                        should_stop = (yield y) or should_stop
                        while True:
                            y = iterator.send(should_stop)
                            should_stop = (yield y) or should_stop
                    except StopIteration:
                        pass
                if should_stop:
                    return

    ### PUBLIC PROPERTIES ###

    @property
    def is_infinite(self):
        if self._iterations is None:
            return True
        for x in self._sequence:
            if isinstance(x, Pattern) and x.is_infinite:
                return True
        return False
