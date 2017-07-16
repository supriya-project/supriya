from supriya.tools.ugentools.OnePole import OnePole


class OneZero(OnePole):
    """

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> one_zero = ugentools.OneZero.ar(
        ...     coefficient=0.5,
        ...     source=source,
        ...     )
        >>> one_zero
        OneZero.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'coefficient',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        coefficient=0.5,
        source=None,
        ):
        OnePole.__init__(
            self,
            calculation_rate=calculation_rate,
            coefficient=coefficient,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        coefficient=0.5,
        source=None,
        ):
        """
        Constructs an audio-rate OneZero.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> one_zero = ugentools.OneZero.ar(
            ...     coefficient=0.5,
            ...     source=source,
            ...     )
            >>> one_zero
            OneZero.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            coefficient=coefficient,
            source=source,
            )
        return ugen

    # def coeffs(): ...

    @classmethod
    def kr(
        cls,
        coefficient=0.5,
        source=None,
        ):
        """
        Constructs a control-rate OneZero.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> one_zero = ugentools.OneZero.kr(
            ...     coefficient=0.5,
            ...     source=source,
            ...     )
            >>> one_zero
            OneZero.kr()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            coefficient=coefficient,
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
    def coefficient(self):
        """
        Gets `coefficient` input of OneZero.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> one_zero = ugentools.OneZero.ar(
            ...     coefficient=0.5,
            ...     source=source,
            ...     )
            >>> one_zero.coefficient
            0.5

        Returns ugen input.
        """
        index = self._ordered_input_names.index('coefficient')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of OneZero.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> one_zero = ugentools.OneZero.ar(
            ...     coefficient=0.5,
            ...     source=source,
            ...     )
            >>> one_zero.source
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
