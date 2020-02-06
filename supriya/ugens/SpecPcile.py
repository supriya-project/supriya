import collections

from supriya import CalculationRate
from supriya.synthdefs import UGen


class SpecPcile(UGen):
    """
    Find a percentile of FFT magnitude spectrum.

    ::

        >>> source = supriya.ugens.SoundIn.ar(bus=0)
        >>> pv_chain = supriya.ugens.FFT(source=source)
        >>> spec_pcile = supriya.ugens.SpecPcile.kr(
        ...     pv_chain=pv_chain,
        ...     fraction=0.5,
        ...     interpolate=0,
        ...     )
        >>> spec_pcile
        SpecPcile.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Machine Listening UGens"

    _ordered_input_names = collections.OrderedDict(
        [("pv_chain", None), ("fraction", 0.5), ("interpolate", 0)]
    )

    _valid_calculation_rates = (CalculationRate.CONTROL,)
