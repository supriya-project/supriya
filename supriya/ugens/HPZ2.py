import collections
from supriya import CalculationRate
from supriya.ugens.LPZ2 import LPZ2


class HPZ2(LPZ2):
    """
    A two zero fixed midcut filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> hpz_2 = supriya.ugens.HPZ2.ar(
        ...     source=source,
        ...     )
        >>> hpz_2
        HPZ2.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Filter UGens"

    _ordered_input_names = collections.OrderedDict([("source", None)])

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
