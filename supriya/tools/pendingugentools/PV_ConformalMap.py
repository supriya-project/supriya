# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_ConformalMap(PV_ChainUGen):
    r'''

    ::

        >>> pv_conformal_map = ugentools.PV_ConformalMap.(
        ...     )
        >>> pv_conformal_map

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
        aimag=0,
        areal=0,
        buffer_=None,
        ):
        r'''Constructs a PV_ConformalMap.

        ::

            >>> pv_conformal_map = ugentools.PV_ConformalMap.new(
            ...     aimag=0,
            ...     areal=0,
            ...     buffer_=None,
            ...     )
            >>> pv_conformal_map

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            aimag=aimag,
            areal=areal,
            buffer_=buffer_,
            )
        return ugen
