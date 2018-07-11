from supriya.commands.ResponseCallback import ResponseCallback


class BufferResponseCallback(ResponseCallback):

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
            #address_pattern='/b_(info|set|setn)',
            procedure=self.__call__,
            prototype=(
                supriya.commands.BufferInfoResponse,
                supriya.commands.BufferSetResponse,
                supriya.commands.BufferSetContiguousResponse,
                ),
            )
        assert isinstance(server, supriya.realtime.Server)
        self._server = server

    ### SPECIAL METHODS ###

    def __call__(self, response):
        self.server._handle_buffer_response(response)

    ### PUBLIC PROPERTIES ###

    @property
    def server(self):
        return self._server
