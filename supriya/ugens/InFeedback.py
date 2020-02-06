import collections

from supriya import CalculationRate
from supriya.synthdefs import MultiOutUGen


class InFeedback(MultiOutUGen):
    r"""A bus input unit generator.

    Reads signal from a bus with a current or one cycle old timestamp.

    ::

        >>> in_feedback = supriya.ugens.InFeedback.ar(
        ...     bus=0,
        ...     channel_count=2,
        ...     )
        >>> in_feedback
        UGenArray({2})

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Input/Output UGens"

    _default_channel_count = 1

    _has_settable_channel_count = True

    _is_input = True

    _ordered_input_names = collections.OrderedDict([("bus", 0)])

    _valid_calculation_rates = (CalculationRate.AUDIO,)
