import supriya.ugens
from supriya import SynthDefBuilder


def _make_synthdef(channel_count=2):
    with SynthDefBuilder(
        frequency_1=200,
        frequency_2=2000,
        frequency_3=5000,
        band_1_clamp_time=0.01,
        band_1_postgain=0,
        band_1_pregain=0,
        band_1_relax_time=0.1,
        band_1_slope_above=0.5,
        band_1_slope_below=1.0,
        band_1_threshold=-12,
        band_2_clamp_time=0.01,
        band_2_postgain=0,
        band_2_pregain=0,
        band_2_relax_time=0.1,
        band_2_slope_above=0.5,
        band_2_slope_below=1.0,
        band_2_threshold=-12,
        band_3_clamp_time=0.01,
        band_3_postgain=0,
        band_3_pregain=0,
        band_3_relax_time=0.1,
        band_3_slope_above=0.5,
        band_3_slope_below=1.0,
        band_3_threshold=-12,
        band_4_clamp_time=0.01,
        band_4_postgain=0,
        band_4_pregain=0,
        band_4_relax_time=0.1,
        band_4_slope_above=0.5,
        band_4_slope_below=1.0,
        band_4_threshold=-12,
        pregain=0,
        postgain=0,
        in_=0,
        out=0,
        limiter_lookahead=0.01,
    ) as builder:
        source = supriya.ugens.In.ar(bus=builder["in_"], channel_count=channel_count)
        source *= builder["pregain"].db_to_amplitude()
        band_1 = supriya.ugens.LPF.ar(frequency=builder["frequency_1"], source=source)
        band_4 = supriya.ugens.HPF.ar(frequency=builder["frequency_3"], source=source)
        center = source - band_1 - band_4
        band_2 = supriya.ugens.LPF.ar(frequency=builder["frequency_2"], source=center)
        band_3 = supriya.ugens.HPF.ar(frequency=builder["frequency_2"], source=center)
        band_1 = supriya.ugens.CompanderD.ar(
            clamp_time=builder["band_1_clamp_time"],
            relax_time=builder["band_1_relax_time"],
            slope_above=builder["band_1_slope_above"],
            slope_below=builder["band_1_slope_below"],
            source=band_1 * builder["band_1_pregain"].db_to_amplitude(),
            threshold=builder["band_1_threshold"].db_to_amplitude(),
        )
        band_2 = supriya.ugens.CompanderD.ar(
            clamp_time=builder["band_2_clamp_time"],
            relax_time=builder["band_2_relax_time"],
            slope_above=builder["band_2_slope_above"],
            slope_below=builder["band_2_slope_below"],
            source=band_2 * builder["band_2_pregain"].db_to_amplitude(),
            threshold=builder["band_2_threshold"].db_to_amplitude(),
        )
        band_3 = supriya.ugens.CompanderD.ar(
            clamp_time=builder["band_3_clamp_time"],
            relax_time=builder["band_3_relax_time"],
            slope_above=builder["band_3_slope_above"],
            slope_below=builder["band_3_slope_below"],
            source=band_3 * builder["band_3_pregain"].db_to_amplitude(),
            threshold=builder["band_3_threshold"].db_to_amplitude(),
        )
        band_4 = supriya.ugens.CompanderD.ar(
            clamp_time=builder["band_4_clamp_time"],
            relax_time=builder["band_4_relax_time"],
            slope_above=builder["band_4_slope_above"],
            slope_below=builder["band_4_slope_below"],
            source=band_4 * builder["band_4_pregain"].db_to_amplitude(),
            threshold=builder["band_4_threshold"].db_to_amplitude(),
        )
        band_1 *= builder["band_1_postgain"].db_to_amplitude()
        band_2 *= builder["band_2_postgain"].db_to_amplitude()
        band_3 *= builder["band_3_postgain"].db_to_amplitude()
        band_4 *= builder["band_4_postgain"].db_to_amplitude()
        source = supriya.ugens.Sum4.new(
            input_one=band_1, input_two=band_2, input_three=band_3, input_four=band_4
        )
        source *= builder["postgain"].db_to_amplitude()
        source = supriya.ugens.Limiter.ar(
            source=source, duration=builder["limiter_lookahead"]
        )
        supriya.ugens.ReplaceOut.ar(bus=builder["out"], source=source)
    return builder.build()


multiband_compressor = _make_synthdef(channel_count=2)


__all__ = ("multiband_compressor",)
