import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class Pause(UGen):
    """
    Pauses the node at `node_id` when triggered by `trigger`.

    ::

        >>> node_id = 1000
        >>> trigger = supriya.ugens.Impulse.kr(frequency=1.0)
        >>> pause = supriya.ugens.Pause.kr(
        ...     node_id=node_id,
        ...     trigger=trigger,
        ...     )
        >>> pause
        Pause.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Envelope Utility UGens"

    _ordered_input_names = collections.OrderedDict(
        [("trigger", None), ("node_id", None)]
    )

    _valid_calculation_rates = (CalculationRate.CONTROL,)
