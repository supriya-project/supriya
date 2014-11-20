# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_HainsworthFoote(PV_ChainUGen):
    r'''

    ::

        >>> pv_hainsworth_foote = ugentools.PV_HainsworthFoote(
        ...     pv_chain=None,
        ...     propf=0,
        ...     proph=0,
        ...     threshold=1,
        ...     waittime=0.04,
        ...     )
        >>> pv_hainsworth_foote

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'FFT UGens'

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain',
        'proph',
        'propf',
        'threshold',
        'waittime',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pv_chain=None,
        propf=0,
        proph=0,
        threshold=1,
        waittime=0.04,
        ):
        PV_ChainUGen.__init__(
            self,
            pv_chain=pv_chain,
            propf=propf,
            proph=proph,
            threshold=threshold,
            waittime=waittime,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def(
        cls,
        pv_chain=None,
        propf=0,
        proph=0,
        threshold=1,
        waittime=0.04,
        ):
        r'''Constructs an audio-rate PV_HainsworthFoote.

        ::

            >>> pv_hainsworth_foote = ugentools.PV_HainsworthFoote(
            ...     pv_chain=None,
            ...     propf=0,
            ...     proph=0,
            ...     threshold=1,
            ...     waittime=0.04,
            ...     )
            >>> pv_hainsworth_foote

        Returns ugen graph.
        '''
        ugen = cls._new_expanded(
            pv_chain=pv_chain,
            propf=propf,
            proph=proph,
            threshold=threshold,
            waittime=waittime,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain(self):
        r'''Gets `pv_chain` input of PV_HainsworthFoote.

        ::

            >>> pv_hainsworth_foote = ugentools.PV_HainsworthFoote(
            ...     pv_chain=None,
            ...     propf=0,
            ...     proph=0,
            ...     threshold=1,
            ...     waittime=0.04,
            ...     )
            >>> pv_hainsworth_foote.pv_chain

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('pv_chain')
        return self._inputs[index]

    @property
    def propf(self):
        r'''Gets `propf` input of PV_HainsworthFoote.

        ::

            >>> pv_hainsworth_foote = ugentools.PV_HainsworthFoote(
            ...     pv_chain=None,
            ...     propf=0,
            ...     proph=0,
            ...     threshold=1,
            ...     waittime=0.04,
            ...     )
            >>> pv_hainsworth_foote.propf

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('propf')
        return self._inputs[index]

    @property
    def proph(self):
        r'''Gets `proph` input of PV_HainsworthFoote.

        ::

            >>> pv_hainsworth_foote = ugentools.PV_HainsworthFoote(
            ...     pv_chain=None,
            ...     propf=0,
            ...     proph=0,
            ...     threshold=1,
            ...     waittime=0.04,
            ...     )
            >>> pv_hainsworth_foote.proph

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('proph')
        return self._inputs[index]

    @property
    def threshold(self):
        r'''Gets `threshold` input of PV_HainsworthFoote.

        ::

            >>> pv_hainsworth_foote = ugentools.PV_HainsworthFoote(
            ...     pv_chain=None,
            ...     propf=0,
            ...     proph=0,
            ...     threshold=1,
            ...     waittime=0.04,
            ...     )
            >>> pv_hainsworth_foote.threshold

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('threshold')
        return self._inputs[index]

    @property
    def waittime(self):
        r'''Gets `waittime` input of PV_HainsworthFoote.

        ::

            >>> pv_hainsworth_foote = ugentools.PV_HainsworthFoote(
            ...     pv_chain=None,
            ...     propf=0,
            ...     proph=0,
            ...     threshold=1,
            ...     waittime=0.04,
            ...     )
            >>> pv_hainsworth_foote.waittime

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('waittime')
        return self._inputs[index]