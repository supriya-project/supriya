from supriya.ugens.TwoPole import TwoPole


class TwoZero(TwoPole):
    """
    A two zero filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> two_zero = supriya.ugens.TwoZero.ar(
        ...     frequency=440,
        ...     radius=0.8,
        ...     source=source,
        ...     )
        >>> two_zero
        TwoZero.ar()

    """

    ### CLASS VARIABLES ###

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
        TwoPole.__init__(
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
        Constructs an audio-rate TwoZero.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> two_zero = supriya.ugens.TwoZero.ar(
            ...     frequency=440,
            ...     radius=0.8,
            ...     source=source,
            ...     )
            >>> two_zero
            TwoZero.ar()

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
        Constructs a control-rate TwoZero.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> two_zero = supriya.ugens.TwoZero.kr(
            ...     frequency=440,
            ...     radius=0.8,
            ...     source=source,
            ...     )
            >>> two_zero
            TwoZero.kr()

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

    ### PUBLIC PROPERTIES ###

    @property
    def frequency(self):
        """
        Gets `frequency` input of TwoZero.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> two_zero = supriya.ugens.TwoZero.ar(
            ...     frequency=440,
            ...     radius=0.8,
            ...     source=source,
            ...     )
            >>> two_zero.frequency
            440.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def radius(self):
        """
        Gets `radius` input of TwoZero.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> two_zero = supriya.ugens.TwoZero.ar(
            ...     frequency=440,
            ...     radius=0.8,
            ...     source=source,
            ...     )
            >>> two_zero.radius
            0.8

        Returns ugen input.
        """
        index = self._ordered_input_names.index('radius')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of TwoZero.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> two_zero = supriya.ugens.TwoZero.ar(
            ...     frequency=440,
            ...     radius=0.8,
            ...     source=source,
            ...     )
            >>> two_zero.source
            In.ar()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
