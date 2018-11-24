import collections

from supriya import CalculationRate
from supriya.ugens.PureUGen import PureUGen


class DC(PureUGen):
    """
    A DC unit generator.

    ::

        >>> supriya.ugens.DC.ar(
        ...     source=0,
        ...     )
        DC.ar()

    ::

        >>> supriya.ugens.DC.ar(
        ...     source=(1, 2, 3),
        ...     )
        UGenArray({3})

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Utility UGens"

    _ordered_input_names = collections.OrderedDict([("source", None)])

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
