from typing import Type

from ..contexts import AsyncServer
from ..enums import AddAction, DoneAction
from ..ugens import (
    DC,
    Linen,
    Out,
    SynthDef,
    SynthDefBuilder,
    system,
)
from .components import C, Component
from .constants import Address, ChannelCount, Names
from .specs import GroupSpec, Spec, SynthDefSpec, SynthSpec


class DeviceContainer(Component[C]):
    """
    A container for device components.

    Supports adding devices and grouping them.
    """

    def __init__(self) -> None:
        self._devices: list[Device] = []

    def _add_device(
        self, device_class: Type["Device"], name: str | None = None
    ) -> "Device":
        self._devices.append(
            device := device_class(
                id_=self._ensure_session()._get_next_id(), name=name, parent=self
            )
        )
        return device

    # TODO: add_effect(
    #           effect_synthdefs: ...,
    #           parameters: ...,
    #           mappings: ...,
    #           sidechains: ...,
    #       ) -> Effect:

    # TODO: add_instrument(
    #           voice_synthdefs: ...,
    #           effect_synthdefs: ...,
    #           parameters: ...,
    #           mappings: ...,
    #           sidechains: ...,
    #           polyphony: ...,
    #       ) -> Instrument:

    async def add_device(
        self, device_class: Type["Device"], name: str | None = None
    ) -> "Device":
        """
        Add a new device to the device container.
        """
        async with (session := self._ensure_session())._lock:
            device = self._add_device(device_class=device_class, name=name)
            await Component._reconcile(
                context=self.context,
                reconciling_components=[device],
                session=session,
            )
            return device

    @property
    def devices(self) -> list["Device"]:
        """
        Get the device container's devices.
        """
        return self._devices[:]


class Device(Component[DeviceContainer]):
    """
    A device component.

    Base class for implementing control devices (e.g. MIDI manipulation), audio
    effects, and instruments.
    """

    def __init__(
        self,
        *,
        id_: int,
        name: str | None = None,
        parent: DeviceContainer | None = None,
    ) -> None:
        Component.__init__(self, id_=id_, name=name, parent=parent)

    def _disconnect_parentage(self) -> None:
        self._ensure_parent()._devices.remove(self)
        super()._disconnect_parentage()

    def _get_nested_address(self) -> Address:
        if self.parent is None:
            return "devices[?]"
        index = self.parent.devices.index(self)
        return f"{self.parent.address}.devices[{index}]"

    def _get_numeric_address(self) -> Address:
        return f"devices[{self._id}]"

    def _move(self, *, new_parent: DeviceContainer, index: int) -> None:
        # Validate if moving is possible
        if self.mixer is not new_parent.mixer:
            raise RuntimeError
        elif self in new_parent.parentage:
            raise RuntimeError
        elif index < 0:
            raise RuntimeError
        elif index and index >= len(new_parent.devices):
            raise RuntimeError
        # Reconfigure parentage and bail if this is a no-op
        old_parent = self._ensure_parent()
        old_index = old_parent._devices.index(self)
        if old_parent is new_parent and old_index == index:
            return  # Bail
        old_parent._devices.remove(self)
        self._parent = new_parent
        new_parent._devices.insert(index, self)

    async def delete(self) -> None:
        """
        Delete the device.
        """
        async with (session := self._ensure_session())._lock:
            await Component._reconcile(
                context=None,
                deleting_components=[self],
                reconciling_components=[self],
                session=session,
            )

    async def move(self, parent: DeviceContainer, index: int) -> None:
        """
        Move the device to another device container and/or index in a device
        container.
        """
        async with (session := self._ensure_session())._lock:
            self._move(new_parent=parent, index=index)
            await Component._reconcile(
                context=self.context,
                reconciling_components=[self],
                session=session,
            )

    def set_name(self, name: str | None = None) -> None:
        """
        Set the devices's name.
        """
        self._name = name


class SignalTesterDevice(Device):
    """
    A device for testing signal routing.
    """

    def _build_synthdef(self, channel_count: ChannelCount = 2) -> SynthDef:
        with SynthDefBuilder(
            active=1,
            dc=1,
            done_action=DoneAction.FREE_SYNTH,
            gate=1,
            out=0,
        ) as builder:
            active_gate = Linen.kr(
                attack_time=system.LAG_TIME,
                gate=builder["active"],
                release_time=system.LAG_TIME,
            )
            free_gate = Linen.kr(
                attack_time=system.LAG_TIME,
                done_action=builder["done_action"],
                gate=builder["gate"],
                release_time=system.LAG_TIME,
            )
            source = DC.ar(source=builder["dc"])
            source *= active_gate * free_gate
            Out.ar(bus=builder["out"], source=[source] * channel_count)
        return builder.build(f"supriya:device-dc-tester:{channel_count}")

    def _resolve_specs(self, context: AsyncServer | None) -> list[Spec]:
        if not context:
            return []
        parent = self._ensure_parent()
        synthdef = self._build_synthdef(self.effective_channel_count)
        device_index: int = parent.devices.index(self)
        if device_index:
            group_add_action: AddAction = AddAction.ADD_AFTER
            group_target: Address = Spec.get_address(
                parent.devices[device_index - 1],
                Names.NODES,
                Names.GROUP,
            )
        else:
            group_add_action = AddAction.ADD_TO_HEAD
            group_target = Spec.get_address(parent, Names.NODES, Names.DEVICES)
        return [
            SynthDefSpec(
                component=self,
                context=context,
                name=synthdef.effective_name,
                synthdef=synthdef,
            ),
            GroupSpec(
                add_action=group_add_action,
                component=self,
                context=context,
                destroy_strategy={"gate": 0},
                name=Names.GROUP,
                parent_node=Spec.get_address(parent, Names.NODES, Names.DEVICES),
                target_node=group_target,
            ),
            SynthSpec(
                add_action=AddAction.ADD_TO_TAIL,
                component=self,
                context=context,
                destroy_strategy={
                    "done_action": DoneAction.FREE_SYNTH_AND_ENCLOSING_GROUP
                },
                kwargs={
                    "out": Spec.get_address(
                        parent,
                        Names.AUDIO_BUSSES,
                        Names.MAIN,
                    )
                },
                name=Names.SYNTH,
                parent_node=None,
                synthdef=Spec.get_address(
                    None,
                    Names.SYNTHDEFS,
                    synthdef.effective_name,
                ),
                target_node=Spec.get_address(self, Names.NODES, Names.GROUP),
            ),
        ]
