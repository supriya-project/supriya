import collections
from supriya import CalculationRate
from supriya.ugens.Filter import Filter


class Lag3(Filter):
    """
    An exponential lag generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> lag_3 = supriya.ugens.Lag3.ar(
        ...     lag_time=0.1,
        ...     source=source,
        ...     )
        >>> lag_3
        Lag3.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Filter UGens'

    _ordered_input_names = collections.OrderedDict(
        [('source', None), ('lag_time', 0.1)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
