import dataclasses
from collections import ChainMap
from typing import TYPE_CHECKING, Optional

from ..contexts import AsyncServer, Buffer, BusGroup, Node
from ..enums import AddAction, CalculationRate, DoneAction
from ..ugens import SynthDef
from .constants import Address, Names

if TYPE_CHECKING:
    from .components import Component


@dataclasses.dataclass
class Artifacts:
    audio_buses: dict[Address, BusGroup] = dataclasses.field(default_factory=dict)
    buffers: dict[Address, Buffer] = dataclasses.field(default_factory=dict)
    control_buses: dict[Address, BusGroup] = dataclasses.field(default_factory=dict)
    nodes: dict[Address, Node] = dataclasses.field(default_factory=dict)
    synthdefs: dict[Address, SynthDef] = dataclasses.field(default_factory=dict)

    def merge(self, other: "Artifacts") -> None:
        self.audio_buses.update(other.audio_buses)
        self.buffers.update(other.buffers)
        self.control_buses.update(other.control_buses)
        self.nodes.update(other.nodes)
        self.synthdefs.update(other.synthdefs)


@dataclasses.dataclass
class Spec:
    component: "Component"
    context: AsyncServer | None
    name: str

    def create(
        self,
        *,
        context: AsyncServer,
        new_artifacts: Artifacts,
        old_artifacts: Artifacts,
    ) -> None:
        raise NotImplementedError

    def destroy(
        self,
        *,
        context: AsyncServer,
        old_artifacts: Artifacts,
    ) -> None:
        raise NotImplementedError

    @classmethod
    def feedsback(
        cls,
        source_order: tuple[int, ...] | None,
        target_order: tuple[int, ...] | None,
        writing: bool = True,
    ) -> bool | None:
        if source_order is None or target_order is None:
            return None
        length = min(len(target_order), len(source_order))
        # If source_order is shallower than target_order, source_order might contain target_order
        if len(source_order) < len(target_order):
            feedsback = target_order[:length] <= source_order
        # If target_order is shallower than source_order, target_order might contain source_order
        elif len(target_order) < len(source_order):
            feedsback = target_order < source_order[:length]
        # If orders are same depth, check difference strictly
        else:
            feedsback = target_order <= source_order
        return feedsback

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
        context: AsyncServer,
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
        context: AsyncServer,
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
        return target_node or context.default_group

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
        context: AsyncServer,
        old_artifacts: Artifacts,
        new_artifacts: Artifacts,
    ) -> None:
        raise NotImplementedError

    def destroy(self, context: AsyncServer, old_artifacts: Artifacts) -> None:
        old_artifacts.buffers.pop(self.address).free()
        self.component._artifacts.buffers.pop(self.name)

    def mutate(
        self,
        context: AsyncServer,
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
        context: AsyncServer,
        old_artifacts: Artifacts,
        new_artifacts: Artifacts,
    ) -> None:
        if self.calculation_rate == CalculationRate.AUDIO:
            bus_group = context.add_bus_group(
                calculation_rate=self.calculation_rate,
                count=self.channel_count,
            )
            new_artifacts.audio_buses[self.address] = bus_group
            self.component._artifacts.audio_buses[self.name] = bus_group
        elif self.calculation_rate == CalculationRate.CONTROL:
            bus_group = context.add_bus_group(
                calculation_rate=self.calculation_rate,
                count=self.channel_count,
            )
            bus_group.set(self.default)
            new_artifacts.control_buses[self.address] = bus_group
            self.component._artifacts.control_buses[self.name] = bus_group
        else:
            raise ValueError

    def destroy(self, context: AsyncServer, old_artifacts: Artifacts) -> None:
        if self.calculation_rate == CalculationRate.AUDIO:
            old_artifacts.audio_buses.pop(self.address).free()
            self.component._artifacts.audio_buses.pop(self.name)
        elif self.calculation_rate == CalculationRate.CONTROL:
            old_artifacts.control_buses.pop(self.address).free()
            self.component._artifacts.control_buses.pop(self.name)

    def mutate(
        self,
        context: AsyncServer,
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
        context: AsyncServer,
        old_artifacts: Artifacts,
        new_artifacts: Artifacts,
    ) -> None:
        context.add_synthdefs(self.synthdef)
        new_artifacts.synthdefs[self.address] = self.synthdef

    def destroy(self, context: AsyncServer, old_artifacts: Artifacts) -> None:
        return

    def mutate(
        self,
        context: AsyncServer,
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

    def create(
        self,
        context: AsyncServer,
        old_artifacts: Artifacts,
        new_artifacts: Artifacts,
    ) -> None:
        group = context.add_group(
            add_action=self.add_action,
            target_node=self.resolve_node(
                address=self.target_node,
                context=context,
                new_artifacts=new_artifacts,
                old_artifacts=old_artifacts,
            ),
        )
        new_artifacts.nodes[self.address] = group
        self.component._artifacts.nodes[self.name] = group

    def destroy(self, context: AsyncServer, old_artifacts: Artifacts) -> None:
        # Handle actual freeing via synths contained in the group to ensure
        # fade-outs get applied.
        old_artifacts.nodes.pop(self.address)
        self.component._artifacts.nodes.pop(self.name)

    def mutate(
        self,
        context: AsyncServer,
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
                    context=context,
                    new_artifacts=new_artifacts,
                    old_artifacts=old_artifacts,
                ),
            )

    def requires_recreation(self, old_spec: "Spec") -> bool:
        if not isinstance(old_spec, GroupSpec):
            raise ValueError(old_spec)
        if self.context != old_spec.context:
            return True
        return False


