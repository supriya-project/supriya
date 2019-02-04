from supriya import DoneAction, synthdefs, ugens

from .. import project_settings


def signal_block(builder, source, state):
    source = ugens.PlayBuf.ar(
        channel_count=state["channel_count"],
        buffer_id=builder["buffer_id"],
        done_action=DoneAction.FREE_SYNTH,
    )
    fade_in_duration = builder["fade_in_duration"]
    fade_out_duration = builder["fade_out_duration"]
    sustain_duration = (
        builder["duration"] - builder["fade_in_duration"] - builder["fade_out_duration"]
    )
    envelope = synthdefs.Envelope(
        amplitudes=[0, 1, 1, 0],
        durations=[fade_in_duration, sustain_duration, fade_out_duration],
        curves=[builder["fade_in_curve"], builder["fade_out_curve"]],
    ).kr(done_action=DoneAction.FREE_SYNTH)
    return source * envelope * builder["gain"].db_to_amplitude()


factory = (
    synthdefs.SynthDefFactory(
        buffer_id=0,
        channel_count=project_settings["server_options"]["output_bus_channel_count"],
        duration=0,
        fade_in_duration=0,
        fade_in_curve=-4,
        fade_out_duration=0,
        fade_out_curve=-4,
        gain=0,
    )
    .with_signal_block(signal_block)
    .with_output()
)

player_synthdef = factory.build(name="player")

__all__ = ["player_synthdef"]
