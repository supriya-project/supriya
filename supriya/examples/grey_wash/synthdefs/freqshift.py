from supriya import synthdefs, ugens

from .. import project_settings


def signal_block(builder, source, state):
    source *= ugens.Line.kr(duration=0.1)  # protect against clicks
    sign = builder["sign"]
    frequency = ugens.LFNoise2.kr(frequency=0.01).scale(-1, 1, 100, 1000) * sign
    source = ugens.FreqShift.ar(
        source=source, frequency=frequency, phase=ugens.LFNoise2.kr(frequency=0.01)
    )
    return source


factory = (
    synthdefs.SynthDefFactory(
        channel_count=project_settings["server_options"]["output_bus_channel_count"],
        sign=1,
    )
    .with_input()
    .with_signal_block(signal_block)
    .with_rand_id()
)

freqshift_synthdef = factory.with_gate().with_output(crossfaded=True).build("freqshift")

windowed_freqshift_synthdef = factory.with_output(
    crossfaded=True, leveled=True, windowed=True
).build(name="windowed_freqshift")

__all__ = ["freqshift_synthdef", "windowed_freqshift_synthdef"]