@dataclasses.dataclass
class SynthSpec(NodeSpec):
    kwargs: dict[str, Address | BusGroup | float]
    synthdef: Address
    destroy_strategy: DoneAction | None = None

    def create(
        self,
        context: AsyncServer,
        old_artifacts: Artifacts,
        new_artifacts: Artifacts,
    ) -> None:
        set_kwargs, map_kwargs = self.resolve_kwargs(
            kwargs=self.kwargs,
            new_artifacts=new_artifacts,
            old_artifacts=old_artifacts,
        )
        synth = context.add_synth(
            add_action=self.add_action,
            synthdef=self.resolve_synthdef(
                address=self.synthdef,
                new_artifacts=new_artifacts,
                old_artifacts=old_artifacts,
            ),
            target_node=self.resolve_node(
                address=self.target_node,
                context=context,
                new_artifacts=new_artifacts,
                old_artifacts=old_artifacts,
            ),
            permanent=False,
            **set_kwargs,
            **map_kwargs,
        )
        new_artifacts.nodes[self.address] = synth
        self.component._artifacts.nodes[self.name] = synth

    def destroy(self, context: AsyncServer, old_artifacts: Artifacts) -> None:
        synth = old_artifacts.nodes.pop(self.address)
        self.component._artifacts.nodes.pop(self.name)
        if self.destroy_strategy:
            synth.set(gate=0, done_action=self.destroy_strategy)

    def mutate(
        self,
        context: AsyncServer,
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
                    context=context,
                    new_artifacts=new_artifacts,
                    old_artifacts=old_artifacts,
                ),
            )
        if self.kwargs != old_spec.kwargs:
            set_kwargs, map_kwargs = self.resolve_kwargs(
                kwargs=self.kwargs,
                new_artifacts=new_artifacts,
                old_artifacts=old_artifacts,
            )
            if map_kwargs:
                old_artifacts.nodes[self.address].map(**map_kwargs)
            if set_kwargs:
                old_artifacts.nodes[self.address].set(**set_kwargs)

    def requires(self) -> list[Address]:
        return [
            *super().requires(),
            self.synthdef,
            *[value for value in self.kwargs.values() if isinstance(value, Address)],
        ]

    def requires_recreation(self, old_spec: "Spec") -> bool:
        if not isinstance(old_spec, SynthSpec):
            raise ValueError(old_spec)
        if self.context != old_spec.context:
            return True
        elif self.synthdef != old_spec.synthdef:
            return True
        return False
