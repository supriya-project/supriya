from supriya.realtime import Group

from .Device import Device
from .DeviceType import DeviceType


class Instrument(Device):

    ### INITIALIZER ###

    def __init__(self, channel_count=None, name=None):
        Device.__init__(self, channel_count=channel_count, name=name)
        self._node = Group(name=name or "instrument")

    ### PRIVATE PROPERTIES ###

    @property
    def _device_type(self):
        return DeviceType.INSTRUMENT
