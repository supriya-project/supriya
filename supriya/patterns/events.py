import enum
from typing import Any, Dict, Optional, Sequence, Tuple, Union
from uuid import UUID

from uqbar.objects import get_repr, get_vars, new

from ..assets.synthdefs.default import default
from ..contexts import BusGroup, Context, ContextObject, Node
from ..enums import AddAction, CalculationRate
from ..synthdefs import SynthDef
from ..typing import AddActionLike, CalculationRateLike
from ..utils import expand


class Priority(enum.IntEnum):
    NONE = 0
    START = 1
    STOP = 2


class Event:
    def __init__(self, *, delta: float = 0.0) -> None:
        self.delta = delta

    def __eq__(self, expr: Any) -> bool:
        self_values = type(self), get_vars(self)
        try:
            expr_values = type(expr), get_vars(expr)
        except AttributeError:
            expr_values = type(expr), expr
        return self_values == expr_values

    def __repr__(self) -> str:
        return get_repr(self, multiline=False)

    def expand(self, offset: float) -> Sequence[Tuple[float, Priority, "Event"]]:
        return [(offset, Priority.START, self)]

    def perform(
        self,
        context: Context,
        proxy_mapping: Dict[Union[UUID, Tuple[UUID, int]], ContextObject],
        *,
        current_offset: float,
        notes_mapping: Dict[Union[UUID, Tuple[UUID, int]], float],
        priority: Priority,
    ) -> None:
        raise NotImplementedError


class StartEvent(Event):
    """
    The first event injected by a pattern player.
    """

    def perform(
        self,
        context: Context,
        proxy_mapping: Dict[Union[UUID, Tuple[UUID, int]], ContextObject],
        *,
        current_offset: float,
        notes_mapping: Dict[Union[UUID, Tuple[UUID, int]], float],
        priority: Priority,
    ) -> None:
        pass


class StopEvent(Event):
    """
    The last event injected by a pattern player.
    """

    def perform(
        self,
        context: Context,
        proxy_mapping: Dict[Union[UUID, Tuple[UUID, int]], ContextObject],
        *,
        current_offset: float,
        notes_mapping: Dict[Union[UUID, Tuple[UUID, int]], float],
        priority: Priority,
    ) -> None:
        pass


class BusAllocateEvent(Event):
    def __init__(
        self,
        id_: Union[UUID, Tuple[UUID, int]],
        *,
        calculation_rate: CalculationRateLike = "audio",
        channel_count: int = 1,
        delta: float = 0.0,
    ) -> None:
        Event.__init__(self, delta=delta)
        self.id_ = id_
        self.calculation_rate = CalculationRate.from_expr(calculation_rate)
        self.channel_count = channel_count

    def perform(
        self,
        context: Context,
        proxy_mapping: Dict[Union[UUID, Tuple[UUID, int]], ContextObject],
        *,
        current_offset: float,
        notes_mapping: Dict[Union[UUID, Tuple[UUID, int]], float],
        priority: Priority,
    ) -> None:
        proxy_mapping[self.id_] = context.add_bus_group(
            calculation_rate=self.calculation_rate, count=self.channel_count
        )


class BusFreeEvent(Event):
    def __init__(
        self, id_: Union[UUID, Tuple[UUID, int]], *, delta: float = 0.0
    ) -> None:
        Event.__init__(self, delta=delta)
        self.id_ = id_

    def perform(
        self,
        context: Context,
        proxy_mapping: Dict[Union[UUID, Tuple[UUID, int]], ContextObject],
        *,
        current_offset: float,
        notes_mapping: Dict[Union[UUID, Tuple[UUID, int]], float],
        priority: Priority,
    ) -> None:
        if not isinstance(bus_group := proxy_mapping.pop(self.id_), BusGroup):
            raise RuntimeError(bus_group)
        context.free_bus_group(bus_group)


class CompositeEvent(Event):
    def __init__(self, events, *, delta: float = 0.0) -> None:
        Event.__init__(self, delta=delta)
        self.events = events

    def expand(self, offset) -> Sequence[Tuple[float, Priority, "Event"]]:
        events = []
        for event in self.events:
            events.extend(event.expand(offset))
            offset += event.delta
        return events


class GroupAllocateEvent(Event):
    def __init__(
        self,
        id_: Union[UUID, Tuple[UUID, int]],
        *,
        add_action: AddActionLike = AddAction.ADD_TO_HEAD,
        delta: float = 0.0,
        target_node: Optional[Union[Node, UUID]] = None,
    ) -> None:
        Event.__init__(self, delta=delta)
        self.id_ = id_
        self.add_action = AddAction.from_expr(add_action)
        self.target_node = target_node

    def perform(
        self,
        context: Context,
        proxy_mapping: Dict[Union[UUID, Tuple[UUID, int]], ContextObject],
        *,
        current_offset: float,
        notes_mapping: Dict[Union[UUID, Tuple[UUID, int]], float],
        priority: Priority,
    ) -> None:
        target_node: Optional[Node] = None
        if isinstance(self.target_node, UUID):
            if not isinstance(
                target_node_ := proxy_mapping.get(self.target_node), Node
            ):
                raise RuntimeError(target_node_)
            target_node = target_node_
        else:
            target_node = self.target_node
        proxy_mapping[self.id_] = context.add_group(
            add_action=self.add_action, target_node=target_node
        )


