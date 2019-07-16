from typing import List, Tuple

from supriya.realtime import Group

from .Device import Device
from .DeviceType import DeviceType
from .Note import Note


class AudioDevice(Device):

    ### INITIALIZER ###

    def __init__(self, *, channel_count=None, name=None):
        Device.__init__(self, channel_count=channel_count, name=name)
        self._node = Group(name=name or "audio device")

    ### PUBLIC METHODS ###

    def perform(
        self, moment, start_notes, stop_notes
    ) -> List[Tuple["Device", List[Note], List[Note]]]:
        return []

    ### PRIVATE PROPERTIES ###

    @property
    def _device_type(self):
        return DeviceType.AUDIO
