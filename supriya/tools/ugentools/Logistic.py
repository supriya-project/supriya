# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Logistic(UGen):
    r'''A chaotic noise function.

    ::

        >>> logistic = ugentools.Logistic.ar(
        ...     chaos_parameter=3.,
        ...     frequency=1000,
        ...     initial_y=0.5,
        ...     )
        >>> logistic
        Logistic.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Noise UGens'

    __slots__ = ()

    _ordered_input_names = (
        'chaos_parameter',
        'frequency',
        'initial_y',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        chaos_parameter=3,
        frequency=1000,
        initial_y=0.5,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            chaos_parameter=chaos_parameter,
            frequency=frequency,
            initial_y=initial_y,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        chaos_parameter=3,
        frequency=1000,
        initial_y=0.5,
        ):
        r'''Constructs an audio-rate chaotic noise function.

        ::

            >>> logistic = ugentools.Logistic.ar(
            ...     chaos_parameter=3.,
            ...     frequency=[666, 1000],
            ...     initial_y=0.5,
            ...     )
            >>> logistic
            UGenArray({2})

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            chaos_parameter=chaos_parameter,
            frequency=frequency,
            initial_y=initial_y,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        chaos_parameter=3,
        frequency=1000,
        initial_y=0.5,
        ):
        r'''Constructs a control-rate chaotic noise function.

        ::

            >>> logistic = ugentools.Logistic.kr(
            ...     chaos_parameter=3.,
            ...     frequency=[6, 10],
            ...     initial_y=0.5,
            ...     )
            >>> logistic
            UGenArray({2})

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            chaos_parameter=chaos_parameter,
            frequency=frequency,
            initial_y=initial_y,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def chaos_parameter(self):
        r'''Gets `chaos_parameter` input of Logistic.

        ::

            >>> logistic = ugentools.Logistic.ar(
            ...     chaos_parameter=3.,
            ...     frequency=1000,
            ...     initial_y=0.5,
            ...     )
            >>> logistic.chaos_parameter
            3.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('chaos_parameter')
        return self._inputs[index]

    @property
    def frequency(self):
        r'''Gets `frequency` input of Logistic.

        ::

            >>> logistic = ugentools.Logistic.ar(
            ...     chaos_parameter=3.,
            ...     frequency=1000,
            ...     initial_y=0.5,
            ...     )
            >>> logistic.frequency
            1000.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def initial_y(self):
        r'''Gets `initial_y` input of Logistic.

        ::

            >>> logistic = ugentools.Logistic.ar(
            ...     chaos_parameter=3.,
            ...     frequency=1000,
            ...     initial_y=0.5,
            ...     )
            >>> logistic.initial_y
            0.5

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('initial_y')
        return self._inputs[index]
