# -*- encoding: utf-8 -*-
from supriya.tools.osctools.OscCallback import OscCallback


class ControlBusResponseCallback(OscCallback):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_server',
        )

    ### INITIALIZER ###

    def __init__(self, server):
        from supriya.tools import servertools
        OscCallback.__init__(
            self,
            address_pattern='/c_(set|setn)',
            procedure=self.__call__,
            )
        assert isinstance(server, servertools.Server)
        self._server = server

    ### SPECIAL METHODS ###

    def __call__(self, message):
        from supriya.tools import responsetools
        response = responsetools.ResponseManager.handle_message(message)
        if isinstance(response, responsetools.ControlBusSetResponse):
            for item in response:
                bus_id = item.bus_id
                bus_proxy = self._server._get_control_bus_proxy(bus_id)
                bus_proxy._value = item.bus_value
        elif isinstance(response,
            responsetools.ControlBusSetContiguousResponse):
            for item in response:
                starting_bus_id = item.starting_bus_id
                for i, value in enumerate(item.bus_values):
                    bus_id = starting_bus_id + i
                    bus_proxy = self._server._get_control_bus_proxy(bus_id)
                    bus_proxy._value = value