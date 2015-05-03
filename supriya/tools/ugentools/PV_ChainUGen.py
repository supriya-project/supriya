# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.CalculationRate import CalculationRate
from supriya.tools.ugentools.WidthFirstUGen import WidthFirstUGen


class PV_ChainUGen(WidthFirstUGen):
    r'''Abstract base class for all phase-vocoder-chain unit generators.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'FFT UGens'

    __slots__ = ()

    _valid_calculation_rates = (
        CalculationRate.CONTROL,
        )

    ### INITIALIZER ###

    def __init__(
        self,
        **kwargs
        ):
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        WidthFirstUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            **kwargs
            )

    ### PUBLIC PROPERTIES ###

    @property
    def fft_size(self):
        r'''Gets FFT size as UGen input.

        Returns ugen input.
        '''
        return self.pv_chain.fft_size