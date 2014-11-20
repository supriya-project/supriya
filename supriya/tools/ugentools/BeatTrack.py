# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class BeatTrack(MultiOutUGen):
    r'''

    ::

        >>> beat_track = ugentools.BeatTrack.(
        ...     pv_chain=None,
        ...     lock=0,
        ...     )
        >>> beat_track

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Machine Listening UGens'

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain',
        'lock',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        pv_chain=None,
        lock=0,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            pv_chain=pv_chain,
            lock=lock,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        pv_chain=None,
        lock=0,
        ):
        r'''Constructs a control-rate BeatTrack.

        ::

            >>> beat_track = ugentools.BeatTrack.kr(
            ...     pv_chain=None,
            ...     lock=0,
            ...     )
            >>> beat_track

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            pv_chain=pv_chain,
            lock=lock,
            )
        return ugen

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain(self):
        r'''Gets `pv_chain` input of BeatTrack.

        ::

            >>> beat_track = ugentools.BeatTrack.ar(
            ...     pv_chain=None,
            ...     lock=0,
            ...     )
            >>> beat_track.pv_chain

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('pv_chain')
        return self._inputs[index]

    @property
    def lock(self):
        r'''Gets `lock` input of BeatTrack.

        ::

            >>> beat_track = ugentools.BeatTrack.ar(
            ...     pv_chain=None,
            ...     lock=0,
            ...     )
            >>> beat_track.lock

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('lock')
        return self._inputs[index]