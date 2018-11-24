import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class Duty(UGen):
    """
    A value is demanded of each UGen in the list and output according to a stream of duration values.

    ::

        >>> duty = supriya.ugens.Duty.kr(
        ...     done_action=0,
        ...     duration=supriya.ugens.Drand(
        ...         sequence=[0.01, 0.2, 0.4],
        ...         repeats=2,
        ...     ),
        ...     reset=0,
        ...     level=supriya.ugens.Dseq(
        ...         sequence=[204, 400, 201, 502, 300, 200],
        ...         repeats=2,
        ...         ),
        ...     )
        >>> duty
        Duty.kr()

    """

    # ### CLASS VARIABLES ###

    __documentation_section__ = None

    _ordered_input_names = collections.OrderedDict(
        [("duration", 1.0), ("reset", 0.0), ("level", 1.0), ("done_action", 0.0)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
