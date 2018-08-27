import collections
from supriya import CalculationRate
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

    _has_channel_count = True

    _has_settable_channel_count = True

    _ordered_input_names = collections.OrderedDict([
        ('bus', 0),
    ])

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
        CalculationRate.CONTROL,
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
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
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
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
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
    def is_input_ugen(self):
        return True
