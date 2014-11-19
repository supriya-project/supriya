# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PureUGen import PureUGen


class LFTri(PureUGen):
    r'''A non-band-limited triangle oscillator unit generator.

    ::

        >>> ugentools.LFTri.ar()
        LFTri.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Oscillator UGens'

    __slots__ = ()

    _ordered_input_names = (
        'frequency',
        'initial_phase',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        frequency=440.,
        initial_phase=0.,
        ):
        PureUGen.__init__(
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
        r'''Constructs an audio-rate non-band-limited triangle oscillator.

        ::

            >>> ugentools.LFTri.ar(
            ...     frequency=443,
            ...     initial_phase=0.25,
            ...     )
            LFTri.ar()

        Returns unit generator graph.
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
        r'''Constructs a control-rate non-band-limited triangle oscillator.

        ::

            >>> ugentools.LFTri.kr(
            ...     frequency=443,
            ...     initial_phase=0.25,
            ...     )
            LFTri.kr()

        Returns unit generator graph.
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
        r'''Gets `frequency` input of LFTri.

        ::

            >>> frequency = 442
            >>> l_f_tri = ugentools.LFTri.ar(
            ...     frequency=frequency,
            ...     )
            >>> l_f_tri.frequency
            442.0

        Returns input.
        '''
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def initial_phase(self):
        r'''Gets `initial_phase` input of LFTri.

        ::

            >>> initial_phase = 0.5
            >>> l_f_tri = ugentools.LFTri.ar(
            ...     initial_phase=initial_phase,
            ...     )
            >>> l_f_tri.initial_phase
            0.5

        Returns input.
        '''
        index = self._ordered_input_names.index('initial_phase')
        return self._inputs[index]