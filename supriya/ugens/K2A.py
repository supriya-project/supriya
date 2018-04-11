from supriya.ugens.PureUGen import PureUGen


class K2A(PureUGen):
    """
    A control-rate to audio-rate converter unit generator.

    ::

        >>> source = supriya.ugens.SinOsc.kr()
        >>> k_2_a = supriya.ugens.K2A.ar(
        ...     source=source,
        ...     )
        >>> k_2_a
        K2A.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utility UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        source=None,
        calculation_rate=None,
        ):
        PureUGen.__init__(
            self,
            source=source,
            calculation_rate=calculation_rate,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        source=None,
        ):
        """
        Constructs a control-rate to audio-rate converter.

        ::

            >>> source = supriya.ugens.SinOsc.kr(frequency=[2, 3])
            >>> supriya.ugens.K2A.ar(
            ...     source=source,
            ...     )
            UGenArray({2})

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def source(self):
        """
        Gets `source` input of K2A.

        ::

            >>> source = supriya.ugens.WhiteNoise.kr()
            >>> k_2_a = supriya.ugens.K2A.ar(
            ...     source=source,
            ...     )
            >>> k_2_a.source
            WhiteNoise.kr()[0]

        Returns input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
