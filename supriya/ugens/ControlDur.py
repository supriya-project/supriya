import collections
from supriya import CalculationRate
from supriya.ugens.InfoUGenBase import InfoUGenBase


class ControlDur(InfoUGenBase):
    """
    A control duration info unit generator.

    ::

        >>> supriya.ugens.ControlDur.ir()
        ControlDur.ir()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Info UGens'

    _ordered_input_names = collections.OrderedDict()

    _valid_calculation_rates = (
        CalculationRate.SCALAR,
    )
