import collections

from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class Wrap(UGen):
    """
    Wraps a signal outside given thresholds.

    ::

        >>> source = supriya.ugens.SinOsc.ar()
        >>> wrap = supriya.ugens.Wrap.ar(
        ...     maximum=0.9,
        ...     minimum=0.1,
        ...     source=source,
        ...     )
        >>> wrap
        Wrap.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Trigger Utility UGens"

    _ordered_input_names = collections.OrderedDict(
        [("source", 0), ("minimum", 0), ("maximum", 1)]
    )

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
        CalculationRate.CONTROL,
        CalculationRate.SCALAR,
    )
