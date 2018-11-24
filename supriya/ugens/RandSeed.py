import collections

from supriya import CalculationRate
from supriya.ugens.WidthFirstUGen import WidthFirstUGen


class RandSeed(WidthFirstUGen):
    """
    Sets the synth's random generator seed.

    ::

        >>> trigger = supriya.ugens.Impulse.ar()
        >>> rand_seed = supriya.ugens.RandSeed.ar(
        ...     seed=1,
        ...     trigger=trigger,
        ...     )
        >>> rand_seed
        RandSeed.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Noise UGens"

    _ordered_input_names = collections.OrderedDict([("trigger", 0), ("seed", 56789)])

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
        CalculationRate.CONTROL,
        CalculationRate.SCALAR,
    )
