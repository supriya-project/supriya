from ..ugens import (
    DC,
    Out,
    SynthDef,
    SynthDefBuilder,
)


def build_device_dc_tester(channel_count: int = 2) -> SynthDef:
    with SynthDefBuilder(dc=1, out=0) as builder:
        Out.ar(bus=builder["out"], source=[DC.ar(source=builder["dc"])] * channel_count)
    return builder.build(f"supriya:device-dc-tester:{channel_count}")
