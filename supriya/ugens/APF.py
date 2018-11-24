import collections

from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class APF(UGen):
    """
    An all-pass filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> apf = supriya.ugens.APF.ar(
        ...     frequency=440,
        ...     radius=0.8,
        ...     source=source,
        ...     )
        >>> apf
        APF.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Filter UGens"

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("frequency", 440.0), ("radius", 0.8)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
