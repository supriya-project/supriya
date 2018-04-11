from supriya.realtime.Group import Group


class RootNode(Group):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Server Internals'

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, server=None):
        import supriya.realtime
        supriya.realtime.Group.__init__(self)
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
    def parent(self):
        return None
