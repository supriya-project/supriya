from supriya import synthdefs, ugens


def signal_block(builder, source, state):
    source = ugens.PinkNoise.ar()
    source = ugens.PanB2.ar(
        source=source, azimuth=ugens.LFNoise2.kr(frequency=0.05), gain=1
    )
    source = ugens.DecodeB2.ar(
        channel_count=state["channel_count"], w=source[0], x=source[1], y=source[2]
    )
    hp_frequency = state["line"].clip(0, 0.5) * 2
    hp_frequency = hp_frequency.scale(
        0, 1, ugens.SampleRate.ir() * 0.45, 20, exponential=True
    )
    lp_frequency = state["line"].clip(0.5, 1).scale(0.5, 1.0, 0, 1)
    lp_frequency = lp_frequency.scale(0, 1, ugens.SampleRate.ir() * 0.45, 20)
    source = ugens.BHiPass.ar(source=source, frequency=hp_frequency, reciprocal_of_q=10)
    source = ugens.BLowPass.ar(
        source=source, frequency=lp_frequency, reciprocal_of_q=10
    )
    source *= builder["gain"].db_to_amplitude()
    return source


factory = (
    synthdefs.SynthDefFactory(channel_count=2, gain=0)
    .with_signal_block(signal_block)
    .with_rand_id()
    .with_output(crossfaded=True, leveled=True, windowed=True)
)


noise_wash_synthdef = factory.build(name="noise_wash")


__all__ = ["noise_wash_synthdef"]
