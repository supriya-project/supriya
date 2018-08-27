import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class ReplaceOut(UGen):
    """
    An overwriting bus output unit generator.

    ::

        >>> source = supriya.ugens.SinOsc.ar()
        >>> supriya.ugens.ReplaceOut.ar(
        ...     bus=0,
        ...     source=source,
        ...     )
        ReplaceOut.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Input/Output UGens'

    _ordered_input_names = collections.OrderedDict([
        ('bus', 0),
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
        source=None,
    ):
        """
        Constructs an audio-rate overwriting bus output.

        ::

            >>> source = supriya.ugens.SinOsc.ar(frequency=[440, 442])
            >>> out = supriya.ugens.ReplaceOut.ar(
            ...     bus=0,
            ...     source=source,
            ...     )
            >>> out
            ReplaceOut.ar()

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
            bus=bus,
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        bus=0,
        source=None,
    ):
        """
        Constructs a control-rate overwriting bus output.

        ::

            >>> source = supriya.ugens.SinOsc.kr(frequency=[4, 2])
            >>> out = supriya.ugens.ReplaceOut.kr(
            ...     bus=0,
            ...     source=source,
            ...     )
            >>> out
            ReplaceOut.kr()

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
            bus=bus,
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def is_output_ugen(self):
        return True
