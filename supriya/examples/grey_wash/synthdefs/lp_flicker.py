from supriya import synthdefs, ugens

from .. import project_settings


def signal_block(builder, source, state):
    line = state["line"]
    lfo_frequency = line.scale(
        0, 1, ugens.ExpRand.ir(1, 20), ugens.ExpRand.ir(1, 20), exponential=True
    )
    lfo = ugens.LFPar.kr(frequency=lfo_frequency)
    frequency = lfo.scale(
        -1,
        1,
        ugens.Rand.ir(500, ugens.SampleRate.ir() / 2),
        ugens.SampleRate.ir() * 0.5,
    )
    source = ugens.LPF.ar(source=source, frequency=frequency)
    return source


factory = (
    synthdefs.SynthDefFactory(
        channel_count=project_settings["server_options"]["output_bus_channel_count"]
    )
    .with_input()
    .with_signal_block(signal_block)
    .with_output(crossfaded=True, leveled=True, windowed=True)
    .with_rand_id()
)

lp_flicker_synthdef = factory.build(name="lp_flicker")

__all__ = ["lp_flicker_synthdef"]
