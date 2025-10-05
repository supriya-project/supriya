from typing import Literal

from ..contexts import AsyncServer
from ..enums import AddAction, CalculationRate, DoneAction
from ..ugens.system import build_channel_strip_synthdef
from .components import ChannelSettable, Component, Deletable, Movable, NameSettable
from .constants import Address, Names, PatchMode
from .devices import DeviceBase, DeviceContainer
from .parameters import FloatField
from .specs import BusSpec, GroupSpec, Spec, Specs, SynthDefSpec, SynthSpec


class Rack(DeviceBase, ChannelSettable):
    """
    A device rack.
    """

    # TODO: Rack and Device aren't really similar, so fix inheritance with a
    #       shared base? Or maybe we just support union types for
    #       DeviceContainer children.

    # TODO: How to define how racks sum/replace with their parent's audio?
    #       Should they have a mix parameter e.g. XOut?
    #       Or a parameter to mix vs replace vs sum?
    #       Yes to the latter, because mixing is different from summing.
    #       But this will require extending patch-cable logic

    # TODO: How to define how rack's read their parent's audio, or don't?

    # TODO: Can we ensure that we don't over-allocate buses?
    #       Can we find some optimization to ensure that, when parallelization
    #       is no concern, buses are re-used?

    def __init__(
        self,
        *,
        id_: int,
        name: str | None = None,
        parent: DeviceContainer | None = None,
        read_mode: Literal[PatchMode.IGNORE, PatchMode.REPLACE] = PatchMode.REPLACE,
        write_mode: PatchMode = PatchMode.SUM,
    ) -> None:
        DeviceBase.__init__(self, id_=id_, name=name, parent=parent)
        self._chains: list[Chain] = []
        self._add_parameter(
            name=Names.MIX,
            field=FloatField(default=1.0, has_bus=True, minimum=0.0, maximum=1.0),
        )
        self._read_mode = read_mode
        self._write_mode = write_mode

    def _add_chain(self, name: str | None = None) -> "Chain":
        self._chains.append(
            chain := Chain(
                id_=self._ensure_session()._get_next_id(), name=name, parent=self
            )
        )
        return chain

    def _get_nested_address(self) -> Address:
        if self.parent is None:
            return "devices[?]"
        index = self.parent.devices.index(self)
        return f"{self.parent.address}.devices[{index}]"

    def _get_numeric_address(self) -> Address:
        return f"devices[{self._id}]"

    def _resolve_specs(self, context: AsyncServer | None) -> Specs:
        # TODO: Can we re-use a shared aux bus?
        #       E.g. multiple racks in serial with the same channel-count
        #       should be able to re-use the same aux audio bus?
        specs = Specs()
        if not context:
            return specs
        parent = self._ensure_parent()
        specs.bus_specs.append(
            BusSpec(
                calculation_rate=CalculationRate.AUDIO,
                channel_count=self.effective_channel_count,
                component=self,
                context=context,
                name=Names.MAIN,
            )
        )
        specs.group_specs.extend(
            [
                self._resolve_container_spec(
                    context=context,
                    destroy_strategy={"gate": 0},
                    parent=(parent := self._ensure_parent()),
                    parent_container=parent.devices,
                    parent_container_group_name=Names.DEVICES,
                ),
                GroupSpec(
                    add_action=AddAction.ADD_TO_HEAD,
                    component=self,
                    context=context,
                    name=Names.CHAINS,
                    parent_node=None,
                    target_node=Spec.get_address(self, Names.NODES, Names.GROUP),
                ),
            ]
        )
        return specs

    def _ungroup(self) -> list[DeviceBase]:
        parent = self._ensure_parent()
        if not self.chains:
            raise RuntimeError
        elif len(self.chains) > 1:
            raise RuntimeError
        index = parent.devices.index(self)
        devices = self.chains[0].devices[:]
        parent._devices[index + 1 : index + 1] = devices
        for device in devices:
            device._parent = parent
        self._chains[0]._devices[:] = []
        return devices

    async def add_chain(self, name: str | None = None) -> "Chain":
        """
        Add a new chain to the rack.
        """
        async with (session := self._ensure_session())._lock:
            chain = self._add_chain(name=name)
            await Component._reconcile(
                context=self.context,
                reconciling_components=[chain],
                session=session,
            )
            return chain

    async def set_read_mode(
        self, mode: Literal[PatchMode.IGNORE, PatchMode.REPLACE]
    ) -> None:
        async with (session := self._ensure_session())._lock:
            self._read_mode = mode
            await Component._reconcile(
                context=self.context,
                reconciling_components=[self],
                session=session,
            )

    async def set_write_mode(self, mode: PatchMode) -> None:
        async with (session := self._ensure_session())._lock:
            self._write_mode = mode
            await Component._reconcile(
                context=self.context,
                reconciling_components=[self],
                session=session,
            )

    async def ungroup(self) -> None:
        """
        Ungroup the rack.

        Replace the rack in its parent with the rack's children.

        Only works if the rack contains only one chain.
        """
        async with (session := self._ensure_session())._lock:
            devices = self._ungroup()
            await Component._reconcile(
                context=self.context,
                deleting_components=[self],
                reconciling_components=[self, *devices],
                session=session,
            )

    @property
    def chains(self) -> list["Chain"]:
        """
        Get the rack's chains.
        """
        return self._chains[:]

    @property
    def children(self) -> list[Component]:
        """
        Get the track's child components.
        """
        return [*self._chains]


