import collections
from supriya import CalculationRate
from supriya.ugens.MultiOutUGen import MultiOutUGen


class BeatTrack(MultiOutUGen):
    """
    Autocorrelation beat tracker.

    ::

        >>> source = supriya.ugens.SoundIn.ar(bus=0)
        >>> pv_chain = supriya.ugens.FFT(source=source)
        >>> beat_track = supriya.ugens.BeatTrack.kr(
        ...     pv_chain=pv_chain,
        ...     lock=0,
        ...     )
        >>> beat_track
        UGenArray({4})

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Machine Listening UGens"

    _default_channel_count = 4

    _has_settable_channel_count = False

    _ordered_input_names = collections.OrderedDict([("pv_chain", None), ("lock", 0.0)])

    _valid_calculation_rates = (CalculationRate.CONTROL,)
