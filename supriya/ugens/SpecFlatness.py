import collections

from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class SpecFlatness(UGen):
    """
    A spectral flatness measure.

    ::

        >>> source = supriya.ugens.SoundIn.ar(bus=0)
        >>> pv_chain = supriya.ugens.FFT(source=source)
        >>> spec_flatness = supriya.ugens.SpecFlatness.kr(
        ...     pv_chain=pv_chain,
        ...     )
        >>> spec_flatness
        SpecFlatness.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Machine Listening UGens"

    _ordered_input_names = collections.OrderedDict([("pv_chain", None)])

    _valid_calculation_rates = (CalculationRate.CONTROL,)
