# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_BinScramble(PV_ChainUGen):
    r'''

    ::

        >>> pv_bin_scramble = ugentools.PV_BinScramble(
        ...     pv_chain=None,
        ...     trigger=0,
        ...     width=0.2,
        ...     wipe=0,
        ...     )
        >>> pv_bin_scramble

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'FFT UGens'

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain',
        'wipe',
        'width',
        'trigger',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pv_chain=None,
        trigger=0,
        width=0.2,
        wipe=0,
        ):
        PV_ChainUGen.__init__(
            self,
            pv_chain=pv_chain,
            trigger=trigger,
            width=width,
            wipe=wipe,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        pv_chain=None,
        trigger=0,
        width=0.2,
        wipe=0,
        ):
        r'''Constructs a PV_BinScramble.

        ::

            >>> pv_bin_scramble = ugentools.PV_BinScramble.new(
            ...     pv_chain=None,
            ...     trigger=0,
            ...     width=0.2,
            ...     wipe=0,
            ...     )
            >>> pv_bin_scramble

        Returns ugen graph.
        '''
        ugen = cls._new_expanded(
            pv_chain=pv_chain,
            trigger=trigger,
            width=width,
            wipe=wipe,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain(self):
        r'''Gets `pv_chain` input of PV_BinScramble.

        ::

            >>> pv_bin_scramble = ugentools.PV_BinScramble(
            ...     pv_chain=None,
            ...     trigger=0,
            ...     width=0.2,
            ...     wipe=0,
            ...     )
            >>> pv_bin_scramble.pv_chain

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('pv_chain')
        return self._inputs[index]

    @property
    def trigger(self):
        r'''Gets `trigger` input of PV_BinScramble.

        ::

            >>> pv_bin_scramble = ugentools.PV_BinScramble(
            ...     pv_chain=None,
            ...     trigger=0,
            ...     width=0.2,
            ...     wipe=0,
            ...     )
            >>> pv_bin_scramble.trigger

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]

    @property
    def width(self):
        r'''Gets `width` input of PV_BinScramble.

        ::

            >>> pv_bin_scramble = ugentools.PV_BinScramble(
            ...     pv_chain=None,
            ...     trigger=0,
            ...     width=0.2,
            ...     wipe=0,
            ...     )
            >>> pv_bin_scramble.width

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('width')
        return self._inputs[index]

    @property
    def wipe(self):
        r'''Gets `wipe` input of PV_BinScramble.

        ::

            >>> pv_bin_scramble = ugentools.PV_BinScramble(
            ...     pv_chain=None,
            ...     trigger=0,
            ...     width=0.2,
            ...     wipe=0,
            ...     )
            >>> pv_bin_scramble.wipe

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('wipe')
        return self._inputs[index]