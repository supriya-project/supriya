# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_MagAbove(PV_ChainUGen):
    r'''

    ::

        >>> pv_mag_above = ugentools.PV_MagAbove.(
        ...     pv_chain=None,
        ...     threshold=0,
        ...     )
        >>> pv_mag_above

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

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
        PV_ChainUGen.__init__(
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
        r'''Constructs a PV_MagAbove.

        ::

            >>> pv_mag_above = ugentools.PV_MagAbove.new(
            ...     pv_chain=None,
            ...     threshold=0,
            ...     )
            >>> pv_mag_above

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
        r'''Gets `pv_chain` input of PV_MagAbove.

        ::

            >>> pv_mag_above = ugentools.PV_MagAbove.ar(
            ...     pv_chain=None,
            ...     threshold=0,
            ...     )
            >>> pv_mag_above.pv_chain

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('pv_chain')
        return self._inputs[index]

    @property
    def threshold(self):
        r'''Gets `threshold` input of PV_MagAbove.

        ::

            >>> pv_mag_above = ugentools.PV_MagAbove.ar(
            ...     pv_chain=None,
            ...     threshold=0,
            ...     )
            >>> pv_mag_above.threshold

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('threshold')
        return self._inputs[index]