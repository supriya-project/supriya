import dataclasses
from typing import Literal

import pytest

from supriya import CalculationRate, SynthDef
from supriya.sessions import (
    ChannelCount,
    Device,
    DeviceContainer,
    FloatField,
    Names,
    ParameterConfig,
    PatchMode,
    Rack,
    SidechainConfig,
    SynthConfig,
)
from supriya.typing import INHERIT
from supriya.ugens import In, ReplaceOut, SynthDefBuilder

from .conftest import Scenario


def build_effect_synthdef(channel_count: ChannelCount) -> SynthDef:
    with SynthDefBuilder(bus=0, multiplier=1, offset=0) as builder:
        source = In.ar(bus=builder["bus"], channel_count=channel_count)
        source *= builder["multiplier"]
        source += builder["offset"]
        ReplaceOut.ar(bus=builder["bus"], source=source)
    return builder.build(f"test:effect:{channel_count}")


def build_sidechain_synthdef(channel_count: ChannelCount) -> SynthDef:
    with SynthDefBuilder(bus=0, sidechain_bus=0, multiplier=1, offset=0) as builder:
        source = In.ar(bus=builder["bus"], channel_count=channel_count)
        source *= In.ar(bus=builder["sidechain_bus"], channel_count=channel_count)
        source *= builder["multiplier"]
        source += builder["offset"]
        ReplaceOut.ar(bus=builder["bus"], source=source)
    return builder.build(f"test:sidechain:{channel_count}")


