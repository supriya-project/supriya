# -*- encoding: utf-8 -*-
from supriya.tools.responsetools.ResponseCallback import ResponseCallback


class NodeResponseCallback(ResponseCallback):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_server',
        )

    ### INITIALIZER ###

    def __init__(self, server):
        from supriya.tools import responsetools
        from supriya.tools import servertools
        ResponseCallback.__init__(
            self,
            #address_pattern='/n_(end|go|info|move|off|on|set|setn)',
            procedure=self.__call__,
            response_prototype=(
                responsetools.NodeInfoResponse,
                responsetools.NodeSetContiguousResponse,
                responsetools.NodeSetResponse,
                ),
            )
        assert isinstance(server, servertools.Server)
        self._server = server

    ### SPECIAL METHODS ###

    def __call__(self, response):
        node_id = response.node_id
        node = self._server._nodes.get(node_id)
        if node is None:
            return
        node.handle_response(response)

    ### PUBLIC PROPERTIES ###

    @property
    def server(self):
        return self._server