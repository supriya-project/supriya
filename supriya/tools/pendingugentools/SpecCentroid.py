# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class SpecCentroid(UGen):
    r'''

    ::

        >>> spec_centroid = ugentools.SpecCentroid.(
        ...     buffer_id=None,
        ...     )
        >>> spec_centroid

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
        r'''Constructs a control-rate SpecCentroid.

        ::

            >>> spec_centroid = ugentools.SpecCentroid.kr(
            ...     buffer_id=None,
            ...     )
            >>> spec_centroid

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
        r'''Gets `buffer_id` input of SpecCentroid.

        ::

            >>> spec_centroid = ugentools.SpecCentroid.ar(
            ...     buffer_id=None,
            ...     )
            >>> spec_centroid.buffer_id

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]