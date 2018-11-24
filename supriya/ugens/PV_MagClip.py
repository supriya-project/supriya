import collections
from supriya.ugens.PV_MagAbove import PV_MagAbove


class PV_MagClip(PV_MagAbove):
    """
    Clips magnitudes.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ...     )
        >>> pv_mag_clip = supriya.ugens.PV_MagClip.new(
        ...     pv_chain=pv_chain,
        ...     threshold=0,
        ...     )
        >>> pv_mag_clip
        PV_MagClip.kr()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [('pv_chain', None), ('threshold', 0)]
    )
