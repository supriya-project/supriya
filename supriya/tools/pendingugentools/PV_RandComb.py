# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_RandComb(PV_ChainUGen):
    r'''

    ::

        >>> pv_rand_comb = ugentools.PV_RandComb.(
        ...     buffer_id=None,
        ...     trigger=0,
        ...     wipe=0,
        ...     )
        >>> pv_rand_comb

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        'wipe',
        'trigger',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=None,
        trigger=0,
        wipe=0,
        ):
        PV_ChainUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            trigger=trigger,
            wipe=wipe,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        buffer_id=None,
        trigger=0,
        wipe=0,
        ):
        r'''Constructs a PV_RandComb.

        ::

            >>> pv_rand_comb = ugentools.PV_RandComb.new(
            ...     buffer_id=None,
            ...     trigger=0,
            ...     wipe=0,
            ...     )
            >>> pv_rand_comb

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            trigger=trigger,
            wipe=wipe,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        r'''Gets `buffer_id` input of PV_RandComb.

        ::

            >>> pv_rand_comb = ugentools.PV_RandComb.ar(
            ...     buffer_id=None,
            ...     trigger=0,
            ...     wipe=0,
            ...     )
            >>> pv_rand_comb.buffer_id

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def trigger(self):
        r'''Gets `trigger` input of PV_RandComb.

        ::

            >>> pv_rand_comb = ugentools.PV_RandComb.ar(
            ...     buffer_id=None,
            ...     trigger=0,
            ...     wipe=0,
            ...     )
            >>> pv_rand_comb.trigger

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]

    @property
    def wipe(self):
        r'''Gets `wipe` input of PV_RandComb.

        ::

            >>> pv_rand_comb = ugentools.PV_RandComb.ar(
            ...     buffer_id=None,
            ...     trigger=0,
            ...     wipe=0,
            ...     )
            >>> pv_rand_comb.wipe

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('wipe')
        return self._inputs[index]