import contextlib
import dataclasses
import itertools
from collections import ChainMap, deque
from typing import TYPE_CHECKING, Optional

from ..contexts import AsyncServer, Buffer, BusGroup, Node
from ..enums import AddAction, CalculationRate, DoneAction
from ..ugens import SynthDef
from .constants import IO, Address, Names, Reconciliation

if TYPE_CHECKING:
    from .components import Component


@dataclasses.dataclass
class Artifacts:
    audio_buses: dict[Address, BusGroup] = dataclasses.field(default_factory=dict)
    buffers: dict[Address, Buffer] = dataclasses.field(default_factory=dict)
    control_buses: dict[Address, BusGroup] = dataclasses.field(default_factory=dict)
    nodes: dict[Address, Node] = dataclasses.field(default_factory=dict)
    synthdefs: dict[Address, SynthDef] = dataclasses.field(default_factory=dict)

    def clear(self) -> None:
        self.audio_buses.clear()
        self.buffers.clear()
        self.control_buses.clear()
        self.nodes.clear()
        self.synthdefs.clear()

    def merge(self, other: "Artifacts") -> None:
        self.audio_buses.update(other.audio_buses)
        self.buffers.update(other.buffers)
        self.control_buses.update(other.control_buses)
        self.nodes.update(other.nodes)
        self.synthdefs.update(other.synthdefs)


@dataclasses.dataclass
class Spec:
    component: "Component"
    context: AsyncServer
    name: str

    def create(
        self,
        *,
        new_artifacts: Artifacts,
        old_artifacts: Artifacts,
    ) -> None:
        raise NotImplementedError

    def destroy(
        self,
        *,
        old_artifacts: Artifacts,
        reconciliation: Reconciliation,
    ) -> None:
        raise NotImplementedError

    @classmethod
    def feedsback(
        cls,
        writer_order: tuple[int, ...] | None,
        reader_order: tuple[int, ...] | None,
    ) -> bool | None:
        if writer_order is None or reader_order is None:
            return None
        length = min(len(reader_order), len(writer_order))
        # If writer_order is shallower than reader_order, writer_order might
        # contain reader_order
        if len(writer_order) < len(reader_order):
            feedsback = reader_order[:length] <= writer_order
        # If reader_order is shallower than writer_order, reader_order might
        # contain writer_order
        elif len(reader_order) < len(writer_order):
            feedsback = reader_order < writer_order[:length]
        # If orders are same depth, check difference strictly
        else:
            feedsback = reader_order <= writer_order
        return feedsback

    @classmethod
    def needs_feedback(cls, component: "Component") -> bool:
        graph_order = component.graph_order
        for (connection, _), io in component._connections.items():
            if io is IO.WRITE and Spec.feedsback(
                writer_order=connection.feedback_graph_order,
                reader_order=graph_order,
            ):
                return True
        return False

    @staticmethod
    def get_address(
        component: Optional["Component"], type_: Names, name: str
    ) -> Address:
        if type_ == Names.SYNTHDEFS:
            return f"{Names.SYNTHDEFS}:{name}"
        elif component is None:
            raise ValueError
        return f"{component.numeric_address}:{type_}:{name}"

    def mutate(
        self,
        *,
        new_artifacts: Artifacts,
        old_artifacts: Artifacts,
        old_spec: "Spec",
    ) -> None:
        raise NotImplementedError

    def requires(self) -> list[Address]:
        return []

    def requires_recreation(self, old_spec: "Spec") -> bool:
        raise NotImplementedError

    def resolve_bus(
        self,
        *,
        address: Address,
        new_artifacts: Artifacts,
        old_artifacts: Artifacts,
    ) -> BusGroup:
        return ChainMap(
            new_artifacts.audio_buses,
            new_artifacts.control_buses,
            old_artifacts.audio_buses,
            old_artifacts.control_buses,
        )[address]

    def resolve_kwargs(
        self,
        *,
        kwargs: dict[str, Address | BusGroup | float],
        new_artifacts: Artifacts,
        old_artifacts: Artifacts,
    ) -> tuple[dict[str, float], dict[str, str]]:
        map_kwargs: dict[str, str] = {}
        set_kwargs: dict[str, float] = {}
        for key, value in kwargs.items():
            if isinstance(value, float):
                set_kwargs[key] = value
            else:
                if isinstance(value, BusGroup):
                    bus = value
                elif isinstance(value, Address):
                    bus = self.resolve_bus(
                        address=value,
                        new_artifacts=new_artifacts,
                        old_artifacts=old_artifacts,
                    )
                if key in ("bus", "in_", "out"):
                    set_kwargs[key] = int(bus)
                else:
                    map_kwargs[key] = bus.map_symbol()
        return set_kwargs, map_kwargs

    def resolve_node(
        self,
        *,
        address: Address | None,
        new_artifacts: Artifacts,
        old_artifacts: Artifacts,
    ) -> Node:
        target_node: Node | None = None
        if address and not (
            target_node := ChainMap(new_artifacts.nodes, old_artifacts.nodes).get(
                address
            )
        ):
            raise ValueError
        return target_node or self.context.default_group

    def resolve_synthdef(
        self,
        *,
        address: Address,
        old_artifacts: Artifacts,
        new_artifacts: Artifacts,
    ) -> SynthDef:
        return ChainMap(
            new_artifacts.synthdefs,
            old_artifacts.synthdefs,
        )[address]

    @property
    def address(self) -> Address:
        raise NotImplementedError


