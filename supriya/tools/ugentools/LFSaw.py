# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PureUGen import PureUGen


class LFSaw(PureUGen):
    r'''A non-band-limited sawtooth oscillator unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> ugentools.LFSaw.ar()
        LFSaw.ar()

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
        r'''Creates an audio-rate non-band-limited sawtooth oscillator.

        ::

            >>> from supriya.tools import ugentools
            >>> ugentools.LFSaw.ar(
            ...     frequency=443,
            ...     initial_phase=0.25,
            ...     )
            LFSaw.ar()

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
        r'''Creates a control-rate non-band-limited sawtooth oscillator.

        ::

            >>> from supriya.tools import ugentools
            >>> ugentools.LFSaw.kr(
            ...     frequency=443,
            ...     initial_phase=0.25,
            ...     )
            LFSaw.kr()

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
        r'''Gets `frequency` input of LFSaw.

        ::

            >>> frequency = None
            >>> lfsaw = ugentools.LFSaw.ar(
            ...     frequency=frequency,
            ...     )
            >>> lfsaw.frequency

        Returns input.
        '''
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def initial_phase(self):
        r'''Gets `initial_phase` input of LFSaw.

        ::

            >>> initial_phase = None
            >>> lfsaw = ugentools.LFSaw.ar(
            ...     initial_phase=initial_phase,
            ...     )
            >>> lfsaw.initial_phase

        Returns input.
        '''
        index = self._ordered_input_names.index('initial_phase')
        return self._inputs[index]