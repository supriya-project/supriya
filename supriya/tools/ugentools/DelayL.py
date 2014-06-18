# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.DelayN import DelayN


class DelayL(DelayN):
    r'''Linear interpolating delay line unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> source = ugentools.In.ar(bus=0)
        >>> ugentools.DelayL.ar(source=source)
        DelayL.ar()

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        delay_time=0.2,
        maximum_delay_time=0.2,
        source=None,
        ):
        r'''Create an audio-rate linear-interpolating delay line.

        ::

            >>> from supriya.tools import ugentools
            >>> in_ = ugentools.In.ar(bus=0)
            >>> ugentools.DelayL.ar(
            ...     delay_time=0.5,
            ...     maximum_delay_time=1.0,
            ...     source=in_,
            ...     )
            DelayL.ar()

        Returns unit generator graph.
        '''
        return super(DelayL, cls).ar(
            delay_time=delay_time,
            maximum_delay_time=maximum_delay_time,
            source=source,
            )

    @classmethod
    def kr(
        cls,
        delay_time=0.2,
        maximum_delay_time=0.2,
        source=None,
        ):
        r'''Create a control-rate linear-interpolating delay line.

        ::

            >>> from supriya.tools import ugentools
            >>> in_ = ugentools.In.kr(bus=0)
            >>> ugentools.DelayL.kr(
            ...     delay_time=0.5,
            ...     maximum_delay_time=1.0,
            ...     source=in_,
            ...     )
            DelayL.ar()

        Returns unit generator graph.
        '''
        return super(DelayL, cls).kr(
            delay_time=delay_time,
            maximum_delay_time=maximum_delay_time,
            source=source,
            )
