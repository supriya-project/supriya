# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class FSinOsc(UGen):
    r'''

    ::

        >>> fsin_osc = ugentools.FSinOsc.ar(
        ...     frequency=440,
        ...     initial_phase=0,
        ...     )
        >>> fsin_osc
        FSinOsc.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'frequency',
        'initial_phase',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        frequency=440,
        initial_phase=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            frequency=frequency,
            initial_phase=initial_phase,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        frequency=440,
        initial_phase=0,
        ):
        r'''Constructs an audio-rate FSinOsc.

        ::

            >>> fsin_osc = ugentools.FSinOsc.ar(
            ...     frequency=440,
            ...     initial_phase=0,
            ...     )
            >>> fsin_osc
            FSinOsc.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            initial_phase=initial_phase,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        frequency=440,
        initial_phase=0,
        ):
        r'''Constructs a control-rate FSinOsc.

        ::

            >>> fsin_osc = ugentools.FSinOsc.kr(
            ...     frequency=440,
            ...     initial_phase=0,
            ...     )
            >>> fsin_osc
            FSinOsc.kr()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            initial_phase=initial_phase,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def frequency(self):
        r'''Gets `frequency` input of FSinOsc.

        ::

            >>> fsin_osc = ugentools.FSinOsc.ar(
            ...     frequency=440,
            ...     initial_phase=0,
            ...     )
            >>> fsin_osc.frequency
            440.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def initial_phase(self):
        r'''Gets `initial_phase` input of FSinOsc.

        ::

            >>> fsin_osc = ugentools.FSinOsc.ar(
            ...     frequency=440,
            ...     initial_phase=0,
            ...     )
            >>> fsin_osc.initial_phase
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('initial_phase')
        return self._inputs[index]