import collections
from supriya.ugens.PV_ChainUGen import PV_ChainUGen


class PV_BinWipe(PV_ChainUGen):
    """
    Copies low bins from one input and the high bins of the other.

    ::

        >>> pv_chain_a = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ...     )
        >>> pv_chain_b = supriya.ugens.FFT.new(
        ...     source=supriya.ugens.LFSaw.ar(),
        ...     )
        >>> pv_bin_wipe = supriya.ugens.PV_BinWipe.new(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ...     wipe=0,
        ...     )
        >>> pv_bin_wipe
        PV_BinWipe.kr()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [("pv_chain_a", None), ("pv_chain_b", None), ("wipe", 0)]
    )
