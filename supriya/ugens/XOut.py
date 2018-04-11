import collections
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

    __slots__ = ()

    _ordered_input_names = (
        'bus',
        'crossfade',
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
        crossfade=0,
        source=None,
        ):
        if not isinstance(source, collections.Sequence):
            source = (source,)
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            bus=bus,
            crossfade=crossfade,
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
        calculation_rate = supriya.synthdefs.CalculationRate.AUDIO
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
        calculation_rate = supriya.synthdefs.CalculationRate.CONTROL
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

    ### PUBLIC PROPERTIES ###

    @property
    def bus(self):
        """
        Gets `bus` input of XOut.

        ::

            >>> source = supriya.ugens.WhiteNoise.ar()
            >>> xout = supriya.ugens.XOut.ar(
            ...     bus=0,
            ...     crossfade=0.5,
            ...     source=source,
            ...     )
            >>> xout.bus
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('bus')
        return self._inputs[index]

    @property
    def crossfade(self):
        """
        Gets `crossfade` input of XOut.

        ::

            >>> source = supriya.ugens.WhiteNoise.ar()
            >>> xout = supriya.ugens.XOut.ar(
            ...     bus=0,
            ...     crossfade=0.5,
            ...     source=source,
            ...     )
            >>> xout.crossfade
            0.5

        Returns ugen input.
        """
        index = self._ordered_input_names.index('crossfade')
        return self._inputs[index]

    @property
    def is_output_ugen(self):
        return True

    @property
    def source(self):
        """
        Gets `source` input of XOut.

        ::

            >>> source = supriya.ugens.WhiteNoise.ar()
            >>> xout = supriya.ugens.XOut.ar(
            ...     bus=0,
            ...     crossfade=0.5,
            ...     source=source,
            ...     )
            >>> xout.source
            (WhiteNoise.ar()[0],)

        Returns ugen input.
        """
        # TODO: This seems odd.
        index = self._ordered_input_names.index('source')
        return tuple(self._inputs[index:])
