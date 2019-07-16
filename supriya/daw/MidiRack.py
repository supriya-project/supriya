from uqbar.containers import UniqueTreeTuple

from .ChainContainer import ChainContainer
from .MidiChain import MidiChain
from .RackDevice import RackDevice


class MidiRack(RackDevice):

    ### INITIALIZER ###

    def __init__(self):
        RackDevice.__init__(self)
        self._chains = ChainContainer(chain_class=MidiChain)
        UniqueTreeTuple.__init__(self, children=[self.chains])

    ### PUBLIC PROPERTIES ###

    @property
    def chains(self):
        return self._chains
