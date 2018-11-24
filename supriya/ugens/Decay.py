import collections
from supriya import CalculationRate
from supriya.ugens.Filter import Filter


class Decay(Filter):
    """
    A leaky signal integrator.

    ::

        >>> source = supriya.ugens.Impulse.ar()
        >>> decay = supriya.ugens.Decay.ar(
        ...     source=source,
        ...     )
        >>> decay
        Decay.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("decay_time", 1.0)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
