# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_MagSquared import PV_MagSquared


class PV_Conj(PV_MagSquared):
    r'''

    ::

        >>> pv_conj = ugentools.PV_Conj(
        ...     pv_chain=None,
        ...     )
        >>> pv_conj

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
        PV_MagSquared.__init__(
            self,
            pv_chain=pv_chain,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        pv_chain=None,
        ):
        r'''Constructs a PV_Conj.

        ::

            >>> pv_conj = ugentools.PV_Conj.new(
            ...     pv_chain=None,
            ...     )
            >>> pv_conj

        Returns ugen graph.
        '''
        ugen = cls._new_expanded(
            pv_chain=pv_chain,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain(self):
        r'''Gets `pv_chain` input of PV_Conj.

        ::

            >>> pv_conj = ugentools.PV_Conj(
            ...     pv_chain=None,
            ...     )
            >>> pv_conj.pv_chain

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('pv_chain')
        return self._inputs[index]