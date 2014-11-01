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

    __documentation_section__ = 'Delay UGens'

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
            >>> source = ugentools.In.ar(bus=0)
            >>> ugentools.DelayC.ar(
            ...     delay_time=0.5,
            ...     maximum_delay_time=1.0,
            ...     source=source,
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
            >>> source = ugentools.In.kr(bus=0)
            >>> ugentools.DelayC.kr(
            ...     delay_time=0.5,
            ...     maximum_delay_time=1.0,
            ...     source=source,
            ...     )
            DelayC.ar()

        Returns unit generator graph.
        '''
        return super(DelayC, cls).kr(
            delay_time=delay_time,
            maximum_delay_time=maximum_delay_time,
            source=source,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def delay_time(self):
        r'''Gets `delay_time` input of DelayC.

        ::

            >>> delay_time = None
            >>> delay_c = ugentools.DelayC.ar(
            ...     delay_time=delay_time,
            ...     )
            >>> delay_c.delay_time

        Returns input.
        '''
        index = self._ordered_input_names.index('delay_time')
        return self._inputs[index]

    @property
    def maximum_delay_time(self):
        r'''Gets `maximum_delay_time` input of DelayC.

        ::

            >>> maximum_delay_time = None
            >>> delay_c = ugentools.DelayC.ar(
            ...     maximum_delay_time=maximum_delay_time,
            ...     )
            >>> delay_c.maximum_delay_time

        Returns input.
        '''
        index = self._ordered_input_names.index('maximum_delay_time')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of DelayC.

        ::

            >>> source = None
            >>> delay_c = ugentools.DelayC.ar(
            ...     source=source,
            ...     )
            >>> delay_c.source

        Returns input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]