import collections
from supriya import CalculationRate
from supriya.ugens.BufInfoUGenBase import BufInfoUGenBase


class BufRateScale(BufInfoUGenBase):
    """
    A buffer sample-rate scale info unit generator.

    ::

        >>> supriya.ugens.BufRateScale.kr(buffer_id=0)
        BufRateScale.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Buffer UGens"

    _ordered_input_names = collections.OrderedDict([("buffer_id", None)])

    _valid_calculation_rates = (CalculationRate.CONTROL, CalculationRate.SCALAR)
