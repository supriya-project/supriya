import collections
from supriya import CalculationRate
from supriya.ugens.Filter import Filter


class Lag3UD(Filter):
    """
    An up/down exponential lag generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> lag_3_ud = supriya.ugens.Lag3UD.ar(
        ...     lag_time_d=0.1,
        ...     lag_time_u=0.1,
        ...     source=source,
        ...     )
        >>> lag_3_ud
        Lag3UD.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Filter UGens"

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("lag_time_u", 0.1), ("lag_time_d", 0.1)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
