import collections

from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class FreqShift(UGen):
    """

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> freq_shift = supriya.ugens.FreqShift.ar(
        ...     frequency=0,
        ...     phase=0,
        ...     source=source,
        ...     )
        >>> freq_shift
        FreqShift.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("frequency", 0.0), ("phase", 0.0)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO,)
