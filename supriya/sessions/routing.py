from typing import Generic, TypeVar

from ..contexts import AsyncServer, BusGroup
from ..enums import AddAction
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
        component: Component,
        kwargs: dict[str, float | str] | None = None,
        name: str,
        target_bus_name: str,
        target_node_name: str,
    ) -> None:
        self._add_action = add_action
        self._cached_input: BusGroup | C | None = None
        self._component = component
        self._input: BusGroup | C | None = None
        self._kwargs = kwargs or {}
        self._name = name
        self._target_bus_name = target_bus_name
        self._target_node_name = target_node_name

    def _get_target_channel_count(self) -> ChannelCount:
        return self._component.effective_channel_count

    def _notify_disconnected(self, connection: "Component") -> None:
        if connection is self._input:
            self.set(None)

    def _reconcile_connections(self, *, deleting: bool = False) -> list[Component]:
        related: list[Component] = []
        old_input = self._cached_input
        if deleting:
            if isinstance(self._cached_input, Component):
                self._cached_input._connections.pop(
                    (self._component, Names.INPUT), None
                )
                related.append(self._cached_input)
        else:
            new_input: Component | None = None
            if isinstance(self._input, Component):
                new_input = self._cached_input = self._input
            if old_input != new_input:
                if isinstance(old_input, Component):
                    old_input._connections.pop((self._component, Names.INPUT))
                if isinstance(new_input, Component):
                    new_input._connections[(self._component, Names.INPUT)] = IO.READ
            if isinstance(old_input, Component):
                related.append(old_input)
            if isinstance(new_input, Component):
                related.append(new_input)
        return sorted(set(related), key=lambda x: x.graph_order)

    def _resolve_specs(self, context: AsyncServer | None) -> Specs:
        specs = Specs()
        if not (context is not None and self._input):
            return specs
        if isinstance(self._input, BusGroup):
            input_address: int | str = int(self._input)
            input_channel_count = len(self._input)
            input_feedsback = False
        else:
            input_address = Spec.get_address(
                self._input,
                Names.AUDIO_BUSES,
                Names.MAIN,
            )
            input_channel_count = self._input.effective_channel_count
            input_feedsback = bool(
                Spec.feedsback(
                    writer_order=self._input.feedback_graph_order,
                    reader_order=self._component.graph_order,
                )
            )
        input_patch_cable_synthdef = build_patch_cable_synthdef(
            source_channel_count=input_channel_count,
            target_channel_count=self._get_target_channel_count(),
            feedback=input_feedsback,
        )
        specs.synthdef_specs.append(
            SynthDefSpec(
                component=self._component,
                context=context,
                name=input_patch_cable_synthdef.effective_name,
                synthdef=input_patch_cable_synthdef,
            )
        )
        specs.synth_specs.append(
            SynthSpec(
                add_action=self._add_action,
                component=self._component,
                context=context,
                name=self._name,
                kwargs={
                    "in_": input_address,
                    "out": Spec.get_address(
                        self._component, Names.AUDIO_BUSES, self._target_bus_name
                    ),
                    **self._kwargs,
                },
                parent_node=None,
                synthdef=Spec.get_address(
                    None,
                    Names.SYNTHDEFS,
                    input_patch_cable_synthdef.effective_name,
                ),
                target_node=Spec.get_address(
                    self._component, Names.NODES, self._target_node_name
                ),
            )
        )
        return specs

    def set(self, input: BusGroup | C | None) -> None:
        self._input = input
