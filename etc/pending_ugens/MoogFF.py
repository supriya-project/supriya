from supriya.ugens.Filter import Filter


class MoogFF(Filter):
    """

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> moog_ff = supriya.ugens.MoogFF.ar(
        ...     frequency=100,
        ...     gain=2,
        ...     reset=0,
        ...     source=source,
        ...     )
        >>> moog_ff
        MoogFF.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'frequency',
        'gain',
        'reset',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        frequency=100,
        gain=2,
        reset=0,
        source=None,
        ):
        Filter.__init__(
            self,
            calculation_rate=calculation_rate,
            frequency=frequency,
            gain=gain,
            reset=reset,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        frequency=100,
        gain=2,
        reset=0,
        source=None,
        ):
        """
        Constructs an audio-rate MoogFF.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> moog_ff = supriya.ugens.MoogFF.ar(
            ...     frequency=100,
            ...     gain=2,
            ...     reset=0,
            ...     source=source,
            ...     )
            >>> moog_ff
            MoogFF.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            gain=gain,
            reset=reset,
            source=source,
            )
        return ugen

    # def coeffs(): ...

    @classmethod
    def kr(
        cls,
        frequency=100,
        gain=2,
        reset=0,
        source=None,
        ):
        """
        Constructs a control-rate MoogFF.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> moog_ff = supriya.ugens.MoogFF.kr(
            ...     frequency=100,
            ...     gain=2,
            ...     reset=0,
            ...     source=source,
            ...     )
            >>> moog_ff
            MoogFF.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            gain=gain,
            reset=reset,
            source=source,
            )
        return ugen

    # def magResponse(): ...

    # def magResponse2(): ...

    # def magResponse5(): ...

    # def magResponseN(): ...

    # def scopeResponse(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def frequency(self):
        """
        Gets `frequency` input of MoogFF.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> moog_ff = supriya.ugens.MoogFF.ar(
            ...     frequency=100,
            ...     gain=2,
            ...     reset=0,
            ...     source=source,
            ...     )
            >>> moog_ff.frequency
            100.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def gain(self):
        """
        Gets `gain` input of MoogFF.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> moog_ff = supriya.ugens.MoogFF.ar(
            ...     frequency=100,
            ...     gain=2,
            ...     reset=0,
            ...     source=source,
            ...     )
            >>> moog_ff.gain
            2.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('gain')
        return self._inputs[index]

    @property
    def reset(self):
        """
        Gets `reset` input of MoogFF.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> moog_ff = supriya.ugens.MoogFF.ar(
            ...     frequency=100,
            ...     gain=2,
            ...     reset=0,
            ...     source=source,
            ...     )
            >>> moog_ff.reset
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('reset')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of MoogFF.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> moog_ff = supriya.ugens.MoogFF.ar(
            ...     frequency=100,
            ...     gain=2,
            ...     reset=0,
            ...     source=source,
            ...     )
            >>> moog_ff.source
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
