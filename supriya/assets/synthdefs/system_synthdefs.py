from ...enums import EnvelopeShape
from ...synthdefs import Envelope, SynthDefBuilder
from ...ugens import EnvGen, In, InFeedback, Out

__all__ = []


def _build_link_audio_synthdef(channel_count):
    name = "system_link_audio_{}".format(channel_count)
    builder = SynthDefBuilder(
        name=name, out=0, in_=16, gate=1, fade_time=0.02, done_action=2
    )
    with builder:
        start_value = builder["fade_time"] <= 0
        envelope = Envelope(
            amplitudes=[start_value, 1.0, 0.0],
            durations=[1.0, 1.0],
            curves=[EnvelopeShape.SINE, -EnvelopeShape.SINE],
            release_node=1.0,
        )
        envelope = EnvGen.kr(
            done_action=builder["done_action"],
            envelope=envelope,
            gate=builder["gate"],
            time_scale=builder["fade_time"],
        )
        source = InFeedback.ar(bus=builder["in_"], channel_count=channel_count)
        Out.ar(bus=builder["out"], source=source * envelope)
    globals()[name] = builder.build()
    __all__.append(name)


def _build_link_control_synthdef(channel_count):
    name = "system_link_control_{}".format(channel_count)
    builder = SynthDefBuilder(
        name=name, out=0, in_=16, gate=1, fade_time=0.02, done_action=2
    )
    with builder:
        start_value = builder["fade_time"] <= 0
        envelope = Envelope(
            amplitudes=[start_value, 1.0, 0.0],
            durations=[1.0, 1.0],
            curves=EnvelopeShape.LINEAR,
            release_node=1.0,
        )
        envelope = EnvGen.kr(
            done_action=builder["done_action"],
            envelope=envelope,
            gate=builder["gate"],
            time_scale=builder["fade_time"],
        )
        input_ = In.kr(bus=builder["in_"], channel_count=channel_count)
        Out.kr(bus=builder["out"], source=input_ * envelope)
    globals()[name] = builder.build()
    __all__.append(name)


for i in range(1, 17):
    _build_link_audio_synthdef(i)
    _build_link_control_synthdef(i)
