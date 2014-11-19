# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_MagAbove import PV_MagAbove


class PV_LocalMax(PV_MagAbove):
    r'''

    ::

        >>> pv_local_max = ugentools.PV_LocalMax.(
        ...     )
        >>> pv_local_max

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
        r'''Constructs a PV_LocalMax.

        ::

            >>> pv_local_max = ugentools.PV_LocalMax.new(
            ...     buffer_=None,
            ...     threshold=0,
            ...     )
            >>> pv_local_max

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
