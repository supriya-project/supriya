from supriya.realtime import Group

from .DawContainer import DawContainer
from .DirectOut import DirectOut
from .Send import Send


class SendContainer(DawContainer):

    ### INITIALIZER ###

    def __init__(self):
        DawContainer.__init__(self)
        self._node = None
        self._pre_fader_group = Group(name="pre-fader sends")
        self._post_fader_group = Group(name="post-fader sends")

    ### PRIVATE METHODS ###

    def _insertion_hook(self, new_items, start_index, stop_index):
        pass

    ### PRIVATE PROPERTIES ###

    @property
    def _node_class(self):
        return (Send, DirectOut)

    ### PUBLIC PROPERTIES ###

    @property
    def post_fader_group(self):
        return self._post_fader_group

    @property
    def pre_fader_group(self):
        return self._pre_fader_group
