# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_MagSmear(PV_ChainUGen):
    r'''

    ::

        >>> pv_mag_smear = ugentools.PV_MagSmear.(
        ...     bins=0,
        ...     pv_chain=None,
        ...     )
        >>> pv_mag_smear

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain',
        'bins',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        bins=0,
        pv_chain=None,
        ):
        PV_ChainUGen.__init__(
            self,
            bins=bins,
            pv_chain=pv_chain,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        bins=0,
        pv_chain=None,
        ):
        r'''Constructs a PV_MagSmear.

        ::

            >>> pv_mag_smear = ugentools.PV_MagSmear.new(
            ...     bins=0,
            ...     pv_chain=None,
            ...     )
            >>> pv_mag_smear

        Returns ugen graph.
        '''
        ugen = cls._new_expanded(
            bins=bins,
            pv_chain=pv_chain,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def bins(self):
        r'''Gets `bins` input of PV_MagSmear.

        ::

            >>> pv_mag_smear = ugentools.PV_MagSmear.ar(
            ...     bins=0,
            ...     pv_chain=None,
            ...     )
            >>> pv_mag_smear.bins

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('bins')
        return self._inputs[index]

    @property
    def pv_chain(self):
        r'''Gets `pv_chain` input of PV_MagSmear.

        ::

            >>> pv_mag_smear = ugentools.PV_MagSmear.ar(
            ...     bins=0,
            ...     pv_chain=None,
            ...     )
            >>> pv_mag_smear.pv_chain

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('pv_chain')
        return self._inputs[index]