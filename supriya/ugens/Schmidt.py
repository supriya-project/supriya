import collections

from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class Schmidt(UGen):
    """
    A Schmidt trigger.

    ::

        >>> source = supriya.ugens.SinOsc.ar()
        >>> schmidt = supriya.ugens.Schmidt.ar(
        ...     maximum=0.9,
        ...     minimum=0.1,
        ...     source=source,
        ...     )
        >>> schmidt
        Schmidt.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Trigger Utility UGens"

    _ordered_input_names = collections.OrderedDict(
        [("source", 0), ("minimum", 0), ("maximum", 1)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
