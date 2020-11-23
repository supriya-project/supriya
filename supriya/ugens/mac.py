import collections

from supriya import CalculationRate, SignalRange
from supriya.synthdefs import UGen


class KeyState(UGen):
    _ordered_input_names = collections.OrderedDict(
        [("keycode", 0.0), ("minimum", 0.0), ("maximum", 1.0), ("lag", 0.2)]
    )
    _signal_range = SignalRange.UNIPOLAR
    _valid_calculation_rates = (CalculationRate.CONTROL,)


class MouseButton(UGen):
    """
    A mouse-button tracker.

    ::

        >>> supriya.ugens.MouseButton.kr()
        MouseButton.kr()

    """

    _ordered_input_names = collections.OrderedDict(
        [("minimum", 0), ("maximum", 1), ("lag", 0.2)]
    )
    _signal_range = SignalRange.UNIPOLAR
    _valid_calculation_rates = (CalculationRate.CONTROL,)


class MouseX(UGen):
    """
    A mouse cursor tracker.

    MouseX tracks the y-axis of the mouse cursor position.

    ::

        >>> supriya.ugens.MouseX.kr()
        MouseX.kr()

    """

    _ordered_input_names = collections.OrderedDict(
        [("minimum", 0), ("maximum", 1), ("warp", 0), ("lag", 0.2)]
    )
    _signal_range = SignalRange.UNIPOLAR
    _valid_calculation_rates = (CalculationRate.CONTROL,)


class MouseY(UGen):
    """
    A mouse cursor tracker.

    MouseY tracks the y-axis of the mouse cursor position.

    ::

        >>> supriya.ugens.MouseY.kr()
        MouseY.kr()

    """

    _ordered_input_names = collections.OrderedDict(
        [("minimum", 0), ("maximum", 1), ("warp", 0), ("lag", 0.2)]
    )
    _signal_range = SignalRange.UNIPOLAR
    _valid_calculation_rates = (CalculationRate.CONTROL,)
