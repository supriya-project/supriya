# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.UGen import UGen


class LFClipNoise(UGen):
    r'''A dynamic clipped noise generator.

    ::

        >>> ugentools.LFClipNoise.ar()
        LFClipNoise.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Noise UGens'

    __slots__ = ()

    _ordered_input_names = (
        'frequency',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        frequency=500,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            frequency=frequency,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        frequency=500,
        ):
        r'''Constructs an audio-rate clipped noise generator.

        ::

            >>> ugentools.LFClipNoise.ar(
            ...     frequency=10,
            ...     )
            LFClipNoise.ar()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        frequency=500,
        ):
        r'''Constructs a control-rate clipped noise generator.

        ::

            >>> ugentools.LFClipNoise.kr(
            ...     frequency=10,
            ...     )
            LFClipNoise.kr()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def frequency(self):
        r'''Gets `frequency` input of LFClipNoise.

        ::

            >>> frequency = 0.5
            >>> lf_noise_0 = ugentools.LFClipNoise.ar(
            ...     frequency=frequency,
            ...     )
            >>> lf_noise_0.frequency
            0.5

        Returns input.
        '''
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]