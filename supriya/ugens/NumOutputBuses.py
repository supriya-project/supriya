import collections
from supriya import CalculationRate
from supriya.ugens.InfoUGenBase import InfoUGenBase


class NumOutputBuses(InfoUGenBase):
    """
    A number of output buses info unit generator.

    ::

        >>> supriya.ugens.NumOutputBuses.ir()
        NumOutputBuses.ir()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Info UGens'

    _ordered_input_names = collections.OrderedDict()

    _valid_calculation_rates = (
        CalculationRate.SCALAR,
    )
