import enum
import warnings
from typing import Any, Sequence, SupportsFloat
from uuid import UUID

from uqbar.objects import get_repr, get_vars, new

from ..contexts import BusGroup, Context, ContextObject, Node
from ..enums import AddAction, CalculationRate
from ..typing import AddActionLike, CalculationRateLike
from ..ugens import SynthDef, default
from ..utils import expand


def _process_synth_settings(
    proxy_mapping: dict[UUID | tuple[UUID, int], ContextObject],
    **kwargs: SupportsFloat | UUID | str | Sequence[SupportsFloat | UUID | str],
) -> dict[str, float | str | Sequence[float | str]]:
    """
    Resolve UUIDs into context object ids
    """
    settings: dict[str, float | str | Sequence[float | str]] = {}
    for key, value in kwargs.items():
        if not isinstance(value, Sequence) or isinstance(value, str):
            value = [value]
        processed_values: list[float | str] = []
        for v in value:
            if isinstance(v, UUID):
                processed_values.append(float(proxy_mapping[v]))
            else:
                processed_values.append(float(v) if not isinstance(v, str) else v)
        settings[key] = (
            processed_values[0] if len(processed_values) == 1 else processed_values
        )
    return settings


class PatternWarning(Warning):
    pass


warnings.simplefilter("always", PatternWarning)


def _partition_synth_settings(
    **kwargs: float | str | Sequence[float | str],
) -> tuple[dict[str, float | Sequence[float]], dict[str, str]]:
    """
    Split synth settings into two maps suitable for set_node and map_node
    """
    set_kwargs: dict[str, float | Sequence[float]] = {}
    map_kwargs: dict[str, str] = {}
    for key, value in kwargs.items():
        if isinstance(value, float):
            set_kwargs[key] = value
        elif isinstance(value, str):
            map_kwargs[key] = value
        elif isinstance(value, Sequence):
            if all(isinstance(v, float) for v in value):
                set_kwargs[key] = [float(v) for v in value]
            else:
                warnings.warn(f"Cannot process {value}")
        # Unclear to me if we can map with a sequence of strings.
    return set_kwargs, map_kwargs


class Priority(enum.IntEnum):
    NONE = 0
    START = 1
    STOP = 2


class Event:
    def __init__(self, *, delta: float = 0.0, **kwargs) -> None:
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

    def expand(self, offset: float) -> Sequence[tuple[float, Priority, "Event"]]:
        return [(offset, Priority.START, self)]

    def merge(self, event: "Event") -> "Event":
        _, _, kwargs = get_vars(event)
        return new(self, **kwargs)

    def perform(
        self,
        context: Context,
        proxy_mapping: dict[UUID | tuple[UUID, int], ContextObject],
        *,
        current_offset: float,
        notes_mapping: dict[UUID | tuple[UUID, int], float],
        priority: Priority,
        **kwargs,
    ) -> None:
        pass


class StartEvent(Event):
    """
    The first event injected by a pattern player.
    """


class StopEvent(Event):
    """
    The last event injected by a pattern player.
    """


class BusAllocateEvent(Event):
    def __init__(
        self,
        id_: UUID | tuple[UUID, int],
        *,
        calculation_rate: CalculationRateLike = "audio",
        channel_count: int = 1,
        delta: float = 0.0,
        **kwargs,
    ) -> None:
        Event.__init__(self, delta=delta, **kwargs)
        self.id_ = id_
        self.calculation_rate = CalculationRate.from_expr(calculation_rate)
        self.channel_count = channel_count

    def perform(
        self,
        context: Context,
        proxy_mapping: dict[UUID | tuple[UUID, int], ContextObject],
        *,
        current_offset: float,
        notes_mapping: dict[UUID | tuple[UUID, int], float],
        priority: Priority,
        **kwargs,
    ) -> None:
        proxy_mapping[self.id_] = context.add_bus_group(
            calculation_rate=self.calculation_rate, count=self.channel_count
        )


