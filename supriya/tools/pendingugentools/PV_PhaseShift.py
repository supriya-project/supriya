# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_PhaseShift(PV_ChainUGen):
    r'''

    ::

        >>> pv_phase_shift = ugentools.PV_PhaseShift.(
        ...     buffer_id=None,
        ...     integrate=0,
        ...     shift=None,
        ...     )
        >>> pv_phase_shift

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        'shift',
        'integrate',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=None,
        integrate=0,
        shift=None,
        ):
        PV_ChainUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            integrate=integrate,
            shift=shift,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        buffer_id=None,
        integrate=0,
        shift=None,
        ):
        r'''Constructs a PV_PhaseShift.

        ::

            >>> pv_phase_shift = ugentools.PV_PhaseShift.new(
            ...     buffer_id=None,
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
            buffer_id=buffer_id,
            integrate=integrate,
            shift=shift,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        r'''Gets `buffer_id` input of PV_PhaseShift.

        ::

            >>> pv_phase_shift = ugentools.PV_PhaseShift.ar(
            ...     buffer_id=None,
            ...     integrate=0,
            ...     shift=None,
            ...     )
            >>> pv_phase_shift.buffer_id

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def integrate(self):
        r'''Gets `integrate` input of PV_PhaseShift.

        ::

            >>> pv_phase_shift = ugentools.PV_PhaseShift.ar(
            ...     buffer_id=None,
            ...     integrate=0,
            ...     shift=None,
            ...     )
            >>> pv_phase_shift.integrate

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('integrate')
        return self._inputs[index]

    @property
    def shift(self):
        r'''Gets `shift` input of PV_PhaseShift.

        ::

            >>> pv_phase_shift = ugentools.PV_PhaseShift.ar(
            ...     buffer_id=None,
            ...     integrate=0,
            ...     shift=None,
            ...     )
            >>> pv_phase_shift.shift

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('shift')
        return self._inputs[index]