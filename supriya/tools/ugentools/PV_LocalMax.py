# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_MagAbove import PV_MagAbove


class PV_LocalMax(PV_MagAbove):
    r'''

    ::

        >>> pv_local_max = ugentools.PV_LocalMax(
        ...     pv_chain=None,
        ...     threshold=0,
        ...     )
        >>> pv_local_max

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'FFT UGens'

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain',
        'threshold',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pv_chain=None,
        threshold=0,
        ):
        PV_MagAbove.__init__(
            self,
            pv_chain=pv_chain,
            threshold=threshold,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        pv_chain=None,
        threshold=0,
        ):
        r'''Constructs a PV_LocalMax.

        ::

            >>> pv_local_max = ugentools.PV_LocalMax.new(
            ...     pv_chain=None,
            ...     threshold=0,
            ...     )
            >>> pv_local_max

        Returns ugen graph.
        '''
        ugen = cls._new_expanded(
            pv_chain=pv_chain,
            threshold=threshold,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain(self):
        r'''Gets `pv_chain` input of PV_LocalMax.

        ::

            >>> pv_local_max = ugentools.PV_LocalMax(
            ...     pv_chain=None,
            ...     threshold=0,
            ...     )
            >>> pv_local_max.pv_chain

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('pv_chain')
        return self._inputs[index]

    @property
    def threshold(self):
        r'''Gets `threshold` input of PV_LocalMax.

        ::

            >>> pv_local_max = ugentools.PV_LocalMax(
            ...     pv_chain=None,
            ...     threshold=0,
            ...     )
            >>> pv_local_max.threshold

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('threshold')
        return self._inputs[index]