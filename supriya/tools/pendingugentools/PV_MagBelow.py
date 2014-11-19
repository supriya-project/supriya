# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_MagAbove import PV_MagAbove


class PV_MagBelow(PV_MagAbove):
    r'''

    ::

        >>> pv_mag_below = ugentools.PV_MagBelow.(
        ...     )
        >>> pv_mag_below

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
        threshold=0,
        ):
        r'''Constructs a PV_MagBelow.

        ::

            >>> pv_mag_below = ugentools.PV_MagBelow.new(
            ...     buffer_=None,
            ...     threshold=0,
            ...     )
            >>> pv_mag_below

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_=buffer_,
            threshold=threshold,
            )
        return ugen
