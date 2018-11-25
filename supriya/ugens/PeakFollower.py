import collections

from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class PeakFollower(UGen):
    """
    Tracks peak signal amplitude.

    ::

        >>> source = supriya.ugens.In.ar(0)
        >>> peak_follower = supriya.ugens.PeakFollower.ar(
        ...     decay=0.999,
        ...     source=source,
        ...     )
        >>> peak_follower
        PeakFollower.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Trigger Utility UGens"

    _ordered_input_names = collections.OrderedDict([("source", None), ("decay", 0.999)])

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
