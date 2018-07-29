from supriya.ugens.UGen import UGen


class Gate(UGen):
    """
    Gates or holds.

    ::

        >>> source = supriya.ugens.WhiteNoise.ar()
        >>> trigger = supriya.ugens.Dust.kr(1)
        >>> gate = supriya.ugens.Gate.ar(
        ...     source=source,
        ...     trigger=trigger,
        ...     )
        >>> gate
        Gate.ar()

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
        UGen.__init__(
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
        Constructs an audio-rate Gate.

        ::

            >>> source = supriya.ugens.WhiteNoise.ar()
            >>> trigger = supriya.ugens.Dust.kr(1)
            >>> gate = supriya.ugens.Gate.ar(
            ...     source=source,
            ...     trigger=trigger,
            ...     )
            >>> gate
            Gate.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
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
        Constructs a control-rate Gate.

        ::

            >>> source = supriya.ugens.WhiteNoise.ar()
            >>> trigger = supriya.ugens.Dust.kr(1)
            >>> gate = supriya.ugens.Gate.kr(
            ...     source=source,
            ...     trigger=trigger,
            ...     )
            >>> gate
            Gate.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
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
        Gets `source` input of Gate.

        ::

            >>> source = supriya.ugens.WhiteNoise.ar()
            >>> trigger = supriya.ugens.Dust.kr(1)
            >>> gate = supriya.ugens.Gate.ar(
            ...     source=source,
            ...     trigger=trigger,
            ...     )
            >>> gate.source
            WhiteNoise.ar()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def trigger(self):
        """
        Gets `trigger` input of Gate.

        ::

            >>> source = supriya.ugens.WhiteNoise.ar()
            >>> trigger = supriya.ugens.Dust.kr(1)
            >>> gate = supriya.ugens.Gate.ar(
            ...     source=source,
            ...     trigger=trigger,
            ...     )
            >>> gate.trigger
            Dust.kr()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]
