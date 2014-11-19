# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_MagSquared(PV_ChainUGen):
    r'''

    ::

        >>> pv_mag_squared = ugentools.PV_MagSquared.(
        ...     )
        >>> pv_mag_squared

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
        ):
        r'''Constructs a PV_MagSquared.

        ::

            >>> pv_mag_squared = ugentools.PV_MagSquared.new(
            ...     buffer_=None,
            ...     )
            >>> pv_mag_squared

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_=buffer_,
            )
        return ugen
