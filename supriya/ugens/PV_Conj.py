import collections

from supriya.ugens.PV_MagSquared import PV_MagSquared


class PV_Conj(PV_MagSquared):
    """
    Complex conjugate.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ...     )
        >>> pv_conj = supriya.ugens.PV_Conj.new(
        ...     pv_chain=pv_chain,
        ...     )
        >>> pv_conj
        PV_Conj.kr()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict([("pv_chain", None)])
