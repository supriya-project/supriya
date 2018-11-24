import collections
from supriya.ugens.PV_ChainUGen import PV_ChainUGen


class PV_Min(PV_ChainUGen):
    """
    Minimum magnitude.

    ::

        >>> pv_chain_a = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ...     )
        >>> pv_chain_b = supriya.ugens.FFT(
        ...     source=supriya.ugens.LFSaw.ar(),
        ...     )
        >>> pv_min = supriya.ugens.PV_Min.new(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ...     )
        >>> pv_min
        PV_Min.kr()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [("pv_chain_a", None), ("pv_chain_b", None)]
    )
