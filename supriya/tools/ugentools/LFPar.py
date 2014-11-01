# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PureUGen import PureUGen


class LFPar(PureUGen):
    r'''A parabolic oscillator unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> ugentools.LFPar.ar()
        LFPar.ar()

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
        rate=None,
        frequency=440.,
        initial_phase=0.,
        ):
        PureUGen.__init__(
            self,
            rate=rate,
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
        r'''Creates an audio-rate parabolic oscillator.

        ::

            >>> from supriya.tools import ugentools
            >>> ugentools.LFPar.ar(
            ...     frequency=443,
            ...     initial_phase=0.25,
            ...     )
            LFPar.ar()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.AUDIO
        ugen = cls._new_expanded(
            rate=rate,
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
        r'''Creates a control-rate parabolic oscillator.

        ::

            >>> from supriya.tools import ugentools
            >>> ugentools.LFPar.kr(
            ...     frequency=443,
            ...     initial_phase=0.25,
            ...     )
            LFPar.kr()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.CONTROL
        ugen = cls._new_expanded(
            rate=rate,
            frequency=frequency,
            initial_phase=initial_phase,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def frequency(self):
        r'''Gets `frequency` input of LFPar.

        ::

            >>> frequency = None
            >>> lfpar = ugentools.LFPar.ar(
            ...     frequency=frequency,
            ...     )
            >>> lfpar.frequency

        Returns input.
        '''
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def initial_phase(self):
        r'''Gets `initial_phase` input of LFPar.

        ::

            >>> initial_phase = None
            >>> lfpar = ugentools.LFPar.ar(
            ...     initial_phase=initial_phase,
            ...     )
            >>> lfpar.initial_phase

        Returns input.
        '''
        index = self._ordered_input_names.index('initial_phase')
        return self._inputs[index]