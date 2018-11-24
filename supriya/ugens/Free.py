import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class Free(UGen):
    """
    Frees the node at `node_id` when triggered by `trigger`.

    ::

        >>> node_id = 1000
        >>> trigger = supriya.ugens.Impulse.kr(frequency=1.0)
        >>> free = supriya.ugens.Free.kr(
        ...     node_id=node_id,
        ...     trigger=trigger,
        ...     )
        >>> free
        Free.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Envelope Utility UGens"

    _ordered_input_names = collections.OrderedDict(
        [("trigger", 0.0), ("node_id", None)]
    )

    _valid_calculation_rates = (CalculationRate.CONTROL,)
