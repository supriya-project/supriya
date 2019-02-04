from supriya import synthdefs, ugens

from .. import project_settings


def signal_block_pre(builder, source, state):
    source *= ugens.Line.kr(duration=0.1)  # protect against clicks
    return source


def signal_block(builder, source, state):
    source = ugens.PitchShift.ar(
        source=source,
        pitch_dispersion=builder["pitch_dispersion"],
        pitch_ratio=builder["pitch_shift"].semitones_to_ratio(),
        time_dispersion=builder["time_dispersion"] * builder["window_size"],
        window_size=builder["window_size"],
    )
    return source


def signal_block_post(builder, source, state):
    source = ugens.LeakDC.ar(source=source)
    source *= builder["gain"].db_to_amplitude()
    source = ugens.Limiter.ar(duration=ugens.Rand.ir(0.005, 0.015), source=source)
    return source


def feedback_loop(builder, source, state):
    source *= ugens.LFNoise1.kr(frequency=0.05).squared().s_curve()
    source = ugens.FreqShift.ar(source=source, frequency=ugens.Rand.ir(-1, 1))
    source = ugens.DelayC.ar(
        source=source,
        delay_time=ugens.LFNoise1.kr(frequency=0.05).scale(-1, 1, 0.1, 0.2),
        maximum_delay_time=0.2,
    )
    return source


factory = (
    synthdefs.SynthDefFactory(
        channel_count=project_settings["server_options"]["output_bus_channel_count"],
        gain=0,
        pitch_dispersion=0,
        pitch_shift=0.0,
        time_dispersion=0,
        window_size=0.5,
    )
    .with_input()
    .with_signal_block(signal_block_pre)
    .with_signal_block(signal_block)
    .with_signal_block(signal_block_post)
    .with_feedback_loop(feedback_loop)
    .with_rand_id()
)

windowed_pitchshift_synthdef = factory.with_output(
    crossfaded=True, leveled=True, windowed=True
).build(name="windowed_pitchshift")

pitchshift_synthdef = (factory.with_gate().with_output(crossfaded=True)).build(
    name="pitchshift"
)

__all__ = ["pitchshift_synthdef", "windowed_pitchshift_synthdef"]
