from supriya.ugens.MultiOutUGen import MultiOutUGen


class In(MultiOutUGen):
    """
    A bus input unit generator.

    ::

        >>> supriya.ugens.In.ar(bus=0, channel_count=4)
        UGenArray({4})

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Input/Output UGens'

    __slots__ = ()

    _ordered_input_names = (
        'bus',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        bus=0,
        calculation_rate=None,
        channel_count=1,
        ):
        MultiOutUGen.__init__(
            self,
            bus=bus,
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        bus=0,
        channel_count=1,
        ):
        """
        Constructs an audio-rate bus input.

        ::

            >>> supriya.ugens.In.ar(bus=0, channel_count=4)
            UGenArray({4})

        Returns ugen graph.
        """
        import supriya.realtime
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        prototype = (
            supriya.realtime.Bus,
            supriya.realtime.BusGroup,
            supriya.realtime.BusProxy,
            )
        if isinstance(bus, prototype):
            if isinstance(bus, supriya.realtime.BusGroup):
                channel_count = len(bus)
            else:
                channel_count = 1
            bus = int(bus)
        ugen = cls._new_expanded(
            bus=bus,
            channel_count=channel_count,
            calculation_rate=calculation_rate,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        bus=0,
        channel_count=1,
        ):
        """
        Constructs a control-rate bus input.

        ::

            >>> supriya.ugens.In.kr(bus=0, channel_count=4)
            UGenArray({4})

        Returns ugen graph.
        """
        import supriya.realtime
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        prototype = (
            supriya.realtime.Bus,
            supriya.realtime.BusGroup,
            supriya.realtime.BusProxy,
            )
        if isinstance(bus, prototype):
            if isinstance(bus, supriya.realtime.BusGroup):
                channel_count = len(bus)
            else:
                channel_count = 1
            bus = int(bus)
        ugen = cls._new_expanded(
            bus=bus,
            channel_count=channel_count,
            calculation_rate=calculation_rate,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def bus(self):
        """
        Gets `bus` input of DC.

        ::

            >>> bus = 2
            >>> in_ = supriya.ugens.In.ar(
            ...     bus=bus,
            ...     )
            >>> in_.source.bus
            2.0

        Returns input.
        """
        index = self._ordered_input_names.index('bus')
        return self._inputs[index]

    @property
    def is_input_ugen(self):
        return True
