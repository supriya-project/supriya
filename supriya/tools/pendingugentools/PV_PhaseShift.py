# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_PhaseShift(PV_ChainUGen):
    r'''

    ::

        >>> pv_phase_shift = ugentools.PV_PhaseShift.(
        ...     )
        >>> pv_phase_shift

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
        integrate=0,
        shift=None,
        ):
        r'''Constructs a PV_PhaseShift.

        ::

            >>> pv_phase_shift = ugentools.PV_PhaseShift.new(
            ...     buffer_=None,
            ...     integrate=0,
            ...     shift=None,
            ...     )
            >>> pv_phase_shift

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_=buffer_,
            integrate=integrate,
            shift=shift,
            )
        return ugen
