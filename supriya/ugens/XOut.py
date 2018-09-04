import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class XOut(UGen):
    """
    A cross-fading bus output unit generator.

    ::

        >>> source = supriya.ugens.WhiteNoise.ar()
        >>> xout = supriya.ugens.XOut.ar(
        ...     bus=0,
        ...     crossfade=0.5,
        ...     source=source,
        ...     )
        >>> xout
        XOut.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Input/Output UGens'

    _is_output = True

    _ordered_input_names = collections.OrderedDict([
        ('bus', 0),
        ('crossfade', 0),
        ('source', None),
    ])

    _unexpanded_input_names = (
        'source',
    )

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
        CalculationRate.CONTROL,
    )

    ### PRIVATE METHODS ###

    def _get_outputs(self):
        return []

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        bus=0,
        crossfade=0,
        source=None,
    ):
        """
        Constructs an audio-rate XOut.

        ::

            >>> source = supriya.ugens.WhiteNoise.ar()
            >>> xout = supriya.ugens.XOut.ar(
            ...     bus=0,
            ...     crossfade=0.5,
            ...     source=source,
            ...     )
            >>> xout
            XOut.ar()

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
            bus = int(bus)
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bus=bus,
            crossfade=crossfade,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        bus=0,
        crossfade=0,
        source=None,
    ):
        """
        Constructs a control-rate XOut.

        ::

            >>> source = supriya.ugens.WhiteNoise.ar()
            >>> xout = supriya.ugens.XOut.kr(
            ...     bus=0,
            ...     crossfade=0.5,
            ...     source=source,
            ...     )
            >>> xout
            XOut.kr()

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
            bus = int(bus)
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bus=bus,
            crossfade=crossfade,
            source=source,
            )
        return ugen