@dataclasses.dataclass(frozen=True)
class AddDeviceScenario(Scenario):
    parameter_configs: list[ParameterConfig] | None
    sidechain_configs: list[SidechainConfig] | None
    synth_configs: list[SynthConfig]


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "scenario",
    [
        # effect with one synth, no parameter specs
        AddDeviceScenario(
            commands=[(None, "add_mixer", {"name": "Mixer"})],
            subject="mixers[0]",
            parameter_configs=None,
            sidechain_configs=None,
            synth_configs=[
                SynthConfig(synthdef=build_effect_synthdef),
            ],
            expected_components_diff=lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,3 +1,4 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
            +            <Device 2 'Device'>
            """,
            expected_messages="""
            - ['/d_recv', <SynthDef: test:effect:2>]
            - ['/sync', 3]
            - ['/c_fill', 5, 2, 0.0]
            - [None,
               [['/g_new', 1007, 0, 1002],
                ['/s_new', 'test:effect:2', 1008, 1, 1007, 'bus', 16.0],
                ['/s_new', 'supriya:meters:2', 1009, 3, 1008, 'in_', 16.0, 'out', 5.0]]]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -4,6 +4,11 @@
                     1004 supriya:meters:2 (session.mixers[0]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (session.mixers[0]:devices)
            +            1007 group (session.mixers[0].devices[0]:group)
            +                1008 test:effect:2 (session.mixers[0].devices[0]:synth-0)
            +                    bus: 16.0, multiplier: 1.0, offset: 0.0
            +                1009 supriya:meters:2 (session.mixers[0].devices[0]:output-levels)
            +                    in_: 16.0, out: 5.0
                     1003 supriya:channel-strip:2 (session.mixers[0]:channel-strip)
                         active: 1.0, done_action: 2.0, gain: c0, gate: 1.0, out: 16.0
                     1005 supriya:meters:2 (session.mixers[0]:output-levels)
            """,
        ),
        # effect with one synth, two parameter specs
        AddDeviceScenario(
            commands=[(None, "add_mixer", {"name": "Mixer"})],
            subject="mixers[0]",
            parameter_configs=[
                ParameterConfig(
                    name="mult", field=FloatField(default=0.5, has_bus=True)
                ),
                ParameterConfig(
                    name="add", field=FloatField(default=0.25, has_bus=True)
                ),
            ],
            sidechain_configs=None,
            synth_configs=[
                SynthConfig(
                    synthdef=build_effect_synthdef,
                    parameters={
                        "multiplier": (CalculationRate.CONTROL, "mult"),
                        "offset": (CalculationRate.CONTROL, "add"),
                    },
                ),
            ],
            expected_components_diff=lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,3 +1,4 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
            +            <Device 2 'Device'>
            """,
            expected_messages="""
            - ['/d_recv', <SynthDef: test:effect:2>]
            - ['/sync', 3]
            - [None, [['/c_set', 5, 0.25, 6, 0.5], ['/c_fill', 7, 2, 0.0]]]
            - [None,
               [['/g_new', 1007, 0, 1002],
                ['/s_new', 'test:effect:2', 1008, 1, 1007, 'bus', 16.0, 'multiplier', 'c6', 'offset', 'c5'],
                ['/s_new', 'supriya:meters:2', 1009, 3, 1008, 'in_', 16.0, 'out', 7.0]]]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -4,6 +4,11 @@
                     1004 supriya:meters:2 (session.mixers[0]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (session.mixers[0]:devices)
            +            1007 group (session.mixers[0].devices[0]:group)
            +                1008 test:effect:2 (session.mixers[0].devices[0]:synth-0)
            +                    bus: 16.0, multiplier: c6, offset: c5
            +                1009 supriya:meters:2 (session.mixers[0].devices[0]:output-levels)
            +                    in_: 16.0, out: 7.0
                     1003 supriya:channel-strip:2 (session.mixers[0]:channel-strip)
                         active: 1.0, done_action: 2.0, gain: c0, gate: 1.0, out: 16.0
                     1005 supriya:meters:2 (session.mixers[0]:output-levels)
            """,
        ),
        # effect with one synth, one default-channeled sidechain
        AddDeviceScenario(
            commands=[(None, "add_mixer", {"name": "Mixer"})],
            subject="mixers[0]",
            parameter_configs=[],
            sidechain_configs=[
                SidechainConfig(name=Names.SIDECHAIN, channel_count=INHERIT)
            ],
            synth_configs=[
                SynthConfig(
                    synthdef=build_sidechain_synthdef,
                    parameters={
                        "sidechain_bus": (CalculationRate.AUDIO, Names.SIDECHAIN),
                    },
                ),
            ],
            expected_components_diff=lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,3 +1,4 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
            +            <Device 2 'Device'>
            """,
            expected_messages="""
            - ['/d_recv', <SynthDef: test:sidechain:2>]
            - ['/sync', 3]
            - ['/c_fill', 5, 2, 0.0]
            - [None,
               [['/g_new', 1007, 0, 1002],
                ['/s_new', 'test:sidechain:2', 1008, 1, 1007, 'bus', 16.0, 'sidechain_bus', 18.0],
                ['/s_new', 'supriya:meters:2', 1009, 3, 1008, 'in_', 16.0, 'out', 5.0]]]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -4,6 +4,11 @@
                     1004 supriya:meters:2 (session.mixers[0]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (session.mixers[0]:devices)
            +            1007 group (session.mixers[0].devices[0]:group)
            +                1008 test:sidechain:2 (session.mixers[0].devices[0]:synth-0)
            +                    bus: 16.0, multiplier: 1.0, offset: 0.0, sidechain_bus: 18.0
            +                1009 supriya:meters:2 (session.mixers[0].devices[0]:output-levels)
            +                    in_: 16.0, out: 5.0
                     1003 supriya:channel-strip:2 (session.mixers[0]:channel-strip)
                         active: 1.0, done_action: 2.0, gain: c0, gate: 1.0, out: 16.0
                     1005 supriya:meters:2 (session.mixers[0]:output-levels)
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_DeviceContainer_add_device(
    scenario: AddDeviceScenario, online: bool
) -> None:
    async with scenario.run(online=online) as session:
        subject = session[scenario.subject]
        assert isinstance(subject, DeviceContainer)
        device = await subject.add_device(
            name="Device",
            parameter_configs=scenario.parameter_configs,
            sidechain_configs=scenario.sidechain_configs,
            synth_configs=scenario.synth_configs,
        )
    assert isinstance(device, Device)
    assert device in subject.devices
    assert device.parent is subject
    assert subject.devices[0] is device


@dataclasses.dataclass(frozen=True)
class AddRackScenario(Scenario):
    chain_count: int = 1
    read_mode: Literal[PatchMode.IGNORE, PatchMode.REPLACE] = PatchMode.REPLACE
    write_mode: PatchMode = PatchMode.SUM


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "scenario",
    [
        AddRackScenario(
            id="add rack to mixer",
            commands=[(None, "add_mixer", {"name": "Mixer"})],
            subject="mixers[0]",
            expected_components_diff=lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,3 +1,5 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
            +            <Rack 2 'Rack'>
            +                <Chain 3>
            """,
            expected_messages="""
            - ['/d_recv', <SynthDef: supriya:patch-cable:2x2:replace>]
            - ['/sync', 3]
            - ['/c_set', 5, 1.0]
            - [None, [['/c_set', 6, 1.0, 7, 0.0], ['/c_fill', 8, 2, 0.0, 10, 2, 0.0]]]
            - [None,
               [['/g_new', 1007, 0, 1002, 1008, 0, 1007],
                ['/s_new', 'supriya:patch-cable:2x2', 1009, 3, 1008, 'in_', 20.0, 'out', 16.0]]]
            - [None,
               [['/g_new', 1010, 0, 1008, 1011, 1, 1010],
                ['/s_new', 'supriya:patch-cable:2x2:replace', 1012, 2, 1011, 'in_', 16.0, 'out', 18.0],
                ['/s_new', 'supriya:meters:2', 1013, 3, 1012, 'in_', 18.0, 'out', 8.0],
                ['/s_new', 'supriya:channel-strip:2', 1014, 3, 1011, 'active', 'c6', 'gain', 'c7', 'out', 18.0],
                ['/s_new', 'supriya:meters:2', 1015, 3, 1014, 'in_', 18.0, 'out', 10.0],
                ['/s_new', 'supriya:patch-cable:2x2', 1016, 3, 1014, 'in_', 18.0, 'out', 20.0]]]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -4,6 +4,22 @@
                     1004 supriya:meters:2 (session.mixers[0]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (session.mixers[0]:devices)
            +            1007 group (session.mixers[0].devices[0]:group)
            +                1008 group (session.mixers[0].devices[0]:chains)
            +                    1010 group (session.mixers[0].devices[0].chains[0]:group)
            +                        1012 supriya:patch-cable:2x2:replace (session.mixers[0].devices[0].chains[0]:input)
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 18.0
            +                        1013 supriya:meters:2 (session.mixers[0].devices[0].chains[0]:input-levels)
            +                            in_: 18.0, out: 8.0
            +                        1011 group (session.mixers[0].devices[0].chains[0]:devices)
            +                        1014 supriya:channel-strip:2 (session.mixers[0].devices[0].chains[0]:channel-strip)
            +                            active: c6, done_action: 2.0, gain: c7, gate: 1.0, out: 18.0
            +                        1016 supriya:patch-cable:2x2 (session.mixers[0].devices[0].chains[0]:output)
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            +                        1015 supriya:meters:2 (session.mixers[0].devices[0].chains[0]:output-levels)
            +                            in_: 18.0, out: 10.0
            +                1009 supriya:patch-cable:2x2 (session.mixers[0].devices[0]:output)
            +                    active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
                     1003 supriya:channel-strip:2 (session.mixers[0]:channel-strip)
                         active: 1.0, done_action: 2.0, gain: c0, gate: 1.0, out: 16.0
                     1005 supriya:meters:2 (session.mixers[0]:output-levels)
            """,
        ),
        AddRackScenario(
            id="add rack to track",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Track"}),
            ],
            subject="mixers[0].tracks[0]",
            expected_components_diff=lambda session: """
            --- initial
            +++ mutation
            @@ -2,3 +2,5 @@
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
                         <Track 2 'Track'>
            +                <Rack 3 'Rack'>
            +                    <Chain 4>
            """,
            expected_messages="""
            - ['/d_recv', <SynthDef: supriya:patch-cable:2x2:replace>]
            - ['/sync', 3]
            - ['/c_set', 11, 1.0]
            - [None, [['/c_set', 12, 1.0, 13, 0.0], ['/c_fill', 14, 2, 0.0, 16, 2, 0.0]]]
            - [None,
               [['/g_new', 1014, 0, 1009, 1015, 0, 1014],
                ['/s_new', 'supriya:patch-cable:2x2', 1016, 3, 1015, 'in_', 22.0, 'out', 18.0]]]
            - [None,
               [['/g_new', 1017, 0, 1015, 1018, 1, 1017],
                ['/s_new', 'supriya:patch-cable:2x2:replace', 1019, 2, 1018, 'in_', 18.0, 'out', 20.0],
                ['/s_new', 'supriya:meters:2', 1020, 3, 1019, 'in_', 20.0, 'out', 14.0],
                ['/s_new', 'supriya:channel-strip:2', 1021, 3, 1018, 'active', 'c12', 'gain', 'c13', 'out', 20.0],
                ['/s_new', 'supriya:meters:2', 1022, 3, 1021, 'in_', 20.0, 'out', 16.0],
                ['/s_new', 'supriya:patch-cable:2x2', 1023, 3, 1021, 'in_', 20.0, 'out', 22.0]]]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -6,6 +6,22 @@
                             1011 supriya:meters:2 (session.mixers[0].tracks[0]:input-levels)
                                 in_: 18.0, out: 7.0
                             1009 group (session.mixers[0].tracks[0]:devices)
            +                    1014 group (session.mixers[0].tracks[0].devices[0]:group)
            +                        1015 group (session.mixers[0].tracks[0].devices[0]:chains)
            +                            1017 group (session.mixers[0].tracks[0].devices[0].chains[0]:group)
            +                                1019 supriya:patch-cable:2x2:replace (session.mixers[0].tracks[0].devices[0].chains[0]:input)
            +                                    active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            +                                1020 supriya:meters:2 (session.mixers[0].tracks[0].devices[0].chains[0]:input-levels)
            +                                    in_: 20.0, out: 14.0
            +                                1018 group (session.mixers[0].tracks[0].devices[0].chains[0]:devices)
            +                                1021 supriya:channel-strip:2 (session.mixers[0].tracks[0].devices[0].chains[0]:channel-strip)
            +                                    active: c12, done_action: 2.0, gain: c13, gate: 1.0, out: 20.0
            +                                1023 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].devices[0].chains[0]:output)
            +                                    active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 22.0
            +                                1022 supriya:meters:2 (session.mixers[0].tracks[0].devices[0].chains[0]:output-levels)
            +                                    in_: 20.0, out: 16.0
            +                        1016 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].devices[0]:output)
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 18.0
                             1010 supriya:channel-strip:2 (session.mixers[0].tracks[0]:channel-strip)
                                 active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
                             1012 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
            """,
        ),
        AddRackScenario(
            id="add rack to mixer, read:ignore, write:replace",
            commands=[(None, "add_mixer", {"name": "Mixer"})],
            subject="mixers[0]",
            read_mode=PatchMode.IGNORE,
            write_mode=PatchMode.REPLACE,
            expected_components_diff=lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,3 +1,5 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
            +            <Rack 2 'Rack'>
            +                <Chain 3>
            """,
            expected_messages="""
            - ['/d_recv', <SynthDef: supriya:patch-cable:2x2:replace>]
            - ['/d_recv', <SynthDef: supriya:zero:2>]
            - ['/sync', 3]
            - ['/c_set', 5, 1.0]
            - [None, [['/c_set', 6, 1.0, 7, 0.0], ['/c_fill', 8, 2, 0.0]]]
            - [None,
               [['/g_new', 1007, 0, 1002, 1008, 0, 1007],
                ['/s_new', 'supriya:patch-cable:2x2:replace', 1009, 3, 1008, 'in_', 20.0, 'out', 16.0]]]
            - [None,
               [['/g_new', 1010, 0, 1008, 1011, 1, 1010],
                ['/s_new', 'supriya:zero:2', 1012, 2, 1011, 'out', 18.0],
                ['/s_new', 'supriya:channel-strip:2', 1013, 3, 1011, 'active', 'c6', 'gain', 'c7', 'out', 18.0],
                ['/s_new', 'supriya:meters:2', 1014, 3, 1013, 'in_', 18.0, 'out', 8.0],
                ['/s_new', 'supriya:patch-cable:2x2', 1015, 3, 1013, 'in_', 18.0, 'out', 20.0]]]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -4,6 +4,20 @@
                     1004 supriya:meters:2 (session.mixers[0]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (session.mixers[0]:devices)
            +            1007 group (session.mixers[0].devices[0]:group)
            +                1008 group (session.mixers[0].devices[0]:chains)
            +                    1010 group (session.mixers[0].devices[0].chains[0]:group)
            +                        1012 supriya:zero:2 (session.mixers[0].devices[0].chains[0]:input)
            +                            out: 18.0
            +                        1011 group (session.mixers[0].devices[0].chains[0]:devices)
            +                        1013 supriya:channel-strip:2 (session.mixers[0].devices[0].chains[0]:channel-strip)
            +                            active: c6, done_action: 2.0, gain: c7, gate: 1.0, out: 18.0
            +                        1015 supriya:patch-cable:2x2 (session.mixers[0].devices[0].chains[0]:output)
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            +                        1014 supriya:meters:2 (session.mixers[0].devices[0].chains[0]:output-levels)
            +                            in_: 18.0, out: 8.0
            +                1009 supriya:patch-cable:2x2:replace (session.mixers[0].devices[0]:output)
            +                    active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
                     1003 supriya:channel-strip:2 (session.mixers[0]:channel-strip)
                         active: 1.0, done_action: 2.0, gain: c0, gate: 1.0, out: 16.0
                     1005 supriya:meters:2 (session.mixers[0]:output-levels)
            """,
        ),
        AddRackScenario(
            id="add rack to mixer, chains:2, write:mix",
            commands=[(None, "add_mixer", {"name": "Mixer"})],
            subject="mixers[0]",
            chain_count=2,
            write_mode=PatchMode.MIX,
            expected_components_diff=lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,3 +1,6 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
            +            <Rack 2 'Rack'>
            +                <Chain 3>
            +                <Chain 4>
            """,
            expected_messages="""
            - ['/d_recv', <SynthDef: supriya:patch-cable:2x2:mix>]
            - ['/d_recv', <SynthDef: supriya:patch-cable:2x2:replace>]
            - ['/sync', 3]
            - ['/c_set', 5, 1.0]
            - [None, [['/c_set', 6, 1.0, 7, 0.0], ['/c_fill', 8, 2, 0.0, 10, 2, 0.0]]]
            - [None, [['/c_set', 12, 1.0, 13, 0.0], ['/c_fill', 14, 2, 0.0, 16, 2, 0.0]]]
            - [None,
               [['/g_new', 1007, 0, 1002, 1008, 0, 1007],
                ['/s_new', 'supriya:patch-cable:2x2:mix', 1009, 3, 1008, 'in_', 20.0, 'mix', 'c5', 'out', 16.0]]]
            - [None,
               [['/g_new', 1010, 0, 1008, 1011, 1, 1010],
                ['/s_new', 'supriya:patch-cable:2x2:replace', 1012, 2, 1011, 'in_', 16.0, 'out', 18.0],
                ['/s_new', 'supriya:meters:2', 1013, 3, 1012, 'in_', 18.0, 'out', 8.0],
                ['/s_new', 'supriya:channel-strip:2', 1014, 3, 1011, 'active', 'c6', 'gain', 'c7', 'out', 18.0],
                ['/s_new', 'supriya:meters:2', 1015, 3, 1014, 'in_', 18.0, 'out', 10.0],
                ['/s_new', 'supriya:patch-cable:2x2', 1016, 3, 1014, 'in_', 18.0, 'out', 20.0]]]
            - [None,
               [['/g_new', 1017, 3, 1010, 1018, 1, 1017],
                ['/s_new', 'supriya:patch-cable:2x2:replace', 1019, 2, 1018, 'in_', 16.0, 'out', 18.0],
                ['/s_new', 'supriya:meters:2', 1020, 3, 1019, 'in_', 18.0, 'out', 14.0],
                ['/s_new', 'supriya:channel-strip:2', 1021, 3, 1018, 'active', 'c12', 'gain', 'c13', 'out', 18.0],
                ['/s_new', 'supriya:meters:2', 1022, 3, 1021, 'in_', 18.0, 'out', 16.0],
                ['/s_new', 'supriya:patch-cable:2x2', 1023, 3, 1021, 'in_', 18.0, 'out', 20.0]]]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -4,6 +4,34 @@
                     1004 supriya:meters:2 (session.mixers[0]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (session.mixers[0]:devices)
            +            1007 group (session.mixers[0].devices[0]:group)
            +                1008 group (session.mixers[0].devices[0]:chains)
            +                    1010 group (session.mixers[0].devices[0].chains[0]:group)
            +                        1012 supriya:patch-cable:2x2:replace (session.mixers[0].devices[0].chains[0]:input)
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 18.0
            +                        1013 supriya:meters:2 (session.mixers[0].devices[0].chains[0]:input-levels)
            +                            in_: 18.0, out: 8.0
            +                        1011 group (session.mixers[0].devices[0].chains[0]:devices)
            +                        1014 supriya:channel-strip:2 (session.mixers[0].devices[0].chains[0]:channel-strip)
            +                            active: c6, done_action: 2.0, gain: c7, gate: 1.0, out: 18.0
            +                        1016 supriya:patch-cable:2x2 (session.mixers[0].devices[0].chains[0]:output)
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            +                        1015 supriya:meters:2 (session.mixers[0].devices[0].chains[0]:output-levels)
            +                            in_: 18.0, out: 10.0
            +                    1017 group (session.mixers[0].devices[0].chains[1]:group)
            +                        1019 supriya:patch-cable:2x2:replace (session.mixers[0].devices[0].chains[1]:input)
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 18.0
            +                        1020 supriya:meters:2 (session.mixers[0].devices[0].chains[1]:input-levels)
            +                            in_: 18.0, out: 14.0
            +                        1018 group (session.mixers[0].devices[0].chains[1]:devices)
            +                        1021 supriya:channel-strip:2 (session.mixers[0].devices[0].chains[1]:channel-strip)
            +                            active: c12, done_action: 2.0, gain: c13, gate: 1.0, out: 18.0
            +                        1023 supriya:patch-cable:2x2 (session.mixers[0].devices[0].chains[1]:output)
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            +                        1022 supriya:meters:2 (session.mixers[0].devices[0].chains[1]:output-levels)
            +                            in_: 18.0, out: 16.0
            +                1009 supriya:patch-cable:2x2:mix (session.mixers[0].devices[0]:output)
            +                    active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, mix: c5, out: 16.0
                     1003 supriya:channel-strip:2 (session.mixers[0]:channel-strip)
                         active: 1.0, done_action: 2.0, gain: c0, gate: 1.0, out: 16.0
                     1005 supriya:meters:2 (session.mixers[0]:output-levels)
            """,
        ),
    ],
    ids=lambda scenario: scenario.id,
)
@pytest.mark.asyncio
async def test_DeviceContainer_add_rack(
    scenario: AddRackScenario,
    online: bool,
) -> None:
    async with scenario.run(online=online) as session:
        subject = session[scenario.subject]
        assert isinstance(subject, DeviceContainer)
        rack = await subject.add_rack(
            name="Rack",
            chain_count=scenario.chain_count,
            read_mode=scenario.read_mode,
            write_mode=scenario.write_mode,
        )
    assert isinstance(rack, Rack)
    assert rack in subject.devices
    assert rack.parent is subject
    assert subject.devices[0] is rack
