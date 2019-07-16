from typing import List, Tuple

from .Device import Device
from .DeviceType import DeviceType
from .Note import Note


class MidiDevice(Device):

    ### PRIVATE PROPERTIES ###

    @property
    def _device_type(self):
        return DeviceType.MIDI

    ### PUBLIC METHODS ###

    def perform(
        self, moment, start_notes, stop_notes
    ) -> List[Tuple["Device", List[Note], List[Note]]]:
        next_device = self.next_device()
        return [(next_device, start_notes, stop_notes)]
