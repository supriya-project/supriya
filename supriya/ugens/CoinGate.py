from supriya.ugens.UGen import UGen


class CoinGate(UGen):
    """
    A probabilistic trigger gate.

    ::

        >>> trigger = supriya.ugens.Impulse.ar()
        >>> coin_gate = supriya.ugens.CoinGate.ar(
        ...     probability=0.5,
        ...     trigger=trigger,
        ...     )
        >>> coin_gate
        CoinGate.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Noise UGens'

    __slots__ = ()

    _ordered_input_names = (
        'probability',
        'trigger',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        probability=None,
        trigger=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            probability=probability,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        probability=None,
        trigger=None,
        ):
        """
        Constructs an audio-rate probabilitic trigger gate.

        ::

            >>> trigger = supriya.ugens.Impulse.ar()
            >>> coin_gate = supriya.ugens.CoinGate.ar(
            ...     probability=[0.9, 0.1],
            ...     trigger=trigger,
            ...     )
            >>> coin_gate
            UGenArray({2})

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            probability=probability,
            trigger=trigger,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        probability=None,
        trigger=None,
        ):
        """
        Constructs a control-rate probabilitic trigger gate.

        ::

            >>> trigger = supriya.ugens.Impulse.kr()
            >>> coin_gate = supriya.ugens.CoinGate.kr(
            ...     probability=[0.9, 0.1],
            ...     trigger=trigger,
            ...     )
            >>> coin_gate
            UGenArray({2})

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            probability=probability,
            trigger=trigger,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def probability(self):
        """
        Gets `probability` input of Crackle.

        ::

            >>> trigger = supriya.ugens.Impulse.ar()
            >>> coin_gate = supriya.ugens.CoinGate.ar(
            ...     probability=0.5,
            ...     trigger=trigger,
            ...     )
            >>> coin_gate.probability
            0.5

        Returns ugen input.
        """
        index = self._ordered_input_names.index('probability')
        return self._inputs[index]

    @property
    def trigger(self):
        """
        Gets `trigger` input of Crackle.

        ::

            >>> trigger = supriya.ugens.Impulse.ar()
            >>> coin_gate = supriya.ugens.CoinGate.ar(
            ...     probability=0.5,
            ...     trigger=trigger,
            ...     )
            >>> coin_gate.trigger
            Impulse.ar()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]
