from supriya.tools.ugentools.UGen import UGen


class Sweep(UGen):
    """

    ::

        >>> sweep = ugentools.Sweep.ar(
        ...     rate=1,
        ...     trigger=0,
        ...     )
        >>> sweep
        Sweep.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'trigger',
        'rate',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        rate=1,
        trigger=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            rate=rate,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        rate=1,
        trigger=0,
        ):
        """
        Constructs an audio-rate Sweep.

        ::

            >>> sweep = ugentools.Sweep.ar(
            ...     rate=1,
            ...     trigger=0,
            ...     )
            >>> sweep
            Sweep.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            rate=rate,
            trigger=trigger,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        rate=1,
        trigger=0,
        ):
        """
        Constructs a control-rate Sweep.

        ::

            >>> sweep = ugentools.Sweep.kr(
            ...     rate=1,
            ...     trigger=0,
            ...     )
            >>> sweep
            Sweep.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            rate=rate,
            trigger=trigger,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def rate(self):
        """
        Gets `rate` input of Sweep.

        ::

            >>> sweep = ugentools.Sweep.ar(
            ...     rate=1,
            ...     trigger=0,
            ...     )
            >>> sweep.rate
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('rate')
        return self._inputs[index]

    @property
    def trigger(self):
        """
        Gets `trigger` input of Sweep.

        ::

            >>> sweep = ugentools.Sweep.ar(
            ...     rate=1,
            ...     trigger=0,
            ...     )
            >>> sweep.trigger
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]
