import collections
from supriya import CalculationRate
from supriya.synthdefs.SignalRange import SignalRange
from supriya.ugens.UGen import UGen


class MouseButton(UGen):
    """
    A mouse-button tracker.

    ::

        >>> supriya.ugens.MouseButton.kr()
        MouseButton.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'User Interaction UGens'

    _ordered_input_names = collections.OrderedDict(
        [('minimum', 0), ('maximum', 1), ('lag', 0.2)]
    )

    _signal_range = SignalRange.UNIPOLAR

    _valid_calculation_rates = (CalculationRate.CONTROL,)
