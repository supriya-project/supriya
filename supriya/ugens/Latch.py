from supriya.ugens.UGen import UGen


class Latch(UGen):
    """
    Samples and holds.

    ::

        >>> source = supriya.ugens.WhiteNoise.ar()
        >>> trigger = supriya.ugens.Dust.kr(1)
        >>> latch = supriya.ugens.Latch.ar(
        ...     source=source,
        ...     trigger=trigger,
        ...     )
        >>> latch
        Latch.ar()

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
        Constructs an audio-rate Latch.

        ::

            >>> source = supriya.ugens.WhiteNoise.ar()
            >>> trigger = supriya.ugens.Dust.kr(1)
            >>> latch = supriya.ugens.Latch.ar(
            ...     source=source,
            ...     trigger=trigger,
            ...     )
            >>> latch
            Latch.ar()

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
        Constructs a control-rate Latch.

        ::

            >>> source = supriya.ugens.WhiteNoise.ar()
            >>> trigger = supriya.ugens.Dust.kr(1)
            >>> latch = supriya.ugens.Latch.kr(
            ...     source=source,
            ...     trigger=0,
            ...     )
            >>> latch
            Latch.kr()

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
        Gets `source` input of Latch.

        ::

            >>> source = supriya.ugens.WhiteNoise.ar()
            >>> trigger = supriya.ugens.Dust.kr(1)
            >>> latch = supriya.ugens.Latch.ar(
            ...     source=source,
            ...     trigger=trigger,
            ...     )
            >>> latch.source
            WhiteNoise.ar()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def trigger(self):
        """
        Gets `trigger` input of Latch.

        ::

            >>> source = supriya.ugens.WhiteNoise.ar()
            >>> trigger = supriya.ugens.Dust.kr(1)
            >>> latch = supriya.ugens.Latch.ar(
            ...     source=source,
            ...     trigger=trigger,
            ...     )
            >>> latch.trigger
            Dust.kr()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]
