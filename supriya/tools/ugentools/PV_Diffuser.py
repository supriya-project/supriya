# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_Diffuser(PV_ChainUGen):
    r'''

    ::

        >>> pv_diffuser = ugentools.PV_Diffuser(
        ...     pv_chain=None,
        ...     trigger=0,
        ...     )
        >>> pv_diffuser

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'FFT UGens'

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain',
        'trigger',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pv_chain=None,
        trigger=0,
        ):
        PV_ChainUGen.__init__(
            self,
            pv_chain=pv_chain,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        pv_chain=None,
        trigger=0,
        ):
        r'''Constructs a PV_Diffuser.

        ::

            >>> pv_diffuser = ugentools.PV_Diffuser.new(
            ...     pv_chain=None,
            ...     trigger=0,
            ...     )
            >>> pv_diffuser

        Returns ugen graph.
        '''
        ugen = cls._new_expanded(
            pv_chain=pv_chain,
            trigger=trigger,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain(self):
        r'''Gets `pv_chain` input of PV_Diffuser.

        ::

            >>> pv_diffuser = ugentools.PV_Diffuser(
            ...     pv_chain=None,
            ...     trigger=0,
            ...     )
            >>> pv_diffuser.pv_chain

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('pv_chain')
        return self._inputs[index]

    @property
    def trigger(self):
        r'''Gets `trigger` input of PV_Diffuser.

        ::

            >>> pv_diffuser = ugentools.PV_Diffuser(
            ...     pv_chain=None,
            ...     trigger=0,
            ...     )
            >>> pv_diffuser.trigger

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]