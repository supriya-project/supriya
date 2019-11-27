from supriya.realtime import Group

from .Device import Device
from .DeviceType import DeviceType


class AudioDevice(Device):

    ### INITIALIZER ###

    def __init__(self, *, channel_count=None, name=None):
        Device.__init__(self, name=name)
        self._node = Group(name=name or "audio device")

    ### PRIVATE PROPERTIES ###

    @property
    def _device_type(self):
        return DeviceType.AUDIO
