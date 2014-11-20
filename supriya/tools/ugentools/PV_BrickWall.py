# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_BrickWall(PV_ChainUGen):
    r'''

    ::

        >>> pv_brick_wall = ugentools.PV_BrickWall(
        ...     pv_chain=None,
        ...     wipe=0,
        ...     )
        >>> pv_brick_wall

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'FFT UGens'

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain',
        'wipe',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pv_chain=None,
        wipe=0,
        ):
        PV_ChainUGen.__init__(
            self,
            pv_chain=pv_chain,
            wipe=wipe,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        pv_chain=None,
        wipe=0,
        ):
        r'''Constructs a PV_BrickWall.

        ::

            >>> pv_brick_wall = ugentools.PV_BrickWall.new(
            ...     pv_chain=None,
            ...     wipe=0,
            ...     )
            >>> pv_brick_wall

        Returns ugen graph.
        '''
        ugen = cls._new_expanded(
            pv_chain=pv_chain,
            wipe=wipe,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain(self):
        r'''Gets `pv_chain` input of PV_BrickWall.

        ::

            >>> pv_brick_wall = ugentools.PV_BrickWall(
            ...     pv_chain=None,
            ...     wipe=0,
            ...     )
            >>> pv_brick_wall.pv_chain

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('pv_chain')
        return self._inputs[index]

    @property
    def wipe(self):
        r'''Gets `wipe` input of PV_BrickWall.

        ::

            >>> pv_brick_wall = ugentools.PV_BrickWall(
            ...     pv_chain=None,
            ...     wipe=0,
            ...     )
            >>> pv_brick_wall.wipe

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('wipe')
        return self._inputs[index]