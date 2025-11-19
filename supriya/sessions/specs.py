import contextlib
import dataclasses
import itertools
from collections import ChainMap, deque
from typing import TYPE_CHECKING, Iterator, Optional, Sequence

from ..contexts import AsyncServer, Buffer, BusGroup, Node
from ..enums import AddAction, CalculationRate, DoneAction
from ..ugens import SynthDef
from .constants import IO, Address, Entities, Names, Reconciliation

if TYPE_CHECKING:
    from .components import Component


# TODO: Implement non-resource specs, e.g. NodeOrderSpec
#       which depends on both the target node and the ordered nodes and
#       which can issue an /n_order command to enforce node ordering in
#       more complex synth setups, e.g. effect devices with conditional
#       synths.


@dataclasses.dataclass
class Artifacts:
    """
    Utility for associating context entities with addresses.
    """

    audio_buses: dict[Address, BusGroup] = dataclasses.field(default_factory=dict)
    buffers: dict[Address, Buffer] = dataclasses.field(default_factory=dict)
    control_buses: dict[Address, BusGroup] = dataclasses.field(default_factory=dict)
    nodes: dict[Address, Node] = dataclasses.field(default_factory=dict)
    synthdefs: dict[Address, SynthDef] = dataclasses.field(default_factory=dict)
    hashes: dict[Address, int] = dataclasses.field(default_factory=dict)

    def clear(self) -> None:
        """
        Clear the artifacts.
        """
        self.audio_buses.clear()
        self.buffers.clear()
        self.control_buses.clear()
        self.nodes.clear()
        self.synthdefs.clear()
        self.hashes.clear()

    def merge(self, other: "Artifacts") -> None:
        """
        Merge ``other`` artifacts in this one, overriding any existing addresses.
        """
        self.audio_buses.update(other.audio_buses)
        self.buffers.update(other.buffers)
        self.control_buses.update(other.control_buses)
        self.nodes.update(other.nodes)
        self.synthdefs.update(other.synthdefs)
        self.hashes.update(other.hashes)


