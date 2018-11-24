import collections
from supriya import CalculationRate
from supriya.ugens.DUGen import DUGen


class Dunique(DUGen):
    """
    Returns the same unique series of values for several demand streams.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> dunique = supriya.ugens.Dunique.new(
        ...     max_buffer_size=1024,
        ...     protected=True,
        ...     source=source,
        ...     )
        >>> dunique
        Dunique()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [('source', None), ('max_buffer_size', 1024), ('protected', True)]
    )

    _valid_calculation_rates = (CalculationRate.DEMAND,)
