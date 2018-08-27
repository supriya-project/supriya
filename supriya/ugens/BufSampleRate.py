import collections
from supriya import CalculationRate
from supriya.ugens.BufInfoUGenBase import BufInfoUGenBase


class BufSampleRate(BufInfoUGenBase):
    """
    A buffer sample-rate info unit generator.

    ::

        >>> supriya.ugens.BufSampleRate.kr(buffer_id=0)
        BufSampleRate.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Buffer UGens'

    _ordered_input_names = collections.OrderedDict([
        ('buffer_id', None),
    ])

    _valid_calculation_rates = (
        CalculationRate.CONTROL,
        CalculationRate.SCALAR,
    )
