from supriya.ugens.Filter import Filter


class Slope(Filter):
    """
    Calculates slope of signal.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> slope = supriya.ugens.Slope.ar(
        ...     source=source,
        ...     )
        >>> slope
        Slope.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Filter UGens'

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
        Filter.__init__(
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
        Constructs an audio-rate Slope.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> slope = supriya.ugens.Slope.ar(
            ...     source=source,
            ...     )
            >>> slope
            Slope.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    # def coeffs(): ...

    @classmethod
    def kr(
        cls,
        source=None,
        ):
        """
        Constructs a control-rate Slope.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> slope = supriya.ugens.Slope.kr(
            ...     source=source,
            ...     )
            >>> slope
            Slope.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    # def magResponse(): ...

    # def magResponse2(): ...

    # def magResponse5(): ...

    # def magResponseN(): ...

    # def scopeResponse(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def source(self):
        """
        Gets `source` input of Slope.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> slope = supriya.ugens.Slope.ar(
            ...     source=source,
            ...     )
            >>> slope.source
            In.ar()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
