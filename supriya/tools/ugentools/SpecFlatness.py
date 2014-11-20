# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class SpecFlatness(UGen):
    r'''

    ::

        >>> spec_flatness = ugentools.SpecFlatness.(
        ...     pv_chain=None,
        ...     )
        >>> spec_flatness

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Machine Listening UGens'

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        pv_chain=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            pv_chain=pv_chain,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        pv_chain=None,
        ):
        r'''Constructs a control-rate SpecFlatness.

        ::

            >>> spec_flatness = ugentools.SpecFlatness.kr(
            ...     pv_chain=None,
            ...     )
            >>> spec_flatness

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            pv_chain=pv_chain,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain(self):
        r'''Gets `pv_chain` input of SpecFlatness.

        ::

            >>> spec_flatness = ugentools.SpecFlatness.ar(
            ...     pv_chain=None,
            ...     )
            >>> spec_flatness.pv_chain

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('pv_chain')
        return self._inputs[index]