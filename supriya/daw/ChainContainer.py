from supriya.realtime import Group

from .DawContainer import DawContainer


class ChainContainer(DawContainer):

    ### INITIALIZER ###

    def __init__(self, chain_class, *, name=None):
        DawContainer.__init__(self)
        self._chain_class = chain_class
        self._node = Group(name=name or "chain container")

    ### PRIVATE PROPERTIES ###

    @property
    def _node_class(self):
        return self._chain_class
