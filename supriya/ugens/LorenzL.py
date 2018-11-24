import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class LorenzL(UGen):
    """
    A linear-interpolating Lorenz chaotic generator.

    ::

        >>> lorenz_l = supriya.ugens.LorenzL.ar(
        ...     b=2.667,
        ...     frequency=22050,
        ...     h=0.05,
        ...     r=28,
        ...     s=10,
        ...     xi=0.1,
        ...     yi=0,
        ...     zi=0,
        ...     )
        >>> lorenz_l
        LorenzL.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Chaos UGens'

    _ordered_input_names = collections.OrderedDict(
        [
            ('frequency', 22050),
            ('s', 10),
            ('r', 28),
            ('b', 2.667),
            ('h', 0.05),
            ('xi', 0.1),
            ('yi', 0),
            ('zi', 0),
        ]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO,)
