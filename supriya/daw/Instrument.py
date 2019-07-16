from typing import List, Tuple

from supriya.realtime import Group

from .Device import Device
from .DeviceType import DeviceType
from .Note import Note


class Instrument(Device):

    ### INITIALIZER ###

    def __init__(self):
        Device.__init__(self)
        self._node = Group(name="instrument")

    ### PRIVATE PROPERTIES ###

    @property
    def _device_type(self):
        return DeviceType.INSTRUMENT

    ### PUBLIC METHODS ###

    def perform(
        self, moment, start_notes, stop_notes
    ) -> List[Tuple["Device", List[Note], List[Note]]]:
        return []
