import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class StandardL(UGen):
    """
    A linear-interpolating standard map chaotic generator.

    ::

        >>> standard_l = supriya.ugens.StandardL.ar(
        ...     frequency=22050,
        ...     k=1,
        ...     xi=0.5,
        ...     yi=0,
        ...     )
        >>> standard_l
        StandardL.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Chaos UGens'

    _ordered_input_names = collections.OrderedDict(
        [('frequency', 22050), ('k', 1), ('xi', 0.5), ('yi', 0)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO,)
