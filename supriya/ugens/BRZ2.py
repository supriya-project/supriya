import collections

from supriya import CalculationRate
from supriya.ugens.LPZ2 import LPZ2


class BRZ2(LPZ2):
    """
    A two zero fixed midcut filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> brz_2 = supriya.ugens.BRZ2.ar(
        ...     source=source,
        ...     )
        >>> brz_2
        BRZ2.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Filter UGens"

    _ordered_input_names = collections.OrderedDict([("source", None)])

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
