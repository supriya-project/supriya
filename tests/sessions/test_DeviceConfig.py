import dataclasses

import pytest

from supriya.sessions import DeviceConfig
from supriya.sessions.device_configs import COMPRESSOR_CONFIG

from .conftest import Scenario, apply_commands

COMMANDS: list[tuple[str | None, str, dict | None]] = [
    (None, "add_mixer", {"name": "Mixer"}),
    ("mixers[0]", "add_track", {"name": "Track One"}),
    ("mixers[0]", "add_track", {"name": "Track Two"}),
]


@dataclasses.dataclass(frozen=True)
class DeviceConfigScenario(Scenario):
    actions: list[tuple[str | None, str, dict | None]] = dataclasses.field(
        default_factory=list, kw_only=True
    )


@pytest.mark.parametrize(
    "scenario",
    [
        DeviceConfigScenario(
            id="empty device",
            actions=[
                (
                    "mixers[0].tracks[0]",
                    "add_device",
                    {"device_config": DeviceConfig()},
                ),
            ],
            commands=COMMANDS,
            expected_components_diff="""
            --- initial
            +++ mutation
            @@ -2,4 +2,5 @@
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
                         <Track 2 'Track One'>
            +                <Device 4>
                         <Track 3 'Track Two'>
            """,
            expected_messages="""
            - ['/c_fill', 17, 2, 0.0]
            - [None,
               [['/g_new', 1021, 0, 1009, 1022, 0, 1021], ['/s_new', 'supriya:meters:2', 1023, 1, 1021, 'in_', 18.0, 'out', 17.0]]]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -6,6 +6,10 @@
                             1011 supriya:meters:2 (session.mixers[0].tracks[0]:input-levels)
                                 in_: 18.0, out: 7.0
                             1009 group (session.mixers[0].tracks[0]:devices)
            +                    1021 group (session.mixers[0].tracks[0].devices[0]:group)
            +                        1022 group (session.mixers[0].tracks[0].devices[0]:synths)
            +                        1023 supriya:meters:2 (session.mixers[0].tracks[0].devices[0]:output-levels)
            +                            in_: 18.0, out: 17.0
                             1010 supriya:channel-strip:2 (session.mixers[0].tracks[0]:channel-strip)
                                 active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
                             1012 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
            """,
        ),
        DeviceConfigScenario(
            id="compressor, defaults",
            actions=[
                (
                    "mixers[0].tracks[0]",
                    "add_device",
                    {"device_config": COMPRESSOR_CONFIG},
                ),
            ],
            commands=COMMANDS,
            expected_components_diff="""
            --- initial
            +++ mutation
            @@ -2,4 +2,5 @@
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
                         <Track 2 'Track One'>
            +                <Device 4 'Compressor'>
                         <Track 3 'Track Two'>
            """,
            expected_messages="""
            - ['/d_recv', <SynthDef: supriya:compressor:compressor:2x2>]
            - ['/d_recv', <SynthDef: supriya:compressor:sidechain:2>]
            - ['/sync', 3]
            - [None, [['/c_set', 17, 0.01], ['/c_fill', 18, 2, 0.0], ['/c_set', 20, 0.25, 21, 0.1, 22, -6.0]]]
            - [None,
               [['/g_new', 1021, 0, 1009, 1022, 0, 1021],
                ['/s_new', 'supriya:compressor:sidechain:2', 1023, 1, 1022, 'clamp_time', 'c17', 'in_', 18.0, 'out', 22.0],
                ['/s_new',
                 'supriya:compressor:compressor:2x2',
                 1024,
                 3,
                 1023,
                 'bus',
                 18.0,
                 'clamp_time',
                 'c17',
                 'ratio',
                 'c20',
                 'relax_time',
                 'c21',
                 'sidechain',
                 22.0,
                 'threshold',
                 'c22'],
                ['/s_new', 'supriya:meters:2', 1025, 1, 1021, 'in_', 18.0, 'out', 18.0]]]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -6,6 +6,14 @@
                             1011 supriya:meters:2 (session.mixers[0].tracks[0]:input-levels)
                                 in_: 18.0, out: 7.0
                             1009 group (session.mixers[0].tracks[0]:devices)
            +                    1021 group (session.mixers[0].tracks[0].devices[0]:group)
            +                        1022 group (session.mixers[0].tracks[0].devices[0]:synths)
            +                            1023 supriya:compressor:sidechain:2 (session.mixers[0].tracks[0].devices[0]:synth-0)
            +                                clamp_time: c17, gate: 1.0, in_: 18.0, out: 22.0
            +                            1024 supriya:compressor:compressor:2x2 (session.mixers[0].tracks[0].devices[0]:synth-1)
            +                                bus: 18.0, clamp_time: c17, gate: 1.0, ratio: c20, relax_time: c21, sidechain: 22.0, threshold: c22
            +                        1025 supriya:meters:2 (session.mixers[0].tracks[0].devices[0]:output-levels)
            +                            in_: 18.0, out: 18.0
                             1010 supriya:channel-strip:2 (session.mixers[0].tracks[0]:channel-strip)
                                 active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
                             1012 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
            """,
        ),
        DeviceConfigScenario(
            id="compressor, -> mono_sidechain=True",
            actions=[
                (
                    "mixers[0].tracks[0].devices[0]",
                    "set_parameter",
                    {"name": "mono_sidechain", "value": True},
                ),
            ],
            commands=[
                *COMMANDS,
                (
                    "mixers[0].tracks[0]",
                    "add_device",
                    {"device_config": COMPRESSOR_CONFIG},
                ),
            ],
            expected_components_diff="",
            expected_messages="""
            - ['/d_recv', <SynthDef: supriya:compressor:compressor:2x1>]
            - ['/d_recv', <SynthDef: supriya:compressor:sidechain:1>]
            - ['/sync', 3]
            - [None,
               [['/s_new', 'supriya:compressor:sidechain:1', 1026, 1, 1015, 'clamp_time', 'c11', 'in_', 18.0, 'out', 24.0],
                ['/s_new',
                 'supriya:compressor:compressor:2x1',
                 1027,
                 3,
                 1026,
                 'bus',
                 18.0,
                 'clamp_time',
                 'c11',
                 'ratio',
                 'c14',
                 'relax_time',
                 'c15',
                 'sidechain',
                 24.0,
                 'threshold',
                 'c16']]]
            - [None, [['/n_set', 1016, 'done_action', 2.0, 'gate', 0.0], ['/n_set', 1017, 'done_action', 2.0, 'gate', 0.0]]]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -9,9 +9,13 @@
                                 1014 group (session.mixers[0].tracks[0].devices[0]:group)
                                     1015 group (session.mixers[0].tracks[0].devices[0]:synths)
                                         1016 supriya:compressor:sidechain:2 (session.mixers[0].tracks[0].devices[0]:synth-0)
            -                                clamp_time: c11, gate: 1.0, in_: 18.0, out: 20.0
            +                                clamp_time: c11, gate: 0.0, in_: 18.0, out: 20.0
                                         1017 supriya:compressor:compressor:2x2 (session.mixers[0].tracks[0].devices[0]:synth-1)
            -                                bus: 18.0, clamp_time: c11, gate: 1.0, ratio: c14, relax_time: c15, sidechain: 20.0, threshold: c16
            +                                bus: 18.0, clamp_time: c11, gate: 0.0, ratio: c14, relax_time: c15, sidechain: 20.0, threshold: c16
            +                            1026 supriya:compressor:sidechain:1 (session.mixers[0].tracks[0].devices[0]:synth-0)
            +                                clamp_time: c11, gate: 1.0, in_: 18.0, out: 24.0
            +                            1027 supriya:compressor:compressor:2x1 (session.mixers[0].tracks[0].devices[0]:synth-1)
            +                                bus: 18.0, clamp_time: c11, gate: 1.0, ratio: c14, relax_time: c15, sidechain: 24.0, threshold: c16
                                     1018 supriya:meters:2 (session.mixers[0].tracks[0].devices[0]:output-levels)
                                         in_: 18.0, out: 12.0
                             1010 supriya:channel-strip:2 (session.mixers[0].tracks[0]:channel-strip)
            """,
        ),
        DeviceConfigScenario(
            id="compressor, -> sidechain=track:3",
            actions=[
                (
                    "mixers[0].tracks[0].devices[0]",
                    "set_sidechain",
                    {"name": "sidechain", "source": "mixers[0].tracks[1]"},
                ),
            ],
            commands=[
                *COMMANDS,
                (
                    "mixers[0].tracks[0]",
                    "add_device",
                    {"device_config": COMPRESSOR_CONFIG},
                ),
            ],
            expected_components_diff="",
            expected_messages="""
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 3]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1026, 0, 1014, 'in_', 22.0, 'out', 20.0]
            - ['/g_tail', 1015, 1017]
            - ['/n_set', 1016, 'done_action', 2.0, 'gate', 0.0]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -7,9 +7,11 @@
                                 in_: 18.0, out: 7.0
                             1009 group (session.mixers[0].tracks[0]:devices)
                                 1014 group (session.mixers[0].tracks[0].devices[0]:group)
            +                        1026 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0].devices[0]:sidechain)
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 20.0
                                     1015 group (session.mixers[0].tracks[0].devices[0]:synths)
                                         1016 supriya:compressor:sidechain:2 (session.mixers[0].tracks[0].devices[0]:synth-0)
            -                                clamp_time: c11, gate: 1.0, in_: 18.0, out: 20.0
            +                                clamp_time: c11, gate: 0.0, in_: 18.0, out: 20.0
                                         1017 supriya:compressor:compressor:2x2 (session.mixers[0].tracks[0].devices[0]:synth-1)
                                             bus: 18.0, clamp_time: c11, gate: 1.0, ratio: c14, relax_time: c15, sidechain: 20.0, threshold: c16
                                     1018 supriya:meters:2 (session.mixers[0].tracks[0].devices[0]:output-levels)
            """,
        ),
        DeviceConfigScenario(
            id="compressor, sidechain=track:3, -> mono_sidechain=True",
            actions=[
                (
                    "mixers[0].tracks[0].devices[0]",
                    "set_parameter",
                    {"name": "mono_sidechain", "value": True},
                ),
            ],
            commands=[
                *COMMANDS,
                (
                    "mixers[0].tracks[0]",
                    "add_device",
                    {"device_config": COMPRESSOR_CONFIG},
                ),
                (
                    "mixers[0].tracks[0].devices[0]",
                    "set_sidechain",
                    {"name": "sidechain", "source": "mixers[0].tracks[1]"},
                ),
            ],
            expected_components_diff="",
            expected_messages="""
            - ['/d_recv', <SynthDef: supriya:compressor:compressor:2x1>]
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x1>]
            - ['/sync', 3]
            - [None,
               [['/s_new', 'supriya:fb-patch-cable:2x1', 1026, 0, 1014, 'in_', 22.0, 'out', 24.0],
                ['/s_new',
                 'supriya:compressor:compressor:2x1',
                 1027,
                 1,
                 1015,
                 'bus',
                 18.0,
                 'clamp_time',
                 'c11',
                 'ratio',
                 'c14',
                 'relax_time',
                 'c15',
                 'sidechain',
                 24.0,
                 'threshold',
                 'c16']]]
            - [None, [['/n_set', 1016, 'done_action', 2.0, 'gate', 0.0], ['/n_set', 1017, 'done_action', 2.0, 'gate', 0.0]]]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -7,11 +7,15 @@
                                 in_: 18.0, out: 7.0
                             1009 group (session.mixers[0].tracks[0]:devices)
                                 1014 group (session.mixers[0].tracks[0].devices[0]:group)
            +                        1026 supriya:fb-patch-cable:2x1 (session.mixers[0].tracks[0].devices[0]:sidechain)
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 24.0
                                     1016 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0].devices[0]:sidechain)
            -                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 20.0
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 22.0, out: 20.0
                                     1015 group (session.mixers[0].tracks[0].devices[0]:synths)
                                         1017 supriya:compressor:compressor:2x2 (session.mixers[0].tracks[0].devices[0]:synth-1)
            -                                bus: 18.0, clamp_time: c11, gate: 1.0, ratio: c14, relax_time: c15, sidechain: 20.0, threshold: c16
            +                                bus: 18.0, clamp_time: c11, gate: 0.0, ratio: c14, relax_time: c15, sidechain: 20.0, threshold: c16
            +                            1027 supriya:compressor:compressor:2x1 (session.mixers[0].tracks[0].devices[0]:synth-1)
            +                                bus: 18.0, clamp_time: c11, gate: 1.0, ratio: c14, relax_time: c15, sidechain: 24.0, threshold: c16
                                     1018 supriya:meters:2 (session.mixers[0].tracks[0].devices[0]:output-levels)
                                         in_: 18.0, out: 12.0
                             1010 supriya:channel-strip:2 (session.mixers[0].tracks[0]:channel-strip)
            """,
        ),
    ],
    ids=lambda scenario: scenario.id,
)
@pytest.mark.asyncio
async def test_DeviceConfig(scenario: DeviceConfigScenario) -> None:
    async with scenario.run(online=True) as session:
        await apply_commands(session, scenario.actions)
