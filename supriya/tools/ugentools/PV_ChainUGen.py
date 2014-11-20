# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.WidthFirstUGen import WidthFirstUGen


class PV_ChainUGen(WidthFirstUGen):
    r'''Abstract base class for all phase-vocoder-chain unit generators.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'FFT UGens'

    __slots__ = ()

    ### INITIALIZER ###
    
    def __init__(
        self,
        calculation_rate=None,
        **kwargs
        ):
        from supriya.tools import synthdeftools
        if calculation_rate is None:
            calculation_rate = synthdeftools.CalculationRate.CONTROL
        WidthFirstUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            **kwargs
            )