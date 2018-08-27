import collections
from supriya.ugens.PV_ChainUGen import PV_ChainUGen


class PV_RectComb(PV_ChainUGen):
    """
    Makes gaps in the spectrum.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ...     )
        >>> pv_rect_comb = supriya.ugens.PV_RectComb.new(
        ...     pv_chain=pv_chain,
        ...     num_teeth=0,
        ...     phase=0,
        ...     width=0.5,
        ...     )
        >>> pv_rect_comb
        PV_RectComb.kr()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict([
        ('pv_chain', None),
        ('num_teeth', 0),
        ('phase', 0),
        ('width', 0.5),
    ])
