from supriya.ugens.A2K import A2K


class T2K(A2K):
    """

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> t_2_k = supriya.ugens.T2K.ar(
        ...     source=source,
        ...     )
        >>> t_2_k
        T2K.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        source=None,
        ):
        A2K.__init__(
            self,
            calculation_rate=calculation_rate,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        source=None,
        ):
        """
        Constructs a control-rate T2K.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> t_2_k = supriya.ugens.T2K.kr(
            ...     source=source,
            ...     )
            >>> t_2_k
            T2K.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def source(self):
        """
        Gets `source` input of T2K.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> t_2_k = supriya.ugens.T2K.ar(
            ...     source=source,
            ...     )
            >>> t_2_k.source
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