@dataclasses.dataclass
class BufferSpec(Spec):
    channel_count: int
    count: int

    def create(
        self,
        old_artifacts: Artifacts,
        new_artifacts: Artifacts,
    ) -> None:
        raise NotImplementedError

    def destroy(
        self,
        old_artifacts: Artifacts,
        reconciliation: Reconciliation,
    ) -> None:
        if (buffers := self.component._artifacts.buffers)[
            self.name
        ].context is self.context:
            buffers.pop(self.name)
        old_artifacts.buffers.pop(self.address).free()

    def mutate(
        self,
        old_artifacts: Artifacts,
        new_artifacts: Artifacts,
        old_spec: "Spec",
    ) -> None:
        raise NotImplementedError

    def requires_recreation(self, old_spec: "Spec") -> bool:
        return self != old_spec

    @property
    def address(self) -> Address:
        return Spec.get_address(self.component, Names.BUFFERS, self.name)


@dataclasses.dataclass
class BusSpec(Spec):
    calculation_rate: CalculationRate
    channel_count: int
    default: float = 0.0

    def create(
        self,
        old_artifacts: Artifacts,
        new_artifacts: Artifacts,
    ) -> None:
        if self.calculation_rate == CalculationRate.AUDIO:
            bus_group = self.context.add_bus_group(
                calculation_rate=self.calculation_rate,
                count=self.channel_count,
            )
            new_artifacts.audio_buses[self.address] = bus_group
            self.component._artifacts.audio_buses[self.name] = bus_group
        elif self.calculation_rate == CalculationRate.CONTROL:
            bus_group = self.context.add_bus_group(
                calculation_rate=self.calculation_rate,
                count=self.channel_count,
            )
            bus_group.set(self.default)
            new_artifacts.control_buses[self.address] = bus_group
            self.component._artifacts.control_buses[self.name] = bus_group
        else:
            raise ValueError

    def destroy(
        self,
        old_artifacts: Artifacts,
        reconciliation: Reconciliation,
    ) -> None:
        if self.calculation_rate == CalculationRate.AUDIO:
            if (audio_buses := self.component._artifacts.audio_buses)[
                self.name
            ].context is self.context:
                audio_buses.pop(self.name)
            old_artifacts.audio_buses.pop(self.address).free()
        elif self.calculation_rate == CalculationRate.CONTROL:
            if (control_buses := self.component._artifacts.control_buses)[
                self.name
            ].context is self.context:
                control_buses.pop(self.name)
            old_artifacts.control_buses.pop(self.address).free()

    def mutate(
        self,
        old_artifacts: Artifacts,
        new_artifacts: Artifacts,
        old_spec: "Spec",
    ) -> None:
        raise NotImplementedError

    def requires_recreation(self, old_spec: "Spec") -> bool:
        if not isinstance(old_spec, BusSpec):
            raise ValueError(old_spec)
        return self != old_spec

    @property
    def address(self) -> Address:
        if self.calculation_rate == CalculationRate.AUDIO:
            return Spec.get_address(self.component, Names.AUDIO_BUSSES, self.name)
        elif self.calculation_rate == CalculationRate.CONTROL:
            return Spec.get_address(self.component, Names.CONTROL_BUSSES, self.name)
        raise ValueError


