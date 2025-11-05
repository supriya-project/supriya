"""
The core pattern classes.
"""

import abc
import inspect
import itertools
import operator
import random
from typing import (
    TYPE_CHECKING,
    Callable,
    Generator,
    Generic,
    Iterator,
    Sequence,
    TypeVar,
    Union,
    cast,
)
from uuid import UUID

from uqbar.objects import get_vars

from ..clocks import BaseClock, ClockCallbackState, Quantization
from ..contexts import Bus, Context, Node
from ..typing import UUIDDict
from .events import CompositeEvent, Event, Priority

if TYPE_CHECKING:
    from .players import PatternPlayer

T = TypeVar("T")


class Pattern(Generic[T], metaclass=abc.ABCMeta):
    ### CLASSMETHODS ###

    _rngs: dict[int, Iterator[float]] = {}

    ### SPECIAL METHODS ###

    def __abs__(self) -> "UnaryOpPattern[T]":
        return UnaryOpPattern(operator.abs, self)

    def __add__(self, expr: Union["Pattern[T]", T]) -> "BinaryOpPattern[T]":
        return BinaryOpPattern(operator.add, self, expr)

    def __and__(self, expr: Union["Pattern[T]", T]) -> "BinaryOpPattern[T]":
        return BinaryOpPattern(operator.and_, self, expr)

    def __eq__(self, expr) -> bool:
        self_values = type(self), get_vars(self)
        try:
            expr_values = type(expr), get_vars(expr)
        except AttributeError:
            expr_values = type(expr), expr
        return self_values == expr_values

    def __floordiv__(self, expr: Union["Pattern[T]", T]) -> "BinaryOpPattern[T]":
        return BinaryOpPattern(operator.floordiv, self, expr)

    def __ge__(self, expr: Union["Pattern[T]", T]) -> "BinaryOpPattern[T]":
        return BinaryOpPattern(operator.ge, self, expr)

    def __gt__(self, expr: Union["Pattern[T]", T]) -> "BinaryOpPattern[T]":
        return BinaryOpPattern(operator.gt, self, expr)

    def __invert__(self) -> "UnaryOpPattern[T]":
        return UnaryOpPattern(operator.invert, self)

    def __iter__(self) -> Generator[T, bool, None]:
        should_stop = False
        state: UUIDDict | None = self._setup_state()
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

    def __le__(self, expr: Union["Pattern[T]", T]) -> "BinaryOpPattern[T]":
        return BinaryOpPattern(operator.le, self, expr)

    def __lshift__(self, expr: Union["Pattern[T]", T]) -> "BinaryOpPattern[T]":
        return BinaryOpPattern(operator.lshift, self, expr)

    def __lt__(self, expr: Union["Pattern[T]", T]) -> "BinaryOpPattern[T]":
        return BinaryOpPattern(operator.lt, self, expr)

    def __mod__(self, expr: Union["Pattern[T]", T]) -> "BinaryOpPattern[T]":
        return BinaryOpPattern(operator.mod, self, expr)

    def __mul__(self, expr: Union["Pattern[T]", T]) -> "BinaryOpPattern[T]":
        return BinaryOpPattern(operator.mul, self, expr)

    def __neg__(self) -> "UnaryOpPattern[T]":
        return UnaryOpPattern(operator.neg, self)

    def __or__(self, expr: Union["Pattern[T]", T]) -> "BinaryOpPattern[T]":
        return BinaryOpPattern(operator.or_, self, expr)

    def __pos__(self) -> "UnaryOpPattern[T]":
        return UnaryOpPattern(operator.pos, self)

    def __pow__(self, expr: Union["Pattern[T]", T]) -> "BinaryOpPattern[T]":
        return BinaryOpPattern(operator.pow, self, expr)

    def __radd__(self, expr: Union["Pattern[T]", T]) -> "BinaryOpPattern[T]":
        return BinaryOpPattern(operator.add, expr, self)

    def __rand__(self, expr: Union["Pattern[T]", T]) -> "BinaryOpPattern[T]":
        return BinaryOpPattern(operator.and_, expr, self)

    def __rfloordiv__(self, expr: Union["Pattern[T]", T]) -> "BinaryOpPattern[T]":
        return BinaryOpPattern(operator.floordiv, expr, self)

    def __rlshift__(self, expr: Union["Pattern[T]", T]) -> "BinaryOpPattern[T]":
        return BinaryOpPattern(operator.lshift, expr, self)

    def __rmod__(self, expr: Union["Pattern[T]", T]) -> "BinaryOpPattern[T]":
        return BinaryOpPattern(operator.mod, expr, self)

    def __rmul__(self, expr: Union["Pattern[T]", T]) -> "BinaryOpPattern[T]":
        return BinaryOpPattern(operator.mul, expr, self)

    def __ror__(self, expr: Union["Pattern[T]", T]) -> "BinaryOpPattern[T]":
        return BinaryOpPattern(operator.or_, expr, self)

    def __rpow__(self, expr: Union["Pattern[T]", T]) -> "BinaryOpPattern[T]":
        return BinaryOpPattern(operator.pow, expr, self)

    def __rrshift__(self, expr: Union["Pattern[T]", T]) -> "BinaryOpPattern[T]":
        return BinaryOpPattern(operator.rshift, expr, self)

    def __rshift__(self, expr: Union["Pattern[T]", T]) -> "BinaryOpPattern[T]":
        return BinaryOpPattern(operator.rshift, self, expr)

    def __rsub__(self, expr: Union["Pattern[T]", T]) -> "BinaryOpPattern[T]":
        return BinaryOpPattern(operator.sub, expr, self)

    def __rtruediv__(self, expr: Union["Pattern[T]", T]) -> "BinaryOpPattern[T]":
        return BinaryOpPattern(operator.truediv, expr, self)

    def __rxor__(self, expr: Union["Pattern[T]", T]) -> "BinaryOpPattern[T]":
        return BinaryOpPattern(operator.xor, expr, self)

    def __sub__(self, expr: Union["Pattern[T]", T]) -> "BinaryOpPattern[T]":
        return BinaryOpPattern(operator.sub, self, expr)

    def __truediv__(self, expr: Union["Pattern[T]", T]) -> "BinaryOpPattern[T]":
        return BinaryOpPattern(operator.truediv, self, expr)

    def __xor__(self, expr: Union["Pattern[T]", T]) -> "BinaryOpPattern[T]":
        return BinaryOpPattern(operator.xor, self, expr)

    ### PRIVATE METHODS ###

    def _adjust(self, expr: T, state: UUIDDict | None = None) -> T:
        return expr

    def _adjust_recursive(self, expr: T, state: UUIDDict | None = None) -> T:
        if isinstance(expr, CompositeEvent):
            return cast(
                T,
                CompositeEvent(
                    [
                        cast(Event, self._adjust_recursive(cast(T, event), state=state))
                        for event in expr.events
                    ],
                    delta=expr.delta,
                ),
            )
        return self._adjust(expr, state=state)

    def _apply_recursive(self, procedure, *exprs):
        if all(
            not isinstance(x, Sequence) or isinstance(x, (str, bytes)) for x in exprs
        ):
            return procedure(*exprs)
        coerced_exprs = [
            (
                expr
                if (isinstance(expr, Sequence) and not isinstance(expr, (str, bytes)))
                else [expr]
            )
            for expr in exprs
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

    def _get_rng(self) -> Iterator[float]:
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
        mask = 0x7FFFFFFF
        while True:
            seed = (seed * 1_103_515_245 + 12345) & mask
            yield float(seed) / mask

    def _get_stdlib_rng(self) -> Iterator[float]:
        while True:
            yield random.random()

    @abc.abstractmethod
    def _iterate(self, state: UUIDDict | None = None) -> Generator[T, bool, None]:
        raise NotImplementedError

    def _loop(self, iterations: int | None = None) -> Iterator[bool]:
        if iterations is None:
            while True:
                yield True
        else:
            for _ in range(iterations):
                yield True

    def _setup_state(self) -> UUIDDict | None:
        return None

    def _setup_peripherals(self, state: UUIDDict | None) -> tuple[T | None, T | None]:
        return None, None

    ### PUBLIC METHODS ###

    def play(
        self,
        context: Context,
        *,
        callback: (
            Callable[
                ["PatternPlayer", ClockCallbackState, Event, Priority],
                None,
            ]
            | None
        ) = None,
        clock: BaseClock,
        quantization: Quantization | None = None,
        target_bus: Bus | None = None,
        target_node: Node | None = None,
        tempo: float | None = None,
        until: float | None = None,
        uuid: UUID | None = None,
    ) -> "PatternPlayer":
        from .players import PatternPlayer  # Avoid circular import

        player = PatternPlayer(
            pattern=self,
            context=context,
            clock=clock,
            callback=callback,
            target_bus=target_bus,
            target_node=target_node,
            uuid=uuid,
        )
        player.play(quantization=quantization, until=until)
        return player

    ### PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def is_infinite(self) -> bool:
        raise NotImplementedError


class BinaryOpPattern(Pattern[T]):
    ### INITIALIZER ###

    def __init__(
        self,
        operator_: Callable,
        expr_one: Union[Pattern[T], T],
        expr_two: Union[Pattern[T], T],
    ) -> None:
        self.operator_ = operator_
        self.expr_one = self._freeze_recursive(expr_one)
        self.expr_two = self._freeze_recursive(expr_two)

    ### PRIVATE METHODS ###

    def _iterate(self, state: UUIDDict | None = None) -> Generator[T, bool, None]:
        iterator_one: Iterator[T] = iter(
            self.expr_one
            if isinstance(self.expr_one, Pattern)
            else SequencePattern([self.expr_one], None)
        )
        iterator_two: Iterator[T] = iter(
            self.expr_two
            if isinstance(self.expr_two, Pattern)
            else SequencePattern([self.expr_two], None)
        )
        for item_one, item_two in zip(iterator_one, iterator_two):
            yield self._apply_recursive(self.operator_, item_one, item_two)

    ### PUBLIC PROPERTIES ###

    @property
    def is_infinite(self) -> bool:
        expr_one_is_infinite = (
            not isinstance(self.expr_one, Pattern) or self.expr_one.is_infinite
        )
        expr_two_is_infinite = (
            not isinstance(self.expr_two, Pattern) or self.expr_two.is_infinite
        )
        return expr_one_is_infinite and expr_two_is_infinite


class UnaryOpPattern(Pattern[T]):
    ### INITIALIZER ###

    def __init__(self, operator_: Callable, expr: Union[Pattern[T], T]) -> None:
        self.operator_ = operator_
        self.expr = expr

    def _iterate(self, state: UUIDDict | None = None) -> Generator[T, bool, None]:
        iterator: Iterator[T] = iter(
            self.expr
            if isinstance(self.expr, Pattern)
            else SequencePattern([self.expr], None)
        )
        for item in iterator:
            yield self._apply_recursive(self.operator_, item)

    ### PUBLIC PROPERTIES ###

    @property
    def is_infinite(self) -> bool:
        return not isinstance(self.expr, Pattern) or self.expr.is_infinite


class SeedPattern(Pattern[T]):
    ### INITIALIZER ###

    def __init__(self, pattern: Pattern[T], seed: int = 0) -> None:
        if not isinstance(pattern, Pattern):
            raise ValueError(f"Must be pattern: {pattern!r}")
        self._pattern = pattern
        self._seed = int(seed)

    ### PRIVATE METHODS ###

    def _iterate(self, state: UUIDDict | None = None) -> Generator[T, bool, None]:
        try:
            identifier = id(inspect.currentframe())
            rng = self._get_seeded_rng(seed=self.seed)
            self._rngs[identifier] = rng
            yield from self._pattern
        finally:
            del self._rngs[identifier]

    ### PUBLIC PROPERTIES ###

    @property
    def is_infinite(self) -> bool:
        return self._pattern.is_infinite

    @property
    def pattern(self) -> Pattern:
        return self._pattern

    @property
    def seed(self) -> int:
        return self._seed


class SequencePattern(Pattern[T]):
    ### INITIALIZER ###

    def __init__(
        self, sequence: Sequence[Union[T, Pattern[T]]], iterations: int | None = 1
    ) -> None:
        if not isinstance(sequence, Sequence):
            raise ValueError(f"Must be sequence: {sequence!r}")
        if iterations is not None:
            iterations = int(iterations)
            if iterations < 1:
                raise ValueError("Iterations must be null or greater than 0")
        self._sequence: Sequence[Union[T, Pattern[T]]] = self._freeze_recursive(
            sequence
        )
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
    def is_infinite(self) -> bool:
        if self._iterations is None:
            return True
        x: Union[T, Pattern[T]]
        for x in self._sequence:
            if isinstance(x, Pattern) and x.is_infinite:
                return True
        return False
