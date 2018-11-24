import collections
from supriya import CalculationRate
from supriya.ugens.BufInfoUGenBase import BufInfoUGenBase


class BufChannels(BufInfoUGenBase):
    """
    A buffer channel count info unit generator.

    ::

        >>> supriya.ugens.BufChannels.kr(buffer_id=0)
        BufChannels.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Buffer UGens'

    _ordered_input_names = collections.OrderedDict([('buffer_id', None)])

    _valid_calculation_rates = (CalculationRate.CONTROL, CalculationRate.SCALAR)
