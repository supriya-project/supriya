from supriya.ugens.Filter import Filter


class TwoPole(Filter):
    """
    A two pole filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> two_pole = supriya.ugens.TwoPole.ar(
        ...     frequency=440,
        ...     radius=0.8,
        ...     source=source,
        ...     )
        >>> two_pole
        TwoPole.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Filter UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'frequency',
        'radius',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        frequency=440,
        radius=0.8,
        source=None,
        ):
        Filter.__init__(
            self,
            calculation_rate=calculation_rate,
            frequency=frequency,
            radius=radius,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        frequency=440,
        radius=0.8,
        source=None,
        ):
        """
        Constructs an audio-rate TwoPole.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> two_pole = supriya.ugens.TwoPole.ar(
            ...     frequency=440,
            ...     radius=0.8,
            ...     source=source,
            ...     )
            >>> two_pole
            TwoPole.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            radius=radius,
            source=source,
            )
        return ugen

    # def coeffs(): ...

    @classmethod
    def kr(
        cls,
        frequency=440,
        radius=0.8,
        source=None,
        ):
        """
        Constructs a control-rate TwoPole.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> two_pole = supriya.ugens.TwoPole.kr(
            ...     frequency=440,
            ...     radius=0.8,
            ...     source=source,
            ...     )
            >>> two_pole
            TwoPole.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            radius=radius,
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
    def frequency(self):
        """
        Gets `frequency` input of TwoPole.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> two_pole = supriya.ugens.TwoPole.ar(
            ...     frequency=440,
            ...     radius=0.8,
            ...     source=source,
            ...     )
            >>> two_pole.frequency
            440.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def radius(self):
        """
        Gets `radius` input of TwoPole.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> two_pole = supriya.ugens.TwoPole.ar(
            ...     frequency=440,
            ...     radius=0.8,
            ...     source=source,
            ...     )
            >>> two_pole.radius
            0.8

        Returns ugen input.
        """
        index = self._ordered_input_names.index('radius')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of TwoPole.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> two_pole = supriya.ugens.TwoPole.ar(
            ...     frequency=440,
            ...     radius=0.8,
            ...     source=source,
            ...     )
            >>> two_pole.source
            In.ar()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
