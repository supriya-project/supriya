import collections

from supriya.ugens.PV_ChainUGen import PV_ChainUGen


class PV_MagFreeze(PV_ChainUGen):
    """
    Freezes magnitudes.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ...     )
        >>> pv_mag_freeze = supriya.ugens.PV_MagFreeze.new(
        ...     pv_chain=pv_chain,
        ...     freeze=0,
        ...     )
        >>> pv_mag_freeze
        PV_MagFreeze.kr()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict([("pv_chain", None), ("freeze", 0)])
