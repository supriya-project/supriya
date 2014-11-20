# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_ConformalMap(PV_ChainUGen):
    r'''

    ::

        >>> pv_conformal_map = ugentools.PV_ConformalMap.(
        ...     aimag=0,
        ...     areal=0,
        ...     pv_chain=None,
        ...     )
        >>> pv_conformal_map

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'FFT UGens'

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain',
        'areal',
        'aimag',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        aimag=0,
        areal=0,
        pv_chain=None,
        ):
        PV_ChainUGen.__init__(
            self,
            aimag=aimag,
            areal=areal,
            pv_chain=pv_chain,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        aimag=0,
        areal=0,
        pv_chain=None,
        ):
        r'''Constructs a PV_ConformalMap.

        ::

            >>> pv_conformal_map = ugentools.PV_ConformalMap.new(
            ...     aimag=0,
            ...     areal=0,
            ...     pv_chain=None,
            ...     )
            >>> pv_conformal_map

        Returns ugen graph.
        '''
        ugen = cls._new_expanded(
            aimag=aimag,
            areal=areal,
            pv_chain=pv_chain,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def aimag(self):
        r'''Gets `aimag` input of PV_ConformalMap.

        ::

            >>> pv_conformal_map = ugentools.PV_ConformalMap.ar(
            ...     aimag=0,
            ...     areal=0,
            ...     pv_chain=None,
            ...     )
            >>> pv_conformal_map.aimag

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('aimag')
        return self._inputs[index]

    @property
    def areal(self):
        r'''Gets `areal` input of PV_ConformalMap.

        ::

            >>> pv_conformal_map = ugentools.PV_ConformalMap.ar(
            ...     aimag=0,
            ...     areal=0,
            ...     pv_chain=None,
            ...     )
            >>> pv_conformal_map.areal

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('areal')
        return self._inputs[index]

    @property
    def pv_chain(self):
        r'''Gets `pv_chain` input of PV_ConformalMap.

        ::

            >>> pv_conformal_map = ugentools.PV_ConformalMap.ar(
            ...     aimag=0,
            ...     areal=0,
            ...     pv_chain=None,
            ...     )
            >>> pv_conformal_map.pv_chain

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('pv_chain')
        return self._inputs[index]