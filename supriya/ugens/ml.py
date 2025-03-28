from typing import Any

from uqbar.enums import IntEnumeration

from ..enums import CalculationRate
from .core import UGen, param, ugen


@ugen(kr=True, channel_count=4, fixed_channel_count=True)
class BeatTrack(UGen):
    """
    Autocorrelation beat tracker.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> pv_chain = supriya.ugens.FFT.kr(source=source)
        >>> beat_track = supriya.ugens.BeatTrack.kr(
        ...     pv_chain=pv_chain,
        ...     lock=0,
        ... )
        >>> beat_track
        <BeatTrack.kr()>
    """

    pv_chain = param()
    lock = param(0.0)


@ugen(kr=True, channel_count=6, fixed_channel_count=True)
class BeatTrack2(UGen):
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
        <BeatTrack2.kr()>
    """

    bus_index = param(0.0)
    feature_count = param()
    window_size = param(2)
    phase_accuracy = param(0.02)
    lock = param(0.0)
    weighting_scheme = param(-2.1)


@ugen(kr=True)
class KeyTrack(UGen):
    """
    A key tracker.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> pv_chain = supriya.ugens.FFT.kr(source=source)
        >>> key_track = supriya.ugens.KeyTrack.kr(
        ...     pv_chain=pv_chain,
        ...     chroma_leak=0.5,
        ...     key_decay=2,
        ... )
        >>> key_track
        <KeyTrack.kr()[0]>
    """

    pv_chain = param()
    key_decay = param(2)
    chroma_leak = param(0.5)


@ugen(kr=True)
class Loudness(UGen):
    """
    Extraction of instantaneous loudness in `sones`.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> pv_chain = supriya.ugens.FFT.kr(source=source)
        >>> loudness = supriya.ugens.Loudness.kr(
        ...     pv_chain=pv_chain,
        ...     smask=0.25,
        ...     tmask=1,
        ... )
        >>> loudness
        <Loudness.kr()[0]>
    """

    pv_chain = param()
    smask = param(0.25)
    tmask = param(1)


@ugen(kr=True, fixed_channel_count=True)
class MFCC(UGen):
    """
    Mel frequency cepstral coefficients.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> pv_chain = supriya.ugens.FFT.kr(source=source)
        >>> mfcc = supriya.ugens.MFCC.kr(
        ...     pv_chain=pv_chain,
        ... )
        >>> mfcc
        <MFCC.kr()>
    """

    pv_chain = param()
    coeff_count = param(13)

    def _postprocess_kwargs(
        self,
        *,
        calculation_rate: CalculationRate,
        **kwargs,
    ) -> tuple[CalculationRate, dict[str, Any]]:
        self._channel_count = int(kwargs["coeff_count"])
        return calculation_rate, kwargs


@ugen(kr=True)
class Onsets(UGen):
    """
    An onset detector.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> pv_chain = supriya.ugens.FFT.kr(source=source)
        >>> onsets = supriya.ugens.Onsets.kr(
        ...     pv_chain=pv_chain,
        ...     floor_=0.1,
        ...     medianspan=11,
        ...     mingap=10,
        ...     odftype=supriya.ugens.Onsets.ODFType.RCOMPLEX,
        ...     rawodf=0,
        ...     relaxtime=1,
        ...     threshold=0.5,
        ...     whtype=1,
        ... )
        >>> onsets
        <Onsets.kr()[0]>
    """

    class ODFType(IntEnumeration):
        POWER = 0
        MAGSUM = 1
        COMPLEX = 2
        RCOMPLEX = 3
        PHASE = 4
        WPHASE = 5
        MKL = 6

    pv_chain = param()
    threshold = param(0.5)
    odftype = param(3)
    relaxtime = param(1)
    floor_ = param(0.1)
    mingap = param(10)
    medianspan = param(11)
    whtype = param(1)
    rawodf = param(0)


@ugen(kr=True, channel_count=2, fixed_channel_count=True)
class Pitch(UGen):
    """
    An autocorrelation pitch follower.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> pitch = supriya.ugens.Pitch.kr(source=source)
        >>> pitch
        <Pitch.kr()>
    """

    source = param()
    initial_frequency = param(440)
    min_frequency = param(60)
    max_frequency = param(4000)
    exec_frequency = param(100)
    max_bins_per_octave = param(16)
    median = param(1)
    amplitude_threshold = param(0.01)
    peak_threshold = param(0.5)
    down_sample_factor = param(1)
    clarity = param(0)


@ugen(kr=True)
class SpecCentroid(UGen):
    """
    A spectral centroid measure.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> pv_chain = supriya.ugens.FFT.kr(source=source)
        >>> spec_centroid = supriya.ugens.SpecCentroid.kr(
        ...     pv_chain=pv_chain,
        ... )
        >>> spec_centroid
        <SpecCentroid.kr()[0]>
    """

    pv_chain = param()


@ugen(kr=True)
class SpecFlatness(UGen):
    """
    A spectral flatness measure.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> pv_chain = supriya.ugens.FFT.kr(source=source)
        >>> spec_flatness = supriya.ugens.SpecFlatness.kr(
        ...     pv_chain=pv_chain,
        ... )
        >>> spec_flatness
        <SpecFlatness.kr()[0]>
    """

    pv_chain = param()


@ugen(kr=True)
class SpecPcile(UGen):
    """
    Find a percentile of FFT magnitude spectrum.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> pv_chain = supriya.ugens.FFT.kr(source=source)
        >>> spec_pcile = supriya.ugens.SpecPcile.kr(
        ...     pv_chain=pv_chain,
        ...     fraction=0.5,
        ...     interpolate=0,
        ... )
        >>> spec_pcile
        <SpecPcile.kr()[0]>
    """

    pv_chain = param()
    fraction = param(0.5)
    interpolate = param(0)
