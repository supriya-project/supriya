from ..contexts import AsyncServer
from ..enums import AddAction
from ..ugens import SynthDef
from .components import AllocatableComponent, C, ComponentNames
from .synthdefs import build_device_dc_tester


class DeviceContainer(AllocatableComponent[C]):

    def __init__(self) -> None:
        self._devices: list[Device] = []

    def _add_device(self, name: str | None = None) -> "Device":
        self._devices.append(device := Device(name=name, parent=self))
        return device

    async def add_device(self, name: str | None = None) -> "Device":
        async with self._lock:
            device = self._add_device(name=name)
            if context := self._can_allocate():
                await device._allocate_deep(context=context)
            return device

    @property
    def devices(self) -> list["Device"]:
        return self._devices[:]


class Device(AllocatableComponent):

    def _allocate(self, *, context: AsyncServer) -> bool:
        if not super()._allocate(context=context):
            return False
        elif self.parent is None:
            raise RuntimeError
        main_audio_bus = self.parent._get_audio_bus(context, name=ComponentNames.MAIN)
        target_node = self.parent._nodes[ComponentNames.DEVICES]
        with context.at():
            self._nodes[ComponentNames.GROUP] = group = target_node.add_group(
                add_action=AddAction.ADD_TO_TAIL
            )
            self._nodes[ComponentNames.SYNTH] = group.add_synth(
                add_action=AddAction.ADD_TO_TAIL,
                out=main_audio_bus,
                synthdef=build_device_dc_tester(2),
            )
        return True

    def _disconnect_parentage(self) -> None:
        if self._parent is not None:
            self._parent._devices.remove(self)
        super()._disconnect_parentage()

    def _get_synthdefs(self) -> list[SynthDef]:
        return [build_device_dc_tester(2)]

    async def set_active(self, active: bool = True) -> None:
        async with self._lock:
            pass

    def set_name(self, name: str | None = None) -> None:
        self._name = name

    @property
    def address(self) -> str:
        if self.parent is None:
            return "devices[?]"
        index = self.parent.devices.index(self)
        return f"{self.parent.address}.devices[{index}]"
