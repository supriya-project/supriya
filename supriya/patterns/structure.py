import bisect
from typing import Generator, Sequence, SupportsInt
from uuid import uuid4

from uqbar.objects import get_vars, new

from supriya.enums import CalculationRate

from ..typing import CalculationRateLike, UUIDDict
from ..ugens import SYSTEM_SYNTHDEFS, SynthDef, default
from .events import (
    BusAllocateEvent,
    BusFreeEvent,
    CompositeEvent,
    Event,
    GroupAllocateEvent,
    NodeFreeEvent,
    NullEvent,
    SynthAllocateEvent,
)
from .patterns import Pattern


class BusPattern(Pattern[Event]):
    """
    Peform node events from a pattern into a dynamically allocated bus and group.
    """

    ### INITIALIZER ###

    def __init__(
        self,
        pattern: Pattern[Event],
        calculation_rate: CalculationRateLike = "audio",
        channel_count: int = 1,
        release_time: float = 0.25,
    ) -> None:
        self._pattern = pattern
        self._calculation_rate: CalculationRate = CalculationRate.from_expr(
            calculation_rate
        )
        self._channel_count = channel_count
        self._release_time = release_time

    ### PRIVATE METHODS ###

    def _adjust(self, expr: Event, state: UUIDDict | None = None) -> Event:
        if state is None:
            raise RuntimeError
        args, _, kwargs = get_vars(expr)
        updates = {}
        if hasattr(expr, "target_node") and expr.target_node is None:
            updates["target_node"] = state["group"]
        if hasattr(expr, "synthdef"):
            synthdef = getattr(expr, "synthdef") or default
            parameter_names = synthdef.parameters
            for name in ("in_", "out"):
                if name in parameter_names and kwargs.get(name) is None:
                    updates[name] = state["bus"]
        if updates:
            return new(expr, **updates)
        return expr

    def _iterate(self, state: UUIDDict | None = None) -> Generator[Event, bool, None]:
        return iter(self._pattern)

    def _setup_peripherals(self, state: UUIDDict | None) -> tuple[Event, Event]:
        if state is None:
            raise RuntimeError
        token = self._calculation_rate.token
        link_synthdef_name = f"supriya:link-{token}:{self._channel_count}"
        starts = [
            BusAllocateEvent(
                calculation_rate=self._calculation_rate,
                channel_count=self._channel_count,
                id_=state["bus"],
            ),
            GroupAllocateEvent(id_=state["group"]),
            SynthAllocateEvent(
                add_action="ADD_AFTER",
                amplitude=1.0,
                fade_time=self._release_time,
                in_=state["bus"],
                synthdef=SYSTEM_SYNTHDEFS[link_synthdef_name],
                target_node=state["group"],
                id_=state["link"],
            ),
        ]
        stops = [
            NodeFreeEvent(id_=state["link"]),
            NodeFreeEvent(id_=state["group"]),
            BusFreeEvent(id_=state["bus"]),
        ]
        if self._release_time:
            stops.insert(1, NullEvent(delta=self._release_time))
        return CompositeEvent(starts), CompositeEvent(stops)

    def _setup_state(self) -> UUIDDict:
        return {"bus": uuid4(), "link": uuid4(), "group": uuid4()}

    ### PUBLIC PROPERTIES ###

    @property
    def is_infinite(self) -> bool:
        return self._pattern.is_infinite


class FxPattern(Pattern[Event]):
    """
    Add a synth to the tail of the nodes performed by a pattern.
    """

    ### INITIALIZER ###

    def __init__(
        self,
        pattern: Pattern[Event],
        synthdef: SynthDef,
        release_time: float = 0.25,
        **kwargs,
    ) -> None:
        self._pattern = pattern
        self._release_time = release_time
        self._synthdef = synthdef
        self._kwargs = kwargs

    ### PRIVATE METHODS ###

    def _iterate(self, state: UUIDDict | None = None) -> Generator[Event, bool, None]:
        return iter(self._pattern)

    def _setup_peripherals(self, state: UUIDDict | None = None) -> tuple[Event, Event]:
        if state is None:
            raise RuntimeError
        starts: list[Event] = [
            SynthAllocateEvent(
                add_action="ADD_TO_TAIL",
                synthdef=self._synthdef,
                id_=state["synth"],
                **self._kwargs,
            )
        ]
        stops: list[Event] = [NodeFreeEvent(id_=state["synth"])]
        if self._release_time:
            stops.insert(0, NullEvent(delta=self._release_time))
        return CompositeEvent(starts), CompositeEvent(stops)

    def _setup_state(self) -> UUIDDict:
        return {"synth": uuid4()}

    ### PUBLIC PROPERTIES ###

    @property
    def is_infinite(self) -> bool:
        return self._pattern.is_infinite


