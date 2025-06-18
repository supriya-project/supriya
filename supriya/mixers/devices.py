from .components import (
    C,
    Component,
)


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
