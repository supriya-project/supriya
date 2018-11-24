import collections
from supriya import CalculationRate
from supriya.ugens.Filter import Filter


class Integrator(Filter):
    """
    A leaky integrator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> integrator = supriya.ugens.Integrator.ar(
        ...     coefficient=1,
        ...     source=source,
        ...     )
        >>> integrator
        Integrator.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Filter UGens"

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("coefficient", 1)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
