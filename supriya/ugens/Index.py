import collections
from supriya.enums import CalculationRate
from supriya.ugens.PureUGen import PureUGen


class Index(PureUGen):
    """
    A clipping buffer indexer.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> index = supriya.ugens.Index.ar(
        ...     buffer_id=23,
        ...     source=source,
        ...     )
        >>> index
        Index.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [('buffer_id', None), ('source', None)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
