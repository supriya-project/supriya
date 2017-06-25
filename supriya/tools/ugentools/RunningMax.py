from supriya.tools.ugentools.Peak import Peak


class RunningMax(Peak):
    """
    Tracks maximum signal amplitude.

    ::

        >>> source = ugentools.In.ar(0)
        >>> trigger = ugentools.Impulse.kr(1)
        >>> running_max = ugentools.RunningMax.ar(
        ...     source=source,
        ...     trigger=0,
        ...     )
        >>> running_max
        RunningMax.ar()

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
        Constructs an audio-rate RunningMax.

        ::

            >>> source = ugentools.In.ar(0)
            >>> trigger = ugentools.Impulse.kr(1)
            >>> running_max = ugentools.RunningMax.ar(
            ...     source=source,
            ...     trigger=trigger,
            ...     )
            >>> running_max
            RunningMax.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
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
        Constructs a control-rate RunningMax.

        ::

            >>> source = ugentools.In.ar(0)
            >>> trigger = ugentools.Impulse.kr(1)
            >>> running_max = ugentools.RunningMax.kr(
            ...     source=source,
            ...     trigger=trigger,
            ...     )
            >>> running_max
            RunningMax.kr()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
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
        Gets `source` input of RunningMax.

        ::

            >>> source = ugentools.In.ar(0)
            >>> trigger = ugentools.Impulse.kr(1)
            >>> running_max = ugentools.RunningMax.ar(
            ...     source=source,
            ...     trigger=trigger,
            ...     )
            >>> running_max.source
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

    @property
    def trigger(self):
        """
        Gets `trigger` input of RunningMax.

        ::

            >>> source = ugentools.In.ar(0)
            >>> trigger = ugentools.Impulse.kr(1)
            >>> running_max = ugentools.RunningMax.ar(
            ...     source=source,
            ...     trigger=trigger,
            ...     )
            >>> running_max.trigger
            OutputProxy(
                source=Impulse(
                    calculation_rate=CalculationRate.CONTROL,
                    frequency=1.0,
                    phase=0.0
                    ),
                output_index=0
                )

        Returns ugen input.
        """
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]