class NodeFreeEvent(Event):
    def __init__(
        self, id_: Union[UUID, Tuple[UUID, int]], *, delta: float = 0.0
    ) -> None:
        Event.__init__(self, delta=delta)
        self.id_ = id_

    def perform(
        self,
        context: Context,
        proxy_mapping: Dict[Union[UUID, Tuple[UUID, int]], ContextObject],
        *,
        current_offset: float,
        notes_mapping: Dict[Union[UUID, Tuple[UUID, int]], float],
        priority: Priority,
    ) -> None:
        if not isinstance(node := proxy_mapping.pop(self.id_), Node):
            raise RuntimeError(node)
        context.free_node(node)


class NoteEvent(Event):
    def __init__(
        self,
        id_: Union[UUID, Tuple[UUID, int]],
        *,
        add_action: AddActionLike = AddAction.ADD_TO_HEAD,
        delta: float = 1.0,
        duration: float = 1.0,
        synthdef: Optional[SynthDef] = None,
        target_node: Optional[Union[Node, UUID]] = None,
        **kwargs,
    ) -> None:
        Event.__init__(self, delta=delta)
        self.id_ = id_
        self.add_action = AddAction.from_expr(add_action)
        self.duration = duration
        self.synthdef = synthdef
        self.target_node = target_node
        self.kwargs = kwargs

    def expand(self, offset: float) -> Sequence[Tuple[float, Priority, "Event"]]:
        starts, stops = [], []
        for i, proxy_mapping in enumerate(expand(self.kwargs)):
            if not isinstance(self.id_, UUID):
                raise RuntimeError("How did we get here?")
            event: Event = type(self)(
                id_=(self.id_, i),
                add_action=self.add_action,
                duration=self.duration,
                synthdef=self.synthdef,
                target_node=self.target_node,
                **proxy_mapping,
            )
            start_offset = offset
            stop_offset = offset + self.duration
            starts.append((start_offset, Priority.START, event))
            stops.append((stop_offset, Priority.STOP, event))
        return starts + stops

    def merge(self, event) -> "Event":
        _, _, kwargs = get_vars(event)
        return new(self, **kwargs)

    def perform(
        self,
        context: Context,
        proxy_mapping: Dict[Union[UUID, Tuple[UUID, int]], ContextObject],
        *,
        current_offset: float,
        notes_mapping: Dict[Union[UUID, Tuple[UUID, int]], float],
        priority: Priority,
        **kwargs,
    ) -> None:
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
                target_node: Optional[Node] = None
                if isinstance(self.target_node, UUID):
                    if not isinstance(
                        target_node_ := proxy_mapping.get(self.target_node), Node
                    ):
                        raise RuntimeError(target_node_)
                    target_node = target_node_
                else:
                    target_node = self.target_node
                proxy_mapping[self.id_] = context.add_synth(
                    add_action=self.add_action,
                    synthdef=self.synthdef or default,
                    target_node=target_node,
                    **settings,
                )
            else:
                if not isinstance(node := proxy_mapping.get(self.id_), Node):
                    raise RuntimeError(node)
                context.set_node(node, **settings)
            if self.duration:
                notes_mapping[self.id_] = current_offset + self.duration
        elif priority == Priority.STOP:
            # check notes mapping for expected completion offset:
            # if expected completion >= current_offset or non-existent? bail
            # otherwise release
            expected_completion = notes_mapping.get(self.id_)
            if expected_completion is None:
                proxy_mapping.pop(self.id_, None)
            elif expected_completion > current_offset:
                return
            else:
                notes_mapping.pop(self.id_)
                if not isinstance(node := proxy_mapping.pop(self.id_), Node):
                    raise RuntimeError(node)
                context.free_node(node)


class NullEvent(Event):
    def expand(self, offset) -> Sequence[Tuple[float, Priority, "Event"]]:
        return []


class SynthAllocateEvent(Event):
    def __init__(
        self,
        id_: Union[UUID, Tuple[UUID, int]],
        synthdef: SynthDef,
        *,
        add_action: AddActionLike = AddAction.ADD_TO_HEAD,
        delta: float = 0.0,
        target_node: Optional[Union[Node, UUID]] = None,
        **kwargs,
    ) -> None:
        Event.__init__(self, delta=delta)
        self.id_ = id_
        self.add_action = AddAction.from_expr(add_action)
        self.synthdef = synthdef
        self.target_node = target_node
        self.kwargs = kwargs

    def perform(
        self,
        context: Context,
        proxy_mapping: Dict[Union[UUID, Tuple[UUID, int]], ContextObject],
        *,
        current_offset: float,
        notes_mapping: Dict[Union[UUID, Tuple[UUID, int]], float],
        priority: Priority,
    ) -> None:
        target_node: Optional[Node] = None
        if isinstance(self.target_node, UUID):
            if not isinstance(
                target_node_ := proxy_mapping.get(self.target_node), Node
            ):
                raise RuntimeError(target_node_)
            target_node = target_node_
        else:
            target_node = self.target_node
        settings = self.kwargs.copy()
        for key, value in settings.items():
            if isinstance(value, UUID):
                settings[key] = proxy_mapping[value]
        proxy_mapping[self.id_] = context.add_synth(
            add_action=self.add_action,
            synthdef=self.synthdef,
            target_node=target_node,
            **settings,
        )
