# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.DelayN import DelayN


class DelayC(DelayN):
    r'''A cubic-interpolating delay line unit generator.

    ::

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

            >>> delay_time = 1.5
            >>> source = ugentools.In.ar(bus=0)
            >>> delay_c = ugentools.DelayC.ar(
            ...     delay_time=delay_time,
            ...     source=source,
            ...     )
            >>> delay_c.delay_time
            1.5

        Returns input.
        '''
        index = self._ordered_input_names.index('delay_time')
        return self._inputs[index]

    @property
    def maximum_delay_time(self):
        r'''Gets `maximum_delay_time` input of DelayC.

        ::

            >>> maximum_delay_time = 2.0
            >>> source = ugentools.In.ar(bus=0)
            >>> delay_c = ugentools.DelayC.ar(
            ...     maximum_delay_time=maximum_delay_time,
            ...     source=source,
            ...     )
            >>> delay_c.maximum_delay_time
            2.0

        Returns input.
        '''
        index = self._ordered_input_names.index('maximum_delay_time')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of DelayC.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> delay_c = ugentools.DelayC.ar(
            ...     source=source,
            ...     )
            >>> delay_c.source
            OutputProxy(
                source=In(
                    bus=0.0,
                    calculation_rate=<CalculationRate.AUDIO: 2>,
                    channel_count=1
                    ),
                output_index=0
                )

        Returns input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]