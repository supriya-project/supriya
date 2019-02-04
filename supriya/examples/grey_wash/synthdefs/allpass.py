from supriya import synthdefs, ugens

from .. import project_settings


def signal_block_pre(builder, source, state):
    source *= ugens.Line.kr(duration=0.1)  # protect against clicks
    return source


def signal_block(builder, source, state):
    allpasses = []
    maximum_delay = 1
    iterations = state.get("iterations") or 3
    for output in source:
        for _ in range(iterations):
            output = ugens.AllpassC.ar(
                decay_time=ugens.LFDNoise3.kr(
                    frequency=ugens.ExpRand.ir(0.01, 0.1)
                ).scale(-1, 1, 0.01, 1),
                delay_time=ugens.LFDNoise3.kr(
                    frequency=ugens.ExpRand.ir(0.01, 0.1)
                ).scale(-1, 1, 0.01, 1, exponential=True),
                maximum_delay_time=maximum_delay,
                source=output,
            )
        allpasses.append(output)
    source = synthdefs.UGenArray(allpasses)
    return source


def signal_block_post(builder, source, state):
    source = ugens.LeakDC.ar(source=source)
    source *= builder["gain"].db_to_amplitude()
    source = ugens.Limiter.ar(duration=ugens.Rand.ir(0.005, 0.015), source=source)
    return source


def feedback_loop(builder, source, state):
    source = ugens.HPF.ar(source=source, frequency=1000)
    source *= ugens.LFNoise1.kr(frequency=0.05).squared().s_curve()
    source *= -0.99
    return source


factory = (
    synthdefs.SynthDefFactory(
        channel_count=project_settings["server_options"]["output_bus_channel_count"],
        gain=0,
    )
    .with_input()
    .with_signal_block(signal_block_pre)
    .with_signal_block(signal_block)
    .with_signal_block(signal_block_post)
    .with_feedback_loop(feedback_loop)
    .with_rand_id()
)

allpass_synthdef = factory.with_output(crossfaded=True).build(name="allpass")

windowed_allpass_synthdef = factory.with_output(
    crossfaded=True, leveled=True, windowed=True
).build(name="windowed_allpass")

__all__ = ["allpass_synthdef", "windowed_allpass_synthdef"]
