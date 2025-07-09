from ..enums import DoneAction
from ..ugens import (
    DC,
    Linen,
    Out,
    SynthDef,
    SynthDefBuilder,
    system,
)


def build_device_dc_tester(channel_count: int = 2) -> SynthDef:
    with SynthDefBuilder(
        active=1,
        dc=1,
        done_action=DoneAction.FREE_SYNTH,
        gate=1,
        out=0,
    ) as builder:
        active_gate = Linen.kr(
            attack_time=system.LAG_TIME,
            gate=builder["active"],
            release_time=system.LAG_TIME,
        )
        free_gate = Linen.kr(
            attack_time=system.LAG_TIME,
            done_action=builder["done_action"],
            gate=builder["gate"],
            release_time=system.LAG_TIME,
        )
        source = DC.ar(source=builder["dc"])
        source *= active_gate * free_gate
        Out.ar(bus=builder["out"], source=[source] * channel_count)
    return builder.build(f"supriya:device-dc-tester:{channel_count}")
