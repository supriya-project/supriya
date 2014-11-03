# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.BufDelayN import BufDelayN


class BufDelayL(BufDelayN):
    r'''Buffer-based linear-interpolating delay line unit generator.

    ::

        >>> buffer_id = 0
        >>> source = ugentools.In.ar(bus=0)
        >>> ugentools.BufDelayL.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ...     )
        BufDelayL.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Delay UGens'

    __slots__ = ()

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer_id=None,
        delay_time=0.2,
        maximum_delay_time=0.2,
        source=None,
        ):
        r'''Create an audio-rate buffer-based linear-interpolating delay line.

        ::

            >>> buffer_id = 0
            >>> source = ugentools.In.ar(bus=0)
            >>> ugentools.BufDelayL.ar(
            ...     buffer_id=buffer_id,
            ...     delay_time=0.5,
            ...     maximum_delay_time=1.0,
            ...     source=source,
            ...     )
            BufDelayL.ar()

        Returns unit generator graph.
        '''
        return super(BufDelayL, cls).ar(
            buffer_id=buffer_id,
            delay_time=delay_time,
            maximum_delay_time=maximum_delay_time,
            source=source,
            )

    @classmethod
    def kr(
        cls,
        buffer_id=None,
        delay_time=0.2,
        maximum_delay_time=0.2,
        source=None,
        ):
        r'''Create a control-rate buffer-based linear-interpolating delay line.

        ::

            >>> buffer_id = 0
            >>> source = ugentools.In.kr(bus=0)
            >>> ugentools.BufDelayL.kr(
            ...     buffer_id=buffer_id,
            ...     delay_time=0.5,
            ...     maximum_delay_time=1.0,
            ...     source=source,
            ...     )
            BufDelayL.ar()

        Returns unit generator graph.
        '''
        return super(BufDelayL, cls).kr(
            buffer_id=buffer_id,
            delay_time=delay_time,
            maximum_delay_time=maximum_delay_time,
            source=source,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        r'''Gets `buffer_id` input of BufDelayL.

        ::

            >>> buffer_id = 23
            >>> source = ugentools.In.ar(bus=0)
            >>> buf_delay_l = ugentools.BufDelayL.ar(
            ...     buffer_id=buffer_id,
            ...     source=source,
            ...     )
            >>> buf_delay_l.buffer_id
            23.0

        Returns input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def delay_time(self):
        r'''Gets `delay_time` input of BufDelayL.

        ::

            >>> buffer_id = 23
            >>> delay_time = 1.5
            >>> source = ugentools.In.ar(bus=0)
            >>> buf_delay_l = ugentools.BufDelayL.ar(
            ...     buffer_id=buffer_id,
            ...     delay_time=delay_time,
            ...     source=source,
            ...     )
            >>> buf_delay_l.delay_time
            1.5

        Returns input.
        '''
        index = self._ordered_input_names.index('delay_time')
        return self._inputs[index]

    @property
    def maximum_delay_time(self):
        r'''Gets `maximum_delay_time` input of BufDelayL.

        ::

            >>> buffer_id = 23
            >>> maximum_delay_time = 2.0
            >>> source = ugentools.In.ar(bus=0)
            >>> buf_delay_l = ugentools.BufDelayL.ar(
            ...     buffer_id=buffer_id,
            ...     maximum_delay_time=maximum_delay_time,
            ...     source=source,
            ...     )
            >>> buf_delay_l.maximum_delay_time
            2.0

        Returns input.
        '''
        index = self._ordered_input_names.index('maximum_delay_time')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of BufDelayL.

        ::

            >>> buffer_id = 23
            >>> source = ugentools.In.ar(bus=0)
            >>> buf_delay_l = ugentools.BufDelayL.ar(
            ...     buffer_id=buffer_id,
            ...     source=source,
            ...     )
            >>> buf_delay_l.source
            OutputProxy(
                source=In(
                    bus=0.0,
                    rate=<CalculationRate.AUDIO: 2>,
                    channel_count=1
                    ),
                output_index=0
                )

        Returns input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]