import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class FBSineC(UGen):
    """
    A cubic-interpolating feedback sine with chaotic phase indexing.

    ::

        >>> fbsine_c = supriya.ugens.FBSineC.ar(
        ...     a=1.1,
        ...     c=0.5,
        ...     fb=0.1,
        ...     frequency=22050,
        ...     im=1,
        ...     xi=0.1,
        ...     yi=0.1,
        ...     )
        >>> fbsine_c
        FBSineC.ar()

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
