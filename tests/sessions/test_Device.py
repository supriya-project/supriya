import dataclasses

import pytest

from supriya import CalculationRate
from supriya.sessions import (
    ChannelCount,
    Device,
    DeviceConfig,
    Names,
    SynthConfig,
    Track,
)
from supriya.typing import INHERIT
from supriya.ugens import In, ReplaceOut, SynthDef, SynthDefBuilder

from .conftest import Scenario


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
    sidechain_configs={Names.SIDECHAIN: INHERIT},
    synth_configs=[
        SynthConfig(
            controls={
                "sidechain_bus": (
                    CalculationRate.AUDIO,
                    Names.SIDECHAIN,
                ),
            },
            synthdef=build_sidechain_synthdef,
        ),
    ],
)


@dataclasses.dataclass(frozen=True)
class SetSidechainScenario(Scenario):
    target: str
    sidechain_name: str
    sidechain_target: str | None


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "scenario",
    [
        SetSidechainScenario(
            id="sidechain from older auntie",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Older Auntie"}),
                ("mixers[0]", "add_track", {"name": "Parent"}),
                (
                    "mixers[0].tracks[1]",
                    "add_device",
                    {"device_config": SIDECHAIN_DEVICE_CONFIG},
                ),
            ],
            target="mixers[0].tracks[1].devices[0]",
            sidechain_name=Names.SIDECHAIN,
            sidechain_target="mixers[0].tracks[0]",
            expected_components_diff="",
            expected_messages="""
            - ['/s_new', 'supriya:patch-cable:2x2', 1025, 0, 1021, 'in_', 18.0, 'out', 22.0]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -18,6 +18,8 @@
                                 in_: 20.0, out: 13.0
                             1016 group (session.mixers[0].tracks[1]:devices)
                                 1021 group (session.mixers[0].tracks[1].devices[0]:group)
            +                        1025 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].devices[0]:sidechain)
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 22.0
                                     1022 group (session.mixers[0].tracks[1].devices[0]:synths)
                                         1023 test:sidechain:2 (session.mixers[0].tracks[1].devices[0]:synth-0)
                                             bus: 20.0, multiplier: 1.0, offset: 0.0, sidechain_bus: 22.0
            """,
        ),
        SetSidechainScenario(
            id="sidechain from younger auntie",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Parent"}),
                ("mixers[0]", "add_track", {"name": "Younger Auntie"}),
                (
                    "mixers[0].tracks[0]",
                    "add_device",
                    {"device_config": SIDECHAIN_DEVICE_CONFIG},
                ),
            ],
            target="mixers[0].tracks[0].devices[0]",
            sidechain_name=Names.SIDECHAIN,
            sidechain_target="mixers[0].tracks[1]",
            expected_components_diff="",
            expected_messages="""
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 3]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1025, 0, 1014, 'in_', 22.0, 'out', 20.0]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -7,6 +7,8 @@
                                 in_: 18.0, out: 7.0
                             1009 group (session.mixers[0].tracks[0]:devices)
                                 1014 group (session.mixers[0].tracks[0].devices[0]:group)
            +                        1025 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0].devices[0]:sidechain)
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 20.0
                                     1015 group (session.mixers[0].tracks[0].devices[0]:synths)
                                         1016 test:sidechain:2 (session.mixers[0].tracks[0].devices[0]:synth-0)
                                             bus: 18.0, multiplier: 1.0, offset: 0.0, sidechain_bus: 20.0
            """,
        ),
        SetSidechainScenario(
            id="sidechain from younger auntie to none",
            commands=[
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
            target="mixers[0].tracks[0].devices[0]",
            sidechain_name=Names.SIDECHAIN,
            sidechain_target=None,
            expected_components_diff="",
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -8,7 +8,7 @@
                             1009 group (session.mixers[0].tracks[0]:devices)
                                 1014 group (session.mixers[0].tracks[0].devices[0]:group)
                                     1016 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0].devices[0]:sidechain)
            -                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 20.0
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 22.0, out: 20.0
                                     1015 group (session.mixers[0].tracks[0].devices[0]:synths)
                                         1017 test:sidechain:2 (session.mixers[0].tracks[0].devices[0]:synth-0)
                                             bus: 18.0, multiplier: 1.0, offset: 0.0, sidechain_bus: 20.0
            """,
            expected_messages="""
            - ['/n_set', 1016, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_Device_set_sidechain(
    scenario: SetSidechainScenario,
    online: bool,
) -> None:
    async with scenario.run(online=online) as session:
        device = session[scenario.target]
        assert isinstance(device, Device)
        track: Track | None = None
        if scenario.sidechain_target is not None:
            track_ = session[scenario.sidechain_target]
            assert isinstance(track_, Track)
            track = track_
        await device.set_sidechain(name=scenario.sidechain_name, source=track)
    if scenario.expected_exception:
        return
    assert device.sidechains[scenario.sidechain_name].source is track
