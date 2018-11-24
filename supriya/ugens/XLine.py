import collections

from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class XLine(UGen):
    """
    An exponential line generating unit generator.

    ::

        >>> supriya.ugens.XLine.ar()
        XLine.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Line Utility UGens"

    _has_done_flag = True

    _ordered_input_names = collections.OrderedDict(
        [("start", 0.0), ("stop", 1.0), ("duration", 1.0), ("done_action", 0.0)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
