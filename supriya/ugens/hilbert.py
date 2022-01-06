import collections

from supriya.enums import CalculationRate
from supriya.synthdefs import MultiOutUGen, UGen


class FreqShift(UGen):
    """

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> freq_shift = supriya.ugens.FreqShift.ar(
        ...     frequency=0,
        ...     phase=0,
        ...     source=source,
        ... )
        >>> freq_shift
        FreqShift.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("frequency", 0.0), ("phase", 0.0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class Hilbert(MultiOutUGen):
    """
    Applies the Hilbert transform.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> hilbert = supriya.ugens.Hilbert.ar(
        ...     source=source,
        ... )
        >>> hilbert
        UGenArray({2})

    """

    _default_channel_count = 2
    _has_settable_channel_count = False
    _ordered_input_names = collections.OrderedDict([("source", None)])
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class HilbertFIR(UGen):
    """
    Applies the Hilbert transform.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> hilbert_fir = supriya.ugens.HilbertFIR.ar(
        ...     buffer_id=23,
        ...     source=source,
        ... )
        >>> hilbert_fir
        HilbertFIR.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("buffer_id", None)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO,)
