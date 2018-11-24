import collections
from supriya import CalculationRate
from supriya.ugens.InfoUGenBase import InfoUGenBase
from supriya.typing import UGenInputMap


class NumAudioBuses(InfoUGenBase):
    """
    A number of audio buses info unit generator.

    ::

        >>> supriya.ugens.NumAudioBuses.ir()
        NumAudioBuses.ir()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Info UGens'

    _ordered_input_names: UGenInputMap = collections.OrderedDict([])

    _valid_calculation_rates = (CalculationRate.SCALAR,)
