# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.CalculationRate import CalculationRate
from supriya.tools.synthdeftools.SignalRange import SignalRange
from supriya.tools.synthdeftools.UGen import UGen


class MouseButton(UGen):
    r'''A mouse-button tracker.

    ::

        >>> ugentools.MouseButton.kr()
        MouseButton.kr()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'User Interaction'

    __slots__ = ()

    _ordered_input_names = (
        'minimum',
        'maximum',
        'lag',
        )

    _signal_range = SignalRange.UNIPOLAR

    _valid_calculation_rates = (
        CalculationRate.CONTROL,
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        lag=0.2,
        maximum=1,
        minimum=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            lag=lag,
            maximum=maximum,
            minimum=minimum,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        lag=0.2,
        maximum=1,
        minimum=0,
        ):
        r'''Creates a control-rate mouse button tracking unit generator.

        ::

            >>> ugentools.MouseButton.kr(
            ...     lag=0.2,
            ...     maximum=1,
            ...     minimum=0,
            ...     )
            MouseButton.kr()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            lag=lag,
            maximum=maximum,
            minimum=minimum,
            )
        return ugen