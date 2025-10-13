from typing import Literal

from ..enums import AddAction, DoneAction
from ..ugens.system import (
    build_channel_strip_synthdef,
    build_meters_synthdef,
    build_patch_cable_synthdef,
)
from .components import ChannelSettable, Component, Deletable, Movable, NameSettable
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

    def _resolve_specs(self, spec_factory: SpecFactory) -> SpecFactory:
        # TODO: Can we re-use a shared aux bus?
        #       E.g. multiple racks in serial with the same channel-count
        #       should be able to re-use the same aux audio bus?
        if not self.chains:
            return spec_factory
        parent = self._ensure_parent()
        parent_effective_channel_count = parent.effective_channel_count
        effective_channel_count = self.effective_channel_count
        main_audio_bus_address = spec_factory.add_audio_bus(
            channel_count=effective_channel_count,
            name=Names.MAIN,
        )
        if len(self.chains) > 1:
            _ = spec_factory.add_audio_bus(
                channel_count=effective_channel_count,
                name=Names.AUX,
            )
        container_group_address = spec_factory.add_container_group(
            destroy_strategy={"gate": 0},
            parent=(parent := self._ensure_parent()),
            parent_container=parent.devices,
            parent_container_group_name=Names.DEVICES,
        )
        _ = spec_factory.add_group(
            add_action=AddAction.ADD_TO_HEAD,
            name=Names.CHAINS,
            target_node=container_group_address,
        )
        # input
        if self._read_mode == PatchMode.REPLACE:
            read_synthdef_address = spec_factory.add_synthdef(
                synthdef=build_patch_cable_synthdef(
                    source_channel_count=parent_effective_channel_count,
                    target_channel_count=effective_channel_count,
                    write_mode="replace",
                )
            )
            spec_factory.add_synth(
                add_action=AddAction.ADD_TO_HEAD,
                destroy_strategy=dict(
                    done_action=DoneAction.FREE_SYNTH_AND_ENCLOSING_GROUP
                ),
                kwargs=dict(
                    in_=parent._get_main_bus_address(),
                    out=main_audio_bus_address,
                ),
                name=Names.INPUT,
                synthdef=read_synthdef_address,
                target_node=container_group_address,
            )
        # output
        if self._write_mode in (PatchMode.MIX, PatchMode.REPLACE, PatchMode.SUM):
            write_synthdef_address = spec_factory.add_synthdef(
                synthdef=build_patch_cable_synthdef(
                    source_channel_count=parent_effective_channel_count,
                    target_channel_count=effective_channel_count,
                    write_mode=self._write_mode,
                )
            )
            spec_factory.add_synth(
                add_action=AddAction.ADD_TO_TAIL,
                destroy_strategy=dict(
                    done_action=DoneAction.FREE_SYNTH_AND_ENCLOSING_GROUP
                ),
                kwargs=dict(
                    in_=main_audio_bus_address,
                    out=parent._get_main_bus_address(),
                    **(
                        dict(
                            mix=Spec.get_address(
                                self, Entities.CONTROL_BUSES, Names.MIX
                            )
                        )
                        if self._write_mode == PatchMode.MIX
                        else {}
                    ),
                ),
                name=Names.OUTPUT,
                synthdef=write_synthdef_address,
                target_node=container_group_address,
            )
        if parent._devices.index(self) < (len(parent._devices) - 1):
            # will the meters synth follow the group on move?
            # we're referencing the output node, but does it even exist?
            levels_control_bus_address = spec_factory.add_control_bus(
                channel_count=self.effective_channel_count,
                default=0.0,
                name=Names.LEVELS,
            )
            meters_synthdef_address = spec_factory.add_synthdef(
                synthdef=build_meters_synthdef(parent_effective_channel_count)
            )
            spec_factory.add_synth(
                add_action=AddAction.ADD_AFTER,
                kwargs=dict(
                    in_=parent._get_main_bus_address(),
                    out=levels_control_bus_address,
                ),
                name=Names.LEVELS,
                synthdef=meters_synthdef_address,
                target_node=Spec.get_address(self, Entities.NODES, Names.OUTPUT),
            )
        return spec_factory

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

    def _get_main_bus_address(self) -> Address:
        # TODO: We may want to just pre-allocated :shrug: because changing
        #       chain count will have odd interactions with held notes in
        #       instruments.
        return Spec.get_address(
            parent := self._ensure_parent(),
            Entities.AUDIO_BUSES,
            Names.AUX if len(parent.chains) > 1 else Names.MAIN,
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

    def _resolve_specs(self, spec_factory: SpecFactory) -> SpecFactory:
        for parameter in self.parameters.values():
            parameter._resolve_specs(spec_factory)
        # TODO: Re-use the rack's main bus.
        #       Don't allocate fresh.
        spec_factory.add_control_bus(
            channel_count=1,
            default=float(self._is_active),
            name=Names.ACTIVE,
        )
        # TODO: Do we even need input levels?
        spec_factory.add_control_bus(
            channel_count=self.effective_channel_count,
            default=0.0,
            name=Names.INPUT_LEVELS,
        )
        # TODO: Don't we need a meters synthdef?
        spec_factory.add_control_bus(
            channel_count=self.effective_channel_count,
            default=0.0,
            name=Names.OUTPUT_LEVELS,
        )
        container_group_address = spec_factory.add_container_group(
            destroy_strategy={"gate": 0},
            parent=(parent := self._ensure_parent()),
            parent_container=parent.chains,
            parent_container_group_name=Names.CHAINS,
        )
        _ = spec_factory.add_group(
            add_action=AddAction.ADD_TO_TAIL,
            name=Names.DEVICES,
            target_node=container_group_address,
        )
        channel_strip_synthdef_address = spec_factory.add_synthdef(
            synthdef=build_channel_strip_synthdef(self.effective_channel_count)
        )
        spec_factory.add_synth(
            add_action=AddAction.ADD_TO_TAIL,
            destroy_strategy=dict(
                done_action=DoneAction.FREE_SYNTH_AND_ENCLOSING_GROUP
            ),
            kwargs=dict(
                active=Spec.get_address(self, Entities.CONTROL_BUSES, Names.ACTIVE),
                gain=Spec.get_address(self, Entities.CONTROL_BUSES, Names.GAIN),
                out=Spec.get_address(parent, Entities.AUDIO_BUSES, Names.MAIN),
            ),
            name=Names.CHANNEL_STRIP,
            synthdef=channel_strip_synthdef_address,
            target_node=container_group_address,
        )
        return spec_factory

    @property
    def children(self) -> list[Component]:
        """
        Get the chain's child components.
        """
        return [*self._devices]
