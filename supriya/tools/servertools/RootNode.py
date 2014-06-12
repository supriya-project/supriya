# -*- encoding: utf-8 -*0
from supriya.tools.servertools.GroupMixin import GroupMixin


class RootNode(GroupMixin):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_children',
        '_server',
        )

    ### INITIALIZER ###

    def __init__(self, server=None):
        from supriya.tools import servertools
        servertools.GroupMixin.__init__(self)
        self._server = server

    ### PUBLIC METHODS ###

    def allocate(self):
        pass

    def free(self):
        pass

    def run(self):
        pass

    ### PUBLIC PROPERTIES ###

    @property
    def node_id(self):
        return 0

    @property
    def server(self):
        return self._server
