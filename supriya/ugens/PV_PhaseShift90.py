import collections
from supriya.ugens.PV_MagSquared import PV_MagSquared


class PV_PhaseShift90(PV_MagSquared):
    """
    Shifts phase by 90 degrees.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ...     )
        >>> pv_phase_shift_90 = supriya.ugens.PV_PhaseShift90.new(
        ...     pv_chain=pv_chain,
        ...     )
        >>> pv_phase_shift_90
        PV_PhaseShift90.kr()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict([("pv_chain", None)])
