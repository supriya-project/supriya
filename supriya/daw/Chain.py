import abc
from typing import Tuple

from uqbar.containers import UniqueTreeTuple

from .DawNode import DawNode
from .DeviceContainer import DeviceContainer
from .DeviceType import DeviceType


class Chain(DawNode, UniqueTreeTuple):

    ### INITIALIZER ###

    def __init__(self):
        self._node = None
        DawNode.__init__(self)
        self._devices = DeviceContainer(device_types=self.device_types)
        UniqueTreeTuple.__init__(self, children=[self.devices])

    ### PUBLIC METHODS ###

    def delete(self):
        self.parent.remove(self)

    ### PUBLIC PROPERTIES ###

    @property
    def default_send_target(self):
        return self.mixer_context

    @property
    def devices(self) -> DeviceContainer:
        return self._devices

    @property
    @abc.abstractmethod
    def device_types(self) -> Tuple[DeviceType, ...]:
        raise NotImplementedError