@dataclasses.dataclass
class SynthDefSpec(Spec):
    synthdef: SynthDef

    def create(
        self,
        old_artifacts: Artifacts,
        new_artifacts: Artifacts,
    ) -> None:
        if self.address in old_artifacts.synthdefs:
            return
        self.context.add_synthdefs(self.synthdef)
        new_artifacts.synthdefs[self.address] = self.synthdef

    def destroy(
        self,
        old_artifacts: Artifacts,
        reconciliation: Reconciliation,
    ) -> None:
        return

    def mutate(
        self,
        old_artifacts: Artifacts,
        new_artifacts: Artifacts,
        old_spec: "Spec",
    ) -> None:
        raise NotImplementedError

    def requires_recreation(self, old_spec: "Spec") -> bool:
        return self != old_spec

    @property
    def address(self) -> Address:
        return Spec.get_address(None, Names.SYNTHDEFS, self.synthdef.effective_name)


@dataclasses.dataclass
class NodeSpec(Spec):
    add_action: AddAction
    target_node: Address | None

    def requires(self) -> list[Address]:
        if self.target_node is not None:
            return [self.target_node]
        return []

    @property
    def address(self) -> Address:
        return Spec.get_address(self.component, Names.NODES, self.name)


@dataclasses.dataclass
class GroupSpec(NodeSpec):
    destroy_strategy: dict[str, float] | None = None

    def create(
        self,
        old_artifacts: Artifacts,
        new_artifacts: Artifacts,
    ) -> None:
        group = self.context.add_group(
            add_action=self.add_action,
            target_node=self.resolve_node(
                address=self.target_node,
                new_artifacts=new_artifacts,
                old_artifacts=old_artifacts,
            ),
        )
        new_artifacts.nodes[self.address] = group
        self.component._artifacts.nodes[self.name] = group

    def destroy(
        self,
        old_artifacts: Artifacts,
        reconciliation: Reconciliation,
    ) -> None:
        if (nodes := self.component._artifacts.nodes)[
            self.name
        ].context is self.context:
            nodes.pop(self.name)
        node = old_artifacts.nodes.pop(self.address)
        if reconciliation is Reconciliation.DESTROY_ROOT and self.destroy_strategy:
            node.set(**self.destroy_strategy)

    def mutate(
        self,
        old_artifacts: Artifacts,
        new_artifacts: Artifacts,
        old_spec: "Spec",
    ) -> None:
        if not isinstance(old_spec, GroupSpec):
            raise ValueError(old_spec)
        if (
            self.add_action != old_spec.add_action
            or self.target_node != old_spec.target_node
        ):
            old_artifacts.nodes[self.address].move(
                add_action=self.add_action,
                target_node=self.resolve_node(
                    address=self.target_node,
                    new_artifacts=new_artifacts,
                    old_artifacts=old_artifacts,
                ),
            )

    def requires_recreation(self, old_spec: "Spec") -> bool:
        return False


