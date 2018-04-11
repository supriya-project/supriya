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
        import supriya.commands
        if isinstance(response, supriya.commands.ControlBusSetResponse):
            for item in response:
                bus_id = item.bus_id
                bus_proxy = self._server._get_control_bus_proxy(bus_id)
                bus_proxy._value = item.bus_value
        elif isinstance(response,
            supriya.commands.ControlBusSetContiguousResponse):
            for item in response:
                starting_bus_id = item.starting_bus_id
                for i, value in enumerate(item.bus_values):
                    bus_id = starting_bus_id + i
                    bus_proxy = self._server._get_control_bus_proxy(bus_id)
                    bus_proxy._value = value

    ### PUBLIC PROPERTIES ###

    @property
    def server(self):
        return self._server
