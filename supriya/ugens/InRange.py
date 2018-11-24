import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class InRange(UGen):
    """
    Tests if a signal is within a given range.

    ::

        >>> source = supriya.ugens.SinOsc.ar()
        >>> in_range = supriya.ugens.InRange.ar(
        ...     maximum=0.9,
        ...     minimum=0.1,
        ...     source=source,
        ...     )
        >>> in_range
        InRange.ar()

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
