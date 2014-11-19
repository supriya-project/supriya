# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_RectComb2(PV_ChainUGen):
    r'''

    ::

        >>> pv_rect_comb_2 = ugentools.PV_RectComb2.(
        ...     )
        >>> pv_rect_comb_2

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
        buffer_a=None,
        buffer_b=None,
        num_teeth=0,
        phase=0,
        width=0.5,
        ):
        r'''Constructs a PV_RectComb2.

        ::

            >>> pv_rect_comb_2 = ugentools.PV_RectComb2.new(
            ...     buffer_a=None,
            ...     buffer_b=None,
            ...     num_teeth=0,
            ...     phase=0,
            ...     width=0.5,
            ...     )
            >>> pv_rect_comb_2

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_a=buffer_a,
            buffer_b=buffer_b,
            num_teeth=num_teeth,
            phase=phase,
            width=width,
            )
        return ugen
