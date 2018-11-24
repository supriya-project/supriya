import collections
from supriya import CalculationRate
from supriya.ugens.Filter import Filter


class Formlet(Filter):
    """
    A FOF-like filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> formlet = supriya.ugens.Formlet.ar(
        ...     attack_time=1,
        ...     decay_time=1,
        ...     frequency=440,
        ...     source=source,
        ...     )
        >>> formlet
        Formlet.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Filter UGens"

    _ordered_input_names = collections.OrderedDict(
        [
            ("source", None),
            ("frequency", 440.0),
            ("attack_time", 1.0),
            ("decay_time", 1.0),
        ]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
