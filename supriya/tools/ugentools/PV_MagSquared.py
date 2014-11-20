# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_MagSquared(PV_ChainUGen):
    r'''

    ::

        >>> pv_mag_squared = ugentools.PV_MagSquared.(
        ...     pv_chain=None,
        ...     )
        >>> pv_mag_squared

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'FFT UGens'

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pv_chain=None,
        ):
        PV_ChainUGen.__init__(
            self,
            pv_chain=pv_chain,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        pv_chain=None,
        ):
        r'''Constructs a PV_MagSquared.

        ::

            >>> pv_mag_squared = ugentools.PV_MagSquared.new(
            ...     pv_chain=None,
            ...     )
            >>> pv_mag_squared

        Returns ugen graph.
        '''
        ugen = cls._new_expanded(
            pv_chain=pv_chain,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain(self):
        r'''Gets `pv_chain` input of PV_MagSquared.

        ::

            >>> pv_mag_squared = ugentools.PV_MagSquared.ar(
            ...     pv_chain=None,
            ...     )
            >>> pv_mag_squared.pv_chain

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('pv_chain')
        return self._inputs[index]