import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class CoinGate(UGen):
    """
    A probabilistic trigger gate.

    ::

        >>> trigger = supriya.ugens.Impulse.ar()
        >>> coin_gate = supriya.ugens.CoinGate.ar(
        ...     probability=0.5,
        ...     trigger=trigger,
        ...     )
        >>> coin_gate
        CoinGate.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Noise UGens"

    _ordered_input_names = collections.OrderedDict(
        [("probability", 0.5), ("trigger", None)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
