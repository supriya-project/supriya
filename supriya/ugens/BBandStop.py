import collections
from supriya import CalculationRate
from supriya.ugens.BEQSuite import BEQSuite


class BBandStop(BEQSuite):
    """
    A band-stop filter.

    ::

        >>> source = supriya.ugens.In.ar(0)
        >>> bband_stop = supriya.ugens.BBandStop.ar(
        ...     bandwidth=1,
        ...     frequency=1200,
        ...     source=source,
        ...     )
        >>> bband_stop
        BBandStop.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict([
        ('source', None),
        ('frequency', 1200),
        ('bandwidth', 1),
    ])

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
    )
