# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_BinWipe(PV_ChainUGen):
    r'''

    ::

        >>> pv_bin_wipe = ugentools.PV_BinWipe.(
        ...     pv_chain_a=None,
        ...     pv_chain_b=None,
        ...     wipe=0,
        ...     )
        >>> pv_bin_wipe

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain_a',
        'pv_chain_b',
        'wipe',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pv_chain_a=None,
        pv_chain_b=None,
        wipe=0,
        ):
        PV_ChainUGen.__init__(
            self,
            pv_chain_a=pv_chain_a,
            pv_chain_b=pv_chain_b,
            wipe=wipe,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        pv_chain_a=None,
        pv_chain_b=None,
        wipe=0,
        ):
        r'''Constructs a PV_BinWipe.

        ::

            >>> pv_bin_wipe = ugentools.PV_BinWipe.new(
            ...     pv_chain_a=None,
            ...     pv_chain_b=None,
            ...     wipe=0,
            ...     )
            >>> pv_bin_wipe

        Returns ugen graph.
        '''
        ugen = cls._new_expanded(
            pv_chain_a=pv_chain_a,
            pv_chain_b=pv_chain_b,
            wipe=wipe,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain_a(self):
        r'''Gets `pv_chain_a` input of PV_BinWipe.

        ::

            >>> pv_bin_wipe = ugentools.PV_BinWipe.ar(
            ...     pv_chain_a=None,
            ...     pv_chain_b=None,
            ...     wipe=0,
            ...     )
            >>> pv_bin_wipe.pv_chain_a

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('pv_chain_a')
        return self._inputs[index]

    @property
    def pv_chain_b(self):
        r'''Gets `pv_chain_b` input of PV_BinWipe.

        ::

            >>> pv_bin_wipe = ugentools.PV_BinWipe.ar(
            ...     pv_chain_a=None,
            ...     pv_chain_b=None,
            ...     wipe=0,
            ...     )
            >>> pv_bin_wipe.pv_chain_b

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('pv_chain_b')
        return self._inputs[index]

    @property
    def wipe(self):
        r'''Gets `wipe` input of PV_BinWipe.

        ::

            >>> pv_bin_wipe = ugentools.PV_BinWipe.ar(
            ...     pv_chain_a=None,
            ...     pv_chain_b=None,
            ...     wipe=0,
            ...     )
            >>> pv_bin_wipe.wipe

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('wipe')
        return self._inputs[index]