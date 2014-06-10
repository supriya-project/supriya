# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.Enumeration import Enumeration


class CalculationRate(Enumeration):
    r'''An enumeration of scsynth calculation rates.

    ::

        >>> from supriya.tools import synthdeftools
        >>> synthdeftools.CalculationRate.AUDIO
        <CalculationRate.AUDIO: 2>

    ::

        >>> synthdeftools.CalculationRate.from_expr('demand')
        <CalculationRate.DEMAND: 3>

    '''

    ### CLASS VARIABLES ###

    AUDIO = 2
    CONTROL = 1
    DEMAND = 3
    SCALAR = 0
