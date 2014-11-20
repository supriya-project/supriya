# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_MagAbove import PV_MagAbove


class PV_MagBelow(PV_MagAbove):
    r'''

    ::

        >>> pv_mag_below = ugentools.PV_MagBelow(
        ...     pv_chain=None,
        ...     threshold=0,
        ...     )
        >>> pv_mag_below

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
        r'''Constructs a PV_MagBelow.

        ::

            >>> pv_mag_below = ugentools.PV_MagBelow.new(
            ...     pv_chain=None,
            ...     threshold=0,
            ...     )
            >>> pv_mag_below

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
        r'''Gets `pv_chain` input of PV_MagBelow.

        ::

            >>> pv_mag_below = ugentools.PV_MagBelow(
            ...     pv_chain=None,
            ...     threshold=0,
            ...     )
            >>> pv_mag_below.pv_chain

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('pv_chain')
        return self._inputs[index]

    @property
    def threshold(self):
        r'''Gets `threshold` input of PV_MagBelow.

        ::

            >>> pv_mag_below = ugentools.PV_MagBelow(
            ...     pv_chain=None,
            ...     threshold=0,
            ...     )
            >>> pv_mag_below.threshold

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('threshold')
        return self._inputs[index]