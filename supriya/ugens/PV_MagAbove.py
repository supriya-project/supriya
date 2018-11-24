import collections
from supriya.ugens.PV_ChainUGen import PV_ChainUGen


class PV_MagAbove(PV_ChainUGen):
    """
    Passes magnitudes above threshold.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ...     )
        >>> pv_mag_above = supriya.ugens.PV_MagAbove.new(
        ...     pv_chain=pv_chain,
        ...     threshold=0,
        ...     )
        >>> pv_mag_above
        PV_MagAbove.kr()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [("pv_chain", None), ("threshold", 0)]
    )
