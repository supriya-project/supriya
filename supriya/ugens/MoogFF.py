import collections

from supriya.enums import CalculationRate
from supriya.ugens.Filter import Filter


class MoogFF(Filter):
    """
    A Moog VCF implementation.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> moog_ff = supriya.ugens.MoogFF.ar(
        ...     frequency=100,
        ...     gain=2,
        ...     reset=0,
        ...     source=source,
        ...     )
        >>> moog_ff
        MoogFF.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("frequency", 100), ("gain", 2), ("reset", 0)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
