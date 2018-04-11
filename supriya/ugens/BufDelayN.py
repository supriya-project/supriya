from supriya.ugens.PureUGen import PureUGen


class BufDelayN(PureUGen):
    """
    A buffer-based non-interpolating delay line unit generator.

    ::

        >>> buffer_id = 0
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.BufDelayN.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ...     )
        BufDelayN.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Delay UGens'

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        'source',
        'maximum_delay_time',
        'delay_time',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_id=None,
        calculation_rate=None,
        delay_time=0.2,
        maximum_delay_time=0.2,
        source=None,
        ):
        PureUGen.__init__(
            self,
            buffer_id=int(buffer_id),
            calculation_rate=calculation_rate,
            delay_time=delay_time,
            maximum_delay_time=maximum_delay_time,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer_id=None,
        delay_time=0.2,
        maximum_delay_time=0.2,
        source=None,
        ):
        """
        Constructs an audio-rate buffer-based non-interpolating delay line.

        ::

            >>> buffer_id = 0
            >>> source = supriya.ugens.In.ar(bus=0)
            >>> supriya.ugens.BufDelayN.ar(
            ...     buffer_id=buffer_id,
            ...     delay_time=0.5,
            ...     maximum_delay_time=1.0,
            ...     source=source,
            ...     )
            BufDelayN.ar()

        Returns unit generator graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        source = cls._as_audio_rate_input(source)
        ugen = cls._new_expanded(
            buffer_id=buffer_id,
            calculation_rate=calculation_rate,
            delay_time=delay_time,
            maximum_delay_time=maximum_delay_time,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        buffer_id=None,
        delay_time=0.2,
        maximum_delay_time=0.2,
        source=None,
        ):
        """
        Constructs a control-rate buffer-based non-interpolating delay line.

        ::

            >>> buffer_id = 0
            >>> source = supriya.ugens.In.kr(bus=0)
            >>> supriya.ugens.BufDelayN.kr(
            ...     buffer_id=buffer_id,
            ...     delay_time=0.5,
            ...     maximum_delay_time=1.0,
            ...     source=source,
            ...     )
            BufDelayN.ar()

        Returns unit generator graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            buffer_id=buffer_id,
            calculation_rate=calculation_rate,
            delay_time=delay_time,
            maximum_delay_time=maximum_delay_time,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        """
        Gets `buffer_id` input of BufDelayN.

        ::

            >>> buffer_id = 23
            >>> source = supriya.ugens.In.ar(bus=0)
            >>> buf_delay_n = supriya.ugens.BufDelayN.ar(
            ...     buffer_id=buffer_id,
            ...     source=source,
            ...     )
            >>> buf_delay_n.buffer_id
            23.0

        Returns input.
        """
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def delay_time(self):
        """
        Gets `delay_time` input of BufDelayN.

        ::

            >>> buffer_id = 23
            >>> delay_time = 1.5
            >>> source = supriya.ugens.In.ar(bus=0)
            >>> buf_delay_n = supriya.ugens.BufDelayN.ar(
            ...     buffer_id=buffer_id,
            ...     delay_time=delay_time,
            ...     source=source,
            ...     )
            >>> buf_delay_n.delay_time
            1.5

        Returns input.
        """
        index = self._ordered_input_names.index('delay_time')
        return self._inputs[index]

    @property
    def maximum_delay_time(self):
        """
        Gets `maximum_delay_time` input of BufDelayN.

        ::

            >>> buffer_id = 23
            >>> maximum_delay_time = 2.0
            >>> source = supriya.ugens.In.ar(bus=0)
            >>> buf_delay_n = supriya.ugens.BufDelayN.ar(
            ...     buffer_id=buffer_id,
            ...     maximum_delay_time=maximum_delay_time,
            ...     source=source,
            ...     )
            >>> buf_delay_n.maximum_delay_time
            2.0

        Returns input.
        """
        index = self._ordered_input_names.index('maximum_delay_time')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of BufDelayN.

        ::

            >>> buffer_id = 23
            >>> source = supriya.ugens.In.ar(bus=0)
            >>> buf_delay_n = supriya.ugens.BufDelayN.ar(
            ...     buffer_id=buffer_id,
            ...     source=source,
            ...     )
            >>> buf_delay_n.source
            In.ar()[0]

        Returns input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
