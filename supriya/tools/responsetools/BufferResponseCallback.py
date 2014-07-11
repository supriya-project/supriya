# -*- encoding: utf-8 -*-
from supriya.tools.responsetools.ResponseCallback import ResponseCallback


class BufferResponseCallback(ResponseCallback):

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
            #address_pattern='/b_(info|set|setn)',
            procedure=self.__call__,
            response_prototype=(
                responsetools.BufferInfoResponse,
                responsetools.BufferSetResponse,
                responsetools.BufferSetContiguousResponse,
                ),
            )
        assert isinstance(server, servertools.Server)
        self._server = server

    ### SPECIAL METHODS ###

    def __call__(self, response):
        buffer_id = response.buffer_id
        buffer_proxy = self._server._get_buffer_proxy(buffer_id)
        buffer_proxy.handle_response(response)

    ### PUBLIC PROPERTIES ###

    @property
    def server(self):
        return self._server