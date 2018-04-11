from supriya.commands.ResponseCallback import ResponseCallback


class NodeResponseCallback(ResponseCallback):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_server',
        )

    ### INITIALIZER ###

    def __init__(self, server):
        import supriya.commands
        import supriya.realtime
        ResponseCallback.__init__(
            self,
            #address_pattern='/n_(end|go|info|move|off|on|set|setn)',
            procedure=self.__call__,
            prototype=(
                supriya.commands.NodeInfoResponse,
                supriya.commands.NodeSetContiguousResponse,
                supriya.commands.NodeSetResponse,
                ),
            )
        assert isinstance(server, supriya.realtime.Server)
        self._server = server

    ### SPECIAL METHODS ###

    def __call__(self, response):
        node_id = response.node_id
        node = self._server._nodes.get(node_id)
        if node is None:
            return
        node._handle_response(response)

    ### PUBLIC PROPERTIES ###

    @property
    def server(self):
        return self._server
