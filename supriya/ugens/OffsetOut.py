import collections
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

    __slots__ = ()

    _ordered_input_names = (
        'bus',
        'source',
        )

    _unexpanded_input_names = (
        'source',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        bus=0,
        source=None,
        ):
        if not isinstance(source, collections.Sequence):
            source = [source]
        UGen.__init__(
            self,
            bus=bus,
            calculation_rate=calculation_rate,
            source=source,
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

    ### PUBLIC PROPERTIES ###

    @property
    def bus(self):
        """
        Gets `bus` input of OffsetOut.

        ::

            >>> bus = 0
            >>> source = supriya.ugens.WhiteNoise.ar()
            >>> offset_out = supriya.ugens.OffsetOut.ar(
            ...     bus=bus,
            ...     source=source,
            ...     )
            >>> offset_out.bus
            0.0

        Returns input.
        """
        index = self._ordered_input_names.index('bus')
        return self._inputs[index]

    @property
    def is_output_ugen(self):
        return True

    @property
    def source(self):
        """
        Gets `source` input of OffsetOut.

        ::

            >>> bus = 0
            >>> source = supriya.ugens.WhiteNoise.ar()
            >>> out = supriya.ugens.OffsetOut.ar(
            ...     bus=bus,
            ...     source=source,
            ...     )
            >>> out.source
            (WhiteNoise.ar()[0],)

        Returns input.
        """
        index = self._ordered_input_names.index('source')
        return tuple(self._inputs[index:])
