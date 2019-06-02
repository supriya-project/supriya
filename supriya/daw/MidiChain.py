from typing import Tuple

from .Chain import Chain
from .DeviceType import DeviceType


class MidiChain(Chain):

    ### PUBLIC PROPERTIES ###

    @property
    def device_types(self) -> Tuple[DeviceType, ...]:
        return (DeviceType.MIDI,)
