import collections
from supriya import CalculationRate
from supriya.ugens.WidthFirstUGen import WidthFirstUGen


class RandID(WidthFirstUGen):
    """
    Sets the synth's random generator ID.

    ::

        >>> rand_id = supriya.ugens.RandID.ir(
        ...     rand_id=1,
        ...     )
        >>> rand_id
        RandID.ir()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Noise UGens'

    _ordered_input_names = collections.OrderedDict([('rand_id', 1)])

    _valid_calculation_rates = (CalculationRate.CONTROL, CalculationRate.SCALAR)
