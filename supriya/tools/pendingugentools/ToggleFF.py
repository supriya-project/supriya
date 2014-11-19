# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class ToggleFF(UGen):
    r'''

    ::

        >>> toggle_ff = ugentools.ToggleFF.(
        ...     trigger=0,
        ...     )
        >>> toggle_ff

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'trigger',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        trigger=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        trigger=0,
        ):
        r'''Constructs an audio-rate ToggleFF.

        ::

            >>> toggle_ff = ugentools.ToggleFF.ar(
            ...     trigger=0,
            ...     )
            >>> toggle_ff

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            trigger=trigger,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        trigger=0,
        ):
        r'''Constructs a control-rate ToggleFF.

        ::

            >>> toggle_ff = ugentools.ToggleFF.kr(
            ...     trigger=0,
            ...     )
            >>> toggle_ff

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            trigger=trigger,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def trigger(self):
        r'''Gets `trigger` input of ToggleFF.

        ::

            >>> toggle_ff = ugentools.ToggleFF.ar(
            ...     trigger=0,
            ...     )
            >>> toggle_ff.trigger

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]