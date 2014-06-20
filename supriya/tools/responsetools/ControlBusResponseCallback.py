# -*- encoding: utf-8 -*-
from supriya.tools.osctools.OscCallback import OscCallback


class ControlBusResponseCallback(OscCallback):

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
            address_pattern='/c_(set|setn)',
            procedure=self.__call__,
            )
        assert isinstance(server, servertools.Server)
        self._server = server
        self._response_manager = server._response_manager

    ### SPECIAL METHODS ###

    def __call__(self, message):
        from supriya.tools import servertools
        response = self._response_manager(message)
        if not isinstance(response, tuple):
            response = (response,)
        for x in response:
            bus_id = x.bus_id
            bus_proxy = self._server._control_bus_proxies.get(bus_id)
            if not bus_proxy:
                bus_proxy = servertools.BusProxy(
                    bus_id=bus_id,
                    calculation_rate='control',
                    server=self._server,
                    )
                self._server._control_bus_proxies[bus_id] = bus_proxy
            bus_proxy.handle_response(x)
