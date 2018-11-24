import collections

from supriya import CalculationRate
from supriya.ugens.LPZ2 import LPZ2


class BPZ2(LPZ2):
    """
    A two zero fixed midpass filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> bpz_2 = supriya.ugens.BPZ2.ar(
        ...     source=source,
        ...     )
        >>> bpz_2
        BPZ2.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Filter UGens"

    _ordered_input_names = collections.OrderedDict([("source", None)])

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
