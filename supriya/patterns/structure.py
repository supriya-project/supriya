import bisect
from uuid import uuid4

from uqbar.objects import get_vars, new

from supriya.assets import synthdefs
from supriya.enums import CalculationRate

from .events import (
    BusAllocateEvent,
    BusFreeEvent,
    CompositeEvent,
    GroupAllocateEvent,
    NodeFreeEvent,
    NullEvent,
    SynthAllocateEvent,
)
from .patterns import Pattern


class BusPattern(Pattern):

    ### INITIALIZER ###

    def __init__(
        self, pattern, calculation_rate="audio", channel_count=1, release_time=0.25
    ):
        self._pattern = pattern
        self._calculation_rate = CalculationRate.from_expr(calculation_rate)
        self._channel_count = channel_count
        self._release_time = release_time

    ### PRIVATE METHODS ###

    def _adjust(self, expr, state):
        args, _, kwargs = get_vars(expr)
        updates = {}
        if hasattr(expr, "target_node") and expr.target_node is None:
            updates["target_node"] = state["group"]
        if hasattr(expr, "synthdef"):
            synthdef = getattr(expr, "synthdef") or synthdefs.default
            parameter_names = synthdef.parameter_names
            for name in ("in_", "out"):
                if name in parameter_names and kwargs.get(name) is None:
                    updates[name] = state["bus"]
        if updates:
            return new(expr, **updates)
        return expr

    def _iterate(self, state=None):
        return iter(self._pattern)

    def _setup_peripherals(self, state):
        rate = self._calculation_rate.name.lower()
        link_synthdef_name = f"system_link_{rate}_{self._channel_count}"
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
                synthdef=getattr(synthdefs, link_synthdef_name),
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

    def _setup_state(self):
        return {"bus": uuid4(), "link": uuid4(), "group": uuid4()}

    ### PUBLIC PROPERTIES ###

    @property
    def is_infinite(self):
        return self._pattern.is_infinite


class FxPattern(Pattern):

    ### INITIALIZER ###

    def __init__(self, pattern, synthdef, release_time=0.25, **kwargs):
        self._pattern = pattern
        self._release_time = release_time
        self._synthdef = synthdef
        self._kwargs = kwargs

    ### PRIVATE METHODS ###

    def _iterate(self, state=None):
        return iter(self._pattern)

    def _setup_peripherals(self, state):
        starts = [
            SynthAllocateEvent(
                add_action="ADD_TO_TAIL",
                synthdef=self._synthdef,
                id_=state["synth"],
                **self._kwargs,
            )
        ]
        stops = [NodeFreeEvent(id_=state["synth"])]
        if self._release_time:
            stops.insert(0, NullEvent(delta=self._release_time))
        return CompositeEvent(starts), CompositeEvent(stops)

    def _setup_state(self):
        return {"synth": uuid4()}

    ### PUBLIC PROPERTIES ###

    @property
    def is_infinite(self):
        return self._pattern.is_infinite


class GroupPattern(Pattern):

    ### INITIALIZER ###

    def __init__(self, pattern, release_time=0.25):
        self._pattern = pattern
        self._release_time = release_time

    ### PRIVATE METHODS ###

    def _adjust(self, expr, state):
        updates = {}
        if hasattr(expr, "target_node") and expr.target_node is None:
            updates["target_node"] = state["group"]
        if updates:
            return new(expr, **updates)
        return expr

    def _iterate(self, state=None):
        return iter(self._pattern)

    def _setup_peripherals(self, state):
        starts = [GroupAllocateEvent(add_action="ADD_TO_HEAD", id_=state["group"])]
        stops = [NodeFreeEvent(id_=state["group"])]
        if self._release_time:
            stops.insert(0, NullEvent(delta=self._release_time))
        return CompositeEvent(starts), CompositeEvent(stops)

    def _setup_state(self):
        return {"group": uuid4()}

    ### PUBLIC PROPERTIES ###

    @property
    def is_infinite(self):
        return self._pattern.is_infinite


class ParallelPattern(Pattern):

    ### INITIALIZER ###

    def __init__(self, patterns):
        self._patterns = tuple(patterns)

    ### PRIVATE METHODS ###

    def _iterate(self, state=None):
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
    def is_infinite(self):
        return any(pattern.is_infinite for pattern in self._patterns)
