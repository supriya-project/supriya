import collections
from supriya import CalculationRate
from supriya.ugens.InfoUGenBase import InfoUGenBase
from supriya.typing import UGenInputMap


class SampleDur(InfoUGenBase):
    """
    A sample duration info unit generator.

    ::

        >>> supriya.ugens.SampleDur.ir()
        SampleDur.ir()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Info UGens"

    _ordered_input_names: UGenInputMap = collections.OrderedDict([])

    _valid_calculation_rates = (CalculationRate.SCALAR,)
