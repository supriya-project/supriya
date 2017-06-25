from supriya.tools.ugentools.PulseCount import PulseCount


class SetResetFF(PulseCount):
    """

    ::

        >>> set_reset_ff = ugentools.SetResetFF.ar(
        ...     reset=0,
        ...     trigger=0,
        ...     )
        >>> set_reset_ff
        SetResetFF.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'trigger',
        'reset',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        reset=0,
        trigger=0,
        ):
        PulseCount.__init__(
            self,
            calculation_rate=calculation_rate,
            reset=reset,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        reset=0,
        trigger=0,
        ):
        """
        Constructs an audio-rate SetResetFF.

        ::

            >>> set_reset_ff = ugentools.SetResetFF.ar(
            ...     reset=0,
            ...     trigger=0,
            ...     )
            >>> set_reset_ff
            SetResetFF.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            reset=reset,
            trigger=trigger,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        reset=0,
        trigger=0,
        ):
        """
        Constructs a control-rate SetResetFF.

        ::

            >>> set_reset_ff = ugentools.SetResetFF.kr(
            ...     reset=0,
            ...     trigger=0,
            ...     )
            >>> set_reset_ff
            SetResetFF.kr()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            reset=reset,
            trigger=trigger,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def reset(self):
        """
        Gets `reset` input of SetResetFF.

        ::

            >>> set_reset_ff = ugentools.SetResetFF.ar(
            ...     reset=0,
            ...     trigger=0,
            ...     )
            >>> set_reset_ff.reset
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('reset')
        return self._inputs[index]

    @property
    def trigger(self):
        """
        Gets `trigger` input of SetResetFF.

        ::

            >>> set_reset_ff = ugentools.SetResetFF.ar(
            ...     reset=0,
            ...     trigger=0,
            ...     )
            >>> set_reset_ff.trigger
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]
