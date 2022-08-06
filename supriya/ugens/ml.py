import collections

from uqbar.enums import IntEnumeration

from supriya import CalculationRate
from supriya.synthdefs import MultiOutUGen, UGen


class BeatTrack(MultiOutUGen):
    """
    Autocorrelation beat tracker.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> pv_chain = supriya.ugens.FFT(source=source)
        >>> beat_track = supriya.ugens.BeatTrack.kr(
        ...     pv_chain=pv_chain,
        ...     lock=0,
        ... )
        >>> beat_track
        UGenArray({4})

    """

    _default_channel_count = 4
    _has_settable_channel_count = False
    _ordered_input_names = collections.OrderedDict([("pv_chain", None), ("lock", 0.0)])
    _valid_calculation_rates = (CalculationRate.CONTROL,)


class BeatTrack2(MultiOutUGen):
    """
    A template-matching beat-tracker.

    ::

        >>> beat_track_2 = supriya.ugens.BeatTrack2.kr(
        ...     bus_index=0,
        ...     lock=False,
        ...     feature_count=4,
        ...     phase_accuracy=0.02,
        ...     weighting_scheme=-2.1,
        ...     window_size=2,
        ... )
        >>> beat_track_2
        UGenArray({6})

    """

    _default_channel_count = 6
    _has_settable_channel_count = False
    _ordered_input_names = collections.OrderedDict(
        [
            ("bus_index", 0.0),
            ("feature_count", None),
            ("window_size", 2),
            ("phase_accuracy", 0.02),
            ("lock", 0.0),
            ("weighting_scheme", -2.1),
        ]
    )
    _valid_calculation_rates = (CalculationRate.CONTROL,)


class KeyTrack(UGen):
    """
    A key tracker.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> pv_chain = supriya.ugens.FFT(source=source)
        >>> key_track = supriya.ugens.KeyTrack.kr(
        ...     pv_chain=pv_chain,
        ...     chroma_leak=0.5,
        ...     key_decay=2,
        ... )
        >>> key_track
        KeyTrack.kr()

    """

    _ordered_input_names = collections.OrderedDict(
        [("pv_chain", None), ("key_decay", 2), ("chroma_leak", 0.5)]
    )
    _valid_calculation_rates = (CalculationRate.CONTROL,)


class Loudness(UGen):
    """
    Extraction of instantaneous loudness in `sones`.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> pv_chain = supriya.ugens.FFT(source=source)
        >>> loudness = supriya.ugens.Loudness.kr(
        ...     pv_chain=pv_chain,
        ...     smask=0.25,
        ...     tmask=1,
        ... )
        >>> loudness
        Loudness.kr()

    """

    _ordered_input_names = collections.OrderedDict(
        [("pv_chain", None), ("smask", 0.25), ("tmask", 1)]
    )
    _valid_calculation_rates = (CalculationRate.CONTROL,)


class MFCC(MultiOutUGen):
    """
    Mel frequency cepstral coefficients.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> pv_chain = supriya.ugens.FFT(source=source)
        >>> mfcc = supriya.ugens.MFCC.kr(
        ...     pv_chain=pv_chain,
        ...     channel_count=13,
        ... )
        >>> mfcc
        UGenArray({13})

    """

    _default_channel_count = 1
    _has_settable_channel_count = True
    _ordered_input_names = collections.OrderedDict([("pv_chain", None)])
    _valid_calculation_rates = (CalculationRate.CONTROL,)


class Onsets(UGen):
    """
    An onset detector.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> pv_chain = supriya.ugens.FFT(source=source)
        >>> onsets = supriya.ugens.Onsets.kr(
        ...     pv_chain=pv_chain,
        ...     floor=0.1,
        ...     medianspan=11,
        ...     mingap=10,
        ...     odftype=supriya.ugens.Onsets.ODFType.RCOMPLEX,
        ...     rawodf=0,
        ...     relaxtime=1,
        ...     threshold=0.5,
        ...     whtype=1,
        ... )
        >>> onsets
        Onsets.kr()

    """

    class ODFType(IntEnumeration):
        POWER = 0
        MAGSUM = 1
        COMPLEX = 2
        RCOMPLEX = 3
        PHASE = 4
        WPHASE = 5
        MKL = 6

    _ordered_input_names = collections.OrderedDict(
        [
            ("pv_chain", None),
            ("threshold", 0.5),
            ("odftype", 3),
            ("relaxtime", 1),
            ("floor", 0.1),
            ("mingap", 10),
            ("medianspan", 11),
            ("whtype", 1),
            ("rawodf", 0),
        ]
    )
    _valid_calculation_rates = (CalculationRate.CONTROL,)


class Pitch(MultiOutUGen):
    """
    An autocorrelation pitch follower.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> pitch = supriya.ugens.Pitch.kr(source=source)
        >>> pitch
        UGenArray({2})

    """

    _default_channel_count = 2
    _has_settable_channel_count = False
    _ordered_input_names = collections.OrderedDict(
        [
            ("source", None),
            ("initial_frequency", 440),
            ("min_frequency", 60),
            ("max_frequency", 4000),
            ("exec_frequency", 100),
            ("max_bins_per_octave", 16),
            ("median", 1),
            ("amplitude_threshold", 0.01),
            ("peak_threshold", 0.5),
            ("down_sample_factor", 1),
            ("clarity", 0),
        ]
    )
    _valid_calculation_rates = (CalculationRate.CONTROL,)


class SpecCentroid(UGen):
    """
    A spectral centroid measure.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> pv_chain = supriya.ugens.FFT(source=source)
        >>> spec_centroid = supriya.ugens.SpecCentroid.kr(
        ...     pv_chain=pv_chain,
        ... )
        >>> spec_centroid
        SpecCentroid.kr()

    """

    _ordered_input_names = collections.OrderedDict([("pv_chain", None)])
    _valid_calculation_rates = (CalculationRate.CONTROL,)


class SpecFlatness(UGen):
    """
    A spectral flatness measure.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> pv_chain = supriya.ugens.FFT(source=source)
        >>> spec_flatness = supriya.ugens.SpecFlatness.kr(
        ...     pv_chain=pv_chain,
        ... )
        >>> spec_flatness
        SpecFlatness.kr()

    """

    _ordered_input_names = collections.OrderedDict([("pv_chain", None)])
    _valid_calculation_rates = (CalculationRate.CONTROL,)


class SpecPcile(UGen):
    """
    Find a percentile of FFT magnitude spectrum.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> pv_chain = supriya.ugens.FFT(source=source)
        >>> spec_pcile = supriya.ugens.SpecPcile.kr(
        ...     pv_chain=pv_chain,
        ...     fraction=0.5,
        ...     interpolate=0,
        ... )
        >>> spec_pcile
        SpecPcile.kr()

    """

    _ordered_input_names = collections.OrderedDict(
        [("pv_chain", None), ("fraction", 0.5), ("interpolate", 0)]
    )
    _valid_calculation_rates = (CalculationRate.CONTROL,)
