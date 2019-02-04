from supriya import synthdefs, ugens

from .. import project_settings


def signal_block_pre(builder, source, state):
    source *= ugens.Line.kr(duration=0.1)  # protect against clicks
    return source


def signal_block(builder, source, state):
    stage_iterations = 3
    inner_iterations = 4
    channel_count = state["channel_count"]
    frequency = [builder["frequency"]] * channel_count
    assert len(frequency) == channel_count
    lowpassed = ugens.LPF.ar(source=source, frequency=1000)
    source -= lowpassed
    for _ in range(stage_iterations):
        all_delays = []
        delay = source
        for i in range(inner_iterations):
            delay_time = ugens.LFNoise2.kr(frequency=frequency)
            delay_time = delay_time.scale(-1, 1, 0.0001, 0.01)
            delay = ugens.DelayC.ar(
                delay_time=delay_time, maximum_delay_time=0.1, source=delay
            )
            all_delays.extend(delay)
        source = ugens.Mix.multichannel(all_delays, state["channel_count"])
        source /= inner_iterations
    source += lowpassed
    return source


def signal_block_post(builder, source, state):
    source = ugens.LeakDC.ar(source=source)
    source *= builder["gain"].db_to_amplitude()
    source = ugens.Limiter.ar(duration=ugens.Rand.ir(0.005, 0.015), source=source)
    return source


def feedback_loop(builder, source, state):
    return source * ugens.DC.kr(-12).db_to_amplitude() * -1


factory = (
    synthdefs.SynthDefFactory(
        channel_count=project_settings["server_options"]["output_bus_channel_count"],
        frequency=1,
        gain=0,
    )
    .with_input()
    .with_signal_block(signal_block_pre)
    .with_signal_block(signal_block)
    .with_signal_block(signal_block_post)
    .with_feedback_loop(feedback_loop)
    .with_rand_id()
)

chorus_synthdef = factory.with_gate().with_output(crossfaded=True).build(name="chorus")

windowed_chorus_factory = factory.with_output(
    crossfaded=True, leveled=True, windowed=True
)

windowed_chorus_synthdef = windowed_chorus_factory.build(name="windowed_chorus")

__all__ = ["chorus_synthdef", "windowed_chorus_synthdef", "windowed_chorus_factory"]
