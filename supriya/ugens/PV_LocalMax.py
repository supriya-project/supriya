import collections
from supriya.ugens.PV_MagAbove import PV_MagAbove


class PV_LocalMax(PV_MagAbove):
    """
    Passes bins which are local maxima.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ...     )
        >>> pv_local_max = supriya.ugens.PV_LocalMax.new(
        ...     pv_chain=pv_chain,
        ...     threshold=0,
        ...     )
        >>> pv_local_max
        PV_LocalMax.kr()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [('pv_chain', None), ('threshold', 0)]
    )
