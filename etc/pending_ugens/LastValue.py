from supriya.ugens.UGen import UGen


class LastValue(UGen):
    """

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> last_value = supriya.ugens.LastValue.ar(
        ...     diff=0.01,
        ...     source=source,
        ...     )
        >>> last_value
        LastValue.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'diff',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        diff=0.01,
        source=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            diff=diff,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        diff=0.01,
        source=None,
        ):
        """
        Constructs an audio-rate LastValue.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> last_value = supriya.ugens.LastValue.ar(
            ...     diff=0.01,
            ...     source=source,
            ...     )
            >>> last_value
            LastValue.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            diff=diff,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        diff=0.01,
        source=None,
        ):
        """
        Constructs a control-rate LastValue.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> last_value = supriya.ugens.LastValue.kr(
            ...     diff=0.01,
            ...     source=source,
            ...     )
            >>> last_value
            LastValue.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            diff=diff,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def diff(self):
        """
        Gets `diff` input of LastValue.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> last_value = supriya.ugens.LastValue.ar(
            ...     diff=0.01,
            ...     source=source,
            ...     )
            >>> last_value.diff
            0.01

        Returns ugen input.
        """
        index = self._ordered_input_names.index('diff')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of LastValue.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> last_value = supriya.ugens.LastValue.ar(
            ...     diff=0.01,
            ...     source=source,
            ...     )
            >>> last_value.source
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
