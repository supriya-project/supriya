from typing import Callable, Generic, TypeVar

from ..contexts import AsyncServer, BusGroup
from ..enums import AddAction
from ..typing import Default
from ..ugens.system import build_patch_cable_synthdef
from .components import Component
from .constants import IO, ChannelCount, Names
from .specs import Spec, Specs, SynthDefSpec, SynthSpec

C = TypeVar("C", bound=Component)


class Input(Generic[C]):
    def __init__(
        self,
        *,
        add_action: AddAction,
        add_node_address: Callable[[Component], str] | str,
        destroy_strategy: dict[str, float] | None = None,
        host_component: Component,
        kwargs: dict[str, Callable[[Component], str] | float | str] | None = None,
        name: str,
        target_bus_name: str,
    ) -> None:
        self._add_action = add_action
        self._add_node_address = add_node_address
        self._cached_input: BusGroup | C | None = None
        self._destroy_strategy = destroy_strategy
        self._host_component = host_component
        self._input: BusGroup | C | None = None
        self._kwargs = kwargs or {}
        self._name = name
        self._target_bus_name = target_bus_name

    def _get_target_channel_count(self) -> ChannelCount:
        return self._host_component.effective_channel_count

    def _notify_disconnected(self, connection: "Component") -> None:
        if connection is self._input:
            self.set(None)

    def _reconcile_connections(self, *, deleting: bool = False) -> list[Component]:
        related: list[Component] = []
        old_input = self._cached_input
        if deleting:
            if isinstance(self._cached_input, Component):
                self._cached_input._connections.pop(
                    (self._host_component, Names.INPUT), None
                )
                related.append(self._cached_input)
        else:
            new_input: BusGroup | Component | None
            if isinstance(self._input, (BusGroup, Component)):
                new_input = self._cached_input = self._input
            else:
                new_input = self._cached_input = None
            if old_input != new_input:
                if isinstance(old_input, Component):
                    old_input._connections.pop((self._host_component, Names.INPUT))
                if isinstance(new_input, Component):
                    new_input._connections[(self._host_component, Names.INPUT)] = (
                        IO.READ
                    )
            if isinstance(old_input, Component):
                related.append(old_input)
            if isinstance(new_input, Component):
                related.append(new_input)
        return sorted(set(related), key=lambda x: x.graph_order)

    def _resolve_specs(self, context: AsyncServer | None) -> Specs:
        specs = Specs()
        if not (context is not None and self._cached_input):
            return specs
        if isinstance(self._cached_input, BusGroup):
            feedsback = False
            source_bus_address: int | str = int(self._cached_input)
            source_channel_count = len(self._cached_input)
        elif isinstance(self._cached_input, Component):
            feedsback = bool(
                Spec.feedsback(
                    writer_order=self._cached_input.feedback_graph_order,
                    reader_order=self._host_component.graph_order,
                )
            )
            source_bus_address = Spec.get_address(
                self._cached_input,
                Names.AUDIO_BUSES,
                Names.MAIN,
            )
            source_channel_count = self._cached_input.effective_channel_count
        specs.synthdef_specs.append(
            SynthDefSpec(
                component=self._host_component,
                context=context,
                name=(
                    patch_cable_synthdef := build_patch_cable_synthdef(
                        source_channel_count=source_channel_count,
                        target_channel_count=self._get_target_channel_count(),
                        feedback=feedsback,
                    )
                ).effective_name,
                synthdef=patch_cable_synthdef,
            )
        )
        specs.synth_specs.append(
            SynthSpec(
                add_action=self._add_action,
                component=self._host_component,
                context=context,
                destroy_strategy=self._destroy_strategy,
                kwargs={
                    "in_": source_bus_address,
                    "out": Spec.get_address(
                        self._host_component, Names.AUDIO_BUSES, self._target_bus_name
                    ),
                    **{
                        key: value(self._host_component) if callable(value) else value
                        for key, value in self._kwargs.items()
                    },
                },
                name=self._name,
                parent_node=None,
                synthdef=Spec.get_address(
                    None,
                    Names.SYNTHDEFS,
                    patch_cable_synthdef.effective_name,
                ),
                target_node=(
                    self._add_node_address(self._host_component)
                    if callable(self._add_node_address)
                    else self._add_node_address
                ),
            )
        )
        return specs

    def set(self, input: BusGroup | C | None) -> None:
        self._input = input


