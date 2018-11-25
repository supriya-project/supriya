import collections

from supriya import CalculationRate
from supriya.ugens.BEQSuite import BEQSuite


class BBandPass(BEQSuite):
    """
    A band-pass filter.

    ::

        >>> source = supriya.ugens.In.ar(0)
        >>> bband_pass = supriya.ugens.BBandPass.ar(
        ...     bandwidth=1,
        ...     frequency=1200,
        ...     source=source,
        ...     )
        >>> bband_pass
        BBandPass.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("frequency", 1200), ("bandwidth", 1)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO,)
