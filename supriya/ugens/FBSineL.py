import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class FBSineL(UGen):
    """
    A linear-interpolating feedback sine with chaotic phase indexing.

    ::

        >>> fbsine_l = supriya.ugens.FBSineL.ar(
        ...     a=1.1,
        ...     c=0.5,
        ...     fb=0.1,
        ...     frequency=22050,
        ...     im=1,
        ...     xi=0.1,
        ...     yi=0.1,
        ...     )
        >>> fbsine_l
        FBSineL.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Chaos UGens'

    _ordered_input_names = collections.OrderedDict([
        ('frequency', 22050),
        ('im', 1.0),
        ('fb', 0.1),
        ('a', 1.1),
        ('c', 0.5),
        ('xi', 0.1),
        ('yi', 0.1),
    ])

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
    )
