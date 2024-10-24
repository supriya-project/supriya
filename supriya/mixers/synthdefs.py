from ..ugens import In, InFeedback, Linen, Out, Parameter, ReplaceOut, SynthDefBuilder

LAG_TIME = 0.005


# TODO: When to allocate?
# TODO: Separate up/down mix sd?
# TODO: Separate levels sd?


def build_channel_strip(channel_count=2):
    with SynthDefBuilder(
        active=1,
        bus=0,
        gain=Parameter(value=0, lag=LAG_TIME),
        gate=1,
    ) as builder:
        source = In.ar(
            channel_count=channel_count,
            bus=builder["bus"],
        )
        active_gate = Linen.kr(
            attack_time=LAG_TIME,
            gate=builder["active"],
            release_time=LAG_TIME,
        )
        free_gate = Linen.kr(
            attack_time=LAG_TIME,
            gate=builder["gate"],
            release_time=LAG_TIME,
        )
        source *= builder["gain"].db_to_amplitude()
        source *= active_gate
        source *= free_gate
        ReplaceOut.ar(bus=builder["bus"], source=source)
    return builder.build(f"channel-strip-{channel_count}")


CHANNEL_STRIP_2 = build_channel_strip(2)


def build_patch_cable(channel_count=2, feedback=False):
    with SynthDefBuilder(
        in_=0,
        out=0,
        gate=1,
    ) as builder:
        if feedback:
            source = InFeedback.ar(
                channel_count=channel_count,
                bus=builder["in_"],
            )
        else:
            source = In.ar(
                channel_count=channel_count,
                bus=builder["in_"],
            )
        free_gate = Linen.kr(
            attack_time=LAG_TIME,
            gate=builder["gate"],
            release_time=LAG_TIME,
        )
        source *= free_gate
        Out.ar(bus=builder["out"], source=source)

    return builder.build(f"patch-cable-{channel_count}")


FB_PATCH_CABLE_2 = build_patch_cable(2, feedback=True)
PATCH_CABLE_2 = build_patch_cable(2)