class BusFreeEvent(Event):
    def __init__(
        self, id_: UUID | tuple[UUID, int], *, delta: float = 0.0, **kwargs
    ) -> None:
        Event.__init__(self, delta=delta, **kwargs)
        self.id_ = id_

    def perform(
        self,
        context: Context,
        proxy_mapping: dict[UUID | tuple[UUID, int], ContextObject],
        *,
        current_offset: float,
        notes_mapping: dict[UUID | tuple[UUID, int], float],
        priority: Priority,
        **kwargs,
    ) -> None:
        if not isinstance(bus_group := proxy_mapping.pop(self.id_), BusGroup):
            raise RuntimeError(bus_group)
        context.free_bus_group(bus_group)


class CompositeEvent(Event):
    def __init__(self, events: list[Event], *, delta: float = 0.0, **kwargs) -> None:
        Event.__init__(self, delta=delta)
        self.events = (
            events if not kwargs else [new(event, **kwargs) for event in events]
        )

    def expand(self, offset: float) -> Sequence[tuple[float, Priority, Event]]:
        events: list[tuple[float, Priority, Event]] = []
        for event in self.events:
            events.extend(event.expand(offset))
            offset += event.delta
        return events


class NodeEvent(Event):
    def __init__(
        self,
        id_: UUID | tuple[UUID, int],
        *,
        add_action: AddActionLike = AddAction.ADD_TO_HEAD,
        delta: float = 0.0,
        target_node: Node | UUID | None = None,
        **kwargs,
    ) -> None:
        Event.__init__(self, delta=delta, **kwargs)
        self.id_ = id_
        self.add_action = AddAction.from_expr(add_action)
        self.target_node = target_node

    def _resolve_target_node(
        self,
        proxy_mapping: dict[UUID | tuple[UUID, int], ContextObject],
    ) -> Node | None:
        if isinstance(self.target_node, UUID):
            if not isinstance(
                target_node_ := proxy_mapping.get(self.target_node), Node
            ):
                raise RuntimeError(target_node_)
            return target_node_
        return self.target_node


class GroupAllocateEvent(NodeEvent):
    def perform(
        self,
        context: Context,
        proxy_mapping: dict[UUID | tuple[UUID, int], ContextObject],
        *,
        current_offset: float,
        notes_mapping: dict[UUID | tuple[UUID, int], float],
        priority: Priority,
        **kwargs,
    ) -> None:
        proxy_mapping[self.id_] = context.add_group(
            add_action=self.add_action,
            target_node=self._resolve_target_node(
                proxy_mapping,
            ),
        )


class NodeFreeEvent(Event):
    def __init__(
        self, id_: UUID | tuple[UUID, int], *, delta: float = 0.0, **kwargs
    ) -> None:
        Event.__init__(self, delta=delta, **kwargs)
        self.id_ = id_

    def perform(
        self,
        context: Context,
        proxy_mapping: dict[UUID | tuple[UUID, int], ContextObject],
        *,
        current_offset: float,
        notes_mapping: dict[UUID | tuple[UUID, int], float],
        priority: Priority,
        **kwargs,
    ) -> None:
        if not isinstance(node := proxy_mapping.pop(self.id_), Node):
            raise RuntimeError(node)
        context.free_node(node)


