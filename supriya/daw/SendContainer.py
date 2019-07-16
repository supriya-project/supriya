from supriya.realtime import Group

from .DawContainer import DawContainer
from .Send import Send


class SendContainer(DawContainer):

    ### INITIALIZER ###

    def __init__(self, name=None):
        DawContainer.__init__(self)
        self._pre_fader_group = Group(name="pre-fader sends")
        self._post_fader_group = Group(name="post-fader sends")

    ### PRIVATE PROPERTIES ###

    @property
    def _node_class(self):
        return Send

    ### PUBLIC PROPERTIES ###

    @property
    def post_fader_group(self):
        return self._post_fader_group

    @property
    def pre_fader_group(self):
        return self._pre_fader_group
