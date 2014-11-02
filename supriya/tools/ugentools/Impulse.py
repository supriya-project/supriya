# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PureUGen import PureUGen


class Impulse(PureUGen):
    r'''A non-band-limited single-sample impulse generator unit generator.

    ::

        >>> ugentools.Impulse.ar()
        Impulse.ar()

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
        rate=None,
        frequency=440.,
        phase=0.,
        ):
        PureUGen.__init__(
            self,
            rate=rate,
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
        r'''Creates an audio-rate non-band-limited single-sample impulse
        generator.

        ::

            >>> ugentools.Impulse.ar(
            ...     frequency=443,
            ...     phase=0.25,
            ...     )
            Impulse.ar()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.AUDIO
        ugen = cls._new_expanded(
            rate=rate,
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
        r'''Creates a control-rate non-band-limited single-sample impulse
        generator.

        ::

            >>> ugentools.Impulse.kr(
            ...     frequency=443,
            ...     phase=0.25,
            ...     )
            Impulse.kr()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.CONTROL
        ugen = cls._new_expanded(
            rate=rate,
            frequency=frequency,
            phase=phase,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def frequency(self):
        r'''Gets `frequency` input of Impulse.

        ::

            >>> frequency = None
            >>> impulse = ugentools.Impulse.ar(
            ...     frequency=frequency,
            ...     )
            >>> impulse.frequency

        Returns input.
        '''
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def phase(self):
        r'''Gets `phase` input of Impulse.

        ::

            >>> phase = None
            >>> impulse = ugentools.Impulse.ar(
            ...     phase=phase,
            ...     )
            >>> impulse.phase

        Returns input.
        '''
        index = self._ordered_input_names.index('phase')
        return self._inputs[index]