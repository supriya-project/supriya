from typing import Literal

from ..contexts import BusGroup
from ..enums import AddAction, DoneAction
from ..ugens.system import (
    build_channel_strip_synthdef,
    build_meters_synthdef,
    build_patch_cable_synthdef,
    build_zero_synthdef,
)
from .components import (
    ChannelSettable,
    Component,
    Deletable,
    LevelsCheckable,
    Movable,
    NameSettable,
)
from .constants import Address, Entities, Names, PatchMode
from .devices import DeviceBase, DeviceContainer
from .parameters import FloatField
from .specs import Spec, SpecFactory


class Rack(DeviceBase, ChannelSettable):
    """
    A device rack.
    """

    # TODO: Can we ensure that we don't over-allocate buses?
    #       Can we find some optimization to ensure that, when parallelization
    #       is no concern, buses are re-used?

    # track:2ch, 0 chains, read:ignore, rack:2ch
    # track:2ch, 0 chains, read:ignore, rack:4ch
    # track:2ch, 0 chains, read:replac, rack:2ch
    # track:2ch, 0 chains, read:replac, rack:4ch
    #     nothing

    # track:2ch, 1 chains, read:ignore, rack:2ch
    # track:2ch, 1 chains, read:ignore, rack:4ch
    #     rack w/ main bus
    #     chain zeroes rack:main
    #     chain uses rack:main

    # track:2ch, 1 chains, read:replac, rack:2ch
    # track:2ch, 1 chains, read:replac, rack:4ch
    #     rack w/ main bus
    #     chain inputs patch:replace track:main to rack:main
    #     rack outputs rack:main to track:main

    # track:2ch, 2 chains, read:ignore, rack:2ch
    # track:2ch, 2 chains, read:ignore, rack:4ch
    #     rack w/ main and aux buses
    #     chains zero rack:aux
    #     chains output patch:sum rack:aux to rack:main
    #     rack outputs rack:main to track:main

    # track:2ch, 2 chains, read:replac, rack:2ch
    # track:2ch, 2 chains, read:replac, rack:4ch
    #     rack w/ main and aux bus
    #     chains input patch:replace track:main to rack:aux
    #     chains output patch:sum rack:aux to rack:main
    #     rack outputs rack:main to track:main

    # N.B. swap rack:aux for rack:main above..
    #      chain need to use rack main so that device parent's main matches
    #      and then they can sum to aux

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
            field=FloatField(default=1.0, minimum=0.0, maximum=1.0),
            has_bus=True,
            name=Names.MIX,
        )
        self._read_mode = read_mode
        self._write_mode = write_mode

    def _add_chain(self, name: str | None = None) -> "Chain":
        self._chains.append(
            chain := Chain(
                id_=self._ensure_session()._get_next_id(),
                name=name or f"Chain {len(self._chains) + 1}",
                parent=self,
            )
        )
        return chain

    def _resolve_specs(self, spec_factory: SpecFactory) -> SpecFactory:
        # TODO: Can we re-use a shared aux bus?
        #       E.g. multiple racks in serial with the same channel-count
        #       should be able to re-use the same aux audio bus?
        # cache
        parent = self._ensure_parent()
        parent_effective_channel_count = parent.effective_channel_count
        effective_channel_count = self.effective_channel_count
        # parameters
        for parameter in self.parameters.values():
            parameter._resolve_specs(spec_factory)
        # audio buses
        _ = spec_factory.add_audio_bus(
            channel_count=effective_channel_count,
            name=Names.MAIN,
        )
        mix_audio_bus_address = spec_factory.add_audio_bus(
            channel_count=effective_channel_count,
            name=Names.MIX,
        )
        # groups
        container_group_address = spec_factory.add_container_group(
            destroy_strategy={"gate": 0},
            parent=parent,
            parent_container=parent.devices,
            parent_container_group_name=Names.DEVICES,
        )
        chains_group_address = spec_factory.add_group(
            add_action=AddAction.ADD_TO_HEAD,
            name=Names.CHAINS,
            target_node=container_group_address,
        )
        # output
        # TODO: Reimplement replace and mix in terms of XOut only where
        #       releasing means multiplying the crossfade parameter of the
        #       XOut with the gate envelope, and the gate envelope does not
        #       multiply the source.
        write_synthdef_address = spec_factory.add_synthdef(
            synthdef=build_patch_cable_synthdef(
                source_channel_count=parent_effective_channel_count,
                target_channel_count=effective_channel_count,
                write_mode=(
                    self._write_mode
                    if self._write_mode
                    in (PatchMode.MIX, PatchMode.REPLACE, PatchMode.SUM)
                    else PatchMode.MIX
                ),
            )
        )
        spec_factory.add_synth(
            add_action=AddAction.ADD_AFTER,
            destroy_strategy=dict(
                done_action=DoneAction.FREE_SYNTH_AND_ENCLOSING_GROUP
            ),
            kwargs=dict(
                active=False
                if self._write_mode == PatchMode.IGNORE
                else bool(self._chains),
                in_=mix_audio_bus_address,
                out=parent._get_main_bus_address(),
                **(
                    dict(mix=Spec.get_address(self, Entities.CONTROL_BUSES, Names.MIX))
                    if self._write_mode == PatchMode.MIX
                    else {}
                ),
            ),
            name=Names.OUTPUT,
            synthdef=write_synthdef_address,
            target_node=chains_group_address,
        )
        # levels
        levels_control_bus_address = spec_factory.add_control_bus(
            channel_count=effective_channel_count,
            default=0.0,
            name=Names.OUTPUT_LEVELS,
        )
        meters_synthdef_address = spec_factory.add_synthdef(
            synthdef=build_meters_synthdef(parent_effective_channel_count)
        )
        spec_factory.add_synth(
            add_action=AddAction.ADD_TO_TAIL,
            kwargs=dict(
                in_=parent._get_main_bus_address(),
                out=levels_control_bus_address,
            ),
            name=Names.OUTPUT_LEVELS,
            synthdef=meters_synthdef_address,
            target_node=container_group_address,
        )
        return spec_factory

    def _ungroup(self) -> list[DeviceBase]:
        parent = self._ensure_parent()
        if len(self.chains) > 1:
            raise RuntimeError
        index = parent.devices.index(self)
        if self.chains:
            devices = self.chains[0].devices[:]
        else:
            devices = []
        parent._devices[index + 1 : index + 1] = devices
        for device in devices:
            device._parent = parent
        if self.chains:
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
        Get the rack's child components.
        """
        return [*self._chains]

    @property
    def read_mode(self) -> PatchMode:
        """
        Get the rack's read mode.
        """
        return self._read_mode

    @property
    def write_mode(self) -> PatchMode:
        """
        Get the rack's write mode.
        """
        return self._write_mode


class Chain(DeviceContainer[Rack], Deletable, LevelsCheckable, Movable, NameSettable):
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
        self._add_parameter(
            field=FloatField(),
            has_bus=True,
            name=Names.GAIN,
        )
        self._cached_parent: Rack | None = None

    def _disconnect_parentage(self) -> None:
        self._ensure_parent()._chains.remove(self)

    def _get_main_bus_address(self) -> Address:
        # TODO: We may want to just pre-allocated :shrug: because changing
        #       chain count will have odd interactions with held notes in
        #       instruments.
        return Spec.get_address(
            self._ensure_parent(),
            Entities.AUDIO_BUSES,
            Names.MAIN,
        )

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

    def _reconcile_connections(
        self,
        *,
        deleting: bool = False,
        roots: list[Component] | None = None,
    ) -> tuple[set[Component], set[Component]]:
        related, deleted = super()._reconcile_connections(
            deleting=deleting,
            roots=roots,
        )
        old_parent = self._cached_parent
        self._cached_parent = new_parent = self._ensure_parent()
        if old_parent:
            related.add(old_parent)
        if new_parent:
            related.add(new_parent)
        return related, deleted

    def _resolve_specs(self, spec_factory: SpecFactory) -> SpecFactory:
        # cache
        effective_channel_count = self.effective_channel_count
        rack = self._ensure_parent()
        rack_container = rack._ensure_parent()
        # parameters
        for parameter in self.parameters.values():
            parameter._resolve_specs(spec_factory)
        # synthdefs
        channel_strip_synthdef_address = spec_factory.add_synthdef(
            synthdef=build_channel_strip_synthdef(effective_channel_count)
        )
        meters_synthdef_address = spec_factory.add_synthdef(
            synthdef=build_meters_synthdef(effective_channel_count)
        )
        # control buses
        active_control_bus_address = spec_factory.add_control_bus(
            channel_count=1,
            default=float(self._is_active),
            name=Names.ACTIVE,
        )
        input_levels_control_bus_address = spec_factory.add_control_bus(
            channel_count=effective_channel_count,
            default=0.0,
            name=Names.INPUT_LEVELS,
        )
        output_levels_control_bus_address = spec_factory.add_control_bus(
            channel_count=effective_channel_count,
            default=0.0,
            name=Names.OUTPUT_LEVELS,
        )
        # audio buses
        rack_main_bus_address = self._get_main_bus_address()
        rack_container_main_bus_address = rack_container._get_main_bus_address()
        # groups
        container_group_address = spec_factory.add_container_group(
            destroy_strategy={"gate": 0},
            parent=rack,
            parent_container=rack.chains,
            parent_container_group_name=Names.CHAINS,
        )
        devices_group_address = spec_factory.add_group(
            add_action=AddAction.ADD_TO_TAIL,
            name=Names.DEVICES,
            target_node=container_group_address,
        )
        # synths: input
        input_kwargs: dict[str, str | BusGroup | float] = dict(
            out=rack_main_bus_address,
        )
        if rack._read_mode == PatchMode.IGNORE:
            input_synthdef_address = spec_factory.add_synthdef(
                synthdef=build_zero_synthdef(
                    channel_count=effective_channel_count,
                )
            )
        else:
            input_synthdef_address = spec_factory.add_synthdef(
                synthdef=build_patch_cable_synthdef(
                    source_channel_count=rack_container.effective_channel_count,
                    target_channel_count=effective_channel_count,
                    write_mode="replace",
                )
            )
            input_kwargs["in_"] = rack_container_main_bus_address
        input_synth_address = spec_factory.add_synth(
            add_action=AddAction.ADD_TO_HEAD,
            kwargs=input_kwargs,
            name=Names.INPUT,
            synthdef=input_synthdef_address,
            target_node=container_group_address,
        )
        # synths: input levels
        spec_factory.add_synth(
            add_action=AddAction.ADD_AFTER,
            kwargs=dict(
                in_=rack_main_bus_address,
                out=input_levels_control_bus_address,
            ),
            name=Names.INPUT_LEVELS,
            synthdef=meters_synthdef_address,
            target_node=input_synth_address,
        )
        # synths: channel strip
        channel_strip_synth_address = spec_factory.add_synth(
            add_action=AddAction.ADD_AFTER,
            destroy_strategy=dict(
                done_action=DoneAction.FREE_SYNTH_AND_ENCLOSING_GROUP
            ),
            kwargs=dict(
                active=active_control_bus_address,
                gain=Spec.get_address(self, Entities.CONTROL_BUSES, Names.GAIN),
                out=rack_main_bus_address,
            ),
            name=Names.CHANNEL_STRIP,
            synthdef=channel_strip_synthdef_address,
            target_node=devices_group_address,
        )
        # synths: output levels
        spec_factory.add_synth(
            add_action=AddAction.ADD_AFTER,
            kwargs=dict(
                in_=rack_main_bus_address,
                out=output_levels_control_bus_address,
            ),
            name=Names.OUTPUT_LEVELS,
            synthdef=meters_synthdef_address,
            target_node=channel_strip_synth_address,
        )
        # synths: output
        output_synthdef_address = spec_factory.add_synthdef(
            synthdef=build_patch_cable_synthdef(
                source_channel_count=effective_channel_count,
                target_channel_count=effective_channel_count,
            )
        )
        spec_factory.add_synth(
            add_action=AddAction.ADD_AFTER,
            kwargs=dict(
                in_=rack_main_bus_address,
                out=Spec.get_address(rack, Entities.AUDIO_BUSES, Names.MIX),
            ),
            name=Names.OUTPUT,
            synthdef=output_synthdef_address,
            target_node=channel_strip_synth_address,
        )
        return spec_factory

    @property
    def children(self) -> list[Component]:
        """
        Get the chain's child components.
        """
        return [*self._devices]
