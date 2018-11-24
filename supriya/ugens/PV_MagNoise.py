import collections
from supriya.ugens.PV_MagSquared import PV_MagSquared


class PV_MagNoise(PV_MagSquared):
    """
    Multiplies magnitudes by noise.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ...     )
        >>> pv_mag_noise = supriya.ugens.PV_MagNoise.new(
        ...     pv_chain=pv_chain,
        ...     )
        >>> pv_mag_noise
        PV_MagNoise.kr()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict([('pv_chain', None)])
