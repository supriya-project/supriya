from ..enums import DoneAction
from ..ugens import (
    DC,
    Amplitude,
    In,
    InFeedback,
    Linen,
    Out,
    Parameter,
    ReplaceOut,
    SynthDef,
    SynthDefBuilder,
)


def _get_lag_time() -> float:
    return 0.05


def get_lag_time() -> float:
    return _get_lag_time()


def build_channel_strip(channel_count: int = 2) -> SynthDef:
    with SynthDefBuilder(
        active=1,
        bus=0,
        done_action=DoneAction.FREE_SYNTH,
        gain=Parameter(value=0, lag=get_lag_time()),
        gate=1,
    ) as builder:
        source = In.ar(
            channel_count=channel_count,
            bus=builder["bus"],
        )
        active_gate = Linen.kr(
            attack_time=get_lag_time(),
            gate=builder["active"],
            release_time=get_lag_time(),
        )
        free_gate = Linen.kr(
            attack_time=get_lag_time(),
            done_action=builder["done_action"],
            gate=builder["gate"],
            release_time=get_lag_time(),
        )
        source *= builder["gain"].db_to_amplitude()
        source *= active_gate
        source *= free_gate
        ReplaceOut.ar(bus=builder["bus"], source=source)
    return builder.build(f"supriya:channel-strip:{channel_count}")


def build_device_dc_tester(channel_count: int = 2) -> SynthDef:
    with SynthDefBuilder(dc=1, out=0) as builder:
        Out.ar(bus=builder["out"], source=[DC.ar(source=builder["dc"])] * channel_count)
    return builder.build(f"supriya:device-dc-tester:{channel_count}")


def build_meters(channel_count: int = 2) -> SynthDef:
    with SynthDefBuilder(in_=0, out=0) as builder:
        Out.kr(
            bus=builder["out"],
            source=Amplitude.kr(
                source=In.ar(bus=builder["in_"], channel_count=channel_count)
            ),
        )
    return builder.build(f"supriya:meters:{channel_count}")


def build_patch_cable(
    input_channel_count: int = 2,
    output_channel_count: int = 2,
    feedback: bool = False,
) -> SynthDef:
    # TODO: Implement up/down channel mixing
    with SynthDefBuilder(
        active=1,
        done_action=DoneAction.FREE_SYNTH,
        gain=0,
        gate=1,
        in_=0,
        out=0,
    ) as builder:
        if feedback:
            source = InFeedback.ar(
                channel_count=input_channel_count,
                bus=builder["in_"],
            )
        else:
            source = In.ar(
                channel_count=input_channel_count,
                bus=builder["in_"],
            )
        active_gate = Linen.kr(
            attack_time=get_lag_time(),
            gate=builder["active"],
            release_time=get_lag_time(),
        )
        free_gate = Linen.kr(
            attack_time=get_lag_time(),
            done_action=builder["done_action"],
            gate=builder["gate"],
            release_time=get_lag_time(),
        )
        source *= builder["gain"].db_to_amplitude()
        source *= free_gate * active_gate
        Out.ar(bus=builder["out"], source=source)

    name = (
        f"supriya:{'fb-' if feedback else ''}"
        f"patch-cable:{input_channel_count}x{output_channel_count}"
    )
    return builder.build(name)
