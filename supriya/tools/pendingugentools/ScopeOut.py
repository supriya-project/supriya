# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class ScopeOut(UGen):
    r'''

    ::

        >>> scope_out = ugentools.ScopeOut.(
        ...     buffer_id=0,
        ...     input_array=None,
        ...     )
        >>> scope_out

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'input_array',
        'buffer_id',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=0,
        input_array=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            input_array=input_array,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer_id=0,
        input_array=None,
        ):
        r'''Constructs an audio-rate ScopeOut.

        ::

            >>> scope_out = ugentools.ScopeOut.ar(
            ...     buffer_id=0,
            ...     input_array=None,
            ...     )
            >>> scope_out

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            input_array=input_array,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        buffer_id=0,
        input_array=None,
        ):
        r'''Constructs a control-rate ScopeOut.

        ::

            >>> scope_out = ugentools.ScopeOut.kr(
            ...     buffer_id=0,
            ...     input_array=None,
            ...     )
            >>> scope_out

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            input_array=input_array,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        r'''Gets `buffer_id` input of ScopeOut.

        ::

            >>> scope_out = ugentools.ScopeOut.ar(
            ...     buffer_id=0,
            ...     input_array=None,
            ...     )
            >>> scope_out.buffer_id

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def input_array(self):
        r'''Gets `input_array` input of ScopeOut.

        ::

            >>> scope_out = ugentools.ScopeOut.ar(
            ...     buffer_id=0,
            ...     input_array=None,
            ...     )
            >>> scope_out.input_array

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('input_array')
        return self._inputs[index]