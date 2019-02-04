from supriya import synthdefs, ugens

from .. import project_settings


def signal_block(builder, source, state):
    source *= ugens.Line.kr(duration=0.1)  # protect against clicks
    just_under_nyquist = (ugens.SampleRate.ir() / 2) * 0.99
    frequency = builder["frequency"].clip(20, just_under_nyquist)
    source = ugens.LPF.ar(source=source, frequency=frequency)
    source *= builder["gain"].db_to_amplitude()
    return source


factory = (
    synthdefs.SynthDefFactory(
        channel_count=project_settings["server_options"]["output_bus_channel_count"],
        frequency=10000,
        gain=0,
    )
    .with_input()
    .with_signal_block(signal_block)
    .with_rand_id()
    .with_output(crossfaded=True, leveled=True, windowed=True)
)

windowed_lpf_dip_synthdef = factory.build(name="windowed_lpf_dip")

__all__ = ["windowed_lpf_dip_synthdef"]
