# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.BufAllpassN import BufAllpassN


class BufAllpassC(BufAllpassN):
    r'''Buffer-based cubic-interpolating allpass delay line unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> buffer_id = 0
        >>> source = ugentools.In.ar(bus=0)
        >>> ugentools.BufAllpassC.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ...     )
        BufAllpassC.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Delay UGens'

    __slots__ = ()

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer_id=None,
        decay_time=1.0,
        delay_time=0.2,
        maximum_delay_time=0.2,
        source=None,
        ):
        r'''Create an audio-rate buffer-based cubic-interpolating allpass
        delay line.

        ::

            >>> from supriya.tools import ugentools
            >>> buffer_id = 0
            >>> source = ugentools.In.ar(bus=0)
            >>> ugentools.BufAllpassC.ar(
            ...     buffer_id=buffer_id,
            ...     decay_time=1.0,
            ...     delay_time=0.2,
            ...     maximum_delay_time=0.2,
            ...     source=source,
            ...     )
            BufAllpassC.ar()

        Returns unit generator graph.
        '''
        return super(BufAllpassC, cls).ar(
            buffer_id=buffer_id,
            decay_time=decay_time,
            delay_time=delay_time,
            maximum_delay_time=maximum_delay_time,
            source=source,
            )

    @classmethod
    def kr(
        cls,
        buffer_id=None,
        decay_time=1.0,
        delay_time=0.2,
        maximum_delay_time=0.2,
        source=None,
        ):
        r'''Create a control-rate buffer-based cubic-interpolating allpass
        delay line.

        ::

            >>> from supriya.tools import ugentools
            >>> buffer_id = 0
            >>> source = ugentools.In.kr(bus=0)
            >>> ugentools.BufAllpassC.kr(
            ...     buffer_id=buffer_id,
            ...     decay_time=1.0,
            ...     delay_time=0.2,
            ...     maximum_delay_time=0.2,
            ...     source=source,
            ...     )
            BufAllpassC.ar()

        Returns unit generator graph.
        '''
        return super(BufAllpassC, cls).kr(
            buffer_id=buffer_id,
            decay_time=decay_time,
            delay_time=delay_time,
            maximum_delay_time=maximum_delay_time,
            source=source,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        r'''Gets `buffer_id` input of BufAllpassC.

        ::

            >>> buffer_id = 23
            >>> buf_allpass_c = ugentools.BufAllpassC.ar(
            ...     buffer_id=buffer_id,
            ...     )
            >>> buf_allpass_c.buffer_id
            23.0

        Returns input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def decay_time(self):
        r'''Gets `decay_time` input of BufAllpassC.

        ::

            >>> decay_time = 1.0
            >>> buf_allpass_c = ugentools.BufAllpassC.ar(
            ...     decay_time=decay_time,
            ...     )
            >>> buf_allpass_c.decay_time
            1.0

        Returns input.
        '''
        index = self._ordered_input_names.index('decay_time')
        return self._inputs[index]

    @property
    def delay_time(self):
        r'''Gets `delay_time` input of BufAllpassC.

        ::

            >>> delay_time = 1.5
            >>> buf_allpass_c = ugentools.BufAllpassC.ar(
            ...     delay_time=delay_time,
            ...     )
            >>> buf_allpass_c.delay_time
            1.5

        Returns input.
        '''
        index = self._ordered_input_names.index('delay_time')
        return self._inputs[index]

    @property
    def maximum_delay_time(self):
        r'''Gets `maximum_delay_time` input of BufAllpassC.

        ::

            >>> maximum_delay_time = 2.0
            >>> buf_allpass_c = ugentools.BufAllpassC.ar(
            ...     maximum_delay_time=maximum_delay_time,
            ...     )
            >>> buf_allpass_c.maximum_delay_time
            2.0

        Returns input.
        '''
        index = self._ordered_input_names.index('maximum_delay_time')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of BufAllpassC.

        ::

            >>> source = None
            >>> buf_allpass_c = ugentools.BufAllpassC.ar(
            ...     source=source,
            ...     )
            >>> buf_allpass_c.source

        Returns input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]