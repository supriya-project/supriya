# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_BrickWall(PV_ChainUGen):
    r'''

    ::

        >>> pv_brick_wall = ugentools.PV_BrickWall.(
        ...     )
        >>> pv_brick_wall

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = ()

    _valid_calculation_rates = None

    ### INITIALIZER ###

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        buffer_=None,
        wipe=0,
        ):
        r'''Constructs a PV_BrickWall.

        ::

            >>> pv_brick_wall = ugentools.PV_BrickWall.new(
            ...     buffer_=None,
            ...     wipe=0,
            ...     )
            >>> pv_brick_wall

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_=buffer_,
            wipe=wipe,
            )
        return ugen
