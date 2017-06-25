from supriya.tools.ugentools.AllpassN import AllpassN


class AllpassC(AllpassN):
    """
    A cubic-interpolating allpass delay line unit generator.

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> allpass_c = ugentools.AllpassC.ar(source=source)
        >>> allpass_c
        AllpassC.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Delay UGens'

    __slots__ = ()

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        decay_time=1.0,
        delay_time=0.2,
        maximum_delay_time=0.2,
        source=None,
        ):
        """
        Constructs an audio-rate cubic-interpolating allpass delay line.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> allpass_c = ugentools.AllpassC.ar(
            ...     decay_time=1.0,
            ...     delay_time=0.2,
            ...     maximum_delay_time=0.2,
            ...     source=source,
            ...     )
            >>> allpass_c
            AllpassC.ar()

        Returns unit generator graph.
        """
        return super(AllpassC, cls).ar(
            decay_time=decay_time,
            delay_time=delay_time,
            maximum_delay_time=maximum_delay_time,
            source=source,
            )

    @classmethod
    def kr(
        cls,
        decay_time=1.0,
        delay_time=0.2,
        maximum_delay_time=0.2,
        source=None,
        ):
        """
        Constructs a control-rate cubic-interpolating allpass delay line.

        ::

            >>> source = ugentools.In.kr(bus=0)
            >>> allpass_c = ugentools.AllpassC.kr(
            ...     decay_time=1.0,
            ...     delay_time=0.2,
            ...     maximum_delay_time=0.2,
            ...     source=source,
            ...     )
            >>> allpass_c
            AllpassC.ar()

        Returns unit generator graph.
        """
        return super(AllpassC, cls).kr(
            decay_time=decay_time,
            delay_time=delay_time,
            maximum_delay_time=maximum_delay_time,
            source=source,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def decay_time(self):
        """
        Gets `decay_time` input of AllpassC.

        ::

            >>> decay_time = 1.0
            >>> source = ugentools.In.ar(bus=0)
            >>> allpass_c = ugentools.AllpassC.ar(
            ...     decay_time=decay_time,
            ...     source=source,
            ...     )
            >>> allpass_c.decay_time
            1.0

        Returns input.
        """
        index = self._ordered_input_names.index('decay_time')
        return self._inputs[index]

    @property
    def delay_time(self):
        """
        Gets `delay_time` input of AllpassC.

        ::

            >>> delay_time = 1.5
            >>> source = ugentools.In.ar(bus=0)
            >>> allpass_c = ugentools.AllpassC.ar(
            ...     delay_time=delay_time,
            ...     source=source,
            ...     )
            >>> allpass_c.delay_time
            1.5

        Returns input.
        """
        index = self._ordered_input_names.index('delay_time')
        return self._inputs[index]

    @property
    def maximum_delay_time(self):
        """
        Gets `maximum_delay_time` input of AllpassC.

        ::

            >>> maximum_delay_time = 2.0
            >>> source = ugentools.In.ar(bus=0)
            >>> allpass_c = ugentools.AllpassC.ar(
            ...     maximum_delay_time=maximum_delay_time,
            ...     source=source,
            ...     )
            >>> allpass_c.maximum_delay_time
            2.0

        Returns input.
        """
        index = self._ordered_input_names.index('maximum_delay_time')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of AllpassC.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> allpass_c = ugentools.AllpassC.ar(
            ...     source=source,
            ...     )
            >>> allpass_c.source
            OutputProxy(
                source=In(
                    bus=0.0,
                    calculation_rate=CalculationRate.AUDIO,
                    channel_count=1
                    ),
                output_index=0
                )

        Returns input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
