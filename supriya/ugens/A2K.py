from supriya.ugens.PureUGen import PureUGen


class A2K(PureUGen):
    """
    An audio-rate to control-rate convert unit generator.

    ::

        >>> source = supriya.ugens.SinOsc.ar()
        >>> a_2_k = supriya.ugens.A2K.kr(
        ...     source=source,
        ...     )
        >>> a_2_k
        A2K.kr()

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
    def kr(
        cls,
        source=None,
        ):
        """
        Constructs an audio-rate to control-rate converter.

        ::

            >>> source = supriya.ugens.SinOsc.ar(frequency=[440, 442])
            >>> supriya.ugens.A2K.kr(
            ...     source=source,
            ...     )
            UGenArray({2})

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def source(self):
        """
        Gets `source` input of A2K.

        ::

            >>> source = supriya.ugens.SinOsc.ar()
            >>> a_2_k = supriya.ugens.A2K.kr(
            ...     source=source,
            ...     )
            >>> a_2_k.source
            SinOsc.ar()[0]

        Returns input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
