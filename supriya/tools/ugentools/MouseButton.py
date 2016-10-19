# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.CalculationRate import CalculationRate
from supriya.tools.synthdeftools.SignalRange import SignalRange
from supriya.tools.ugentools.UGen import UGen


class MouseButton(UGen):
    r"""
    A mouse-button tracker.

    ::

        >>> ugentools.MouseButton.kr()
        MouseButton.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'User Interaction UGens'

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
        r"""
        Constructs a control-rate mouse button tracking unit generator.

        ::

            >>> ugentools.MouseButton.kr(
            ...     lag=0.2,
            ...     maximum=1,
            ...     minimum=0,
            ...     )
            MouseButton.kr()

        Returns unit generator graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            lag=lag,
            maximum=maximum,
            minimum=minimum,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def lag(self):
        r"""
        Gets `lag` input of MouseButton.

        ::

            >>> mouse_button = ugentools.MouseButton.kr(
            ...     lag=0.2,
            ...     maximum=1,
            ...     minimum=0,
            ...     )
            >>> mouse_button.lag
            0.2

        Returns ugen input.
        """
        index = self._ordered_input_names.index('lag')
        return self._inputs[index]

    @property
    def maximum(self):
        r"""
        Gets `maximum` input of MouseButton.

        ::

            >>> mouse_button = ugentools.MouseButton.kr(
            ...     lag=0.2,
            ...     maximum=1,
            ...     minimum=0,
            ...     )
            >>> mouse_button.maximum
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('maximum')
        return self._inputs[index]

    @property
    def minimum(self):
        r"""
        Gets `minimum` input of MouseButton.

        ::

            >>> mouse_button = ugentools.MouseButton.kr(
            ...     lag=0.2,
            ...     maximum=1,
            ...     minimum=0,
            ...     )
            >>> mouse_button.minimum
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('minimum')
        return self._inputs[index]
