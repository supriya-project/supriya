import collections

from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class TRand(UGen):
    """
    A triggered random number generator.

    ::

        >>> trigger = supriya.ugens.Impulse.ar()
        >>> t_rand = supriya.ugens.TRand.ar(
        ...     minimum=-1.,
        ...     maximum=1.,
        ...     trigger=trigger,
        ...     )
        >>> t_rand
        TRand.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Noise UGens"

    _ordered_input_names = collections.OrderedDict(
        [("minimum", 0), ("maximum", 1), ("trigger", 0)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
