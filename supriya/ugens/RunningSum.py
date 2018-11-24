import collections
from supriya.enums import CalculationRate
from supriya.ugens.UGen import UGen


class RunningSum(UGen):
    """
    Tracks running sum over ``n`` frames.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> running_sum = supriya.ugens.RunningSum.ar(
        ...     sample_count=40,
        ...     source=source,
        ...     )
        >>> running_sum
        RunningSum.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("sample_count", 40)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
