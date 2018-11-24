import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class TBall(UGen):
    """
    A bouncing object physical model.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> tball = supriya.ugens.TBall.ar(
        ...     damping=0,
        ...     friction=0.01,
        ...     gravity=10,
        ...     source=source,
        ...     )
        >>> tball
        TBall.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Physical Modelling UGens"

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("gravity", 10), ("damping", 0), ("friction", 0.01)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