@dataclasses.dataclass(frozen=True, slots=True)
class Spec:
    """
    Base class for specifying the desired state of a context entity, and for
    implementing the logic to bring the current state of that entitiy into line
    with the desired state.
    """

    component: "Component"
    context: AsyncServer
    name: str
    address: Address = dataclasses.field(init=False)

    def __post_init__(self):
        object.__setattr__(self, "address", self._address())

    def _address(self) -> Address:
        raise NotImplementedError

    def create(
        self,
        *,
        global_specs: dict[Address, "Spec"],
        new_global_artifacts: Artifacts,
        old_global_artifacts: Artifacts,
    ) -> None:
        raise NotImplementedError

    def destroy(
        self,
        *,
        global_specs: dict[Address, "Spec"],
        old_global_artifacts: Artifacts,
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

    @staticmethod
    def get_address(
        component: Optional["Component"], type_: Entities, name: str
    ) -> Address:
        if type_ == Entities.SYNTHDEFS:
            return f"{Entities.SYNTHDEFS}:{name}"
        elif component is None:
            raise ValueError
        return f"{component.numeric_address}:{type_}:{name}"

    def mutate(
        self,
        *,
        global_specs: dict[Address, "Spec"],
        new_global_artifacts: Artifacts,
        old_global_artifacts: Artifacts,
        old_spec: "Spec",
    ) -> None:
        raise NotImplementedError

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

    def requires(self) -> list[Address]:
        return []

    def requires_recreation(self, old_spec: "Spec") -> bool:
        raise NotImplementedError

    def resolve_bus(
        self,
        *,
        address: Address,
        new_global_artifacts: Artifacts,
        old_global_artifacts: Artifacts,
    ) -> BusGroup:
        return ChainMap(
            new_global_artifacts.audio_buses,
            new_global_artifacts.control_buses,
            old_global_artifacts.audio_buses,
            old_global_artifacts.control_buses,
        )[address]

    def resolve_kwargs(
        self,
        *,
        kwargs: dict[str, Address | BusGroup | float],
        new_global_artifacts: Artifacts,
        old_global_artifacts: Artifacts,
    ) -> tuple[dict[str, float], dict[str, str]]:
        map_kwargs: dict[str, str] = {}
        set_kwargs: dict[str, float] = {}
        for key, value in kwargs.items():
            if isinstance(value, Address):
                value = self.resolve_bus(
                    address=value,
                    new_global_artifacts=new_global_artifacts,
                    old_global_artifacts=old_global_artifacts,
                )
            assert not isinstance(value, Address)
            if isinstance(value, BusGroup):
                if (
                    key in ("bus", "in_", "out")
                    or value.calculation_rate is CalculationRate.AUDIO
                ):
                    set_kwargs[key] = int(value)
                else:
                    map_kwargs[key] = value.map_symbol()
            else:
                set_kwargs[key] = float(value)
        return set_kwargs, map_kwargs

    def resolve_node(
        self,
        *,
        address: Address | None,
        new_global_artifacts: Artifacts,
        old_global_artifacts: Artifacts,
    ) -> Node:
        target_node: Node | None = None
        if address and not (
            target_node := ChainMap(
                new_global_artifacts.nodes, old_global_artifacts.nodes
            ).get(address)
        ):
            raise ValueError(address)
        return target_node or self.context.default_group

    def resolve_synthdef(
        self,
        *,
        address: Address,
        old_global_artifacts: Artifacts,
        new_global_artifacts: Artifacts,
    ) -> SynthDef:
        return ChainMap(
            new_global_artifacts.synthdefs,
            old_global_artifacts.synthdefs,
        )[address]


@dataclasses.dataclass(frozen=True, slots=True)
class BufferSpec(Spec):
    """
    Specification for a buffer context entity.
    """

    channel_count: int
    count: int

    def __hash__(self) -> int:
        return hash(
            (
                type(self),
                self.component,
                self.context,
                self.name,
                self.channel_count,
                self.count,
            ),
        )

    def _address(self) -> Address:
        return Spec.get_address(self.component, Entities.BUFFERS, self.name)

    def create(
        self,
        global_specs: dict[Address, "Spec"],
        old_global_artifacts: Artifacts,
        new_global_artifacts: Artifacts,
    ) -> None:
        raise NotImplementedError

    def destroy(
        self,
        global_specs: dict[Address, "Spec"],
        old_global_artifacts: Artifacts,
        reconciliation: Reconciliation,
    ) -> None:
        raise NotImplementedError

    def mutate(
        self,
        global_specs: dict[Address, "Spec"],
        old_global_artifacts: Artifacts,
        new_global_artifacts: Artifacts,
        old_spec: "Spec",
    ) -> None:
        raise NotImplementedError

    def requires_recreation(self, old_spec: "Spec") -> bool:
        return self != old_spec


@dataclasses.dataclass(frozen=True, slots=True)
class BusSpec(Spec):
    """
    Specification for a bus context entity.
    """

    calculation_rate: CalculationRate
    channel_count: int
    default: float = dataclasses.field(compare=False, default=0.0)

    def __hash__(self) -> int:
        return hash(
            (
                type(self),
                self.component,
                self.context,
                self.name,
                self.calculation_rate,
                self.channel_count,
            ),
        )

    def _address(self) -> Address:
        if self.calculation_rate == CalculationRate.AUDIO:
            return Spec.get_address(self.component, Entities.AUDIO_BUSES, self.name)
        elif self.calculation_rate == CalculationRate.CONTROL:
            return Spec.get_address(self.component, Entities.CONTROL_BUSES, self.name)
        raise ValueError

    def create(
        self,
        global_specs: dict[Address, "Spec"],
        old_global_artifacts: Artifacts,
        new_global_artifacts: Artifacts,
    ) -> None:
        local_artifacts = self.component._local_artifacts
        if self.calculation_rate == CalculationRate.AUDIO:
            bus_group = self.context.add_bus_group(
                calculation_rate=self.calculation_rate,
                count=self.channel_count,
            )
            new_global_artifacts.audio_buses[self.address] = bus_group
            local_artifacts.audio_buses[self.name] = bus_group
        elif self.calculation_rate == CalculationRate.CONTROL:
            bus_group = self.context.add_bus_group(
                calculation_rate=self.calculation_rate,
                count=self.channel_count,
            )
            bus_group.set(self.default)
            new_global_artifacts.control_buses[self.address] = bus_group
            local_artifacts.control_buses[self.name] = bus_group
        else:
            raise ValueError
        local_artifacts.hashes[self.address] = hash(self)
        global_specs[self.address] = self

    def destroy(
        self,
        global_specs: dict[Address, "Spec"],
        old_global_artifacts: Artifacts,
        reconciliation: Reconciliation,
    ) -> None:
        local_artifacts = self.component._local_artifacts
        if self.calculation_rate == CalculationRate.AUDIO:
            buses = local_artifacts.audio_buses
            old_buses = old_global_artifacts.audio_buses
        elif self.calculation_rate == CalculationRate.CONTROL:
            buses = local_artifacts.control_buses
            old_buses = old_global_artifacts.control_buses
        if local_artifacts.hashes[self.address] == hash(self):
            buses.pop(self.name)
            local_artifacts.hashes.pop(self.address)
        old_buses.pop(self.address).free()
        global_specs.pop(self.address)

    def requires_recreation(self, old_spec: "Spec") -> bool:
        if not isinstance(old_spec, BusSpec):
            raise ValueError(old_spec)
        return self != old_spec


@dataclasses.dataclass(frozen=True, slots=True)
class SynthDefSpec(Spec):
    """
    Specification for a SynthDef context entity.
    """

    synthdef: SynthDef

    def __hash__(self) -> int:
        return hash(
            (
                type(self),
                self.component,
                self.context,
                self.name,
                self.synthdef,
            ),
        )

    def _address(self) -> Address:
        return Spec.get_address(None, Entities.SYNTHDEFS, self.synthdef.effective_name)

    def create(
        self,
        global_specs: dict[Address, "Spec"],
        old_global_artifacts: Artifacts,
        new_global_artifacts: Artifacts,
    ) -> None:
        if self.address in old_global_artifacts.synthdefs:
            return
        self.context.add_synthdefs(self.synthdef)
        new_global_artifacts.synthdefs[self.address] = self.synthdef
        global_specs[self.address] = self

    def destroy(
        self,
        *,
        global_specs: dict[Address, "Spec"],
        old_global_artifacts: Artifacts,
        reconciliation: Reconciliation,
    ) -> None:
        pass

    def requires_recreation(self, old_spec: "Spec") -> bool:
        return self != old_spec


@dataclasses.dataclass(frozen=True, slots=True)
class NodeSpec(Spec):
    """
    Specification for a node context entity.

    GroupSpec and SynthSpec inherit from this.
    """

    add_action: AddAction
    parent_node: Address | None
    target_node: Address | None

    def _address(self) -> Address:
        return Spec.get_address(self.component, Entities.NODES, self.name)

    def requires(self) -> list[Address]:
        if self.target_node is not None:
            return [self.target_node]
        return []


@dataclasses.dataclass(frozen=True, slots=True)
class GroupSpec(NodeSpec):
    """
    Specification for a group context entity.
    """

    destroy_strategy: dict[str, float] | None = None

    def __hash__(self) -> int:
        return hash(
            (
                type(self),
                self.component,
                self.context,
                self.name,
                self.add_action,
                self.parent_node,
                self.target_node,
                (
                    tuple(sorted(self.destroy_strategy.items()))
                    if self.destroy_strategy
                    else None,
                ),
            ),
        )

    def create(
        self,
        *,
        global_specs: dict[Address, "Spec"],
        old_global_artifacts: Artifacts,
        new_global_artifacts: Artifacts,
    ) -> None:
        group = self.context.add_group(
            add_action=self.add_action,
            target_node=self.resolve_node(
                address=self.target_node,
                new_global_artifacts=new_global_artifacts,
                old_global_artifacts=old_global_artifacts,
            ),
        )
        global_specs[self.address] = self
        local_artifacts = self.component._local_artifacts
        local_artifacts.hashes[self.address] = hash(self)
        local_artifacts.nodes[self.name] = group
        new_global_artifacts.nodes[self.address] = group

    def destroy(
        self,
        *,
        global_specs: dict[Address, "Spec"],
        old_global_artifacts: Artifacts,
        reconciliation: Reconciliation,
    ) -> None:
        # N.B.: We need to compare new vs old spec hashes before deleting from
        # component artifacts to handle the case of re-creation where a new
        # node was created and added to the component artifacts but with a
        # different hash than this spec's hash.
        local_artifacts = self.component._local_artifacts
        if local_artifacts.hashes[self.address] == hash(self):
            local_artifacts.nodes.pop(self.name)
            local_artifacts.hashes.pop(self.address)
        group = old_global_artifacts.nodes.pop(self.address)
        if reconciliation is Reconciliation.DESTROY_ROOT and self.destroy_strategy:
            group.set(**self.destroy_strategy)
        global_specs.pop(self.address)

    def mutate(
        self,
        *,
        global_specs: dict[Address, "Spec"],
        old_global_artifacts: Artifacts,
        new_global_artifacts: Artifacts,
        old_spec: "Spec",
    ) -> None:
        if not isinstance(old_spec, GroupSpec):
            raise ValueError(old_spec)
        if (
            self.parent_node != old_spec.parent_node
            or self.add_action != old_spec.add_action
            or self.target_node != old_spec.target_node
        ):
            old_global_artifacts.nodes[self.address].move(
                add_action=self.add_action,
                target_node=self.resolve_node(
                    address=self.target_node,
                    new_global_artifacts=new_global_artifacts,
                    old_global_artifacts=old_global_artifacts,
                ),
            )
        global_specs[self.address] = self
        local_artifacts = self.component._local_artifacts
        local_artifacts.hashes[self.address] = hash(self)

    def requires_recreation(self, old_spec: "Spec") -> bool:
        return False


@dataclasses.dataclass(frozen=True, slots=True)
class SynthSpec(NodeSpec):
    """
    Specification for a synth context entity.
    """

    kwargs: dict[str, Address | BusGroup | float]
    synthdef: Address
    destroy_strategy: dict[str, float] | None = None

    def __hash__(self) -> int:
        return hash(
            (
                type(self),
                self.component,
                self.context,
                self.name,
                self.add_action,
                self.parent_node,
                self.target_node,
                tuple(sorted(self.kwargs.items())),
                self.synthdef,
                (
                    tuple(sorted(self.destroy_strategy.items()))
                    if self.destroy_strategy
                    else None,
                ),
            ),
        )

    def create(
        self,
        *,
        global_specs: dict[Address, "Spec"],
        old_global_artifacts: Artifacts,
        new_global_artifacts: Artifacts,
    ) -> None:
        set_kwargs, map_kwargs = self.resolve_kwargs(
            kwargs=self.kwargs,
            new_global_artifacts=new_global_artifacts,
            old_global_artifacts=old_global_artifacts,
        )
        synth = self.context.add_synth(
            add_action=self.add_action,
            synthdef=self.resolve_synthdef(
                address=self.synthdef,
                new_global_artifacts=new_global_artifacts,
                old_global_artifacts=old_global_artifacts,
            ),
            target_node=self.resolve_node(
                address=self.target_node,
                new_global_artifacts=new_global_artifacts,
                old_global_artifacts=old_global_artifacts,
            ),
            permanent=False,
            **set_kwargs,
            **map_kwargs,
        )
        global_specs[self.address] = self
        local_artifacts = self.component._local_artifacts
        local_artifacts.hashes[self.address] = hash(self)
        local_artifacts.nodes[self.name] = synth
        new_global_artifacts.nodes[self.address] = synth

    def destroy(
        self,
        *,
        global_specs: dict[Address, "Spec"],
        old_global_artifacts: Artifacts,
        reconciliation: Reconciliation,
    ) -> None:
        # N.B.: We need to compare new vs old spec hashes before deleting from
        # component artifacts to handle the case of re-creation where a new
        # node was created and added to the component artifacts but with a
        # different hash than this spec's hash.
        local_artifacts = self.component._local_artifacts
        if local_artifacts.hashes[self.address] == hash(self):
            local_artifacts.nodes.pop(self.name)
            local_artifacts.hashes.pop(self.address)
        synth = old_global_artifacts.nodes.pop(self.address)
        if reconciliation in (Reconciliation.DESTROY_SHALLOW, Reconciliation.RECREATE):
            if old_global_artifacts.synthdefs[self.synthdef].has_gate:
                synth.set(done_action=DoneAction.FREE_SYNTH, gate=0)
            else:
                synth.free()
        elif reconciliation is Reconciliation.DESTROY_ROOT and self.destroy_strategy:
            if old_global_artifacts.synthdefs[self.synthdef].has_gate:
                synth.set(**self.destroy_strategy)
            else:
                synth.free()
        global_specs.pop(self.address)

    def mutate(
        self,
        *,
        global_specs: dict[Address, "Spec"],
        old_global_artifacts: Artifacts,
        new_global_artifacts: Artifacts,
        old_spec: "Spec",
    ) -> None:
        if not isinstance(old_spec, SynthSpec):
            raise ValueError(old_spec)
        if (
            self.parent_node != old_spec.parent_node
            or self.add_action != old_spec.add_action
            or self.target_node != old_spec.target_node
        ):
            old_global_artifacts.nodes[self.address].move(
                add_action=self.add_action,
                target_node=self.resolve_node(
                    address=self.target_node,
                    new_global_artifacts=new_global_artifacts,
                    old_global_artifacts=old_global_artifacts,
                ),
            )
        if self.kwargs != old_spec.kwargs:
            old_set_kwargs, old_map_kwargs = self.resolve_kwargs(
                kwargs=old_spec.kwargs,
                new_global_artifacts=new_global_artifacts,
                old_global_artifacts=old_global_artifacts,
            )
            new_set_kwargs, new_map_kwargs = self.resolve_kwargs(
                kwargs=self.kwargs,
                new_global_artifacts=new_global_artifacts,
                old_global_artifacts=old_global_artifacts,
            )
            for key in old_set_kwargs:
                if old_set_kwargs[key] == new_set_kwargs[key]:
                    new_set_kwargs.pop(key)
            for key in old_map_kwargs:
                if old_map_kwargs[key] == new_map_kwargs[key]:
                    new_map_kwargs.pop(key)
            if new_map_kwargs:
                old_global_artifacts.nodes[self.address].map(**new_map_kwargs)
            if new_set_kwargs:
                old_global_artifacts.nodes[self.address].set(**new_set_kwargs)
        global_specs[self.address] = self
        local_artifacts = self.component._local_artifacts
        local_artifacts.hashes[self.address] = hash(self)

    def requires(self) -> list[Address]:
        return [
            *NodeSpec.requires(self),
            self.synthdef,
            *[value for value in self.kwargs.values() if isinstance(value, Address)],
        ]

    def requires_recreation(self, old_spec: "Spec") -> bool:
        if not isinstance(old_spec, SynthSpec):
            raise ValueError(old_spec)
        if self.synthdef != old_spec.synthdef:
            return True
        elif any(
            self.kwargs.get(key) != old_spec.kwargs.get(key) for key in ["in_", "out"]
        ):
            return True
        return False


@dataclasses.dataclass(frozen=True, slots=True)
class SpecFactory:
    component: "Component"
    context: AsyncServer
    _buffers: list[BufferSpec] = dataclasses.field(default_factory=list, init=False)
    _buses: list[BusSpec] = dataclasses.field(default_factory=list, init=False)
    _groups: list[GroupSpec] = dataclasses.field(default_factory=list, init=False)
    _synths: list[SynthSpec] = dataclasses.field(default_factory=list, init=False)
    _synthdefs: list[SynthDefSpec] = dataclasses.field(default_factory=list, init=False)

    def __iter__(self) -> Iterator[Spec]:
        for specs in (
            self._synthdefs,
            self._buffers,
            self._buses,
            self._groups,
            self._synths,
        ):
            for spec in specs:
                yield spec

    def add_audio_bus(
        self,
        *,
        channel_count: int,
        component: Optional["Component"] = None,
        name: str,
    ) -> Address:
        self._buses.append(
            spec := BusSpec(
                calculation_rate=CalculationRate.AUDIO,
                channel_count=channel_count,
                component=component or self.component,
                context=self.context,
                name=name,
            )
        )
        return spec.address

    def add_container_group(
        self,
        *,
        component: Optional["Component"] = None,
        destroy_strategy: dict[str, float] | None = None,
        parent: "Component",
        parent_container: Sequence["Component"],
        parent_container_group_name: str,
    ) -> Address:
        component = component or self.component
        if index := parent_container.index(component):
            # relative to previous member's group
            group_add_action: AddAction = AddAction.ADD_AFTER
            group_target: Address = Spec.get_address(
                parent_container[index - 1],
                Entities.NODES,
                Names.GROUP,
            )
        else:
            # first member in the group
            group_add_action = AddAction.ADD_TO_HEAD
            group_target = Spec.get_address(
                parent, Entities.NODES, parent_container_group_name
            )
        return self.add_group(
            add_action=group_add_action,
            component=component,
            destroy_strategy=destroy_strategy,
            name=Names.GROUP,
            parent_node=Spec.get_address(
                parent, Entities.NODES, parent_container_group_name
            ),
            target_node=group_target,
        )

    def add_control_bus(
        self,
        *,
        channel_count: int,
        component: Optional["Component"] = None,
        default: float = 0.0,
        name: str,
    ) -> Address:
        self._buses.append(
            spec := BusSpec(
                calculation_rate=CalculationRate.CONTROL,
                channel_count=channel_count,
                component=component or self.component,
                context=self.context,
                default=default,
                name=name,
            )
        )
        return spec.address

    def add_group(
        self,
        *,
        add_action: AddAction,
        component: Optional["Component"] = None,
        destroy_strategy: dict[str, float] | None = None,
        name: str,
        parent_node: Address | None = None,
        target_node: Address | None,
    ) -> Address:
        self._groups.append(
            spec := GroupSpec(
                add_action=add_action,
                component=component or self.component,
                context=self.context,
                destroy_strategy=destroy_strategy,
                name=name,
                parent_node=parent_node,
                target_node=target_node,
            )
        )
        return spec.address

    def add_synth(
        self,
        *,
        add_action: AddAction,
        component: Optional["Component"] = None,
        destroy_strategy: dict[str, float] | None = None,
        kwargs: dict[str, Address | BusGroup | float] | None = None,
        name: str,
        parent_node: Address | None = None,
        synthdef: Address,
        target_node: Address | None,
    ) -> Address:
        self._synths.append(
            spec := SynthSpec(
                add_action=add_action,
                component=component or self.component,
                context=self.context,
                destroy_strategy=destroy_strategy,
                kwargs=kwargs or {},
                name=name,
                parent_node=parent_node,
                synthdef=synthdef,
                target_node=target_node,
            )
        )
        return spec.address

    def add_synthdef(
        self,
        *,
        component: Optional["Component"] = None,
        synthdef: SynthDef,
    ) -> Address:
        self._synthdefs.append(
            spec := SynthDefSpec(
                component=component or self.component,
                context=self.context,
                name=synthdef.effective_name,
                synthdef=synthdef,
            )
        )
        return spec.address


@dataclasses.dataclass
class SpecChange:
    """
    Utility for pairing an old context entity specification with a new one.
    """

    address: Address
    component: "Component"
    context: AsyncServer
    reconciliation: Reconciliation
    new_spec: Spec | None = None
    old_spec: Spec | None = None

    def create(
        self,
        global_specs: dict[Address, Spec],
        old_global_artifacts: Artifacts,
        new_global_artifacts: Artifacts,
    ) -> None:
        if self.new_spec is None:
            raise ValueError
        self.new_spec.create(
            global_specs=global_specs,
            new_global_artifacts=new_global_artifacts,
            old_global_artifacts=old_global_artifacts,
        )

    def mutate(
        self,
        global_specs: dict[Address, Spec],
        old_global_artifacts: Artifacts,
        new_global_artifacts: Artifacts,
    ) -> None:
        if self.new_spec is None or self.old_spec is None:
            raise ValueError
        self.new_spec.mutate(
            global_specs=global_specs,
            new_global_artifacts=new_global_artifacts,
            old_global_artifacts=old_global_artifacts,
            old_spec=self.old_spec,
        )

    def destroy(
        self,
        global_specs: dict[Address, Spec],
        old_global_artifacts: Artifacts,
        new_global_artifacts: Artifacts,
        related: bool = False,
        rooted: bool = False,
    ) -> None:
        if self.old_spec is None:
            raise ValueError
        self.old_spec.destroy(
            global_specs=global_specs,
            old_global_artifacts=old_global_artifacts,
            reconciliation=self.reconciliation,
        )

    @classmethod
    def gather(
        cls,
        *,
        destroy_reconciliation: Reconciliation,
        global_artifacts_by_context: dict[AsyncServer, Artifacts],
        new_specs: dict[Address, Spec],
        old_specs: dict[Address, Spec],
    ) -> list["SpecChange"]:
        spec_changes: list[SpecChange] = []
        for address, old_spec in old_specs.items():
            if new_spec := new_specs.pop(address, None):
                # unchanged spec
                if new_spec == old_spec:
                    continue
                # context change: destroy and create
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
                # new and old specs: recreate
                elif new_spec.requires_recreation(old_spec):
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
                # new and old specs: mutate
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
            # no new spec: destroy the old
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
            if (
                isinstance(new_spec, SynthDefSpec)
                and new_spec.address
                in global_artifacts_by_context[new_spec.context].synthdefs
            ):
                # SynthDefs are global to the context,
                # so check that they don't need to be created
                continue
            # no old spec: create the new
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
            buses: dict[Component, list[SpecChange]] = {}
            synthdefs: list[SpecChange] = []
            ordered_nodes: dict[Address, SpecChange] = {}
            unordered_nodes: deque[tuple[SpecChange, set[Address]]] = deque()
            for spec_change in spec_changes.values():
                if not (spec := spec_change.new_spec):
                    raise ValueError
                if isinstance(spec, BufferSpec):
                    buffers.setdefault(spec.component, []).append(spec_change)
                elif isinstance(spec, BusSpec):
                    buses.setdefault(spec.component, []).append(spec_change)
                elif isinstance(spec, SynthDefSpec):
                    synthdefs.append(spec_change)
                elif isinstance(spec, NodeSpec):
                    dependencies: set[Address] = set(
                        [
                            address
                            for address in spec.requires()
                            if f":{Entities.NODES}:" in address
                            and address in spec_changes
                        ]
                    )
                    unordered_nodes.append((spec_change, dependencies))
            # TODO: Implement a better topological sort here
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
                        spec_changes=sorted(group, key=lambda x: x.address),
                        sync=True,
                    )
                )
            for group in buses.values():
                spec_change_groups.append(
                    SpecChangeGroup(
                        group=True,
                        reconciliation=Reconciliation.CREATE,
                        spec_changes=sorted(group, key=lambda x: x.address),
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
    """
    Utility for grouping specification changes together when applying them
    against a synthesis context.
    """

    reconciliation: Reconciliation
    spec_changes: list[SpecChange]
    group: bool = True
    sync: bool = False

    def apply(
        self,
        *,
        context: AsyncServer,
        global_specs: dict[Address, Spec],
        new_global_artifacts: Artifacts,
        old_global_artifacts: Artifacts,
        related: set["Component"],
        roots: list["Component"],
    ) -> None:
        with contextlib.ExitStack() as exit_stack:
            if self.group:
                exit_stack.enter_context(context.at())
            if self.reconciliation is Reconciliation.CREATE:
                for spec_change in self.spec_changes:
                    spec_change.create(
                        global_specs=global_specs,
                        new_global_artifacts=new_global_artifacts,
                        old_global_artifacts=old_global_artifacts,
                    )
            elif self.reconciliation is Reconciliation.MUTATE:
                for spec_change in self.spec_changes:
                    spec_change.mutate(
                        global_specs=global_specs,
                        new_global_artifacts=new_global_artifacts,
                        old_global_artifacts=old_global_artifacts,
                    )
            elif self.reconciliation in Reconciliation.DESTROY:
                for spec_change in self.spec_changes:
                    spec_change.destroy(
                        global_specs=global_specs,
                        new_global_artifacts=new_global_artifacts,
                        old_global_artifacts=old_global_artifacts,
                        related=spec_change.component in related,
                        rooted=spec_change.component in roots,
                    )
            else:
                raise ValueError(self.reconciliation)