@dataclasses.dataclass
class SynthSpec(NodeSpec):
    kwargs: dict[str, Address | BusGroup | float]
    synthdef: Address
    destroy_strategy: dict[str, float] | None = None

    def create(
        self,
        old_artifacts: Artifacts,
        new_artifacts: Artifacts,
    ) -> None:
        set_kwargs, map_kwargs = self.resolve_kwargs(
            kwargs=self.kwargs,
            new_artifacts=new_artifacts,
            old_artifacts=old_artifacts,
        )
        synth = self.context.add_synth(
            add_action=self.add_action,
            synthdef=self.resolve_synthdef(
                address=self.synthdef,
                new_artifacts=new_artifacts,
                old_artifacts=old_artifacts,
            ),
            target_node=self.resolve_node(
                address=self.target_node,
                new_artifacts=new_artifacts,
                old_artifacts=old_artifacts,
            ),
            permanent=False,
            **set_kwargs,
            **map_kwargs,
        )
        new_artifacts.nodes[self.address] = synth
        self.component._artifacts.nodes[self.name] = synth

    def destroy(
        self,
        old_artifacts: Artifacts,
        reconciliation: Reconciliation,
    ) -> None:
        if (nodes := self.component._artifacts.nodes)[
            self.name
        ].context is self.context:
            nodes.pop(self.name)
        synth = old_artifacts.nodes.pop(self.address)
        if reconciliation in (Reconciliation.DESTROY_SHALLOW, Reconciliation.RECREATE):
            synth.set(done_action=DoneAction.FREE_SYNTH, gate=0)
        elif reconciliation is Reconciliation.DESTROY_ROOT and self.destroy_strategy:
            synth.set(**self.destroy_strategy)

    def mutate(
        self,
        old_artifacts: Artifacts,
        new_artifacts: Artifacts,
        old_spec: "Spec",
    ) -> None:
        if not isinstance(old_spec, SynthSpec):
            raise ValueError(old_spec)
        if (
            self.add_action != old_spec.add_action
            or self.target_node != old_spec.target_node
        ):
            old_artifacts.nodes[self.address].move(
                add_action=self.add_action,
                target_node=self.resolve_node(
                    address=self.target_node,
                    new_artifacts=new_artifacts,
                    old_artifacts=old_artifacts,
                ),
            )
        if self.kwargs != old_spec.kwargs:
            old_set_kwargs, old_map_kwargs = self.resolve_kwargs(
                kwargs=self.kwargs,
                new_artifacts=new_artifacts,
                old_artifacts=old_artifacts,
            )
            new_set_kwargs, new_map_kwargs = self.resolve_kwargs(
                kwargs=self.kwargs,
                new_artifacts=new_artifacts,
                old_artifacts=old_artifacts,
            )
            for key in old_set_kwargs:
                if old_set_kwargs[key] == new_set_kwargs[key]:
                    new_set_kwargs.pop(key)
            for key in old_map_kwargs:
                if old_map_kwargs[key] == new_map_kwargs[key]:
                    new_map_kwargs.pop(key)
            if new_map_kwargs:
                old_artifacts.nodes[self.address].map(**new_map_kwargs)
            if new_set_kwargs:
                old_artifacts.nodes[self.address].set(**new_set_kwargs)

    def requires(self) -> list[Address]:
        return [
            *super().requires(),
            self.synthdef,
            *[value for value in self.kwargs.values() if isinstance(value, Address)],
        ]

    def requires_recreation(self, old_spec: "Spec") -> bool:
        if not isinstance(old_spec, SynthSpec):
            raise ValueError(old_spec)
        return self.synthdef != old_spec.synthdef