class Chain(DeviceContainer[Rack], Deletable, Movable, NameSettable):
    """
    A rack chain.
    """

    def __init__(
        self,
        *,
        id_: int,
        name: str | None = None,
        parent: Rack | None = None,
    ) -> None:
        Component.__init__(self, id_=id_, name=name, parent=parent)
        DeviceContainer.__init__(self)
        self._add_parameter(name=Names.GAIN, field=FloatField(has_bus=True))

    def _disconnect_parentage(self) -> None:
        self._ensure_parent()._chains.remove(self)
        super()._disconnect_parentage()

    def _get_nested_address(self) -> Address:
        if self.parent is None:
            return "chains[?]"
        index = self.parent.chains.index(self)
        return f"{self.parent.address}.chains[{index}]"

    def _get_numeric_address(self) -> Address:
        return f"chains[{self._id}]"

    def _move(self, *, new_parent: Rack, index: int) -> None:
        # Validate if moving is possible
        if self.mixer is not new_parent.mixer:
            raise RuntimeError
        elif self in new_parent.parentage:
            raise RuntimeError
        elif index < 0:
            raise RuntimeError
        elif index and index >= len(new_parent.chains):
            raise RuntimeError
        # Reconfigure parentage and bail if this is a no-op
        old_parent = self._ensure_parent()
        old_index = old_parent._chains.index(self)
        if old_parent is new_parent and old_index == index:
            return  # Bail
        old_parent._chains.remove(self)
        self._parent = new_parent
        new_parent._chains.insert(index, self)

    def _resolve_specs(self, context: AsyncServer | None) -> Specs:
        specs = Specs()
        if not context:
            return specs
        channel_strip_synthdef = build_channel_strip_synthdef(
            self.effective_channel_count
        )
        for parameter in self.parameters.values():
            specs.update(parameter._resolve_specs(context=context))
        specs.synthdef_specs.append(
            SynthDefSpec(
                component=self,
                context=context,
                name=channel_strip_synthdef.effective_name,
                synthdef=channel_strip_synthdef,
            ),
        )
        specs.bus_specs.extend(
            [
                BusSpec(
                    calculation_rate=CalculationRate.AUDIO,
                    channel_count=self.effective_channel_count,
                    component=self,
                    context=context,
                    name=Names.MAIN,
                ),
                BusSpec(
                    calculation_rate=CalculationRate.CONTROL,
                    channel_count=1,
                    component=self,
                    context=context,
                    default=float(self._is_active),
                    name=Names.ACTIVE,
                ),
                BusSpec(
                    calculation_rate=CalculationRate.CONTROL,
                    channel_count=self.effective_channel_count,
                    component=self,
                    context=context,
                    default=0.0,
                    name=Names.INPUT_LEVELS,
                ),
                BusSpec(
                    calculation_rate=CalculationRate.CONTROL,
                    channel_count=self.effective_channel_count,
                    component=self,
                    context=context,
                    default=0.0,
                    name=Names.OUTPUT_LEVELS,
                ),
            ]
        )
        specs.group_specs.extend(
            [
                self._resolve_container_spec(
                    context=context,
                    destroy_strategy={"gate": 0},
                    parent=(parent := self._ensure_parent()),
                    parent_container=parent.chains,
                    parent_container_group_name=Names.CHAINS,
                ),
                GroupSpec(
                    add_action=AddAction.ADD_TO_TAIL,
                    component=self,
                    context=context,
                    name=Names.DEVICES,
                    parent_node=None,
                    target_node=Spec.get_address(self, Names.NODES, Names.GROUP),
                ),
            ]
        )
        specs.synth_specs.extend(
            [
                SynthSpec(
                    add_action=AddAction.ADD_TO_TAIL,
                    component=self,
                    context=context,
                    destroy_strategy={
                        "done_action": DoneAction.FREE_SYNTH_AND_ENCLOSING_GROUP
                    },
                    kwargs={
                        "active": Spec.get_address(
                            self, Names.CONTROL_BUSES, Names.ACTIVE
                        ),
                        "gain": Spec.get_address(self, Names.CONTROL_BUSES, Names.GAIN),
                        "out": Spec.get_address(self, Names.AUDIO_BUSES, Names.MAIN),
                    },
                    name=Names.CHANNEL_STRIP,
                    parent_node=None,
                    synthdef=Spec.get_address(
                        None, Names.SYNTHDEFS, channel_strip_synthdef.effective_name
                    ),
                    target_node=Spec.get_address(self, Names.NODES, Names.GROUP),
                ),
            ]
        )
        return specs

    @property
    def children(self) -> list[Component]:
        """
        Get the chain's child components.
        """
        return [*self._devices]
