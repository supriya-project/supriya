from supriya.realtime import Group

from .Device import Device
from .DeviceType import DeviceType


class MidiDevice(Device):
    def __init__(self, name=None):
        Device.__init__(self)
        self._node = Group(name=name or "midi device")

    ### PRIVATE PROPERTIES ###

    @property
    def _device_type(self):
        return DeviceType.MIDI
