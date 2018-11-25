import collections

from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class LinRand(UGen):
    """
    A skewed linear random distribution.

    ::

        >>> lin_rand = supriya.ugens.LinRand.ir(
        ...    minimum=-1.,
        ...    maximum=1.,
        ...    skew=0.5,
        ...    )
        >>> lin_rand
        LinRand.ir()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Noise UGens"

    _ordered_input_names = collections.OrderedDict(
        [("minimum", 0.0), ("maximum", 1.0), ("skew", 0)]
    )

    _valid_calculation_rates = (CalculationRate.SCALAR,)
