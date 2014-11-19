# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class PSinGrain(UGen):
    r'''

    ::

        >>> psin_grain = ugentools.PSinGrain.(
        ...     amp=1,
        ...     duration=0.2,
        ...     frequency=440,
        ...     )
        >>> psin_grain

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'frequency',
        'duration',
        'amp',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        amp=1,
        duration=0.2,
        frequency=440,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            amp=amp,
            duration=duration,
            frequency=frequency,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        amp=1,
        duration=0.2,
        frequency=440,
        ):
        r'''Constructs an audio-rate PSinGrain.

        ::

            >>> psin_grain = ugentools.PSinGrain.ar(
            ...     amp=1,
            ...     duration=0.2,
            ...     frequency=440,
            ...     )
            >>> psin_grain

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            amp=amp,
            duration=duration,
            frequency=frequency,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def frequency(self):
        r'''Gets `frequency` input of PSinGrain.

        ::

            >>> psin_grain = ugentools.PSinGrain.ar(
            ...     amp=1,
            ...     duration=0.2,
            ...     frequency=440,
            ...     )
            >>> psin_grain.frequency

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def duration(self):
        r'''Gets `duration` input of PSinGrain.

        ::

            >>> psin_grain = ugentools.PSinGrain.ar(
            ...     amp=1,
            ...     duration=0.2,
            ...     frequency=440,
            ...     )
            >>> psin_grain.duration

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('duration')
        return self._inputs[index]

    @property
    def amp(self):
        r'''Gets `amp` input of PSinGrain.

        ::

            >>> psin_grain = ugentools.PSinGrain.ar(
            ...     amp=1,
            ...     duration=0.2,
            ...     frequency=440,
            ...     )
            >>> psin_grain.amp

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('amp')
        return self._inputs[index]