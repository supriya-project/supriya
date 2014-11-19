# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class SpecCentroid(UGen):
    r'''

    ::

        >>> spec_centroid = ugentools.SpecCentroid.(
        ...     buffer_=None,
        ...     )
        >>> spec_centroid

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'buffer_',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_=buffer_,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        buffer_=None,
        ):
        r'''Constructs a control-rate SpecCentroid.

        ::

            >>> spec_centroid = ugentools.SpecCentroid.kr(
            ...     buffer_=None,
            ...     )
            >>> spec_centroid

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_=buffer_,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_(self):
        r'''Gets `buffer_` input of SpecCentroid.

        ::

            >>> spec_centroid = ugentools.SpecCentroid.ar(
            ...     buffer_=None,
            ...     )
            >>> spec_centroid.buffer_

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_')
        return self._inputs[index]