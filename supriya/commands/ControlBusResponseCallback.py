from supriya.commands.ResponseCallback import ResponseCallback


class ControlBusResponseCallback(ResponseCallback):

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
            #address_pattern='/c_(set|setn)',
            procedure=self.__call__,
            prototype=(
                supriya.commands.ControlBusSetContiguousResponse,
                supriya.commands.ControlBusSetResponse,
                ),
            )
        assert isinstance(server, supriya.realtime.Server)
        self._server = server

    ### SPECIAL METHODS ###

    def __call__(self, response):
        self.server._handle_control_bus_response(response)

    ### PUBLIC PROPERTIES ###

    @property
    def server(self):
        return self._server
