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
        ... )
        >>> ball
        Ball.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("gravity", 1.0), ("damping", 0.0), ("friction", 0.01)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class Pluck(UGen):
    """
    A Karplus-String UGen.

    ::

        >>> source = supriya.ugens.WhiteNoise.ar()
        >>> trigger = supriya.ugens.Dust.kr(2)
        >>> pluck = supriya.ugens.Pluck.ar(
        ...     coefficient=0.5,
        ...     decay_time=1,
        ...     delay_time=0.2,
        ...     maximum_delay_time=0.2,
        ...     source=source,
        ...     trigger=trigger,
        ... )
        >>> pluck
        Pluck.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [
            ("source", None),
            ("trigger", None),
            ("maximum_delay_time", 0.2),
            ("delay_time", 0.2),
            ("decay_time", 1),
            ("coefficient", 0.5),
        ]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class Spring(UGen):
    """
    A resonating spring physical model.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> spring = supriya.ugens.Spring.ar(
        ...     damping=0,
        ...     source=source,
        ...     spring=1,
        ... )
        >>> spring
        Spring.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("spring", 1), ("damping", 0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


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
        ... )
        >>> tball
        TBall.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("gravity", 10), ("damping", 0), ("friction", 0.01)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
