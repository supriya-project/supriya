from supriya.enums import CalculationRate
from supriya.synthdefs import UGen


class DUGen(UGen):
    """
    Abstract base class of demand-rate UGens.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Demand UGens"

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        kwargs["calculation_rate"] = CalculationRate.DEMAND
        UGen.__init__(self, **kwargs)
