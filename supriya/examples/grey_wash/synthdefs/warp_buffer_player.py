from supriya import synthdefs, ugens

from .. import project_settings


def warp1_parameter_block(iterations, builder, state):
    # Frequency scaling
    transposition_flux = ugens.LFNoise1.kr(frequency=[0.01] * iterations) * (1.0 / 8)
    transposition = builder["transpose"]
    transposition += transposition_flux
    frequency_scaling = transposition.semitones_to_ratio()
    frequency_scaling *= builder["direction"]
    # Buffer pointer
    pointer_scrub = (
        ugens.LFNoise1.kr(frequency=[0.01] * iterations) * state["buffer_window"] * 0.1
    )
    pointer = state["buffer_line"] + pointer_scrub
    # Window rand ratio
    window_rand_ratio = ugens.LFNoise2.kr(frequency=[0.01] * iterations)
    window_rand_ratio = window_rand_ratio.scale(-1, 1, 0.0, 0.01)
    # Window size
    window_size_variance = ugens.LFNoise1.kr(frequency=[0.01] * iterations) * 0.1
    window_size = ugens.LFNoise2.kr(frequency=0.01) + window_size_variance
    window_size = window_size.scale(-1.1, 1.1, 0.25, 0.5)
    # All parameters
    parameters = {
        "buffer_id": builder["buffer_id"],
        "frequency_scaling": frequency_scaling,
        "interpolation": 4,
        "overlaps": builder["overlaps"].as_int(),
        "pointer": pointer,
        "window_rand_ratio": window_rand_ratio,
        "window_size": window_size,
    }
    return parameters


def signal_block(builder, source, state):
    buffer_duration = ugens.BufDur.kr(builder["buffer_id"]) * builder["rate"]
    state["buffer_line"] = ugens.Line.kr(done_action=2, duration=buffer_duration)
    state["buffer_window"] = state["buffer_line"].hanning_window()
    iterations = int(state.get("iterations", 4))
    source = ugens.Warp1.ar(**warp1_parameter_block(iterations, builder, state))
    source = list(source)
    for i in range(iterations):
        if i % 2:
            source[i] *= -1
    if state["channel_count"] > 1:
        azimuth = ugens.LFNoise1.kr(frequency=[0.05] * iterations)
        source = ugens.PanB2.ar(source=source, azimuth=azimuth)
        source = ugens.Mix.multichannel(source, 3)
        source = ugens.DecodeB2.ar(
            channel_count=state["channel_count"], w=source[0], x=source[1], y=source[2]
        )
    if len(source) != state["channel_count"]:
        source = ugens.Mix.multichannel(source, state["channel_count"])
    source *= builder["gain"].db_to_amplitude()
    source *= state["buffer_window"]
    if iterations > 1:
        source /= iterations
    return source


factory = (
    synthdefs.SynthDefFactory(
        buffer_id=0,
        channel_count=project_settings["server_options"]["output_bus_channel_count"],
        direction=1,
        gain=0,
        overlaps=32,
        rate=1,
        transpose=0,
    )
    .with_signal_block(signal_block)
    .with_rand_id()
    .with_output()
)

warp_buffer_player_synthdef = factory.build(name="warp")

warp_buffer_player_factory = factory

__all__ = ["warp_buffer_player_factory", "warp_buffer_player_synthdef"]
