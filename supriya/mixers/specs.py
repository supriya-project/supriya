import dataclasses
from collections import ChainMap
from typing import TypeAlias

from ..contexts import AsyncServer, Buffer, BusGroup, Node
from ..enums import AddAction, CalculationRate
from ..ugens import SynthDef

Address: TypeAlias = str


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
    address: Address
    context: AsyncServer

    def create(
        self,
        context: AsyncServer,
        old_artifacts: Artifacts,
        new_artifacts: Artifacts,
    ) -> None:
        raise NotImplementedError

    def destroy(self, context: AsyncServer, old_artifacts: Artifacts) -> None:
        raise NotImplementedError

    def mutate(
        self,
        context: AsyncServer,
        old_artifacts: Artifacts,
        new_artifacts: Artifacts,
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
        kwargs: dict[str, Address | float],
        new_artifacts: Artifacts,
        old_artifacts: Artifacts,
    ) -> tuple[dict[str, float], dict[str, str]]:
        map_kwargs: dict[str, str] = {}
        set_kwargs: dict[str, float] = {}
        for key, value in kwargs.items():
            if isinstance(value, float):
                set_kwargs[key] = value
            else:
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
        old_artifacts.buffers[self.address].free()

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


@dataclasses.dataclass
class BusSpec(Spec):
    calculation_rate: CalculationRate
    channel_count: int

    def create(
        self,
        context: AsyncServer,
        old_artifacts: Artifacts,
        new_artifacts: Artifacts,
    ) -> None:
        if self.calculation_rate == CalculationRate.AUDIO:
            new_artifacts.audio_buses[self.address] = context.add_bus_group(
                calculation_rate=CalculationRate.AUDIO,
                count=self.channel_count,
            )
        elif self.calculation_rate == CalculationRate.CONTROL:
            new_artifacts.control_buses[self.address] = context.add_bus_group(
                calculation_rate=CalculationRate.AUDIO,
                count=self.channel_count,
            )
        else:
            raise ValueError

    def destroy(self, context: AsyncServer, old_artifacts: Artifacts) -> None:
        if self.calculation_rate == CalculationRate.AUDIO:
            old_artifacts.audio_buses.pop(self.address).free()
        elif self.calculation_rate == CalculationRate.CONTROL:
            old_artifacts.control_buses.pop(self.address).free()

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


@dataclasses.dataclass
class NodeSpec(Spec):
    add_action: AddAction
    target_node: Address | None

    def requires(self) -> list[Address]:
        if self.target_node is not None:
            return [self.target_node]
        return []


@dataclasses.dataclass
class GroupSpec(NodeSpec):

    def create(
        self,
        context: AsyncServer,
        old_artifacts: Artifacts,
        new_artifacts: Artifacts,
    ) -> None:
        new_artifacts.nodes[self.address] = context.add_group(
            add_action=self.add_action,
            target_node=self.resolve_node(
                address=self.target_node,
                context=context,
                new_artifacts=new_artifacts,
                old_artifacts=old_artifacts,
            ),
        )

    def destroy(self, context: AsyncServer, old_artifacts: Artifacts) -> None:
        old_artifacts.nodes[self.address].free()

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
    kwargs: dict[str, Address | float]
    synthdef: Address

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
        new_artifacts.nodes[self.address] = context.add_synth(
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

    def destroy(self, context: AsyncServer, old_artifacts: Artifacts) -> None:
        old_artifacts.nodes[self.address].free()

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
