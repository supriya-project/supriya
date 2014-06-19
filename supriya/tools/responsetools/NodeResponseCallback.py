# -*- encoding: utf-8 -*-
from supriya.tools.osctools.OscCallback import OscCallback


class NodeResponseCallback(OscCallback):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_server',
        '_response_manager',
        )

    ### INITIALIZER ###

    def __init__(self, server):
        from supriya.tools import servertools
        OscCallback.__init__(
            self,
            address_pattern='/n_(end|go|info|move|off|on|set|setn)',
            procedure=self.__call__,
            )
        assert isinstance(server, servertools.Server)
        self._server = server
        self._response_manager = server._response_manager

    ### SPECIAL METHODS ###

    def __call__(self, message):
        response = self._response_manager(message)
        if not isinstance(response, tuple):
            response = (response,)
        for x in response:
            node_id = x.node_id
            node = self._server._nodes.get(node_id)
            if node is None:
                continue
            node.handle_response(x)
