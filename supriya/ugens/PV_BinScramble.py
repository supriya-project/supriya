import collections

from supriya.ugens.PV_ChainUGen import PV_ChainUGen


class PV_BinScramble(PV_ChainUGen):
    """
    Scrambles bins.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ...     )
        >>> pv_bin_scramble = supriya.ugens.PV_BinScramble.new(
        ...     pv_chain=pv_chain,
        ...     trigger=0,
        ...     width=0.2,
        ...     wipe=0,
        ...     )
        >>> pv_bin_scramble
        PV_BinScramble.kr()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [("pv_chain", None), ("wipe", 0), ("width", 0.2), ("trigger", 0)]
    )
