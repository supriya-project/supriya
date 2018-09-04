import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class OffsetOut(UGen):
    """
    A bus output unit generator with sample-accurate timing.

    ::

        >>> source = supriya.ugens.SinOsc.ar()
        >>> supriya.ugens.OffsetOut.ar(
        ...     bus=0,
        ...     source=source,
        ...     )
        OffsetOut.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Input/Output UGens'

    _is_output = True

    _ordered_input_names = collections.OrderedDict([
        ('bus', 0),
        ('source', None),
    ])

    _unexpanded_input_names = (
        'source',
    )

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
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
        Constructs a sample-accurately-timed audio-rate bus output.

        ::

            >>> source = supriya.ugens.SinOsc.ar(frequency=[440, 442])
            >>> offset_out = supriya.ugens.OffsetOut.ar(
            ...     bus=0,
            ...     source=source,
            ...     )
            >>> offset_out
            OffsetOut.ar()

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
        return cls._new_expanded(
            bus=bus,
            calculation_rate=calculation_rate,
            source=source,
            )
