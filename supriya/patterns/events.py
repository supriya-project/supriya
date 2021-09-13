import enum
from typing import Dict, Optional, Tuple
from uuid import UUID

from uqbar.objects import get_repr, get_vars, new

from supriya.enums import AddAction, CalculationRate
from supriya.synthdefs import SynthDef
from supriya.utils import expand


class Priority(enum.IntEnum):
    START = 1
    STOP = 2


class Event:
    def __init__(self, *, delta=0.0):
        self.delta = delta

    def __eq__(self, expr):
        self_values = type(self), get_vars(self)
        try:
            expr_values = type(expr), get_vars(expr)
        except AttributeError:
            expr_values = type(expr), expr
        return self_values == expr_values

    def __repr__(self):
        return get_repr(self, multiline=False)

    def expand(self, offset):
        return [(offset, Priority.START, self)]

    def perform(
        self,
        provider,
        proxy_mapping,
        *,
        current_offset: float,
        notes_mapping: Dict[Tuple[UUID, int], float],
        priority: int,
    ):
        raise NotImplementedError


class BusAllocateEvent(Event):
    def __init__(self, id_, *, calculation_rate="audio", channel_count=1, delta=0.0):
        Event.__init__(self, delta=delta)
        self.id_ = id_
        self.calculation_rate = CalculationRate.from_expr(calculation_rate)
        self.channel_count = channel_count

    def perform(
        self,
        provider,
        proxy_mapping,
        *,
        current_offset: float,
        notes_mapping: Dict[Tuple[UUID, int], float],
        priority: int,
    ):
        proxy_mapping[self.id_] = provider.add_bus_group(
            calculation_rate=self.calculation_rate, channel_count=self.channel_count
        )


class BusFreeEvent(Event):
    def __init__(self, id_, *, delta=0.0):
        Event.__init__(self, delta=delta)
        self.id_ = id_

    def perform(
        self,
        provider,
        proxy_mapping,
        *,
        current_offset: float,
        notes_mapping: Dict[Tuple[UUID, int], float],
        priority: int,
    ):
        provider.free_bus_group(proxy_mapping.pop(self.id_))


class CompositeEvent(Event):
    def __init__(self, events, *, delta=0.0):
        Event.__init__(self, delta=delta)
        self.events = events

    def expand(self, offset):
        events = []
        for event in self.events:
            events.extend(event.expand(offset))
            offset += event.delta
        return events


class GroupAllocateEvent(Event):
    def __init__(
        self, id_, *, add_action=AddAction.ADD_TO_HEAD, delta=0.0, target_node=None
    ):
        Event.__init__(self, delta=delta)
        self.id_ = id_
        self.add_action = AddAction.from_expr(add_action)
        self.target_node = target_node

    def perform(
        self,
        provider,
        proxy_mapping,
        *,
        current_offset: float,
        notes_mapping: Dict[Tuple[UUID, int], float],
        priority: int,
    ):
        proxy_mapping[self.id_] = provider.add_group(
            add_action=self.add_action, target_node=proxy_mapping.get(self.target_node)
        )


class NodeFreeEvent(Event):
    def __init__(self, id_, *, delta=0.0):
        Event.__init__(self, delta=delta)
        self.id_ = id_

    def perform(
        self,
        provider,
        proxy_mapping,
        *,
        current_offset: float,
        notes_mapping: Dict[Tuple[UUID, int], float],
        priority: int,
    ):
        provider.free_node(proxy_mapping.pop(self.id_))


class NoteEvent(Event):
    def __init__(
        self,
        id_,
        *,
        add_action=AddAction.ADD_TO_HEAD,
        delta: float = 1.0,
        duration: float = 1.0,
        synthdef: Optional[SynthDef] = None,
        target_node: Optional[UUID] = None,
        **kwargs,
    ):
        Event.__init__(self, delta=delta)
        self.id_ = id_
        self.add_action = AddAction.from_expr(add_action)
        self.duration = duration
        self.synthdef = synthdef
        self.target_node = target_node
        self.kwargs = kwargs

    def expand(self, offset: float):
        starts, stops = [], []
        for i, proxy_mapping in enumerate(expand(self.kwargs)):
            event = type(self)(
                id_=(self.id_, i),
                add_action=self.add_action,
                duration=self.duration,
                synthdef=self.synthdef,
                target_node=self.target_node,
                **proxy_mapping,
            )
            start_offset = offset
            stop_offset = offset + self.calculate_duration()
            starts.append((start_offset, Priority.START, event))
            stops.append((stop_offset, Priority.STOP, event))
        return starts + stops

    def calculate_duration(self):
        return self.duration or 1.0

    def merge(self, event):
        _, _, kwargs = get_vars(event)
        return new(self, **kwargs)

    def perform(
        self,
        provider,
        proxy_mapping,
        *,
        current_offset: float,
        notes_mapping: Dict[Tuple[UUID, int], float],
        priority: int,
        **kwargs,
    ):
        if priority == Priority.START:
            # does a proxy exist?
            #    if yes, update settings
            #    if no, create proxy
            # update notes mapping with expected completion offset
            settings = self.kwargs.copy()
            for key, value in settings.items():
                if isinstance(value, UUID):
                    settings[key] = proxy_mapping[value]
            if self.id_ not in proxy_mapping:
                proxy_mapping[self.id_] = provider.add_synth(
                    add_action=self.add_action,
                    synthdef=self.synthdef,
                    target_node=proxy_mapping.get(self.target_node),
                    **settings,
                )
            else:
                proxy = proxy_mapping[self.id_]
                provider.set_node(proxy, **settings)
            notes_mapping[self.id_] = current_offset + self.calculate_duration()
        elif priority == Priority.STOP:
            # check notes mapping for expected completion offset
            # is expected completion <= current_offset? release
            # otherwise pass
            expected_completion = notes_mapping.get(self.id_)
            if expected_completion is None or expected_completion > current_offset:
                return
            notes_mapping.pop(self.id_)
            provider.free_node(proxy_mapping.pop(self.id_))


class NullEvent(Event):
    def expand(self, offset):
        return []


class SynthAllocateEvent(Event):
    def __init__(
        self,
        id_,
        *,
        add_action=AddAction.ADD_TO_HEAD,
        delta=0.0,
        synthdef=None,
        target_node=None,
        **kwargs,
    ):
        Event.__init__(self, delta=delta)
        self.id_ = id_
        self.add_action = AddAction.from_expr(add_action)
        self.synthdef = synthdef
        self.target_node = target_node
        self.kwargs = kwargs

    def perform(
        self,
        provider,
        proxy_mapping,
        *,
        current_offset: float,
        notes_mapping: Dict[Tuple[UUID, int], float],
        priority: int,
    ):
        settings = self.kwargs.copy()
        for key, value in settings.items():
            if isinstance(value, UUID):
                settings[key] = proxy_mapping[value]
        proxy_mapping[self.id_] = provider.add_synth(
            add_action=self.add_action,
            synthdef=self.synthdef,
            target_node=proxy_mapping.get(self.target_node),
            **settings,
        )
