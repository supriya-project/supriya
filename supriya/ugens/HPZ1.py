import collections
from supriya import CalculationRate
from supriya.ugens.LPZ1 import LPZ1


class HPZ1(LPZ1):
    """
    A two point difference filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> hpz_1 = supriya.ugens.HPZ1.ar(
        ...     source=source,
        ...     )
        >>> hpz_1
        HPZ1.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Filter UGens"

    _ordered_input_names = collections.OrderedDict([("source", None)])

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