class GroupPattern(Pattern[Event]):
    """
    Perform node events from a pattern into a dynamically allocated group.
    """

    ### INITIALIZER ###

    def __init__(self, pattern: Pattern[Event], release_time: float = 0.25) -> None:
        self._pattern = pattern
        self._release_time = release_time

    ### PRIVATE METHODS ###

    def _adjust(self, expr: Event, state: UUIDDict | None = None) -> Event:
        if state is None:
            raise RuntimeError
        updates = {}
        if hasattr(expr, "target_node") and expr.target_node is None:
            updates["target_node"] = state["group"]
        if updates:
            return new(expr, **updates)
        return expr

    def _iterate(self, state: UUIDDict | None = None) -> Generator[Event, bool, None]:
        return iter(self._pattern)

    def _setup_peripherals(self, state: UUIDDict | None) -> tuple[Event, Event]:
        if state is None:
            raise RuntimeError
        starts: list[Event] = [
            GroupAllocateEvent(add_action="ADD_TO_HEAD", id_=state["group"])
        ]
        stops: list[Event] = [NodeFreeEvent(id_=state["group"])]
        if self._release_time:
            stops.insert(0, NullEvent(delta=self._release_time))
        return CompositeEvent(starts), CompositeEvent(stops)

    def _setup_state(self) -> UUIDDict:
        return {"group": uuid4()}

    ### PUBLIC PROPERTIES ###

    @property
    def is_infinite(self) -> bool:
        return self._pattern.is_infinite


class ParallelPattern(Pattern[Event]):
    """
    Perform patterns simultaneously in parallel.
    """

    ### INITIALIZER ###

    def __init__(self, patterns: Sequence[Pattern[Event]]) -> None:
        self._patterns = tuple(patterns)

    ### PRIVATE METHODS ###

    def _iterate(self, state: UUIDDict | None = None) -> Generator[Event, bool, None]:
        should_stop = False
        iterators = []
        for index, pattern in enumerate(self._patterns):
            iterators.append((0.0, index, iter(pattern)))
        while iterators:
            grouping_offset = iterators[0][0]
            events = []
            while iterators and iterators[0][0] == grouping_offset:
                offset, index, iterator = iterators.pop(0)
                try:
                    if should_stop:
                        event = iterator.send(should_stop)
                    else:
                        event = next(iterator)
                    events.append(event)
                    triple = (offset + event.delta, index, iterator)
                    insert_index = bisect.bisect_left(iterators, triple)
                    iterators.insert(insert_index, triple)
                except StopIteration:
                    pass
            if events:
                if iterators:
                    delta = iterators[0][0] - grouping_offset
                else:
                    delta = max(event.delta for event in events)
                if len(events) == 1:
                    sent = yield new(events[0], delta=delta)
                elif len(events) > 1:
                    sent = yield CompositeEvent(
                        [new(x, delta=0.0) for x in events], delta=delta
                    )
                if sent:
                    should_stop = True

    ### PUBLIC PROPERTIES ###

    @property
    def is_infinite(self) -> bool:
        return any(pattern.is_infinite for pattern in self._patterns)


class PinPattern(Pattern[Event]):
    """
    Utility pattern for assigning an explicit target bus and/or target node to NodeEvents.

    Used internally by pattern players.
    """

    ### INITIALIZER ###

    def __init__(
        self,
        pattern: Pattern[Event],
        *,
        target_bus: SupportsInt | None = None,
        target_node: SupportsInt | None = None,
    ) -> None:
        self._pattern = pattern
        self._target_bus = target_bus
        self._target_node = target_node

    def _adjust(self, expr: Event, state: UUIDDict | None = None) -> Event:
        args, _, kwargs = get_vars(expr)
        updates = {}
        if self._target_node is not None and hasattr(expr, "target_node"):
            updates["target_node"] = expr.target_node or self._target_node
        if self._target_bus is not None and hasattr(expr, "synthdef"):
            synthdef = getattr(expr, "synthdef") or default
            parameter_names = synthdef.parameters
            for name in ("in_", "out"):
                if name in parameter_names and kwargs.get(name) is None:
                    updates[name] = self._target_bus
        if updates:
            return new(expr, **updates)
        return expr

    ### PRIVATE METHODS ###

    def _iterate(self, state: UUIDDict | None = None) -> Generator[Event, bool, None]:
        return iter(self._pattern)

    ### PUBLIC PROPERTIES ###

    @property
    def is_infinite(self) -> bool:
        return self._pattern.is_infinite
