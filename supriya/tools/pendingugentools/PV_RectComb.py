# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_RectComb(PV_ChainUGen):
    r'''

    ::

        >>> pv_rect_comb = ugentools.PV_RectComb.(
        ...     )
        >>> pv_rect_comb

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
        num_teeth=0,
        phase=0,
        width=0.5,
        ):
        r'''Constructs a PV_RectComb.

        ::

            >>> pv_rect_comb = ugentools.PV_RectComb.new(
            ...     buffer_=None,
            ...     num_teeth=0,
            ...     phase=0,
            ...     width=0.5,
            ...     )
            >>> pv_rect_comb

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_=buffer_,
            num_teeth=num_teeth,
            phase=phase,
            width=width,
            )
        return ugen
