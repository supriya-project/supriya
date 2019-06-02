from typing import List, Tuple

from .DawNode import DawNode
from .Note import Note


class Device(DawNode):

    ### PUBLIC METHODS ###

    def delete(self):
        self.parent.remove(self)

    def next_device(self):
        current_device = self
        while current_device.parent is not None:
            device_index = current_device.parent.index(current_device)
            if device_index < len(current_device.parent) - 1:
                return current_device.parent[device_index + 1]
            rack_device = None
            for parent in current_device.parentage[2:]:
                if isinstance(parent, Device):
                    rack_device = parent
                    break
            if rack_device is None:
                return
            current_device = rack_device

    def perform(
        self, moment, start_notes, stop_notes
    ) -> List[Tuple["Device", List[Note], List[Note]]]:
        raise NotImplementedError

    def start(self):
        pass

    def stop(self):
        pass
