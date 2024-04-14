from supriya.enums import EnvelopeShape
from supriya.ugens import (
    EnvGen,
    Envelope,
    In,
    InFeedback,
    Out,
    SynthDef,
    SynthDefBuilder,
)


def _build_link_audio_synthdef(channel_count: int) -> SynthDef:
    with SynthDefBuilder(
        out=0, in_=16, gate=1, fade_time=0.02, done_action=2
    ) as builder:
        start_value = builder["fade_time"] <= 0
        envelope = Envelope(
            amplitudes=[start_value, 1.0, 0.0],
            durations=[1.0, 1.0],
            curves=[EnvelopeShape.SINE],
            release_node=1,
        )
        envgen = EnvGen.kr(
            done_action=builder["done_action"],
            envelope=envelope,
            gate=builder["gate"],
            time_scale=builder["fade_time"],
        )
        source = InFeedback.ar(bus=builder["in_"], channel_count=channel_count)
        Out.ar(bus=builder["out"], source=source * envgen)
    return builder.build(name=f"system_link_audio_{channel_count}")


def _build_link_control_synthdef(channel_count: int) -> SynthDef:
    with SynthDefBuilder(
        out=0, in_=16, gate=1, fade_time=0.02, done_action=2
    ) as builder:
        start_value = builder["fade_time"] <= 0
        envelope = EnvGen.kr(
            done_action=builder["done_action"],
            envelope=Envelope(
                amplitudes=[start_value, 1.0, 0.0],
                durations=[1.0, 1.0],
                curves=[EnvelopeShape.LINEAR],
                release_node=1,
            ),
            gate=builder["gate"],
            time_scale=builder["fade_time"],
        )
        input_ = In.kr(bus=builder["in_"], channel_count=channel_count)
        Out.kr(bus=builder["out"], source=input_ * envelope)
    return builder.build(name=f"system_link_control_{channel_count}")


system_link_audio_1 = _build_link_audio_synthdef(1)
system_link_audio_2 = _build_link_audio_synthdef(2)
system_link_audio_3 = _build_link_audio_synthdef(3)
system_link_audio_4 = _build_link_audio_synthdef(4)
system_link_audio_5 = _build_link_audio_synthdef(5)
system_link_audio_6 = _build_link_audio_synthdef(6)
system_link_audio_7 = _build_link_audio_synthdef(7)
system_link_audio_8 = _build_link_audio_synthdef(8)
system_link_audio_9 = _build_link_audio_synthdef(9)
system_link_audio_10 = _build_link_audio_synthdef(10)
system_link_audio_11 = _build_link_audio_synthdef(11)
system_link_audio_12 = _build_link_audio_synthdef(12)
system_link_audio_13 = _build_link_audio_synthdef(13)
system_link_audio_14 = _build_link_audio_synthdef(14)
system_link_audio_15 = _build_link_audio_synthdef(15)
system_link_audio_16 = _build_link_audio_synthdef(16)
system_link_control_1 = _build_link_control_synthdef(1)
system_link_control_2 = _build_link_control_synthdef(2)
system_link_control_3 = _build_link_control_synthdef(3)
system_link_control_4 = _build_link_control_synthdef(4)
system_link_control_5 = _build_link_control_synthdef(5)
system_link_control_6 = _build_link_control_synthdef(6)
system_link_control_7 = _build_link_control_synthdef(7)
system_link_control_8 = _build_link_control_synthdef(8)
system_link_control_9 = _build_link_control_synthdef(9)
system_link_control_10 = _build_link_control_synthdef(10)
system_link_control_11 = _build_link_control_synthdef(11)
system_link_control_12 = _build_link_control_synthdef(12)
system_link_control_13 = _build_link_control_synthdef(13)
system_link_control_14 = _build_link_control_synthdef(14)
system_link_control_15 = _build_link_control_synthdef(15)
system_link_control_16 = _build_link_control_synthdef(16)

__all__ = [
    "system_link_audio_1",
    "system_link_audio_2",
    "system_link_audio_3",
    "system_link_audio_4",
    "system_link_audio_5",
    "system_link_audio_6",
    "system_link_audio_7",
    "system_link_audio_8",
    "system_link_audio_9",
    "system_link_audio_10",
    "system_link_audio_11",
    "system_link_audio_12",
    "system_link_audio_13",
    "system_link_audio_14",
    "system_link_audio_15",
    "system_link_audio_16",
    "system_link_control_1",
    "system_link_control_2",
    "system_link_control_3",
    "system_link_control_4",
    "system_link_control_5",
    "system_link_control_6",
    "system_link_control_7",
    "system_link_control_8",
    "system_link_control_9",
    "system_link_control_10",
    "system_link_control_11",
    "system_link_control_12",
    "system_link_control_13",
    "system_link_control_14",
    "system_link_control_15",
    "system_link_control_16",
]
