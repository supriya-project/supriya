import collections

from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class Compander(UGen):
    """
    A general purpose hard-knee dynamics processor.

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Dynamics UGens"

    _ordered_input_names = collections.OrderedDict(
        [
            ("source", None),
            ("control", 0.0),
            ("threshold", 0.5),
            ("slope_below", 1.0),
            ("slope_above", 1.0),
            ("clamp_time", 0.01),
            ("relax_time", 0.1),
        ]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO,)
