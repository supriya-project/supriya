import collections

from supriya import CalculationRate
from supriya.synthdefs import UGen


class Ball(UGen):
    """
    A bouncing ball physical model.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> ball = supriya.ugens.Ball.ar(
        ...     damping=0,
        ...     friction=0.01,
        ...     gravity=1,
        ...     source=source,
        ...     )
        >>> ball
        Ball.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Physical Modelling UGens"

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("gravity", 1.0), ("damping", 0.0), ("friction", 0.01)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
