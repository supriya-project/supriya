import collections
from supriya.enums import CalculationRate
from supriya.ugens.UGen import UGen


class WrapIndex(UGen):
    """
    A wrapping buffer indexer.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> wrap_index = supriya.ugens.WrapIndex.ar(
        ...     buffer_id=23,
        ...     source=source,
        ...     )
        >>> wrap_index
        WrapIndex.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict([
        ('buffer_id', None),
        ('source', None),
    ])

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
        CalculationRate.CONTROL,
    )
