import collections
from supriya import CalculationRate
from supriya.ugens.InfoUGenBase import InfoUGenBase


class SampleRate(InfoUGenBase):
    """
    A sample-rate info unit generator.

    ::

        >>> supriya.ugens.SampleRate.ir()
        SampleRate.ir()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Info UGens'

    _ordered_input_names = collections.OrderedDict()

    _valid_calculation_rates = (
        CalculationRate.SCALAR,
    )
