import collections
from supriya import CalculationRate
from supriya.ugens.Filter import Filter


class LagUD(Filter):
    """
    An up/down lag generator.

    ::

        >>> source = supriya.ugens.In.kr(bus=0)
        >>> supriya.ugens.LagUD.kr(
        ...     lag_time_down=1.25,
        ...     lag_time_up=0.5,
        ...     source=source,
        ...     )
        LagUD.kr()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [('source', None), ('lag_time_up', 0.1), ('lag_time_down', 0.1)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
