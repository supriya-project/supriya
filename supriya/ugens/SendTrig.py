import collections

from supriya.enums import CalculationRate
from supriya.synthdefs import UGen


class SendTrig(UGen):

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [("trigger", None), ("id_", 0), ("value", 0)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
