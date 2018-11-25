import collections

from supriya.enums import CalculationRate
from supriya.ugens.MultiOutUGen import MultiOutUGen


class Hilbert(MultiOutUGen):
    """
    Applies the Hilbert transform.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> hilbert = supriya.ugens.Hilbert.ar(
        ...     source=source,
        ...     )
        >>> hilbert
        UGenArray({2})

    """

    ### CLASS VARIABLES ###

    _default_channel_count = 2

    _has_settable_channel_count = False

    _ordered_input_names = collections.OrderedDict([("source", None)])

    _valid_calculation_rates = (CalculationRate.AUDIO,)
