import collections
from supriya import CalculationRate
from supriya.ugens.Filter import Filter


class OnePole(Filter):
    """
    A one pole filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> one_pole = supriya.ugens.OnePole.ar(
        ...     coefficient=0.5,
        ...     source=source,
        ...     )
        >>> one_pole
        OnePole.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Filter UGens"

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("coefficient", 0.5)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
