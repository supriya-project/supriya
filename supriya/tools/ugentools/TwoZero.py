from supriya.tools.ugentools.TwoPole import TwoPole


class TwoZero(TwoPole):
    """
    A two zero filter.

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> two_zero = ugentools.TwoZero.ar(
        ...     frequency=440,
        ...     radius=0.8,
        ...     source=source,
        ...     )
        >>> two_zero
        TwoZero.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

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

            >>> source = ugentools.In.ar(bus=0)
            >>> two_zero = ugentools.TwoZero.ar(
            ...     frequency=440,
            ...     radius=0.8,
            ...     source=source,
            ...     )
            >>> two_zero
            TwoZero.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
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

            >>> source = ugentools.In.ar(bus=0)
            >>> two_zero = ugentools.TwoZero.kr(
            ...     frequency=440,
            ...     radius=0.8,
            ...     source=source,
            ...     )
            >>> two_zero
            TwoZero.kr()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
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
        Gets `frequency` input of TwoZero.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> two_zero = ugentools.TwoZero.ar(
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

            >>> source = ugentools.In.ar(bus=0)
            >>> two_zero = ugentools.TwoZero.ar(
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

            >>> source = ugentools.In.ar(bus=0)
            >>> two_zero = ugentools.TwoZero.ar(
            ...     frequency=440,
            ...     radius=0.8,
            ...     source=source,
            ...     )
            >>> two_zero.source
            OutputProxy(
                source=In(
                    bus=0.0,
                    calculation_rate=CalculationRate.AUDIO,
                    channel_count=1
                    ),
                output_index=0
                )

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
