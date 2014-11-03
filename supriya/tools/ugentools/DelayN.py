# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PureUGen import PureUGen


class DelayN(PureUGen):
    r'''Non-interpolating delay line unit generator.

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> ugentools.DelayN.ar(source=source)
        DelayN.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Delay UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'maximum_delay_time',
        'delay_time',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        delay_time=0.2,
        maximum_delay_time=0.2,
        source=None,
        ):
        PureUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            delay_time=delay_time,
            maximum_delay_time=maximum_delay_time,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        delay_time=0.2,
        maximum_delay_time=0.2,
        source=None,
        ):
        r'''Create an audio-calculation_rate non-interpolating delay line.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> ugentools.DelayN.ar(
            ...     delay_time=0.5,
            ...     maximum_delay_time=1.0,
            ...     source=source,
            ...     )
            DelayN.ar()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        source = cls._as_audio_rate_input(source)
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            delay_time=delay_time,
            maximum_delay_time=maximum_delay_time,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        delay_time=0.2,
        maximum_delay_time=0.2,
        source=None,
        ):
        r'''Create a control-calculation_rate non-interpolating delay line.

        ::

            >>> source = ugentools.In.kr(bus=0)
            >>> ugentools.DelayN.kr(
            ...     delay_time=0.5,
            ...     maximum_delay_time=1.0,
            ...     source=source,
            ...     )
            DelayN.ar()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            delay_time=delay_time,
            maximum_delay_time=maximum_delay_time,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def delay_time(self):
        r'''Gets `delay_time` input of DelayN.

        ::

            >>> delay_time = 1.5
            >>> source = ugentools.In.ar(bus=0)
            >>> delay_n = ugentools.DelayN.ar(
            ...     delay_time=delay_time,
            ...     source=source,
            ...     )
            >>> delay_n.delay_time
            1.5

        Returns input.
        '''
        index = self._ordered_input_names.index('delay_time')
        return self._inputs[index]

    @property
    def maximum_delay_time(self):
        r'''Gets `maximum_delay_time` input of DelayN.

        ::

            >>> maximum_delay_time = 2.0
            >>> source = ugentools.In.ar(bus=0)
            >>> delay_n = ugentools.DelayN.ar(
            ...     maximum_delay_time=maximum_delay_time,
            ...     source=source,
            ...     )
            >>> delay_n.maximum_delay_time
            2.0

        Returns input.
        '''
        index = self._ordered_input_names.index('maximum_delay_time')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of DelayN.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> delay_n = ugentools.DelayN.ar(
            ...     source=source,
            ...     )
            >>> delay_n.source
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