import collections
from supriya import CalculationRate
from supriya.ugens.WidthFirstUGen import WidthFirstUGen


class ClearBuf(WidthFirstUGen):
    """

    ::

        >>> clear_buf = supriya.ugens.ClearBuf.ir(
        ...     buffer_id=23,
        ...     )
        >>> clear_buf
        ClearBuf.ir()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Buffer UGens'

    _ordered_input_names = collections.OrderedDict([
        ('buffer_id', None),
    ])

    _valid_calculation_rates = (
        CalculationRate.SCALAR,
    )
