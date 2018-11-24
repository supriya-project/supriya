import collections
from supriya import CalculationRate
from supriya.ugens.BEQSuite import BEQSuite


class BHiPass(BEQSuite):
    """
    A high-pass filter.

    ::

        >>> source = supriya.ugens.In.ar(0)
        >>> bhi_pass = supriya.ugens.BHiPass.ar(
        ...     frequency=1200,
        ...     reciprocal_of_q=1,
        ...     source=source,
        ...     )
        >>> bhi_pass
        BHiPass.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [('source', None), ('frequency', 1200), ('reciprocal_of_q', 1)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO,)
