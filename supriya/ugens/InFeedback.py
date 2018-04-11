from supriya.ugens.MultiOutUGen import MultiOutUGen


class InFeedback(MultiOutUGen):
    r'''A bus input unit generator.

    Reads signal from a bus with a current or one cycle old timestamp.

    ::

        >>> in_feedback = supriya.ugens.InFeedback.ar(
        ...     bus=0,
        ...     channel_count=2,
        ...     )
        >>> in_feedback
        UGenArray({2})

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Input/Output UGens'

    __slots__ = ()

    _ordered_input_names = (
        'bus',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        bus=0,
        channel_count=1,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            bus=bus,
            channel_count=channel_count,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        bus=0,
        channel_count=1,
        ):
        r'''Constructs an audio-rate InFeedback.

        ::

            >>> supriya.ugens.InFeedback.ar(bus=0, channel_count=2)
            UGenArray({2})

        Returns ugen graph.
        '''
        import supriya.realtime
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.AUDIO
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
        r'''Gets `bus` input of InFeedback.

        ::

            >>> bus = 2
            >>> in_feedback = supriya.ugens.InFeedback.ar(
            ...     bus=bus,
            ...     )
            >>> in_feedback.source.bus
            2.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('bus')
        return self._inputs[index]

    @property
    def is_input_ugen(self):
        return True
