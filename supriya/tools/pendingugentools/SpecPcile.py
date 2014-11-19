# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class SpecPcile(UGen):
    r'''

    ::

        >>> spec_pcile = ugentools.SpecPcile.(
        ...     buffer_id=None,
        ...     fraction=0.5,
        ...     interpolate=0,
        ...     )
        >>> spec_pcile

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        'fraction',
        'interpolate',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=None,
        fraction=0.5,
        interpolate=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            fraction=fraction,
            interpolate=interpolate,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        buffer_id=None,
        fraction=0.5,
        interpolate=0,
        ):
        r'''Constructs a control-rate SpecPcile.

        ::

            >>> spec_pcile = ugentools.SpecPcile.kr(
            ...     buffer_id=None,
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
            buffer_id=buffer_id,
            fraction=fraction,
            interpolate=interpolate,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        r'''Gets `buffer_id` input of SpecPcile.

        ::

            >>> spec_pcile = ugentools.SpecPcile.ar(
            ...     buffer_id=None,
            ...     fraction=0.5,
            ...     interpolate=0,
            ...     )
            >>> spec_pcile.buffer_id

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def fraction(self):
        r'''Gets `fraction` input of SpecPcile.

        ::

            >>> spec_pcile = ugentools.SpecPcile.ar(
            ...     buffer_id=None,
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
            ...     buffer_id=None,
            ...     fraction=0.5,
            ...     interpolate=0,
            ...     )
            >>> spec_pcile.interpolate

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('interpolate')
        return self._inputs[index]