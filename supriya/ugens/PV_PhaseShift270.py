import collections
from supriya.ugens.PV_MagSquared import PV_MagSquared


class PV_PhaseShift270(PV_MagSquared):
    """
    Shifts phase by 270 degrees.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ...     )
        >>> pv_phase_shift_270 = supriya.ugens.PV_PhaseShift270.new(
        ...     pv_chain=pv_chain,
        ...     )
        >>> pv_phase_shift_270
        PV_PhaseShift270.kr()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict([('pv_chain', None)])
