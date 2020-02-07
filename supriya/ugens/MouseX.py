import collections

from supriya import CalculationRate, SignalRange
from supriya.synthdefs import UGen


class MouseX(UGen):
    """
    A mouse cursor tracker.

    MouseX tracks the y-axis of the mouse cursor position.

    ::

        >>> supriya.ugens.MouseX.kr()
        MouseX.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "User Interaction UGens"

    _ordered_input_names = collections.OrderedDict(
        [("minimum", 0), ("maximum", 1), ("warp", 0), ("lag", 0.2)]
    )

    _signal_range = SignalRange.UNIPOLAR

    _valid_calculation_rates = (CalculationRate.CONTROL,)
