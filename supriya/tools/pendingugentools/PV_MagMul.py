# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_MagMul(PV_ChainUGen):
    r'''

    ::

        >>> pv_mag_mul = ugentools.PV_MagMul.(
        ...     )
        >>> pv_mag_mul

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
        r'''Constructs a PV_MagMul.

        ::

            >>> pv_mag_mul = ugentools.PV_MagMul.new(
            ...     buffer_a=None,
            ...     buffer_b=None,
            ...     )
            >>> pv_mag_mul

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
