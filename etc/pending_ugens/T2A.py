from supriya.ugens.K2A import K2A


class T2A(K2A):
    """

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> t_2_a = supriya.ugens.T2A.ar(
        ...     offset=0,
        ...     source=source,
        ...     )
        >>> t_2_a
        T2A.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'offset',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        offset=0,
        source=None,
        ):
        K2A.__init__(
            self,
            calculation_rate=calculation_rate,
            offset=offset,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        offset=0,
        source=None,
        ):
        """
        Constructs an audio-rate T2A.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> t_2_a = supriya.ugens.T2A.ar(
            ...     offset=0,
            ...     source=source,
            ...     )
            >>> t_2_a
            T2A.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            offset=offset,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def offset(self):
        """
        Gets `offset` input of T2A.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> t_2_a = supriya.ugens.T2A.ar(
            ...     offset=0,
            ...     source=source,
            ...     )
            >>> t_2_a.offset
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('offset')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of T2A.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> t_2_a = supriya.ugens.T2A.ar(
            ...     offset=0,
            ...     source=source,
            ...     )
            >>> t_2_a.source
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
