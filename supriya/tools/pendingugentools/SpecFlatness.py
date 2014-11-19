# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class SpecFlatness(UGen):
    r'''

    ::

        >>> spec_flatness = ugentools.SpecFlatness.(
        ...     buffer_id=None,
        ...     )
        >>> spec_flatness

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
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        buffer_id=None,
        ):
        r'''Constructs a control-rate SpecFlatness.

        ::

            >>> spec_flatness = ugentools.SpecFlatness.kr(
            ...     buffer_id=None,
            ...     )
            >>> spec_flatness

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        r'''Gets `buffer_id` input of SpecFlatness.

        ::

            >>> spec_flatness = ugentools.SpecFlatness.ar(
            ...     buffer_id=None,
            ...     )
            >>> spec_flatness.buffer_id

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]