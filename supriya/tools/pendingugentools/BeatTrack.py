# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class BeatTrack(MultiOutUGen):
    r'''

    ::

        >>> beat_track = ugentools.BeatTrack.(
        ...     chain=None,
        ...     lock=0,
        ...     )
        >>> beat_track

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'chain',
        'lock',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        chain=None,
        lock=0,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            chain=chain,
            lock=lock,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        chain=None,
        lock=0,
        ):
        r'''Constructs a control-rate BeatTrack.

        ::

            >>> beat_track = ugentools.BeatTrack.kr(
            ...     chain=None,
            ...     lock=0,
            ...     )
            >>> beat_track

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            chain=chain,
            lock=lock,
            )
        return ugen

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def chain(self):
        r'''Gets `chain` input of BeatTrack.

        ::

            >>> beat_track = ugentools.BeatTrack.ar(
            ...     chain=None,
            ...     lock=0,
            ...     )
            >>> beat_track.chain

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('chain')
        return self._inputs[index]

    @property
    def lock(self):
        r'''Gets `lock` input of BeatTrack.

        ::

            >>> beat_track = ugentools.BeatTrack.ar(
            ...     chain=None,
            ...     lock=0,
            ...     )
            >>> beat_track.lock

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('lock')
        return self._inputs[index]