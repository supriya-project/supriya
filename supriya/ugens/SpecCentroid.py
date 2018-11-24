import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class SpecCentroid(UGen):
    """
    A spectral centroid measure.

    ::

        >>> source = supriya.ugens.SoundIn.ar(bus=0)
        >>> pv_chain = supriya.ugens.FFT(source=source)
        >>> spec_centroid = supriya.ugens.SpecCentroid.kr(
        ...     pv_chain=pv_chain,
        ...     )
        >>> spec_centroid
        SpecCentroid.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Machine Listening UGens"

    _ordered_input_names = collections.OrderedDict([("pv_chain", None)])

    _valid_calculation_rates = (CalculationRate.CONTROL,)
