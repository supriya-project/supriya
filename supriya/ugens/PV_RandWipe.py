import collections
from supriya.ugens.PV_ChainUGen import PV_ChainUGen


class PV_RandWipe(PV_ChainUGen):
    """
    Crossfades in random bin order.

    ::

        >>> pv_chain_a = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ...     )
        >>> pv_chain_b = supriya.ugens.FFT(
        ...     source=supriya.ugens.LFSaw.ar(),
        ...     )
        >>> pv_rand_wipe = supriya.ugens.PV_RandWipe.new(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ...     trigger=0,
        ...     wipe=0,
        ...     )
        >>> pv_rand_wipe
        PV_RandWipe.kr()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [("pv_chain_a", None), ("pv_chain_b", None), ("wipe", 0), ("trigger", 0)]
    )
