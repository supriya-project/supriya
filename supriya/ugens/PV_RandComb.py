import collections

from supriya.ugens.PV_ChainUGen import PV_ChainUGen


class PV_RandComb(PV_ChainUGen):
    """
    Passes random bins.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ...     )
        >>> pv_rand_comb = supriya.ugens.PV_RandComb.new(
        ...     pv_chain=pv_chain,
        ...     trigger=0,
        ...     wipe=0,
        ...     )
        >>> pv_rand_comb
        PV_RandComb.kr()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [("pv_chain", None), ("wipe", 0), ("trigger", 0)]
    )
