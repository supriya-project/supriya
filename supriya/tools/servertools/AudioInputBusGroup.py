# -*- encoding: utf-8 -*-
from supriya.tools.servertools.BusGroup import BusGroup


class AudioInputBusGroup(BusGroup):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Server Internals'

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        server,
        ):
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        assert isinstance(server, servertools.Server)
        assert server.is_running
        self._server = server
        bus_id = server.server_options.output_bus_channel_count
        bus_count = server.server_options.input_bus_channel_count
        rate = synthdeftools.CalculationRate.AUDIO
        BusGroup.__init__(
            self,
            bus_count=bus_count,
            rate=rate,
            )
        self._bus_id = bus_id

    ### PUBLIC METHODS ###

    def allocate(self):
        pass

    def free(self):
        pass