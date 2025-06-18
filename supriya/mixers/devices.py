from ..contexts import AsyncServer
from ..enums import AddAction, DoneAction
from .components import C, Component
from .constants import Address, Names
from .specs import GroupSpec, Spec, SynthDefSpec, SynthSpec
from .synthdefs import build_device_dc_tester


class DeviceContainer(Component[C]):
    def __init__(self) -> None:
        self._devices: list[Device] = []

    def _add_device(self, name: str | None = None) -> "Device":
        if (session := self.session) is None:
            raise RuntimeError
        self._devices.append(
            device := Device(id_=session._get_next_id(), name=name, parent=self)
        )
        return device

    async def add_device(self, name: str | None = None) -> "Device":
        async with self._lock:
            device = self._add_device(name=name)
            if context := self._can_allocate():
                await device._reconcile(context=context)
            else:
                device._reconcile_connections()
            return device

    @property
    def devices(self) -> list["Device"]:
        return self._devices[:]


class Device(Component[DeviceContainer]):
    def __init__(
        self,
        *,
        id_: int,
        name: str | None = None,
        parent: DeviceContainer | None = None,
    ) -> None:
        Component.__init__(self, id_=id_, name=name, parent=parent)

    def _resolve_specs(self, context: AsyncServer | None) -> list[Spec]:
        if not self.parent:
            raise RuntimeError
        if not context:
            return []
        synthdef = build_device_dc_tester(self.effective_channel_count)
        return [
            SynthDefSpec(
                component=self,
                context=context,
                name=synthdef.effective_name,
                synthdef=synthdef,
            ),
            GroupSpec(
                add_action=AddAction.ADD_TO_TAIL,
                component=self,
                context=context,
                destroy_strategy={"gate": 0},
                name=Names.GROUP,
                # TODO: Need more advanced logic here for positioning
                target_node=Spec.get_address(self.parent, Names.NODES, Names.DEVICES),
            ),
            SynthSpec(
                add_action=AddAction.ADD_TO_TAIL,
                component=self,
                context=context,
                destroy_strategy={"done_action": DoneAction.FREE_SYNTH},
                kwargs={
                    "out": Spec.get_address(
                        self.parent,
                        Names.AUDIO_BUSSES,
                        Names.MAIN,
                    )
                },
                name=Names.SYNTH,
                synthdef=Spec.get_address(
                    None,
                    Names.SYNTHDEFS,
                    synthdef.effective_name,
                ),
                target_node=Spec.get_address(self, Names.NODES, Names.GROUP),
            ),
        ]

    @property
    def address(self) -> Address:
        if self.parent is None:
            return "devices[?]"
        index = self.parent.devices.index(self)
        return f"{self.parent.address}.devices[{index}]"

    @property
    def numeric_address(self) -> Address:
        return f"devices[{self._id}]"