class NoteEvent(NodeEvent):
    def __init__(
        self,
        id_: UUID | tuple[UUID, int],
        *,
        add_action: AddActionLike = AddAction.ADD_TO_HEAD,
        delta: float = 1.0,
        duration: float = 1.0,
        rest: bool = False,
        synthdef: SynthDef | None = None,
        target_node: Node | UUID | None = None,
        **kwargs: SupportsFloat | UUID | Sequence[SupportsFloat | UUID],
    ) -> None:
        NodeEvent.__init__(
            self,
            add_action=add_action,
            delta=delta,
            id_=id_,
            target_node=target_node,
            **kwargs,
        )
        self.duration = duration
        self.kwargs = kwargs
        self.rest = rest
        self.synthdef = synthdef

    def expand(self, offset: float) -> Sequence[tuple[float, Priority, Event]]:
        starts, stops = [], []
        for i, proxy_mapping in enumerate(expand(self.kwargs)):
            if not isinstance(self.id_, UUID):
                raise RuntimeError("How did we get here?")
            event: Event = type(self)(
                id_=(self.id_, i),
                add_action=self.add_action,
                delta=self.delta,
                duration=self.duration,
                rest=self.rest,
                synthdef=self.synthdef,
                target_node=self.target_node,
                **proxy_mapping,
            )
            start_offset = offset
            stop_offset = offset + self.duration
            starts.append((start_offset, Priority.START, event))
            stops.append((stop_offset, Priority.STOP, event))
        return starts + stops

    def merge(self, event: Event) -> Event:
        _, _, kwargs = get_vars(event)
        return new(self, **kwargs)

    def perform(
        self,
        context: Context,
        proxy_mapping: dict[UUID | tuple[UUID, int], ContextObject],
        *,
        current_offset: float,
        notes_mapping: dict[UUID | tuple[UUID, int], float],
        priority: Priority,
        **kwargs: SupportsFloat | UUID | str | Sequence[SupportsFloat | UUID | str],
    ) -> None:
        if priority == Priority.START and not self.rest:
            # does a proxy exist?
            #    if yes, update settings
            #    if no, create proxy
            # update notes mapping with expected completion offset
            settings = _process_synth_settings(proxy_mapping, **self.kwargs)
            # add the synth
            if self.id_ not in proxy_mapping:
                proxy_mapping[self.id_] = context.add_synth(
                    add_action=self.add_action,
                    permanent=False,
                    synthdef=self.synthdef or default,
                    target_node=self._resolve_target_node(
                        proxy_mapping,
                    ),
                    **settings,
                )
            else:
                if not isinstance(node := proxy_mapping.get(self.id_), Node):
                    raise RuntimeError(node)
                set_kwargs, map_kwargs = _partition_synth_settings(**settings)
                if set_kwargs:
                    context.set_node(node, **set_kwargs)
                if map_kwargs:
                    context.map_node(node, **map_kwargs)
            if self.duration:
                notes_mapping[self.id_] = current_offset + self.duration
        elif priority == Priority.STOP or self.rest:
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
    def expand(self, offset: float) -> Sequence[tuple[float, Priority, Event]]:
        return []


class SynthAllocateEvent(NodeEvent):
    def __init__(
        self,
        id_: UUID | tuple[UUID, int],
        synthdef: SynthDef,
        *,
        add_action: AddActionLike = AddAction.ADD_TO_HEAD,
        delta: float = 0.0,
        target_node: Node | UUID | None = None,
        **kwargs: SupportsFloat | UUID | str | Sequence[SupportsFloat | UUID | str],
    ) -> None:
        NodeEvent.__init__(
            self,
            add_action=add_action,
            delta=delta,
            id_=id_,
            target_node=target_node,
        )
        self.synthdef = synthdef
        self.kwargs = kwargs

    def perform(
        self,
        context: Context,
        proxy_mapping: dict[UUID | tuple[UUID, int], ContextObject],
        *,
        current_offset: float,
        notes_mapping: dict[UUID | tuple[UUID, int], float],
        priority: Priority,
        **kwargs,
    ) -> None:
        settings = _process_synth_settings(proxy_mapping, **self.kwargs)
        # add the synth
        proxy_mapping[self.id_] = context.add_synth(
            add_action=self.add_action,
            permanent=False,
            synthdef=self.synthdef,
            target_node=self._resolve_target_node(
                proxy_mapping,
            ),
            **settings,
        )
