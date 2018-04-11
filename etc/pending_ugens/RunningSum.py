from supriya.tools.ugentools.UGen import UGen


class RunningSum(UGen):
    """

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> running_sum = ugentools.RunningSum.ar(
        ...     numsamp=40,
        ...     source=source,
        ...     )
        >>> running_sum
        RunningSum.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'numsamp',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        numsamp=40,
        source=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            numsamp=numsamp,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        numsamp=40,
        source=None,
        ):
        """
        Constructs an audio-rate RunningSum.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> running_sum = ugentools.RunningSum.ar(
            ...     numsamp=40,
            ...     source=source,
            ...     )
            >>> running_sum
            RunningSum.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            numsamp=numsamp,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        numsamp=40,
        source=None,
        ):
        """
        Constructs a control-rate RunningSum.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> running_sum = ugentools.RunningSum.kr(
            ...     numsamp=40,
            ...     source=source,
            ...     )
            >>> running_sum
            RunningSum.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            numsamp=numsamp,
            source=source,
            )
        return ugen

    # def rms(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def numsamp(self):
        """
        Gets `numsamp` input of RunningSum.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> running_sum = ugentools.RunningSum.ar(
            ...     numsamp=40,
            ...     source=source,
            ...     )
            >>> running_sum.numsamp
            40.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('numsamp')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of RunningSum.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> running_sum = ugentools.RunningSum.ar(
            ...     numsamp=40,
            ...     source=source,
            ...     )
            >>> running_sum.source
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
