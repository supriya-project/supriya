import collections

from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class NRand(UGen):
    """
    A sum of `n` uniform distributions.

    ::

        >>> n_rand = supriya.ugens.NRand.ir(
        ...     minimum=-1,
        ...     maximum=1,
        ...     n=1,
        ...     )
        >>> n_rand
        NRand.ir()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Noise UGens"

    _ordered_input_names = collections.OrderedDict(
        [("minimum", 0.0), ("maximum", 1.0), ("n", 1)]
    )

    _valid_calculation_rates = (CalculationRate.SCALAR,)
