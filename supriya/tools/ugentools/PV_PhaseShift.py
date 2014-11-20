# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_PhaseShift(PV_ChainUGen):
    r'''

    ::

        >>> pv_phase_shift = ugentools.PV_PhaseShift.(
        ...     pv_chain=None,
        ...     integrate=0,
        ...     shift=None,
        ...     )
        >>> pv_phase_shift

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'FFT UGens'

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain',
        'shift',
        'integrate',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pv_chain=None,
        integrate=0,
        shift=None,
        ):
        PV_ChainUGen.__init__(
            self,
            pv_chain=pv_chain,
            integrate=integrate,
            shift=shift,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        pv_chain=None,
        integrate=0,
        shift=None,
        ):
        r'''Constructs a PV_PhaseShift.

        ::

            >>> pv_phase_shift = ugentools.PV_PhaseShift.new(
            ...     pv_chain=None,
            ...     integrate=0,
            ...     shift=None,
            ...     )
            >>> pv_phase_shift

        Returns ugen graph.
        '''
        ugen = cls._new_expanded(
            pv_chain=pv_chain,
            integrate=integrate,
            shift=shift,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain(self):
        r'''Gets `pv_chain` input of PV_PhaseShift.

        ::

            >>> pv_phase_shift = ugentools.PV_PhaseShift.ar(
            ...     pv_chain=None,
            ...     integrate=0,
            ...     shift=None,
            ...     )
            >>> pv_phase_shift.pv_chain

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('pv_chain')
        return self._inputs[index]

    @property
    def integrate(self):
        r'''Gets `integrate` input of PV_PhaseShift.

        ::

            >>> pv_phase_shift = ugentools.PV_PhaseShift.ar(
            ...     pv_chain=None,
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
            ...     pv_chain=None,
            ...     integrate=0,
            ...     shift=None,
            ...     )
            >>> pv_phase_shift.shift

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('shift')
        return self._inputs[index]