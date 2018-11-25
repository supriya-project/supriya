import collections

from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class Spring(UGen):
    """
    A resonating spring physical model.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> spring = supriya.ugens.Spring.ar(
        ...     damping=0,
        ...     source=source,
        ...     spring=1,
        ...     )
        >>> spring
        Spring.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Physical Modelling UGens"

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("spring", 1), ("damping", 0)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
