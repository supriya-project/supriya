# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PureUGen import PureUGen


class SinOsc(PureUGen):
    r'''A sinusoid oscillator unit generator.

    ::

        >>> ugentools.SinOsc.ar()
        SinOsc.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Oscillator UGens'

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

            >>> ugentools.SinOsc.ar(
            ...     frequency=443,
            ...     phase=0.25,
            ...     )
            SinOsc.ar()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
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

            >>> ugentools.SinOsc.kr(
            ...     frequency=443,
            ...     phase=0.25,
            ...     )
            SinOsc.kr()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            phase=phase,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def frequency(self):
        r'''Gets `frequency` input of SinOsc.

        ::

            >>> frequency = 442
            >>> sin_osc = ugentools.SinOsc.ar(
            ...     frequency=frequency,
            ...     )
            >>> sin_osc.frequency
            442.0

        Returns input.
        '''
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def phase(self):
        r'''Gets `phase` input of SinOsc.

        ::

            >>> phase = 0.5
            >>> sin_osc = ugentools.SinOsc.ar(
            ...     phase=phase,
            ...     )
            >>> sin_osc.phase
            0.5

        Returns input.
        '''
        index = self._ordered_input_names.index('phase')
        return self._inputs[index]