from supriya.realtime.BusGroup import BusGroup


class AudioOutputBusGroup(BusGroup):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Server Internals'

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        server,
        ):
        import supriya.realtime
        from supriya.tools import synthdeftools
        assert isinstance(server, supriya.realtime.Server)
        assert server.is_running
        self._server = server
        bus_id = 0
        bus_count = server.server_options.input_bus_channel_count
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        BusGroup.__init__(
            self,
            bus_count=bus_count,
            calculation_rate=calculation_rate,
            )
        self._bus_id = bus_id

    ### PUBLIC METHODS ###

    def allocate(self):
        pass

    def free(self):
        pass
