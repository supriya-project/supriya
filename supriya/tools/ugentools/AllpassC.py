# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.AllpassN import AllpassN


class AllpassC(AllpassN):
    r'''Cubic-interpolating allpass delay line unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> source = ugentools.In.ar(bus=0)
        >>> allpass_c = ugentools.AllpassC.ar(source=source)
        >>> allpass_c
        AllpassC.ar()

    '''

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
        r'''Create an audio-rate cubic-interpolating allpass delay line.

        ::

            >>> from supriya.tools import ugentools
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
        '''
        return super(AllpassC, cls).ar(
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
        r'''Create a control-rate cubic-interpolating allpass delay line.

        ::

            >>> from supriya.tools import ugentools
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
        '''
        return super(AllpassC, cls).kr(
            delay_time=delay_time,
            maximum_delay_time=maximum_delay_time,
            source=source,
            )