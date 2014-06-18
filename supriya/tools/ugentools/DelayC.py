# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.DelayN import DelayN


class DelayC(DelayN):
    r'''Cubic-interpolating delay line unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> source = ugentools.In.ar(bus=0)
        >>> ugentools.DelayC.ar(source=source)
        DelayC.ar()

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
        r'''Create an audio-rate cubic-interpolating delay line.

        ::

            >>> from supriya.tools import ugentools
            >>> in_ = ugentools.In.ar(bus=0)
            >>> ugentools.DelayC.ar(
            ...     delay_time=0.5,
            ...     maximum_delay_time=1.0,
            ...     source=in_,
            ...     )
            DelayC.ar()

        Returns unit generator graph.
        '''
        return super(DelayC, cls).ar(
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
        r'''Create a control-rate cubic-interpolating delay line.

        ::

            >>> from supriya.tools import ugentools
            >>> in_ = ugentools.In.kr(bus=0)
            >>> ugentools.DelayC.kr(
            ...     delay_time=0.5,
            ...     maximum_delay_time=1.0,
            ...     source=in_,
            ...     )
            DelayC.ar()

        Returns unit generator graph.
        '''
        return super(DelayC, cls).kr(
            delay_time=delay_time,
            maximum_delay_time=maximum_delay_time,
            source=source,
            )
