import collections
from supriya import CalculationRate
from supriya.ugens.MultiOutUGen import MultiOutUGen


class Demand(MultiOutUGen):
    """
    Demands results from demand-rate UGens.

    ::

        >>> source = [
        ...     supriya.ugens.Dseries(),
        ...     supriya.ugens.Dwhite(),
        ...     ]
        >>> trigger = supriya.ugens.Impulse.kr(1)
        >>> demand = supriya.ugens.Demand.ar(
        ...     reset=0,
        ...     source=source,
        ...     trigger=trigger,
        ...     )
        >>> demand
        UGenArray({2})

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Demand UGens"

    _default_channel_count = 1

    _has_settable_channel_count = False

    _ordered_input_names = collections.OrderedDict(
        [("trigger", 0), ("reset", 0), ("source", None)]
    )

    _unexpanded_input_names = ("source",)

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)

    ### INITIALIZER ###

    def __init__(self, calculation_rate=None, trigger=None, reset=None, source=None):
        if not isinstance(source, collections.Sequence):
            source = [source]
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            trigger=trigger,
            reset=reset,
            source=source,
            channel_count=len(source),
        )
