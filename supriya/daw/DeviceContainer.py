from supriya.realtime import Group
from supriya.utils import iterate_nwise

from .DawContainer import DawContainer
from .Device import Device
from .DeviceType import DeviceType


class DeviceContainer(DawContainer):

    ### INITIALIZER ###

    def __init__(self, device_types):
        DawContainer.__init__(self)
        self._device_types = tuple(device_types)
        self._node = Group(name="device container")

    ### PRIVATE METHODS ###

    def _validate(self, new_items, old_items, start_index, stop_index):
        for new_item in new_items:
            if new_item._device_type not in self.device_types:
                raise ValueError("Device mismatch")
        devices_to_validate = (
            self[start_index - 1 : start_index]
            + list(new_items)
            + self[stop_index : stop_index + 1]
        )
        for device_one, device_two in iterate_nwise(devices_to_validate):
            if (
                device_one._device_type
                == device_two._device_type
                == DeviceType.INSTRUMENT
            ):
                raise ValueError("Only one instrument device permitted")
            elif device_one._device_type > device_two._device_type:
                raise ValueError("Device mismatch")

    ### PRIVATE PROPERTIES ###

    @property
    def _node_class(self):
        return Device

    ### PUBLIC PROPERTIES ###

    @property
    def device_types(self) -> bool:
        return self._device_types
