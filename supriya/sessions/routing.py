from typing import Callable

from ..contexts import BusGroup
from ..enums import AddAction
from ..typing import Inherit
from ..ugens.system import build_patch_cable_synthdef
from .components import Component
from .constants import IO, Entities, Names
from .specs import Spec, SpecFactory


class Input:
    """
    An input, controlling audio reads from a bus or component to another component.
    """

    def __init__(
        self,
        *,
        add_action: AddAction,
        add_node_address: Callable[[Component], str] | str,
        destroy_strategy: dict[str, float] | None = None,
        host_component: Component,
        kwargs: dict[str, Callable[[Component], str] | float | str] | None = None,
        name: str,
        source: BusGroup | Component | None = None,
        target: Callable[[Component], Component] | Component | None = None,
        target_bus_address: Callable[[Component], str] | str,
    ) -> None:
        self._add_action = add_action
        self._add_node_address = add_node_address
        self._cached_source: BusGroup | Component | None = None
        self._destroy_strategy = destroy_strategy
        self._host_component = host_component
        self._kwargs = kwargs or {}
        self._name = name
        self._source = source
        self._target = target
        self._target_bus_address = target_bus_address

    def _on_connection_deleted(self, connection: "Component") -> None:
        if connection is self._source:
            self.set(None)

    def _reconcile_connections(self, *, deleting: bool = False) -> list[Component]:
        related: list[Component] = []
        if target := (
            self._target(self._host_component)
            if callable(self._target)
            else self._target
        ):
            related.append(target)
        old_source = self._cached_source
        if deleting:
            if target:
                target._connections.pop((self._host_component, Names.OUTPUT), None)
            if isinstance(self._cached_source, Component):
                self._cached_source._connections.pop(
                    (self._host_component, Names.INPUT), None
                )
                related.append(self._cached_source)
        else:
            if target:
                target._connections[(self._host_component, Names.OUTPUT)] = IO.WRITE
            new_source: BusGroup | Component | None
            if isinstance(self._source, (BusGroup, Component)):
                new_source = self._cached_source = self._source
            else:
                new_source = self._cached_source = None
            if old_source != new_source:
                if isinstance(old_source, Component):
                    old_source._connections.pop((self._host_component, Names.INPUT))
                if isinstance(new_source, Component):
                    new_source._connections[(self._host_component, Names.INPUT)] = (
                        IO.READ
                    )
            if isinstance(old_source, Component):
                related.append(old_source)
            if isinstance(new_source, Component):
                related.append(new_source)
        return sorted(set(related), key=lambda x: x.graph_order)

    def _resolve_specs(
        self, spec_factory: SpecFactory, target_channel_count: int | None = None
    ) -> SpecFactory:
        if not self._cached_source:
            return spec_factory
        if isinstance(self._cached_source, BusGroup):
            feedsback = False
            source_bus_address: int | str = int(self._cached_source)
            source_channel_count = len(self._cached_source)
        elif isinstance(self._cached_source, Component):
            feedsback = bool(
                Spec.feedsback(
                    writer_order=self._cached_source.feedback_graph_order,
                    reader_order=self._host_component.graph_order,
                )
            )
            source_bus_address = Spec.get_address(
                self._cached_source,
                Entities.AUDIO_BUSES,
                Names.MAIN,
            )
            source_channel_count = self._cached_source.effective_channel_count
        if target_channel_count is None:
            target = (
                self._target(self._host_component)
                if callable(self._target)
                else self._target or self._host_component
            )
            target_channel_count = target.effective_channel_count
        patch_cable_synthdef_address = spec_factory.add_synthdef(
            synthdef=build_patch_cable_synthdef(
                source_channel_count=source_channel_count,
                target_channel_count=target_channel_count,
                feedback=feedsback,
            )
        )
        spec_factory.add_synth(
            add_action=self._add_action,
            destroy_strategy=self._destroy_strategy,
            kwargs=dict(
                in_=source_bus_address,
                out=(
                    self._target_bus_address(self._host_component)
                    if callable(self._target_bus_address)
                    else self._target_bus_address
                ),
                **{
                    key: value(self._host_component) if callable(value) else value
                    for key, value in self._kwargs.items()
                },
            ),
            name=self._name,
            synthdef=patch_cable_synthdef_address,
            target_node=(
                self._add_node_address(self._host_component)
                if callable(self._add_node_address)
                else self._add_node_address
            ),
        )
        return spec_factory

    def set(self, source: BusGroup | Component | None) -> None:
        self._source = source


