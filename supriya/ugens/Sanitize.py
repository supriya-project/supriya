import collections

from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class Sanitize(UGen):
    """
    Remove infinity, NaN, and denormals.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Utility UGens"

    _ordered_input_names = collections.OrderedDict([("source", None), ("replace", 0.0)])

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
