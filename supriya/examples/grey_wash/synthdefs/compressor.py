from supriya import synthdefs, ugens

from .. import project_settings

my_frequencies = [150, 300, 600, 1200, 2400, 4800, 9600]
mel_frequencies = [
    160,
    394,
    670,
    1000,
    1420,
    1900,
    2450,
    3120,
    4000,
    5100,
    6600,
    9000,
    14000,
]
umesh_frequencies = [
    161,
    200,
    404,
    693,
    867,
    1000,
    2022,
    3000,
    3393,
    4109,
    5526,
    6500,
    7743,
    12000,
]
bark_frequencies = [
    100,
    200,
    300,
    400,
    510,
    630,
    770,
    920,
    1080,
    1270,
    1480,
    1720,
    2000,
    2320,
    2700,
    3150,
    3700,
    4400,
    5300,
    6400,
    7700,
    9500,
    12000,
    15500,
]


def scale(value, in_lo, in_hi, out_lo, out_hi, exponent=1.0):
    in_range = in_hi - in_lo
    out_range = out_hi - out_lo
    value = (value - in_lo) / in_range
    value = value ** exponent
    value = value * out_range
    value = value + out_lo
    return value


def parameter_block(builder, state):
    frequencies = [20] + list(state["frequencies"])
    pregain = state.get("default_pregain") or 0
    clamp_time = state.get("default_clamp_time") or 0.01
    relax_time = state.get("default_relax_time") or 0.1
    slope_above = state.get("default_slope_above") or 0.5
    slope_below = state.get("default_slope_below") or 1.0
    postgain = state.get("default_postgain") or 0
    band_count = len(frequencies)
    lo_threshold = state.get("default_threshold_low") or -16
    hi_threshold = state.get("default_threshold_high") or -32
    for i in range(band_count):
        frequency = frequencies[i]
        threshold = scale(
            frequency,
            min(frequencies),
            max(frequencies),
            lo_threshold,
            hi_threshold,
            exponent=0.5,
        )
        band_name = "band_{}_".format(i + 1)
        builder._add_parameter(band_name + "pregain", pregain, "CONTROL")
        builder._add_parameter(band_name + "clamp_time", clamp_time, "CONTROL")
        builder._add_parameter(band_name + "relax_time", relax_time, "CONTROL")
        builder._add_parameter(band_name + "threshold", threshold, "CONTROL")
        builder._add_parameter(band_name + "slope_above", slope_above, "CONTROL")
        builder._add_parameter(band_name + "slope_below", slope_below, "CONTROL")
        builder._add_parameter(band_name + "postgain", postgain, "CONTROL")


def signal_block(builder, source, state):
    source *= builder["pregain"].db_to_amplitude()
    bands = []
    frequencies = state["frequencies"]
    for frequency in frequencies:
        band = ugens.LPF.ar(source=source, frequency=frequency)
        bands.append(band)
        source -= band
    bands.append(source)
    compressors = []
    for i, band in enumerate(bands):
        band_name = "band_{}_".format(i + 1)
        threshold = builder[band_name + "threshold"]
        band *= builder[band_name + "pregain"].db_to_amplitude()
        band = ugens.CompanderD.ar(
            clamp_time=builder[band_name + "clamp_time"],
            relax_time=builder[band_name + "relax_time"],
            slope_above=builder[band_name + "slope_above"],
            slope_below=builder[band_name + "slope_below"],
            source=band,
            threshold=threshold.db_to_amplitude(),
        )
        band = band.tanh()  # hmm!
        band *= builder[band_name + "postgain"].db_to_amplitude()
        compressors.extend(band)
    assert len(compressors) == state["channel_count"] * (len(frequencies) + 1)
    source = ugens.Mix.multichannel(compressors, state["channel_count"])
    assert len(source) == state["channel_count"]
    source *= builder[band_name + "postgain"].db_to_amplitude()
    source = ugens.Limiter.ar(source=source, duration=builder["limiter_lookahead"])
    return source


factory = (
    synthdefs.SynthDefFactory(
        channel_count=project_settings["server_options"]["output_bus_channel_count"],
        pregain=0,
        postgain=0,
        limiter_lookahead=0.01,
    )
    .with_initial_state(
        frequencies=mel_frequencies,
        default_threshold_low=-16,
        default_threshold_high=-32,
        default_slope_above=0.75,
    )
    .with_parameter_block(parameter_block)
    .with_input()
    .with_signal_block(signal_block)
    .with_output(replacing=True)
)

compressor_synthdef = factory.build(name="compressor")

__all__ = ["compressor_synthdef"]
