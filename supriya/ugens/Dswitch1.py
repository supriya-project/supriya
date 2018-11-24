import collections
from supriya import CalculationRate
from supriya.ugens.DUGen import DUGen


class Dswitch1(DUGen):
    """
    A demand-rate generator for switching between inputs.

    ::

        >>> index = supriya.ugens.Dseq(sequence=[0, 1, 2, 1, 0])
        >>> sequence = (1., 2., 3.)
        >>> dswitch_1 = supriya.ugens.Dswitch1.new(
        ...     index=index,
        ...     sequence=sequence,
        ...     )
        >>> dswitch_1
        Dswitch1()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [("index", None), ("sequence", None)]
    )

    _unexpanded_input_names = ("sequence",)

    _valid_calculation_rates = (CalculationRate.DEMAND,)
