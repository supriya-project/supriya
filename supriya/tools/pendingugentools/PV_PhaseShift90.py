# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_MagSquared import PV_MagSquared


class PV_PhaseShift90(PV_MagSquared):
    r'''

    ::

        >>> pv_phase_shift_90 = ugentools.PV_PhaseShift90.(
        ...     )
        >>> pv_phase_shift_90

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
        r'''Constructs a PV_PhaseShift90.

        ::

            >>> pv_phase_shift_90 = ugentools.PV_PhaseShift90.new(
            ...     buffer_=None,
            ...     )
            >>> pv_phase_shift_90

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_=buffer_,
            )
        return ugen
