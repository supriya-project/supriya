import collections
from supriya import CalculationRate
from supriya.ugens.BEQSuite import BEQSuite


class BPeakEQ(BEQSuite):
    """
    A parametric equalizer.

    ::

        >>> source = supriya.ugens.In.ar(0)
        >>> bpeak_eq = supriya.ugens.BPeakEQ.ar(
        ...     frequency=1200,
        ...     gain=0,
        ...     reciprocal_of_q=1,
        ...     source=source,
        ...     )
        >>> bpeak_eq
        BPeakEQ.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict([
        ('source', None),
        ('frequency', 1200),
        ('reciprocal_of_q', 1),
        ('gain', 0),
    ])

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
    )
