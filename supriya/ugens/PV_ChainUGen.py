from supriya import CalculationRate
from supriya.ugens.WidthFirstUGen import WidthFirstUGen


class PV_ChainUGen(WidthFirstUGen):
    """
    Abstract base class for all phase-vocoder-chain unit generators.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'FFT UGens'

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        calculation_rate = CalculationRate.CONTROL
        WidthFirstUGen.__init__(self, calculation_rate=calculation_rate, **kwargs)

    ### PUBLIC PROPERTIES ###

    @property
    def fft_size(self):
        """
        Gets FFT size as UGen input.

        Returns ugen input.
        """
        return self.pv_chain.fft_size
