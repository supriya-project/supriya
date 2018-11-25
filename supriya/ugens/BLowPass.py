import collections

from supriya import CalculationRate
from supriya.ugens.BEQSuite import BEQSuite


class BLowPass(BEQSuite):
    """
    A low-pass filter.

    ::

        >>> source = supriya.ugens.In.ar(0)
        >>> blow_pass = supriya.ugens.BLowPass.ar(
        ...     frequency=1200,
        ...     reciprocal_of_q=1,
        ...     source=source,
        ...     )
        >>> blow_pass
        BLowPass.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("frequency", 1200), ("reciprocal_of_q", 1)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO,)
