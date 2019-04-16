from supriya.realtime.BusGroup import BusGroup


class AudioInputBusGroup(BusGroup):
    """
    Audio input bus group.

    Allocated automatically on server boot.

    ::

        >>> import supriya
        >>> server = supriya.Server().boot()
        >>> bus_group = server.audio_input_bus_group
        >>> bus_group
        <+ AudioInputBusGroup{8}: 8 (audio)>

    ::

        >>> bus_group.is_allocated
        True

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Server Internals"

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, server):
        import supriya.realtime
        import supriya.synthdefs

        assert isinstance(server, supriya.realtime.Server)
        assert server.is_running
        BusGroup.__init__(
            self,
            bus_count=server.options.input_bus_channel_count,
            calculation_rate=supriya.CalculationRate.AUDIO,
        )
        self._bus_id = server.options.output_bus_channel_count
        self._server = server

    ### PUBLIC METHODS ###

    def allocate(self):
        pass

    def free(self):
        pass
