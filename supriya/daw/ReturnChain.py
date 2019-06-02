from supriya.realtime import BusGroup

from .AudioChain import AudioChain
from .ChainReceive import ChainReceive


class ReturnChain(AudioChain):

    ### INITIALIZER ###

    def __init__(self):
        AudioChain.__init__(self)
        self._input_bus_group = BusGroup.audio(channel_count=2)
        self._receive = ChainReceive()
        self._mutate([self.receive, self.devices, self.sends])

    ### PUBLIC PROPERTIES ###

    @property
    def bus_group(self):
        return self._bus_group

    @property
    def channel_count(self):
        return len(self._bus_group)

    @property
    def receive(self):
        return self._receive
