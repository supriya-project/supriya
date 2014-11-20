# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class SpecPcile(UGen):
    r'''

    ::

        >>> spec_pcile = ugentools.SpecPcile.(
        ...     pv_chain=None,
        ...     fraction=0.5,
        ...     interpolate=0,
        ...     )
        >>> spec_pcile

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Machine Listening UGens'

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain',
        'fraction',
        'interpolate',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        pv_chain=None,
        fraction=0.5,
        interpolate=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            pv_chain=pv_chain,
            fraction=fraction,
            interpolate=interpolate,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        pv_chain=None,
        fraction=0.5,
        interpolate=0,
        ):
        r'''Constructs a control-rate SpecPcile.

        ::

            >>> spec_pcile = ugentools.SpecPcile.kr(
            ...     pv_chain=None,
            ...     fraction=0.5,
            ...     interpolate=0,
            ...     )
            >>> spec_pcile

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            pv_chain=pv_chain,
            fraction=fraction,
            interpolate=interpolate,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain(self):
        r'''Gets `pv_chain` input of SpecPcile.

        ::

            >>> spec_pcile = ugentools.SpecPcile.ar(
            ...     pv_chain=None,
            ...     fraction=0.5,
            ...     interpolate=0,
            ...     )
            >>> spec_pcile.pv_chain

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('pv_chain')
        return self._inputs[index]

    @property
    def fraction(self):
        r'''Gets `fraction` input of SpecPcile.

        ::

            >>> spec_pcile = ugentools.SpecPcile.ar(
            ...     pv_chain=None,
            ...     fraction=0.5,
            ...     interpolate=0,
            ...     )
            >>> spec_pcile.fraction

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('fraction')
        return self._inputs[index]

    @property
    def interpolate(self):
        r'''Gets `interpolate` input of SpecPcile.

        ::

            >>> spec_pcile = ugentools.SpecPcile.ar(
            ...     pv_chain=None,
            ...     fraction=0.5,
            ...     interpolate=0,
            ...     )
            >>> spec_pcile.interpolate

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('interpolate')
        return self._inputs[index]