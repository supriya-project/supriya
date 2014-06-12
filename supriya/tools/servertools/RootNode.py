# -*- encoding: utf-8 -*0
from supriya.tools.servertools.Group import Group


class RootNode(Group):

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self):
        from supriya.tools import servertools
        servertools.Node.__init__(self)
        self._is_playing = True
        self._is_running = True
        self._node_id = 0
        self._parent = self

    ### PUBLIC METHODS ###

    def allocate(self):
        pass

    def free(self):
        pass

    def run(self):
        pass
