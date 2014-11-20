# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_RandComb(PV_ChainUGen):
    r'''

    ::

        >>> pv_rand_comb = ugentools.PV_RandComb.(
        ...     pv_chain=None,
        ...     trigger=0,
        ...     wipe=0,
        ...     )
        >>> pv_rand_comb

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain',
        'wipe',
        'trigger',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pv_chain=None,
        trigger=0,
        wipe=0,
        ):
        PV_ChainUGen.__init__(
            self,
            pv_chain=pv_chain,
            trigger=trigger,
            wipe=wipe,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        pv_chain=None,
        trigger=0,
        wipe=0,
        ):
        r'''Constructs a PV_RandComb.

        ::

            >>> pv_rand_comb = ugentools.PV_RandComb.new(
            ...     pv_chain=None,
            ...     trigger=0,
            ...     wipe=0,
            ...     )
            >>> pv_rand_comb

        Returns ugen graph.
        '''
        ugen = cls._new_expanded(
            pv_chain=pv_chain,
            trigger=trigger,
            wipe=wipe,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain(self):
        r'''Gets `pv_chain` input of PV_RandComb.

        ::

            >>> pv_rand_comb = ugentools.PV_RandComb.ar(
            ...     pv_chain=None,
            ...     trigger=0,
            ...     wipe=0,
            ...     )
            >>> pv_rand_comb.pv_chain

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('pv_chain')
        return self._inputs[index]

    @property
    def trigger(self):
        r'''Gets `trigger` input of PV_RandComb.

        ::

            >>> pv_rand_comb = ugentools.PV_RandComb.ar(
            ...     pv_chain=None,
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
            ...     pv_chain=None,
            ...     trigger=0,
            ...     wipe=0,
            ...     )
            >>> pv_rand_comb.wipe

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('wipe')
        return self._inputs[index]