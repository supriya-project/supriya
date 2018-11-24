import collections

from supriya import CalculationRate
from supriya.typing import UGenInputMap
from supriya.ugens.InfoUGenBase import InfoUGenBase


class NumControlBuses(InfoUGenBase):
    """
    A number of control buses info unit generator.

    ::

        >>> supriya.ugens.NumControlBuses.ir()
        NumControlBuses.ir()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Info UGens"

    _ordered_input_names: UGenInputMap = collections.OrderedDict([])

    _valid_calculation_rates = (CalculationRate.SCALAR,)
