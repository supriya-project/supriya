from supriya.tools.ugentools.PureUGen import PureUGen


class A2K(PureUGen):
    """
    An audio-rate to control-rate convert unit generator.

    ::

        >>> source = ugentools.SinOsc.ar()
        >>> a_2_k = ugentools.A2K.kr(
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

            >>> source = ugentools.SinOsc.ar(frequency=[440, 442])
            >>> ugentools.A2K.kr(
            ...     source=source,
            ...     )
            UGenArray({2})

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
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

            >>> source = ugentools.SinOsc.ar()
            >>> a_2_k = ugentools.A2K.kr(
            ...     source=source,
            ...     )
            >>> a_2_k.source
            OutputProxy(
                source=SinOsc(
                    calculation_rate=CalculationRate.AUDIO,
                    frequency=440.0,
                    phase=0.0
                    ),
                output_index=0
                )

        Returns input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
