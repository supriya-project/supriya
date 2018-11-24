import collections

from supriya.ugens.PV_ChainUGen import PV_ChainUGen


class PV_MagSmear(PV_ChainUGen):
    """
    Averages magnitudes across bins.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ...     )
        >>> pv_mag_smear = supriya.ugens.PV_MagSmear.new(
        ...     bins=0,
        ...     pv_chain=pv_chain,
        ...     )
        >>> pv_mag_smear
        PV_MagSmear.kr()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict([("pv_chain", None), ("bins", 0)])
