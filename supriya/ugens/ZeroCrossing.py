import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class ZeroCrossing(UGen):
    """
    A zero-crossing frequency follower.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> zero_crossing = supriya.ugens.ZeroCrossing.ar(
        ...     source=source,
        ...     )
        >>> zero_crossing
        ZeroCrossing.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Analysis UGens"

    _ordered_input_names = collections.OrderedDict([("source", None)])

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
