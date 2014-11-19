# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_MagDiv(PV_ChainUGen):
    r'''

    ::

        >>> pv_mag_div = ugentools.PV_MagDiv.(
        ...     )
        >>> pv_mag_div

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
        zeroed=0.0001,
        ):
        r'''Constructs a PV_MagDiv.

        ::

            >>> pv_mag_div = ugentools.PV_MagDiv.new(
            ...     buffer_a=None,
            ...     buffer_b=None,
            ...     zeroed=0.0001,
            ...     )
            >>> pv_mag_div

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_a=buffer_a,
            buffer_b=buffer_b,
            zeroed=zeroed,
            )
        return ugen