class Output:
    def __init__(
        self,
        *,
        add_action: AddAction,
        add_node_address: Callable[[Component], str] | str,
        destroy_strategy: dict[str, float] | None = None,
        host_component: Component,
        kwargs: dict[str, Callable[[Component], str] | float | str] | None = None,
        name: str,
        source_bus_address: Callable[[Component], str] | str,
        target: BusGroup | Component | Default | None = None,
    ) -> None:
        self._add_action = add_action
        self._add_node_address = add_node_address
        self._cached_target: BusGroup | Component | None = None
        self._destroy_strategy = destroy_strategy
        self._host_component = host_component
        self._kwargs = kwargs or {}
        self._name = name
        self._source_bus_address = source_bus_address
        self._target: BusGroup | Component | Default | None = target

    def _get_source_channel_count(self) -> ChannelCount:
        return self._host_component.effective_channel_count

    def _notify_disconnected(self, connection: "Component") -> None:
        if connection is self._target:
            self.set(None)

    def _reconcile_connections(self, *, deleting: bool = False) -> list[Component]:
        related: list[Component] = []
        old_output = self._cached_target
        if deleting:
            if isinstance(self._cached_target, Component):
                self._cached_target._connections.pop(
                    (self._host_component, Names.OUTPUT), None
                )
                related.append(self._cached_target)
        else:
            new_output: BusGroup | Component | None
            if isinstance(self._target, (BusGroup, Component)):
                new_output = self._cached_target = self._target
            elif isinstance(self._target, Default):
                new_output = self._cached_target = self._resolve_default()
            else:
                new_output = self._cached_target = self._target
            if old_output != new_output:
                if isinstance(old_output, Component):
                    old_output._connections.pop((self._host_component, Names.OUTPUT))
                if isinstance(new_output, Component):
                    new_output._connections[(self._host_component, Names.OUTPUT)] = (
                        IO.WRITE
                    )
            if isinstance(old_output, Component):
                related.append(old_output)
            if isinstance(new_output, Component):
                related.append(new_output)
        return sorted(set(related), key=lambda x: x.graph_order)

    def _resolve_default(self) -> Component:
        assert isinstance(parent := self._host_component.parent, Component)
        return parent

    def _resolve_specs(self, context: AsyncServer | None) -> Specs:
        specs = Specs()
        if not (context is not None and self._cached_target):
            return specs
        if isinstance(self._cached_target, BusGroup):
            feedsback = False
            target_bus_address: int | str = int(self._cached_target)
            target_channel_count = len(self._cached_target)
        elif isinstance(self._cached_target, Component):
            feedsback = bool(
                Spec.feedsback(
                    writer_order=self._host_component.feedback_graph_order,
                    reader_order=self._cached_target.graph_order,
                )
            )
            target_bus_address = Spec.get_address(
                self._cached_target,
                Names.AUDIO_BUSES,
                Names.FEEDBACK if feedsback else Names.MAIN,
            )
            target_channel_count = self._cached_target.effective_channel_count
        specs.synthdef_specs.append(
            SynthDefSpec(
                component=self._host_component,
                context=context,
                name=(
                    patch_cable_synthdef := build_patch_cable_synthdef(
                        self._host_component.effective_channel_count,
                        target_channel_count,
                    )
                ).effective_name,
                synthdef=patch_cable_synthdef,
            )
        )
        specs.synth_specs.append(
            SynthSpec(
                add_action=self._add_action,
                component=self._host_component,
                context=context,
                destroy_strategy=self._destroy_strategy,
                kwargs=dict(
                    in_=(
                        self._source_bus_address(self._host_component)
                        if callable(self._source_bus_address)
                        else self._source_bus_address
                    ),
                    out=target_bus_address,
                    **{
                        key: value(self._host_component) if callable(value) else value
                        for key, value in self._kwargs.items()
                    },
                ),
                name=self._name,
                parent_node=None,
                synthdef=Spec.get_address(
                    None,
                    Names.SYNTHDEFS,
                    patch_cable_synthdef.effective_name,
                ),
                target_node=(
                    self._add_node_address(self._host_component)
                    if callable(self._add_node_address)
                    else self._add_node_address
                ),
            )
        )
        return specs

    def set(self, target: BusGroup | Component | Default | None) -> None:
        self._target = target
