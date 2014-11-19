# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_MagMul import PV_MagMul


class PV_Div(PV_MagMul):
    r'''

    ::

        >>> pv_div = ugentools.PV_Div.(
        ...     )
        >>> pv_div

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
        ):
        r'''Constructs a PV_Div.

        ::

            >>> pv_div = ugentools.PV_Div.new(
            ...     buffer_a=None,
            ...     buffer_b=None,
            ...     )
            >>> pv_div

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_a=buffer_a,
            buffer_b=buffer_b,
            )
        return ugen
