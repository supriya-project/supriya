import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class CuspL(UGen):
    """
    A linear-interpolating cusp map chaotic generator.

    ::

        >>> cusp_l = supriya.ugens.CuspL.ar(
        ...     a=1,
        ...     b=1.9,
        ...     frequency=22050,
        ...     xi=0,
        ...     )
        >>> cusp_l
        CuspL.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Chaos UGens'

    _ordered_input_names = collections.OrderedDict([
        ('frequency', 22050),
        ('a', 1.0),
        ('b', 1.9),
        ('xi', 0.0),
    ])

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
    )
