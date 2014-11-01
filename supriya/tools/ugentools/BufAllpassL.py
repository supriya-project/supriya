# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.BufAllpassN import BufAllpassN


class BufAllpassL(BufAllpassN):
    r'''Buffer-based linear-interpolating allpass delay line unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> buffer_id = 0
        >>> source = ugentools.In.ar(bus=0)
        >>> ugentools.BufAllpassL.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ...     )
        BufAllpassL.ar()

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
        r'''Create an audio-rate buffer-based linear-interpolating allpass
        delay line.

        ::

            >>> from supriya.tools import ugentools
            >>> buffer_id = 0
            >>> source = ugentools.In.ar(bus=0)
            >>> ugentools.BufAllpassL.ar(
            ...     buffer_id=buffer_id,
            ...     decay_time=1.0,
            ...     delay_time=0.2,
            ...     maximum_delay_time=0.2,
            ...     source=source,
            ...     )
            BufAllpassL.ar()

        Returns unit generator graph.
        '''
        return super(BufAllpassL, cls).ar(
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
        r'''Create a control-rate buffer-based linear-interpolating allpass
        delay line.

        ::

            >>> from supriya.tools import ugentools
            >>> buffer_id = 0
            >>> source = ugentools.In.kr(bus=0)
            >>> ugentools.BufAllpassL.kr(
            ...     buffer_id=buffer_id,
            ...     decay_time=1.0,
            ...     delay_time=0.2,
            ...     maximum_delay_time=0.2,
            ...     source=source,
            ...     )
            BufAllpassL.ar()

        Returns unit generator graph.
        '''
        return super(BufAllpassL, cls).kr(
            buffer_id=buffer_id,
            decay_time=decay_time,
            delay_time=delay_time,
            maximum_delay_time=maximum_delay_time,
            source=source,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        r'''Gets `buffer_id` input of BufAllpassL.

        ::

            >>> buffer_id = None
            >>> buf_allpass_l = ugentools.BufAllpassL.ar(
            ...     buffer_id=buffer_id,
            ...     )
            >>> buf_allpass_l.buffer_id

        Returns input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def decay_time(self):
        r'''Gets `decay_time` input of BufAllpassL.

        ::

            >>> decay_time = None
            >>> buf_allpass_l = ugentools.BufAllpassL.ar(
            ...     decay_time=decay_time,
            ...     )
            >>> buf_allpass_l.decay_time

        Returns input.
        '''
        index = self._ordered_input_names.index('decay_time')
        return self._inputs[index]

    @property
    def delay_time(self):
        r'''Gets `delay_time` input of BufAllpassL.

        ::

            >>> delay_time = None
            >>> buf_allpass_l = ugentools.BufAllpassL.ar(
            ...     delay_time=delay_time,
            ...     )
            >>> buf_allpass_l.delay_time

        Returns input.
        '''
        index = self._ordered_input_names.index('delay_time')
        return self._inputs[index]

    @property
    def maximum_delay_time(self):
        r'''Gets `maximum_delay_time` input of BufAllpassL.

        ::

            >>> maximum_delay_time = None
            >>> buf_allpass_l = ugentools.BufAllpassL.ar(
            ...     maximum_delay_time=maximum_delay_time,
            ...     )
            >>> buf_allpass_l.maximum_delay_time

        Returns input.
        '''
        index = self._ordered_input_names.index('maximum_delay_time')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of BufAllpassL.

        ::

            >>> source = None
            >>> buf_allpass_l = ugentools.BufAllpassL.ar(
            ...     source=source,
            ...     )
            >>> buf_allpass_l.source

        Returns input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]