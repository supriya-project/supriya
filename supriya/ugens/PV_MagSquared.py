import collections

from supriya.ugens.PV_ChainUGen import PV_ChainUGen


class PV_MagSquared(PV_ChainUGen):
    """
    Squares magnitudes.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ...     )
        >>> pv_mag_squared = supriya.ugens.PV_MagSquared.new(
        ...     pv_chain=pv_chain,
        ...     )
        >>> pv_mag_squared
        PV_MagSquared.kr()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict([("pv_chain", None)])
