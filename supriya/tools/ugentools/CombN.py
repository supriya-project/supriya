from supriya.tools.ugentools.PureUGen import PureUGen


class CombN(PureUGen):
    """
    A non-interpolating comb delay line unit generator.

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> ugentools.CombN.ar(source=source)
        CombN.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Delay UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'maximum_delay_time',
        'delay_time',
        'decay_time',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        decay_time=1.0,
        delay_time=0.2,
        maximum_delay_time=0.2,
        source=None,
        ):
        PureUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            decay_time=decay_time,
            delay_time=delay_time,
            maximum_delay_time=maximum_delay_time,
            source=source,
            )

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
        Constructs an audio-rate non-interpolating comb delay line.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> ugentools.CombN.ar(
            ...     decay_time=1.0,
            ...     delay_time=0.2,
            ...     maximum_delay_time=0.2,
            ...     source=source,
            ...     )
            CombN.ar()

        Returns unit generator graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        source = cls._as_audio_rate_input(source)
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            decay_time=decay_time,
            delay_time=delay_time,
            maximum_delay_time=maximum_delay_time,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        decay_time=1.0,
        delay_time=0.2,
        maximum_delay_time=0.2,
        source=None,
        ):
        """
        Constructs a control-rate non-interpolating comb delay line.

        ::

            >>> source = ugentools.In.kr(bus=0)
            >>> ugentools.CombN.kr(
            ...     decay_time=1.0,
            ...     delay_time=0.2,
            ...     maximum_delay_time=0.2,
            ...     source=source,
            ...     )
            CombN.ar()

        Returns unit generator graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            decay_time=decay_time,
            delay_time=delay_time,
            maximum_delay_time=maximum_delay_time,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def decay_time(self):
        """
        Gets `decay_time` input of CombN.

        ::

            >>> decay_time = 1.0
            >>> source = ugentools.In.ar(bus=0)
            >>> comb_n = ugentools.CombN.ar(
            ...     decay_time=decay_time,
            ...     source=source,
            ...     )
            >>> comb_n.decay_time
            1.0

        Returns input.
        """
        index = self._ordered_input_names.index('decay_time')
        return self._inputs[index]

    @property
    def delay_time(self):
        """
        Gets `delay_time` input of CombN.

        ::

            >>> delay_time = 1.5
            >>> source = ugentools.In.ar(bus=0)
            >>> comb_n = ugentools.CombN.ar(
            ...     delay_time=delay_time,
            ...     source=source,
            ...     )
            >>> comb_n.delay_time
            1.5

        Returns input.
        """
        index = self._ordered_input_names.index('delay_time')
        return self._inputs[index]

    @property
    def maximum_delay_time(self):
        """
        Gets `maximum_delay_time` input of CombN.

        ::

            >>> maximum_delay_time = 2.0
            >>> source = ugentools.In.ar(bus=0)
            >>> comb_n = ugentools.CombN.ar(
            ...     maximum_delay_time=maximum_delay_time,
            ...     source=source,
            ...     )
            >>> comb_n.maximum_delay_time
            2.0

        Returns input.
        """
        index = self._ordered_input_names.index('maximum_delay_time')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of CombN.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> comb_n = ugentools.CombN.ar(
            ...     source=source,
            ...     )
            >>> comb_n.source
            In.ar()[0]

        Returns input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
