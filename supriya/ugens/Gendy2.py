import collections

from supriya import CalculationRate
from supriya.synthdefs import UGen


class Gendy2(UGen):
    """
    A dynamic stochastic synthesis generator.

    ::

        >>> gendy_2 = supriya.ugens.Gendy2.ar(
        ...     a=1.17,
        ...     adparam=1,
        ...     ampdist=1,
        ...     ampscale=0.5,
        ...     c=0.31,
        ...     ddparam=1,
        ...     durdist=1,
        ...     durscale=0.5,
        ...     init_cps=12,
        ...     knum=10,
        ...     maxfrequency=660,
        ...     minfrequency=440,
        ...     )
        >>> gendy_2
        Gendy2.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Noise UGens"

    _ordered_input_names = collections.OrderedDict(
        [
            ("ampdist", 1),
            ("durdist", 1),
            ("adparam", 1),
            ("ddparam", 1),
            ("minfrequency", 440),
            ("maxfrequency", 660),
            ("ampscale", 0.5),
            ("durscale", 0.5),
            ("init_cps", 12),
            ("knum", None),
            ("a", 1.17),
            ("c", 0.31),
        ]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
