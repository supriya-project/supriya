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
