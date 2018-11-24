import collections

from supriya.ugens.PV_ChainUGen import PV_ChainUGen


class PV_RectComb2(PV_ChainUGen):
    """
    Makes gaps in the spectrum.

    ::

        >>> pv_chain_a = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ...     )
        >>> pv_chain_b = supriya.ugens.FFT(
        ...     source=supriya.ugens.LFSaw.ar(),
        ...     )
        >>> pv_rect_comb_2 = supriya.ugens.PV_RectComb2.new(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ...     num_teeth=0,
        ...     phase=0,
        ...     width=0.5,
        ...     )
        >>> pv_rect_comb_2
        PV_RectComb2.kr()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [
            ("pv_chain_a", None),
            ("pv_chain_b", None),
            ("num_teeth", 0),
            ("phase", 0),
            ("width", 0.5),
        ]
    )
