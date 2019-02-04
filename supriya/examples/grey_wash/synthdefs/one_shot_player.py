from supriya import DoneAction, synthdefs, ugens

from .. import project_settings


def signal_block(builder, source, state):
    source = ugens.PlayBuf.ar(
        channel_count=1,
        buffer_id=builder["buffer_id"],
        done_action=DoneAction.FREE_SYNTH,
        rate=builder["rate"] * ugens.BufRateScale.kr(buffer_id=builder["buffer_id"]),
    )
    source = ugens.PanAz.ar(
        source=source, channel_count=state["channel_count"], position=builder["pan"]
    )
    return source * builder["gain"].db_to_amplitude()


factory = (
    synthdefs.SynthDefFactory(
        buffer_id=0,
        channel_count=project_settings["server_options"]["output_bus_channel_count"],
        gain=0,
        pan=0,
        rate=1,
    )
    .with_signal_block(signal_block)
    .with_rand_id()
    .with_output()
)

one_shot_player_synthdef = factory.build(name="one_shot_player")

__all__ = ["one_shot_player_synthdef"]
