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

    ### PUBLIC PROPERTIES ###

    @property
    def decay_time(self):
        r'''Gets `decay_time` input of AllpassC.

        ::

            >>> decay_time = None
            >>> allpass_c = ugentools.AllpassC.ar(
            ...     decay_time=decay_time,
            ...     )
            >>> allpass_c.decay_time

        Returns input.
        '''
        index = self._ordered_input_names.index('decay_time')
        return self._inputs[index]

    @property
    def delay_time(self):
        r'''Gets `delay_time` input of AllpassC.

        ::

            >>> delay_time = None
            >>> allpass_c = ugentools.AllpassC.ar(
            ...     delay_time=delay_time,
            ...     )
            >>> allpass_c.delay_time

        Returns input.
        '''
        index = self._ordered_input_names.index('delay_time')
        return self._inputs[index]

    @property
    def maximum_delay_time(self):
        r'''Gets `maximum_delay_time` input of AllpassC.

        ::

            >>> maximum_delay_time = None
            >>> allpass_c = ugentools.AllpassC.ar(
            ...     maximum_delay_time=maximum_delay_time,
            ...     )
            >>> allpass_c.maximum_delay_time

        Returns input.
        '''
        index = self._ordered_input_names.index('maximum_delay_time')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of AllpassC.

        ::

            >>> source = None
            >>> allpass_c = ugentools.AllpassC.ar(
            ...     source=source,
            ...     )
            >>> allpass_c.source

        Returns input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]