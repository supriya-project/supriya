import collections

from supriya import CalculationRate
from supriya.ugens.Filter import Filter


class TwoPole(Filter):
    """
    A two pole filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> two_pole = supriya.ugens.TwoPole.ar(
        ...     frequency=440,
        ...     radius=0.8,
        ...     source=source,
        ...     )
        >>> two_pole
        TwoPole.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Filter UGens"

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("frequency", 440), ("radius", 0.8)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
