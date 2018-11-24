import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class Linen(UGen):
    """
    A simple line generating unit generator.

    ::

        >>> supriya.ugens.Linen.kr()
        Linen.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Envelope Utility UGens"

    _has_done_flag = True

    _ordered_input_names = collections.OrderedDict(
        [
            ("gate", 1.0),
            ("attack_time", 0.01),
            ("sustain_level", 1.0),
            ("release_time", 1.0),
            ("done_action", 0),
        ]
    )

    _valid_calculation_rates = (CalculationRate.CONTROL,)
