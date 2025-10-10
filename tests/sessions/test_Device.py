from typing import Callable

import pytest

from supriya import CalculationRate
from supriya.sessions import (
    ChannelCount,
    Device,
    DeviceConfig,
    Names,
    Session,
    SidechainConfig,
    SynthConfig,
    Track,
)
from supriya.typing import DEFAULT
from supriya.ugens import In, ReplaceOut, SynthDef, SynthDefBuilder

from .conftest import does_not_raise, run_test


def build_sidechain_synthdef(channel_count: ChannelCount) -> SynthDef:
    with SynthDefBuilder(bus=0, sidechain_bus=0, multiplier=1, offset=0) as builder:
        source = In.ar(bus=builder["bus"], channel_count=channel_count)
        source *= In.ar(bus=builder["sidechain_bus"], channel_count=channel_count)
        source *= builder["multiplier"]
        source += builder["offset"]
        ReplaceOut.ar(bus=builder["bus"], source=source)
    return builder.build(f"test:sidechain:{channel_count}")


SIDECHAIN_DEVICE_CONFIG = DeviceConfig(
    name="Self",
    sidechain_configs=[SidechainConfig(name=Names.SIDECHAIN, channel_count=DEFAULT)],
    synth_configs=[
        SynthConfig(
            synthdef=build_sidechain_synthdef,
            parameters={
                "sidechain_bus": (
                    CalculationRate.AUDIO,
                    Names.SIDECHAIN,
                ),
            },
        ),
    ],
)


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    (
        "commands, device_target, sidechain_name, track_target, "
        "maybe_raises, expected_components_diff, expected_tree_diff, expected_messages"
    ),
    [
        # sidechain from older auntie
        (
            [
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Older Auntie"}),
                ("mixers[0]", "add_track", {"name": "Parent"}),
                (
                    "mixers[0].tracks[1]",
                    "add_device",
                    {"device_config": SIDECHAIN_DEVICE_CONFIG},
                ),
            ],
            "mixers[0].tracks[1].devices[0]",
            Names.SIDECHAIN,
            "mixers[0].tracks[0]",
            does_not_raise,
            "",
            """
            --- initial
            +++ mutation
            @@ -18,6 +18,8 @@
                                 in_: 20.0, out: 13.0
                             1016 group (session.mixers[0].tracks[1]:devices)
                                 1021 group (session.mixers[0].tracks[1].devices[0]:group)
            +                        1023 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].devices[0]:sidechain)
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 22.0
                                     1022 test:sidechain:2 (session.mixers[0].tracks[1].devices[0]:synth-0)
                                         bus: 20.0, multiplier: 1.0, offset: 0.0, sidechain_bus: 22.0
                             1017 supriya:channel-strip:2 (session.mixers[0].tracks[1]:channel-strip)
            """,
            """
            - ['/s_new', 'supriya:patch-cable:2x2', 1023, 0, 1021, 'in_', 18.0, 'out', 22.0]
            """,
        ),
        # sidechain from younger auntie
        (
            [
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Parent"}),
                ("mixers[0]", "add_track", {"name": "Younger Auntie"}),
                (
                    "mixers[0].tracks[0]",
                    "add_device",
                    {"device_config": SIDECHAIN_DEVICE_CONFIG},
                ),
            ],
            "mixers[0].tracks[0].devices[0]",
            Names.SIDECHAIN,
            "mixers[0].tracks[1]",
            does_not_raise,
            "",
            """
            --- initial
            +++ mutation
            @@ -7,6 +7,8 @@
                                 in_: 18.0, out: 7.0
                             1009 group (session.mixers[0].tracks[0]:devices)
                                 1014 group (session.mixers[0].tracks[0].devices[0]:group)
            +                        1023 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0].devices[0]:sidechain)
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 20.0
                                     1015 test:sidechain:2 (session.mixers[0].tracks[0].devices[0]:synth-0)
                                         bus: 18.0, multiplier: 1.0, offset: 0.0, sidechain_bus: 20.0
                             1010 supriya:channel-strip:2 (session.mixers[0].tracks[0]:channel-strip)
            """,
            """
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 3]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1023, 0, 1014, 'in_', 22.0, 'out', 20.0]
            """,
        ),
        # sidechain from younger auntie to none
        (
            [
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Parent"}),
                ("mixers[0]", "add_track", {"name": "Younger Auntie"}),
                (
                    "mixers[0].tracks[0]",
                    "add_device",
                    {"device_config": SIDECHAIN_DEVICE_CONFIG},
                ),
                (
                    "mixers[0].tracks[0].devices[0]",
                    "set_sidechain",
                    {"name": Names.SIDECHAIN, "source": "mixers[0].tracks[1]"},
                ),
            ],
            "mixers[0].tracks[0].devices[0]",
            Names.SIDECHAIN,
            None,
            does_not_raise,
            "",
            """
            --- initial
            +++ mutation
            @@ -7,8 +7,8 @@
                                 in_: 18.0, out: 7.0
                             1009 group (session.mixers[0].tracks[0]:devices)
                                 1014 group (session.mixers[0].tracks[0].devices[0]:group)
            -                        1015 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0].devices[0]:sidechain)
            -                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 20.0
            +                        1015 supriya:fb-patch-cable:2x2
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 22.0, out: 20.0
                                     1016 test:sidechain:2 (session.mixers[0].tracks[0].devices[0]:synth-0)
                                         bus: 18.0, multiplier: 1.0, offset: 0.0, sidechain_bus: 20.0
                             1010 supriya:channel-strip:2 (session.mixers[0].tracks[0]:channel-strip)
            """,
            """
            - ['/n_set', 1015, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_Device_set_sidechain(
    commands: list[tuple[str | None, str, dict | None]],
    expected_components_diff: Callable[[Session], str] | str,
    expected_messages: str,
    expected_tree_diff: str,
    maybe_raises,
    online: bool,
    device_target: str,
    sidechain_name: str,
    track_target: str | None,
) -> None:
    async with run_test(
        commands=commands,
        expected_components_diff=expected_components_diff,
        expected_messages=expected_messages,
        expected_tree_diff=expected_tree_diff,
        online=online,
    ) as session:
        device = session[device_target]
        assert isinstance(device, Device)
        if track_target is not None:
            track = session[track_target]
            assert isinstance(track, Track)
        else:
            track = None
        raised = True
        with maybe_raises:
            await device.set_sidechain(name=sidechain_name, source=track)
            raised = False
    if not raised:
        assert device.sidechains[sidechain_name].source is track
