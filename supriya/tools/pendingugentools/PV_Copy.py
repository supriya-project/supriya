# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_MagMul import PV_MagMul


class PV_Copy(PV_MagMul):
    r'''

    ::

        >>> pv_copy = ugentools.PV_Copy.(
        ...     )
        >>> pv_copy

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
        r'''Constructs a PV_Copy.

        ::

            >>> pv_copy = ugentools.PV_Copy.new(
            ...     buffer_a=None,
            ...     buffer_b=None,
            ...     )
            >>> pv_copy

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
