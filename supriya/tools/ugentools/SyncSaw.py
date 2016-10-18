# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PureUGen import PureUGen


class SyncSaw(PureUGen):
    r'''A hard sync sawtooth wave.

    ::

        >>> ugentools.SyncSaw.ar()
        SyncSaw.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Oscillator UGens'

    __slots__ = ()

    _ordered_input_names = (
        'syncFreq',
        'sawFreq',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        syncFreq=440.,
        sawFreq=440.,
        ):
        PureUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            syncFreq=syncFreq,
            sawFreq=sawFreq,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        syncFreq=440,
        sawFreq=440,
        ):
        r'''Constructs an audio-rate SyncSaw oscillator.

        ::

            >>> ugentools.SyncSaw.ar(
            ...     syncFreq=443,
            ...     sawFreq=0.25,
            ...     )
            SyncSaw.ar()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            syncFreq=syncFreq,
            sawFreq=sawFreq,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        syncFreq=440,
        sawFreq=440,
        ):
        r'''Constructs an control-rate SyncSaw oscillator.

        ::

            >>> ugentools.SyncSaw.kr(
            ...     syncFreq=443,
            ...     sawFreq=0.25,
            ...     )
            SyncSaw.kr()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            syncFreq=syncFreq,
            sawFreq=sawFreq,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def syncFreq(self):
        r'''Gets `syncFreq` input of SyncSaw.

        ::

            >>> syncFreq = 442
            >>> sync_saw = ugentools.SyncSaw.ar(
            ...     syncFreq=syncFreq,
            ...     )
            >>> sync_saw.syncFreq
            442.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('syncFreq')
        return self._inputs[index]

    @property
    def sawFreq(self):
        r'''Gets `sawFreq` input of SyncSaw.

                ::

                    >>> sawFreq = 440
                    >>> sync_saw = ugentools.SyncSaw.ar(
                    ...     sawFreq=sawFreq,
                    ...     )
                    >>> sync_saw.sawFreq
                    440

                Returns ugen input.
                '''
        index = self._ordered_input_names.index('sawFreq')
        return self._inputs[index]
