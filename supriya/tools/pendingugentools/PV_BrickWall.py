# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_BrickWall(PV_ChainUGen):
    r'''

    ::

        >>> pv_brick_wall = ugentools.PV_BrickWall.(
        ...     buffer_id=None,
        ...     wipe=0,
        ...     )
        >>> pv_brick_wall

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        'wipe',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=None,
        wipe=0,
        ):
        PV_ChainUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            wipe=wipe,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        buffer_id=None,
        wipe=0,
        ):
        r'''Constructs a PV_BrickWall.

        ::

            >>> pv_brick_wall = ugentools.PV_BrickWall.new(
            ...     buffer_id=None,
            ...     wipe=0,
            ...     )
            >>> pv_brick_wall

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            wipe=wipe,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        r'''Gets `buffer_id` input of PV_BrickWall.

        ::

            >>> pv_brick_wall = ugentools.PV_BrickWall.ar(
            ...     buffer_id=None,
            ...     wipe=0,
            ...     )
            >>> pv_brick_wall.buffer_id

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def wipe(self):
        r'''Gets `wipe` input of PV_BrickWall.

        ::

            >>> pv_brick_wall = ugentools.PV_BrickWall.ar(
            ...     buffer_id=None,
            ...     wipe=0,
            ...     )
            >>> pv_brick_wall.wipe

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('wipe')
        return self._inputs[index]