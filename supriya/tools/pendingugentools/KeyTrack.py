# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class KeyTrack(UGen):
    r'''

    ::

        >>> key_track = ugentools.KeyTrack.(
        ...     chain=None,
        ...     chromaleak=0.5,
        ...     keydecay=2,
        ...     )
        >>> key_track

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'chain',
        'keydecay',
        'chromaleak',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        chain=None,
        chromaleak=0.5,
        keydecay=2,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            chain=chain,
            chromaleak=chromaleak,
            keydecay=keydecay,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        chain=None,
        chromaleak=0.5,
        keydecay=2,
        ):
        r'''Constructs a control-rate KeyTrack.

        ::

            >>> key_track = ugentools.KeyTrack.kr(
            ...     chain=None,
            ...     chromaleak=0.5,
            ...     keydecay=2,
            ...     )
            >>> key_track

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            chain=chain,
            chromaleak=chromaleak,
            keydecay=keydecay,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def chain(self):
        r'''Gets `chain` input of KeyTrack.

        ::

            >>> key_track = ugentools.KeyTrack.ar(
            ...     chain=None,
            ...     chromaleak=0.5,
            ...     keydecay=2,
            ...     )
            >>> key_track.chain

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('chain')
        return self._inputs[index]

    @property
    def chromaleak(self):
        r'''Gets `chromaleak` input of KeyTrack.

        ::

            >>> key_track = ugentools.KeyTrack.ar(
            ...     chain=None,
            ...     chromaleak=0.5,
            ...     keydecay=2,
            ...     )
            >>> key_track.chromaleak

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('chromaleak')
        return self._inputs[index]

    @property
    def keydecay(self):
        r'''Gets `keydecay` input of KeyTrack.

        ::

            >>> key_track = ugentools.KeyTrack.ar(
            ...     chain=None,
            ...     chromaleak=0.5,
            ...     keydecay=2,
            ...     )
            >>> key_track.keydecay

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('keydecay')
        return self._inputs[index]