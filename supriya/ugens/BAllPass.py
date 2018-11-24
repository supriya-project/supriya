import collections
from supriya import CalculationRate
from supriya.ugens.BEQSuite import BEQSuite


class BAllPass(BEQSuite):
    """
    An all-pass filter.

    ::

        >>> source = supriya.ugens.In.ar(0)
        >>> ball_pass = supriya.ugens.BAllPass.ar(
        ...     frequency=1200,
        ...     reciprocal_of_q=1,
        ...     source=source,
        ...     )
        >>> ball_pass
        BAllPass.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("frequency", 1200), ("reciprocal_of_q", 1)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO,)
