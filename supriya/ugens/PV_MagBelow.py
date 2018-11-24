import collections
from supriya.ugens.PV_MagAbove import PV_MagAbove


class PV_MagBelow(PV_MagAbove):
    """
    Passes magnitudes below threshold.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ...     )
        >>> pv_mag_below = supriya.ugens.PV_MagBelow.new(
        ...     pv_chain=pv_chain,
        ...     threshold=0,
        ...     )
        >>> pv_mag_below
        PV_MagBelow.kr()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [("pv_chain", None), ("threshold", 0)]
    )
