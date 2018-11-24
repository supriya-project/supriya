import collections
from supriya import CalculationRate
from supriya.ugens.Filter import Filter


class Lag2UD(Filter):
    """
    An up/down exponential lag generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> lag_2_ud = supriya.ugens.Lag2UD.ar(
        ...     lag_time_d=0.1,
        ...     lag_time_u=0.1,
        ...     source=source,
        ...     )
        >>> lag_2_ud
        Lag2UD.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Filter UGens"

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("lag_time_u", 0.1), ("lag_time_d", 0.1)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
