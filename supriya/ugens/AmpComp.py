import collections
from supriya import CalculationRate
from supriya.ugens.PureUGen import PureUGen


class AmpComp(PureUGen):
    """
    Basic psychoacoustic amplitude compensation.

    ::

        >>> amp_comp = supriya.ugens.AmpComp.ar(
        ...     exp=0.3333,
        ...     frequency=1000,
        ...     root=0,
        ...     )
        >>> amp_comp
        AmpComp.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Line Utility UGens'

    _ordered_input_names = collections.OrderedDict([
        ('frequency', 1000),
        ('root', 0),
        ('exp', 0.3333),
    ])

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
        CalculationRate.CONTROL,
        CalculationRate.SCALAR,
    )
