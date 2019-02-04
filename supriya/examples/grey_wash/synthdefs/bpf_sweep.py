from supriya import synthdefs, ugens

from .. import project_settings


def signal_block(builder, source, state):
    just_under_nyquist = (ugens.SampleRate.ir() / 2) * 0.99
    start_frequency = builder["start_frequency"].clip(100, just_under_nyquist)
    stop_frequency = builder["stop_frequency"].clip(100, just_under_nyquist)
    frequency = state["line"].scale(
        input_minimum=0,
        input_maximum=1,
        output_minimum=start_frequency,
        output_maximum=stop_frequency,
        exponential=True,
    )
    source = ugens.BPF.ar(source=source, frequency=frequency, reciprocal_of_q=0.25)
    source *= builder["gain"].db_to_amplitude()
    return source


factory = (
    synthdefs.SynthDefFactory(
        channel_count=project_settings["server_options"]["output_bus_channel_count"],
        gain=0,
        start_frequency=15000,
        stop_frequency=100,
    )
    .with_input()
    .with_output(crossfaded=True, leveled=True, windowed=True)
    .with_rand_id()
    .with_signal_block(signal_block)
)

windowed_bpf_sweep_synthdef = factory.build(name="windowed_bpf_sweep")

__all__ = ["windowed_bpf_sweep_synthdef"]
