# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_MagSquared import PV_MagSquared


class PV_PhaseShift270(PV_MagSquared):
    r'''

    ::

        >>> pv_phase_shift_270 = ugentools.PV_PhaseShift270.(
        ...     buffer_id=None,
        ...     )
        >>> pv_phase_shift_270

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=None,
        ):
        PV_MagSquared.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        buffer_id=None,
        ):
        r'''Constructs a PV_PhaseShift270.

        ::

            >>> pv_phase_shift_270 = ugentools.PV_PhaseShift270.new(
            ...     buffer_id=None,
            ...     )
            >>> pv_phase_shift_270

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        r'''Gets `buffer_id` input of PV_PhaseShift270.

        ::

            >>> pv_phase_shift_270 = ugentools.PV_PhaseShift270.ar(
            ...     buffer_id=None,
            ...     )
            >>> pv_phase_shift_270.buffer_id

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]