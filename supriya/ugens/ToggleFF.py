from supriya.ugens.UGen import UGen


class ToggleFF(UGen):
    """
    A toggle flip-flop.

    ::

        >>> trigger = supriya.ugens.Dust.kr(1)
        >>> toggle_ff = supriya.ugens.ToggleFF.ar(
        ...     trigger=trigger,
        ...     )
        >>> toggle_ff
        ToggleFF.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Trigger Utility UGens'

    __slots__ = ()

    _ordered_input_names = (
        'trigger',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        trigger=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        trigger=0,
        ):
        """
        Constructs an audio-rate ToggleFF.

        ::

            >>> trigger = supriya.ugens.Dust.kr(1)
            >>> toggle_ff = supriya.ugens.ToggleFF.ar(
            ...     trigger=trigger,
            ...     )
            >>> toggle_ff
            ToggleFF.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            trigger=trigger,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        trigger=0,
        ):
        """
        Constructs a control-rate ToggleFF.

        ::

            >>> trigger = supriya.ugens.Dust.kr(1)
            >>> toggle_ff = supriya.ugens.ToggleFF.kr(
            ...     trigger=trigger,
            ...     )
            >>> toggle_ff
            ToggleFF.kr()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            trigger=trigger,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def trigger(self):
        """
        Gets `trigger` input of ToggleFF.

        ::

            >>> trigger = supriya.ugens.Dust.kr(1)
            >>> toggle_ff = supriya.ugens.ToggleFF.ar(
            ...     trigger=trigger,
            ...     )
            >>> toggle_ff.trigger
            Dust.kr()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]