@dataclasses.dataclass
class SpecChange:
    address: Address
    component: "Component"
    context: AsyncServer
    reconciliation: Reconciliation
    new_spec: Spec | None = None
    old_spec: Spec | None = None

    def create(
        self,
        old_artifacts: Artifacts,
        new_artifacts: Artifacts,
    ) -> None:
        if self.new_spec is None:
            raise ValueError
        self.new_spec.create(
            new_artifacts=new_artifacts,
            old_artifacts=old_artifacts,
        )

    def mutate(
        self,
        old_artifacts: Artifacts,
        new_artifacts: Artifacts,
    ) -> None:
        if self.new_spec is None or self.old_spec is None:
            raise ValueError
        self.new_spec.mutate(
            new_artifacts=new_artifacts,
            old_artifacts=old_artifacts,
            old_spec=self.old_spec,
        )

    def destroy(
        self,
        old_artifacts: Artifacts,
        new_artifacts: Artifacts,
        related: bool = False,
        rooted: bool = False,
    ) -> None:
        if self.old_spec is None:
            raise ValueError
        self.old_spec.destroy(
            old_artifacts=old_artifacts,
            reconciliation=self.reconciliation,
        )

    @classmethod
    def gather(
        cls,
        *,
        old_specs: dict[Address, Spec],
        new_specs: dict[Address, Spec],
        old_context_artifacts: dict[AsyncServer, Artifacts],
        destroy_reconciliation: Reconciliation,
    ) -> list["SpecChange"]:
        spec_changes: list[SpecChange] = []
        for address, old_spec in old_specs.items():
            if not old_spec.context:
                raise RuntimeError
            if new_spec := new_specs.pop(address, None):
                if not new_spec.context:
                    raise RuntimeError
                if new_spec == old_spec:
                    continue
                if old_spec.context != new_spec.context:
                    spec_changes.extend(
                        [
                            SpecChange(
                                address=address,
                                component=new_spec.component,
                                context=new_spec.context,
                                new_spec=new_spec,
                                reconciliation=Reconciliation.CREATE,
                            ),
                            SpecChange(
                                address=address,
                                component=new_spec.component,
                                context=old_spec.context,
                                old_spec=old_spec,
                                reconciliation=destroy_reconciliation,
                            ),
                        ]
                    )
                elif new_spec.requires_recreation(old_spec):
                    # TODO: Revisit all Spec.requires_recreation() impls
                    #       and remove context comparisons
                    spec_changes.append(
                        SpecChange(
                            address=address,
                            component=new_spec.component,
                            context=new_spec.context,
                            new_spec=new_spec,
                            old_spec=old_spec,
                            reconciliation=Reconciliation.RECREATE,
                        )
                    )
                else:
                    spec_changes.append(
                        SpecChange(
                            address=address,
                            component=new_spec.component,
                            context=new_spec.context,
                            new_spec=new_spec,
                            old_spec=old_spec,
                            reconciliation=Reconciliation.MUTATE,
                        )
                    )
            else:
                spec_changes.append(
                    SpecChange(
                        address=address,
                        component=old_spec.component,
                        context=old_spec.context,
                        old_spec=old_spec,
                        reconciliation=destroy_reconciliation,
                    )
                )
        for address, new_spec in new_specs.items():
            if not new_spec.context:
                raise RuntimeError
            if (
                isinstance(new_spec, SynthDefSpec)
                and new_spec.address
                in old_context_artifacts[new_spec.context].synthdefs
            ):
                # SynthDefs are global to the context,
                # so check that they don't need to be created
                continue
            spec_changes.append(
                SpecChange(
                    address=address,
                    component=new_spec.component,
                    context=new_spec.context,
                    new_spec=new_spec,
                    reconciliation=Reconciliation.CREATE,
                )
            )
        return spec_changes

    @classmethod
    def sort(
        cls, spec_changes: list["SpecChange"]
    ) -> dict[AsyncServer, list["SpecChangeGroup"]]:
        def _sort_create_spec_changes(
            spec_changes: dict[Address, SpecChange],
        ) -> list[SpecChangeGroup]:
            spec_change_groups: list[SpecChangeGroup] = []
            buffers: dict[Component, list[SpecChange]] = {}
            busses: dict[Component, list[SpecChange]] = {}
            synthdefs: list[SpecChange] = []
            ordered_nodes: dict[Address, SpecChange] = {}
            unordered_nodes: deque[tuple[SpecChange, set[Address]]] = deque()
            for spec_change in spec_changes.values():
                if not (spec := spec_change.new_spec):
                    raise ValueError
                if isinstance(spec, BufferSpec):
                    buffers.setdefault(spec.component, []).append(spec_change)
                elif isinstance(spec, BusSpec):
                    busses.setdefault(spec.component, []).append(spec_change)
                elif isinstance(spec, SynthDefSpec):
                    synthdefs.append(spec_change)
                elif isinstance(spec, NodeSpec):
                    dependencies: set[Address] = set(
                        [
                            address
                            for address in spec.requires()
                            if f":{Names.NODES}:" in address and address in spec_changes
                        ]
                    )
                    unordered_nodes.append((spec_change, dependencies))
            while unordered_nodes:
                spec_change, dependencies = unordered_nodes.popleft()
                if all(dependency in ordered_nodes for dependency in dependencies):
                    ordered_nodes[spec_change.address] = spec_change
                else:
                    unordered_nodes.append((spec_change, dependencies))
            if synthdefs:
                spec_change_groups.append(
                    SpecChangeGroup(
                        group=False,
                        reconciliation=Reconciliation.CREATE,
                        spec_changes=sorted(synthdefs, key=lambda x: x.address),
                        sync=True,
                    ),
                )
            for group in buffers.values():
                spec_change_groups.append(
                    SpecChangeGroup(
                        group=True,
                        reconciliation=Reconciliation.CREATE,
                        spec_changes=list(group),
                        sync=True,
                    )
                )
            for group in busses.values():
                spec_change_groups.append(
                    SpecChangeGroup(
                        group=True,
                        reconciliation=Reconciliation.CREATE,
                        spec_changes=list(group),
                        sync=False,
                    )
                )
            for _, iterator in itertools.groupby(
                ordered_nodes.values(), lambda x: x.component
            ):
                spec_change_groups.append(
                    SpecChangeGroup(
                        group=True,
                        reconciliation=Reconciliation.CREATE,
                        spec_changes=list(iterator),
                        sync=False,
                    )
                )
            return spec_change_groups

        sorted_spec_changes: dict[AsyncServer, list[SpecChangeGroup]] = {}
        unsorted_spec_changes: dict[AsyncServer, list[SpecChange]] = {}
        for spec_change in spec_changes:
            unsorted_spec_changes.setdefault(spec_change.context, []).append(
                spec_change
            )
        for context, spec_changes_ in unsorted_spec_changes.items():
            creations: dict[Address, SpecChange] = {}
            mutations: list[SpecChange] = []
            destructions: list[SpecChange] = []
            for spec_change in spec_changes_:
                if spec_change.reconciliation == Reconciliation.CREATE:
                    creations[spec_change.address] = spec_change
                elif spec_change.reconciliation == Reconciliation.RECREATE:
                    creations[spec_change.address] = spec_change
                    destructions.append(spec_change)
                elif spec_change.reconciliation == Reconciliation.MUTATE:
                    mutations.append(spec_change)
                elif spec_change.reconciliation in (
                    Reconciliation.DESTROY_ROOT,
                    Reconciliation.DESTROY_SHALLOW,
                ):
                    destructions.append(spec_change)
            # sort creations
            sorted_spec_changes[context] = _sort_create_spec_changes(creations)
            # sort mutations
            for _, group in itertools.groupby(mutations, lambda x: x.component):
                sorted_spec_changes[context].append(
                    SpecChangeGroup(
                        group=True,
                        reconciliation=Reconciliation.MUTATE,
                        spec_changes=list(group),
                        sync=False,
                    )
                )
            # sort destructions
            for _, group in itertools.groupby(destructions, lambda x: x.component):
                sorted_spec_changes[context].append(
                    SpecChangeGroup(
                        group=True,
                        reconciliation=Reconciliation.DESTROY,
                        spec_changes=list(group),
                        sync=False,
                    )
                )
        return sorted_spec_changes


