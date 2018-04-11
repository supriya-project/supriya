from supriya.ugens.Peak import Peak


class RunningMin(Peak):
    """
    Tracks minimum signal amplitude.

    ::

        >>> source = supriya.ugens.In.ar(0)
        >>> trigger = supriya.ugens.Impulse.kr(1)
        >>> running_min = supriya.ugens.RunningMin.ar(
        ...     source=source,
        ...     trigger=trigger,
        ...     )
        >>> running_min
        RunningMin.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Trigger Utility UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'trigger',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        source=None,
        trigger=0,
        ):
        Peak.__init__(
            self,
            calculation_rate=calculation_rate,
            source=source,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        source=None,
        trigger=0,
        ):
        """
        Constructs an audio-rate RunningMin.

        ::

            >>> source = supriya.ugens.In.ar(0)
            >>> trigger = supriya.ugens.Impulse.kr(1)
            >>> running_min = supriya.ugens.RunningMin.ar(
            ...     source=source,
            ...     trigger=trigger,
            ...     )
            >>> running_min
            RunningMin.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            source=source,
            trigger=trigger,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        source=None,
        trigger=0,
        ):
        """
        Constructs a control-rate RunningMin.

        ::

            >>> source = supriya.ugens.In.ar(0)
            >>> trigger = supriya.ugens.Impulse.kr(1)
            >>> running_min = supriya.ugens.RunningMin.kr(
            ...     source=source,
            ...     trigger=trigger,
            ...     )
            >>> running_min
            RunningMin.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            source=source,
            trigger=trigger,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def source(self):
        """
        Gets `source` input of RunningMin.

        ::

            >>> source = supriya.ugens.In.ar(0)
            >>> trigger = supriya.ugens.Impulse.kr(1)
            >>> running_min = supriya.ugens.RunningMin.ar(
            ...     source=source,
            ...     trigger=trigger,
            ...     )
            >>> running_min.source
            In.ar()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def trigger(self):
        """
        Gets `trigger` input of RunningMin.

        ::

            >>> source = supriya.ugens.In.ar(0)
            >>> trigger = supriya.ugens.Impulse.kr(1)
            >>> running_min = supriya.ugens.RunningMin.ar(
            ...     source=source,
            ...     trigger=trigger,
            ...     )
            >>> running_min.trigger
            Impulse.kr()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]
