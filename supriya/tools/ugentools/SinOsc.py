# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PureUGen import PureUGen


class SinOsc(PureUGen):
    r'''A sinusoid oscillator unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> ugentools.SinOsc.ar()
        SinOsc.ar()

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_input_names = (
        'frequency',
        'phase',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        frequency=440.,
        phase=0.,
        ):
        PureUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            frequency=frequency,
            phase=phase,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        frequency=440,
        phase=0,
        ):
        r'''Creates an audio-rate sinusoid oscillator.

        ::

            >>> from supriya.tools import ugentools
            >>> ugentools.SinOsc.ar(
            ...     frequency=443,
            ...     phase=0.25,
            ...     )
            SinOsc.ar()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new(
            calculation_rate=calculation_rate,
            frequency=frequency,
            phase=phase,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        frequency=440,
        phase=0,
        ):
        r'''Creates a control-rate sinusoid oscillator.

        ::

            >>> from supriya.tools import ugentools
            >>> ugentools.SinOsc.kr(
            ...     frequency=443,
            ...     phase=0.25,
            ...     )
            SinOsc.kr()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new(
            calculation_rate=calculation_rate,
            frequency=frequency,
            phase=phase,
            )
        return ugen
