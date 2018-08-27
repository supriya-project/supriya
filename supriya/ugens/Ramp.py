import collections
from supriya import CalculationRate
from supriya.ugens.Lag import Lag


class Ramp(Lag):
    """
    Breaks a continuous signal into line segments.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> ramp = supriya.ugens.Ramp.ar(
        ...     lag_time=0.1,
        ...     source=source,
        ...     )
        >>> ramp
        Ramp.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Filter UGens'

    _ordered_input_names = collections.OrderedDict([
        ('source', None),
        ('lag_time', 0.1),
    ])

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
        CalculationRate.CONTROL,
    )
