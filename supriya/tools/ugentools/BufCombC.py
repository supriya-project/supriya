# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.BufCombN import BufCombN


class BufCombC(BufCombN):
    r'''Buffer-based cubic-interpolating comb delay line unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> buffer_id = 0
        >>> source = ugentools.In.ar(bus=0)
        >>> ugentools.BufCombC.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ...     )
        BufCombC.ar()

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
        r'''Create an audio-rate buffer-based cubic-interpolating comb delay
        line.

        ::

            >>> from supriya.tools import ugentools
            >>> buffer_id = 0
            >>> source = ugentools.In.ar(bus=0)
            >>> ugentools.BufCombC.ar(
            ...     buffer_id=buffer_id,
            ...     decay_time=1.0,
            ...     delay_time=0.2,
            ...     maximum_delay_time=0.2,
            ...     source=source,
            ...     )
            BufCombC.ar()

        Returns unit generator graph.
        '''
        return super(BufCombC, cls).ar(
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
        r'''Create a control-rate buffer-based cubic-interpolating comb delay
        line.

        ::

            >>> from supriya.tools import ugentools
            >>> buffer_id = 0
            >>> source = ugentools.In.kr(bus=0)
            >>> ugentools.BufCombC.kr(
            ...     buffer_id=buffer_id,
            ...     decay_time=1.0,
            ...     delay_time=0.2,
            ...     maximum_delay_time=0.2,
            ...     source=source,
            ...     )
            BufCombC.ar()

        Returns unit generator graph.
        '''
        return super(BufCombC, cls).kr(
            buffer_id=buffer_id,
            decay_time=decay_time,
            delay_time=delay_time,
            maximum_delay_time=maximum_delay_time,
            source=source,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        r'''Gets `buffer_id` input of BufCombC.

        ::

            >>> buffer_id = None
            >>> buf_comb_c = ugentools.BufCombC.ar(
            ...     buffer_id=buffer_id,
            ...     )
            >>> buf_comb_c.buffer_id

        Returns input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def decay_time(self):
        r'''Gets `decay_time` input of BufCombC.

        ::

            >>> decay_time = None
            >>> buf_comb_c = ugentools.BufCombC.ar(
            ...     decay_time=decay_time,
            ...     )
            >>> buf_comb_c.decay_time

        Returns input.
        '''
        index = self._ordered_input_names.index('decay_time')
        return self._inputs[index]

    @property
    def delay_time(self):
        r'''Gets `delay_time` input of BufCombC.

        ::

            >>> delay_time = None
            >>> buf_comb_c = ugentools.BufCombC.ar(
            ...     delay_time=delay_time,
            ...     )
            >>> buf_comb_c.delay_time

        Returns input.
        '''
        index = self._ordered_input_names.index('delay_time')
        return self._inputs[index]

    @property
    def maximum_delay_time(self):
        r'''Gets `maximum_delay_time` input of BufCombC.

        ::

            >>> maximum_delay_time = None
            >>> buf_comb_c = ugentools.BufCombC.ar(
            ...     maximum_delay_time=maximum_delay_time,
            ...     )
            >>> buf_comb_c.maximum_delay_time

        Returns input.
        '''
        index = self._ordered_input_names.index('maximum_delay_time')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of BufCombC.

        ::

            >>> source = None
            >>> buf_comb_c = ugentools.BufCombC.ar(
            ...     source=source,
            ...     )
            >>> buf_comb_c.source

        Returns input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]