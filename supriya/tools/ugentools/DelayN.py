# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.Argument import Argument
from supriya.tools.ugentools.PureUGen import PureUGen


class DelayN(PureUGen):
    r'''Non-interpolating delay line unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> source = ugentools.In.ar(bus=0)
        >>> ugentools.DelayN.ar(source=source)
        DelayN.ar()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    _argument_specifications = (
        Argument('source'),
        Argument('maximum_delay_time', 0.2),
        Argument('delay_time', 0.2),
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
        r'''Create an audio-rate non-interpolating delay line.

        ::

            >>> from supriya.tools import ugentools
            >>> in_ = ugentools.In.ar(bus=0)
            >>> ugentools.DelayN.ar(
            ...     delay_time=0.5,
            ...     maximum_delay_time=1.0,
            ...     source=in_,
            ...     )
            DelayN.ar()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        source = cls.as_audio_rate_input(source)
        ugen = cls._new(
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
        r'''Create a control-rate non-interpolating delay line.

        ::

            >>> from supriya.tools import ugentools
            >>> in_ = ugentools.In.kr(bus=0)
            >>> ugentools.DelayN.kr(
            ...     delay_time=0.5,
            ...     maximum_delay_time=1.0,
            ...     source=in_,
            ...     )
            DelayN.ar()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new(
            calculation_rate=calculation_rate,
            delay_time=delay_time,
            maximum_delay_time=maximum_delay_time,
            source=source,
            )
        return ugen
