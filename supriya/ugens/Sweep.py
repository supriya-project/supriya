import collections
from supriya.enums import CalculationRate
from supriya.ugens.UGen import UGen


class Sweep(UGen):
    """
    A triggered linear ramp.

    ::

        >>> sweep = supriya.ugens.Sweep.ar(
        ...     rate=1,
        ...     trigger=0,
        ...     )
        >>> sweep
        Sweep.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict([("trigger", 0), ("rate", 1)])

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
