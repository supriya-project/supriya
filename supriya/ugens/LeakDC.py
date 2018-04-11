from supriya.ugens.Filter import Filter


class LeakDC(Filter):
    """
    A DC blocker.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> leak_d_c = supriya.ugens.LeakDC.ar(
        ...     source=source,
        ...     coefficient=0.995,
        ...     )
        >>> leak_d_c
        LeakDC.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Filter UGens'

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
        coefficient=0.995,
        source=0,
        ):
        Filter.__init__(
            self,
            calculation_rate=calculation_rate,
            coefficient=coefficient,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        coefficient=0.995,
        source=0,
        ):
        """
        Constructs an audio-rate DC blocker.

        ::

            >>> source = supriya.ugens.In.ar(bus=0, channel_count=2)
            >>> leak_d_c = supriya.ugens.LeakDC.ar(
            ...     source=source,
            ...     coefficient=0.995,
            ...     )
            >>> leak_d_c
            UGenArray({2})

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            coefficient=coefficient,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        coefficient=0.9,
        source=0,
        ):
        """
        Constructs a control-rate DC blocker.

        ::

            >>> source = supriya.ugens.In.kr(bus=0, channel_count=2)
            >>> leak_d_c = supriya.ugens.LeakDC.kr(
            ...     source=source,
            ...     coefficient=0.995,
            ...     )
            >>> leak_d_c
            UGenArray({2})

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            coefficient=coefficient,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def coefficient(self):
        """
        Gets `coefficient` input of LeakDC.

        ::

            >>> source = supriya.ugens.In.kr(bus=0)
            >>> leak_d_c = supriya.ugens.LeakDC.kr(
            ...     source=source,
            ...     coefficient=0.995,
            ...     )
            >>> leak_d_c.coefficient
            0.995

        Returns ugen input.
        """
        index = self._ordered_input_names.index('coefficient')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of LeakDC.

        ::

            >>> source = supriya.ugens.In.kr(bus=0)
            >>> leak_d_c = supriya.ugens.LeakDC.kr(
            ...     source=source,
            ...     coefficient=0.995,
            ...     )
            >>> leak_d_c.source
            In.kr()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