class Output:
    """
    An output, controlling audio writes from a source component to another component or bus.
    """

    def __init__(
        self,
        *,
        add_action: AddAction,
        add_node_address: Callable[[Component], str] | str,
        destroy_strategy: dict[str, float] | None = None,
        host_component: Component,
        kwargs: dict[str, Callable[[Component], str] | float | str] | None = None,
        name: str,
        source: Callable[[Component], Component] | Component | None = None,
        source_bus_address: Callable[[Component], str] | str,
        target: BusGroup | Component | Inherit | None = None,
    ) -> None:
        self._add_action = add_action
        self._add_node_address = add_node_address
        self._cached_target: BusGroup | Component | None = None
        self._destroy_strategy = destroy_strategy
        self._host_component = host_component
        self._kwargs = kwargs or {}
        self._name = name
        self._source = source
        self._source_bus_address = source_bus_address
        self._target: BusGroup | Component | Inherit | None = target

    def _on_connection_deleted(self, connection: "Component") -> None:
        if connection is self._target:
            self.set(None)

    def _reconcile_connections(self, *, deleting: bool = False) -> list[Component]:
        related: list[Component] = []
        if source := (
            self._source(self._host_component)
            if callable(self._source)
            else self._source
        ):
            related.append(source)
        old_target = self._cached_target
        if deleting:
            if source:
                source._connections.pop((self._host_component, Names.INPUT), None)
            if isinstance(self._cached_target, Component):
                self._cached_target._connections.pop(
                    (self._host_component, Names.OUTPUT), None
                )
                related.append(self._cached_target)
        else:
            if source:
                source._connections[(self._host_component, Names.INPUT)] = IO.READ
            new_target: BusGroup | Component | None
            if isinstance(self._target, (BusGroup, Component)):
                new_target = self._cached_target = self._target
            elif isinstance(self._target, Inherit):
                new_target = self._cached_target = self._resolve_default()
            else:
                new_target = self._cached_target = self._target
            if old_target != new_target:
                if isinstance(old_target, Component):
                    old_target._connections.pop((self._host_component, Names.OUTPUT))
                if isinstance(new_target, Component):
                    new_target._connections[(self._host_component, Names.OUTPUT)] = (
                        IO.WRITE
                    )
            if isinstance(old_target, Component):
                related.append(old_target)
            if isinstance(new_target, Component):
                related.append(new_target)
        return sorted(set(related), key=lambda x: x.graph_order)

    def _resolve_default(self) -> Component:
        assert isinstance(parent := self._host_component.parent, Component)
        return parent

    def _resolve_specs(self, spec_factory: SpecFactory) -> SpecFactory:
        if not self._cached_target:
            return spec_factory
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
                Entities.AUDIO_BUSES,
                Names.FEEDBACK if feedsback else Names.MAIN,
            )
            target_channel_count = self._cached_target.effective_channel_count
        source = (
            self._source(self._host_component)
            if callable(self._source)
            else self._source or self._host_component
        )
        source_channel_count = source.effective_channel_count
        patch_cable_synthdef_address = spec_factory.add_synthdef(
            synthdef=build_patch_cable_synthdef(
                source_channel_count=source_channel_count,
                target_channel_count=target_channel_count,
            )
        )
        spec_factory.add_synth(
            add_action=self._add_action,
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
            synthdef=patch_cable_synthdef_address,
            target_node=(
                self._add_node_address(self._host_component)
                if callable(self._add_node_address)
                else self._add_node_address
            ),
        )
        return spec_factory

    def set(self, target: BusGroup | Component | Inherit | None) -> None:
        self._target = target
