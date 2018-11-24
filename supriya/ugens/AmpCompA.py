import collections
from supriya import CalculationRate
from supriya.ugens.PureUGen import PureUGen


class AmpCompA(PureUGen):
    """
    Basic psychoacoustic amplitude compensation (ANSI A-weighting curve).

    ::

        >>> amp_comp_a = supriya.ugens.AmpCompA.ar(
        ...     frequency=1000,
        ...     min_amp=0.32,
        ...     root=0,
        ...     root_amp=1,
        ...     )
        >>> amp_comp_a
        AmpCompA.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Line Utility UGens'

    _ordered_input_names = collections.OrderedDict(
        [('frequency', 1000), ('root', 0), ('min_amp', 0.32), ('root_amp', 1)]
    )

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
        CalculationRate.CONTROL,
        CalculationRate.SCALAR,
    )
