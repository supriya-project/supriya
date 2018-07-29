from supriya.ugens.UGen import UGen


class ZeroCrossing(UGen):
    """
    A zero-crossing frequency follower.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> zero_crossing = supriya.ugens.ZeroCrossing.ar(
        ...     source=source,
        ...     )
        >>> zero_crossing
        ZeroCrossing.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Analysis UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        source=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        source=None,
        ):
        """
        Constructs an audio-rate ZeroCrossing.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> zero_crossing = supriya.ugens.ZeroCrossing.ar(
            ...     source=source,
            ...     )
            >>> zero_crossing
            ZeroCrossing.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        source=None,
        ):
        """
        Constructs a control-rate ZeroCrossing.

        ::

            >>> source = supriya.ugens.In.kr(bus=0)
            >>> zero_crossing = supriya.ugens.ZeroCrossing.kr(
            ...     source=source,
            ...     )
            >>> zero_crossing
            ZeroCrossing.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def source(self):
        """
        Gets `source` input of ZeroCrossing.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> zero_crossing = supriya.ugens.ZeroCrossing.ar(
            ...     source=source,
            ...     )
            >>> zero_crossing.source
            In.ar()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
