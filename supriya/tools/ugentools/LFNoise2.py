# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class LFNoise2(UGen):
    r'''A quadratic noise generator.

    ::

        >>> ugentools.LFNoise2.ar()
        LFNoise2.ar()

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
        r'''Creates an audio-rate quadratic noise generator.

        ::

            >>> ugentools.LFNoise2.ar(
            ...     frequency=10,
            ...     )
            LFNoise2.ar()

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
        r'''Creates a control-rate quadratic noise generator.

        ::

            >>> ugentools.LFNoise2.kr(
            ...     frequency=10,
            ...     )
            LFNoise2.kr()

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
        r'''Gets `frequency` input of LFNoise2.

        ::

            >>> frequency = 0.5
            >>> lf_noise_0 = ugentools.LFNoise2.ar(
            ...     frequency=frequency,
            ...     )
            >>> lf_noise_0.frequency
            0.5

        Returns input.
        '''
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]