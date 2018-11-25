import collections

from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class Gendy3(UGen):
    """
    A dynamic stochastic synthesis generator.

    ::

        >>> gendy_3 = supriya.ugens.Gendy3.ar(
        ...     adparam=1,
        ...     ampdist=1,
        ...     ampscale=0.5,
        ...     ddparam=1,
        ...     durdist=1,
        ...     durscale=0.5,
        ...     frequency=440,
        ...     init_cps=12,
        ...     knum=10,
        ...     )
        >>> gendy_3
        Gendy3.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Noise UGens"

    _ordered_input_names = collections.OrderedDict(
        [
            ("ampdist", 1),
            ("durdist", 1),
            ("adparam", 1),
            ("ddparam", 1),
            ("frequency", 440),
            ("ampscale", 0.5),
            ("durscale", 0.5),
            ("init_cps", 12),
            ("knum", None),
        ]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