@dataclasses.dataclass
class SpecChangeGroup:
    reconciliation: Reconciliation
    spec_changes: list[SpecChange]
    group: bool = True
    sync: bool = False

    def apply(
        self,
        *,
        context: AsyncServer,
        old_artifacts: Artifacts,
        new_artifacts: Artifacts,
        roots: list["Component"],
        related: list["Component"],
    ) -> None:
        with contextlib.ExitStack() as exit_stack:
            if self.group:
                exit_stack.enter_context(context.at())
            if self.reconciliation is Reconciliation.CREATE:
                for spec_change in self.spec_changes:
                    spec_change.create(
                        old_artifacts=old_artifacts,
                        new_artifacts=new_artifacts,
                    )
            elif self.reconciliation is Reconciliation.MUTATE:
                for spec_change in self.spec_changes:
                    spec_change.mutate(
                        old_artifacts=old_artifacts,
                        new_artifacts=new_artifacts,
                    )
            elif self.reconciliation in Reconciliation.DESTROY:
                for spec_change in self.spec_changes:
                    spec_change.destroy(
                        old_artifacts=old_artifacts,
                        new_artifacts=new_artifacts,
                        rooted=spec_change.component in roots,
                        related=spec_change.component in related,
                    )
            else:
                raise ValueError(self.reconciliation)
