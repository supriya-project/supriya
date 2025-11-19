import dataclasses
from typing import Literal

import pytest

from supriya import CalculationRate, SynthDef
from supriya.sessions import (
    ChannelCount,
    Device,
    DeviceContainer,
    Field,
    FloatField,
    Names,
    ParameterConfig,
    PatchMode,
    Rack,
    SidechainConfig,
    SynthConfig,
)
from supriya.typing import INHERIT, Inherit
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
    parameter_configs: dict[str, Field | ParameterConfig] | None
    sidechain_configs: dict[str, ChannelCount | Inherit | SidechainConfig] | None
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
               [['/g_new', 1007, 0, 1002, 1008, 0, 1007],
                ['/s_new', 'test:effect:2', 1009, 1, 1008, 'bus', 16.0],
                ['/s_new', 'supriya:meters:2', 1010, 1, 1007, 'in_', 16.0, 'out', 5.0]]]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -4,6 +4,12 @@
                     1004 supriya:meters:2 (session.mixers[0]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (session.mixers[0]:devices)
            +            1007 group (session.mixers[0].devices[0]:group)
            +                1008 group (session.mixers[0].devices[0]:synths)
            +                    1009 test:effect:2 (session.mixers[0].devices[0]:synth-0)
            +                        bus: 16.0, multiplier: 1.0, offset: 0.0
            +                1010 supriya:meters:2 (session.mixers[0].devices[0]:output-levels)
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
            parameter_configs={
                "mult": FloatField(default=0.5),
                "add": FloatField(default=0.25),
            },
            sidechain_configs=None,
            synth_configs=[
                SynthConfig(
                    controls={
                        "multiplier": (CalculationRate.CONTROL, "mult"),
                        "offset": (CalculationRate.CONTROL, "add"),
                    },
                    synthdef=build_effect_synthdef,
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
               [['/g_new', 1007, 0, 1002, 1008, 0, 1007],
                ['/s_new', 'test:effect:2', 1009, 1, 1008, 'bus', 16.0, 'multiplier', 'c6', 'offset', 'c5'],
                ['/s_new', 'supriya:meters:2', 1010, 1, 1007, 'in_', 16.0, 'out', 7.0]]]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -4,6 +4,12 @@
                     1004 supriya:meters:2 (session.mixers[0]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (session.mixers[0]:devices)
            +            1007 group (session.mixers[0].devices[0]:group)
            +                1008 group (session.mixers[0].devices[0]:synths)
            +                    1009 test:effect:2 (session.mixers[0].devices[0]:synth-0)
            +                        bus: 16.0, multiplier: c6, offset: c5
            +                1010 supriya:meters:2 (session.mixers[0].devices[0]:output-levels)
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
            parameter_configs={},
            sidechain_configs={Names.SIDECHAIN: SidechainConfig(channel_count=INHERIT)},
            synth_configs=[
                SynthConfig(
                    controls={
                        "sidechain_bus": (CalculationRate.AUDIO, Names.SIDECHAIN),
                    },
                    synthdef=build_sidechain_synthdef,
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
               [['/g_new', 1007, 0, 1002, 1008, 0, 1007],
                ['/s_new', 'test:sidechain:2', 1009, 1, 1008, 'bus', 16.0, 'sidechain_bus', 18.0],
                ['/s_new', 'supriya:meters:2', 1010, 1, 1007, 'in_', 16.0, 'out', 5.0]]]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -4,6 +4,12 @@
                     1004 supriya:meters:2 (session.mixers[0]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (session.mixers[0]:devices)
            +            1007 group (session.mixers[0].devices[0]:group)
            +                1008 group (session.mixers[0].devices[0]:synths)
            +                    1009 test:sidechain:2 (session.mixers[0].devices[0]:synth-0)
            +                        bus: 16.0, multiplier: 1.0, offset: 0.0, sidechain_bus: 18.0
            +                1010 supriya:meters:2 (session.mixers[0].devices[0]:output-levels)
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
            +                <Chain 3 'Chain 1'>
            """,
            expected_messages="""
            - ['/d_recv', <SynthDef: supriya:patch-cable:2x2:replace>]
            - ['/sync', 3]
            - [None, [['/c_set', 5, 1.0], ['/c_fill', 6, 2, 0.0]]]
            - [None, [['/c_set', 8, 1.0, 9, 0.0], ['/c_fill', 10, 2, 0.0, 12, 2, 0.0]]]
            - [None,
               [['/g_new', 1007, 0, 1002, 1008, 0, 1007],
                ['/s_new', 'supriya:patch-cable:2x2', 1009, 3, 1008, 'in_', 20.0, 'out', 16.0],
                ['/s_new', 'supriya:meters:2', 1010, 1, 1007, 'in_', 16.0, 'out', 6.0]]]
            - [None,
               [['/g_new', 1011, 0, 1008, 1012, 1, 1011],
                ['/s_new', 'supriya:patch-cable:2x2:replace', 1013, 0, 1011, 'in_', 16.0, 'out', 18.0],
                ['/s_new', 'supriya:meters:2', 1014, 3, 1013, 'in_', 18.0, 'out', 10.0],
                ['/s_new', 'supriya:channel-strip:2', 1015, 3, 1012, 'active', 'c8', 'gain', 'c9', 'out', 18.0],
                ['/s_new', 'supriya:meters:2', 1016, 3, 1015, 'in_', 18.0, 'out', 12.0],
                ['/s_new', 'supriya:patch-cable:2x2', 1017, 3, 1015, 'in_', 18.0, 'out', 20.0]]]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -4,6 +4,24 @@
                     1004 supriya:meters:2 (session.mixers[0]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (session.mixers[0]:devices)
            +            1007 group (session.mixers[0].devices[0]:group)
            +                1008 group (session.mixers[0].devices[0]:chains)
            +                    1011 group (session.mixers[0].devices[0].chains[0]:group)
            +                        1013 supriya:patch-cable:2x2:replace (session.mixers[0].devices[0].chains[0]:input)
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 18.0
            +                        1014 supriya:meters:2 (session.mixers[0].devices[0].chains[0]:input-levels)
            +                            in_: 18.0, out: 10.0
            +                        1012 group (session.mixers[0].devices[0].chains[0]:devices)
            +                        1015 supriya:channel-strip:2 (session.mixers[0].devices[0].chains[0]:channel-strip)
            +                            active: c8, done_action: 2.0, gain: c9, gate: 1.0, out: 18.0
            +                        1017 supriya:patch-cable:2x2 (session.mixers[0].devices[0].chains[0]:output)
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            +                        1016 supriya:meters:2 (session.mixers[0].devices[0].chains[0]:output-levels)
            +                            in_: 18.0, out: 12.0
            +                1009 supriya:patch-cable:2x2 (session.mixers[0].devices[0]:output)
            +                    active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
            +                1010 supriya:meters:2 (session.mixers[0].devices[0]:output-levels)
            +                    in_: 16.0, out: 6.0
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
            +                    <Chain 4 'Chain 1'>
            """,
            expected_messages="""
            - ['/d_recv', <SynthDef: supriya:patch-cable:2x2:replace>]
            - ['/sync', 3]
            - [None, [['/c_set', 11, 1.0], ['/c_fill', 12, 2, 0.0]]]
            - [None, [['/c_set', 14, 1.0, 15, 0.0], ['/c_fill', 16, 2, 0.0, 18, 2, 0.0]]]
            - [None,
               [['/g_new', 1014, 0, 1009, 1015, 0, 1014],
                ['/s_new', 'supriya:patch-cable:2x2', 1016, 3, 1015, 'in_', 22.0, 'out', 18.0],
                ['/s_new', 'supriya:meters:2', 1017, 1, 1014, 'in_', 18.0, 'out', 12.0]]]
            - [None,
               [['/g_new', 1018, 0, 1015, 1019, 1, 1018],
                ['/s_new', 'supriya:patch-cable:2x2:replace', 1020, 0, 1018, 'in_', 18.0, 'out', 20.0],
                ['/s_new', 'supriya:meters:2', 1021, 3, 1020, 'in_', 20.0, 'out', 16.0],
                ['/s_new', 'supriya:channel-strip:2', 1022, 3, 1019, 'active', 'c14', 'gain', 'c15', 'out', 20.0],
                ['/s_new', 'supriya:meters:2', 1023, 3, 1022, 'in_', 20.0, 'out', 18.0],
                ['/s_new', 'supriya:patch-cable:2x2', 1024, 3, 1022, 'in_', 20.0, 'out', 22.0]]]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -6,6 +6,24 @@
                             1011 supriya:meters:2 (session.mixers[0].tracks[0]:input-levels)
                                 in_: 18.0, out: 7.0
                             1009 group (session.mixers[0].tracks[0]:devices)
            +                    1014 group (session.mixers[0].tracks[0].devices[0]:group)
            +                        1015 group (session.mixers[0].tracks[0].devices[0]:chains)
            +                            1018 group (session.mixers[0].tracks[0].devices[0].chains[0]:group)
            +                                1020 supriya:patch-cable:2x2:replace (session.mixers[0].tracks[0].devices[0].chains[0]:input)
            +                                    active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            +                                1021 supriya:meters:2 (session.mixers[0].tracks[0].devices[0].chains[0]:input-levels)
            +                                    in_: 20.0, out: 16.0
            +                                1019 group (session.mixers[0].tracks[0].devices[0].chains[0]:devices)
            +                                1022 supriya:channel-strip:2 (session.mixers[0].tracks[0].devices[0].chains[0]:channel-strip)
            +                                    active: c14, done_action: 2.0, gain: c15, gate: 1.0, out: 20.0
            +                                1024 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].devices[0].chains[0]:output)
            +                                    active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 22.0
            +                                1023 supriya:meters:2 (session.mixers[0].tracks[0].devices[0].chains[0]:output-levels)
            +                                    in_: 20.0, out: 18.0
            +                        1016 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].devices[0]:output)
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 18.0
            +                        1017 supriya:meters:2 (session.mixers[0].tracks[0].devices[0]:output-levels)
            +                            in_: 18.0, out: 12.0
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
            +                <Chain 3 'Chain 1'>
            """,
            expected_messages="""
            - ['/d_recv', <SynthDef: supriya:patch-cable:2x2:replace>]
            - ['/d_recv', <SynthDef: supriya:zero:2>]
            - ['/sync', 3]
            - [None, [['/c_set', 5, 1.0], ['/c_fill', 6, 2, 0.0]]]
            - [None, [['/c_set', 8, 1.0, 9, 0.0], ['/c_fill', 10, 2, 0.0, 12, 2, 0.0]]]
            - [None,
               [['/g_new', 1007, 0, 1002, 1008, 0, 1007],
                ['/s_new', 'supriya:patch-cable:2x2:replace', 1009, 3, 1008, 'in_', 20.0, 'out', 16.0],
                ['/s_new', 'supriya:meters:2', 1010, 1, 1007, 'in_', 16.0, 'out', 6.0]]]
            - [None,
               [['/g_new', 1011, 0, 1008, 1012, 1, 1011],
                ['/s_new', 'supriya:zero:2', 1013, 0, 1011, 'out', 18.0],
                ['/s_new', 'supriya:meters:2', 1014, 3, 1013, 'in_', 18.0, 'out', 10.0],
                ['/s_new', 'supriya:channel-strip:2', 1015, 3, 1012, 'active', 'c8', 'gain', 'c9', 'out', 18.0],
                ['/s_new', 'supriya:meters:2', 1016, 3, 1015, 'in_', 18.0, 'out', 12.0],
                ['/s_new', 'supriya:patch-cable:2x2', 1017, 3, 1015, 'in_', 18.0, 'out', 20.0]]]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -4,6 +4,24 @@
                     1004 supriya:meters:2 (session.mixers[0]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (session.mixers[0]:devices)
            +            1007 group (session.mixers[0].devices[0]:group)
            +                1008 group (session.mixers[0].devices[0]:chains)
            +                    1011 group (session.mixers[0].devices[0].chains[0]:group)
            +                        1013 supriya:zero:2 (session.mixers[0].devices[0].chains[0]:input)
            +                            out: 18.0
            +                        1014 supriya:meters:2 (session.mixers[0].devices[0].chains[0]:input-levels)
            +                            in_: 18.0, out: 10.0
            +                        1012 group (session.mixers[0].devices[0].chains[0]:devices)
            +                        1015 supriya:channel-strip:2 (session.mixers[0].devices[0].chains[0]:channel-strip)
            +                            active: c8, done_action: 2.0, gain: c9, gate: 1.0, out: 18.0
            +                        1017 supriya:patch-cable:2x2 (session.mixers[0].devices[0].chains[0]:output)
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            +                        1016 supriya:meters:2 (session.mixers[0].devices[0].chains[0]:output-levels)
            +                            in_: 18.0, out: 12.0
            +                1009 supriya:patch-cable:2x2:replace (session.mixers[0].devices[0]:output)
            +                    active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
            +                1010 supriya:meters:2 (session.mixers[0].devices[0]:output-levels)
            +                    in_: 16.0, out: 6.0
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
            +                <Chain 3 'Chain 1'>
            +                <Chain 4 'Chain 2'>
            """,
            expected_messages="""
            - ['/d_recv', <SynthDef: supriya:patch-cable:2x2:mix>]
            - ['/d_recv', <SynthDef: supriya:patch-cable:2x2:replace>]
            - ['/sync', 3]
            - [None, [['/c_set', 5, 1.0], ['/c_fill', 6, 2, 0.0]]]
            - [None, [['/c_set', 8, 1.0, 9, 0.0], ['/c_fill', 10, 2, 0.0, 12, 2, 0.0]]]
            - [None, [['/c_set', 14, 1.0, 15, 0.0], ['/c_fill', 16, 2, 0.0, 18, 2, 0.0]]]
            - [None,
               [['/g_new', 1007, 0, 1002, 1008, 0, 1007],
                ['/s_new', 'supriya:patch-cable:2x2:mix', 1009, 3, 1008, 'in_', 20.0, 'mix', 'c5', 'out', 16.0],
                ['/s_new', 'supriya:meters:2', 1010, 1, 1007, 'in_', 16.0, 'out', 6.0]]]
            - [None,
               [['/g_new', 1011, 0, 1008, 1012, 1, 1011],
                ['/s_new', 'supriya:patch-cable:2x2:replace', 1013, 0, 1011, 'in_', 16.0, 'out', 18.0],
                ['/s_new', 'supriya:meters:2', 1014, 3, 1013, 'in_', 18.0, 'out', 10.0],
                ['/s_new', 'supriya:channel-strip:2', 1015, 3, 1012, 'active', 'c8', 'gain', 'c9', 'out', 18.0],
                ['/s_new', 'supriya:meters:2', 1016, 3, 1015, 'in_', 18.0, 'out', 12.0],
                ['/s_new', 'supriya:patch-cable:2x2', 1017, 3, 1015, 'in_', 18.0, 'out', 20.0]]]
            - [None,
               [['/g_new', 1018, 3, 1011, 1019, 1, 1018],
                ['/s_new', 'supriya:patch-cable:2x2:replace', 1020, 0, 1018, 'in_', 16.0, 'out', 18.0],
                ['/s_new', 'supriya:meters:2', 1021, 3, 1020, 'in_', 18.0, 'out', 16.0],
                ['/s_new', 'supriya:channel-strip:2', 1022, 3, 1019, 'active', 'c14', 'gain', 'c15', 'out', 18.0],
                ['/s_new', 'supriya:meters:2', 1023, 3, 1022, 'in_', 18.0, 'out', 18.0],
                ['/s_new', 'supriya:patch-cable:2x2', 1024, 3, 1022, 'in_', 18.0, 'out', 20.0]]]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -4,6 +4,36 @@
                     1004 supriya:meters:2 (session.mixers[0]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (session.mixers[0]:devices)
            +            1007 group (session.mixers[0].devices[0]:group)
            +                1008 group (session.mixers[0].devices[0]:chains)
            +                    1011 group (session.mixers[0].devices[0].chains[0]:group)
            +                        1013 supriya:patch-cable:2x2:replace (session.mixers[0].devices[0].chains[0]:input)
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 18.0
            +                        1014 supriya:meters:2 (session.mixers[0].devices[0].chains[0]:input-levels)
            +                            in_: 18.0, out: 10.0
            +                        1012 group (session.mixers[0].devices[0].chains[0]:devices)
            +                        1015 supriya:channel-strip:2 (session.mixers[0].devices[0].chains[0]:channel-strip)
            +                            active: c8, done_action: 2.0, gain: c9, gate: 1.0, out: 18.0
            +                        1017 supriya:patch-cable:2x2 (session.mixers[0].devices[0].chains[0]:output)
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            +                        1016 supriya:meters:2 (session.mixers[0].devices[0].chains[0]:output-levels)
            +                            in_: 18.0, out: 12.0
            +                    1018 group (session.mixers[0].devices[0].chains[1]:group)
            +                        1020 supriya:patch-cable:2x2:replace (session.mixers[0].devices[0].chains[1]:input)
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 18.0
            +                        1021 supriya:meters:2 (session.mixers[0].devices[0].chains[1]:input-levels)
            +                            in_: 18.0, out: 16.0
            +                        1019 group (session.mixers[0].devices[0].chains[1]:devices)
            +                        1022 supriya:channel-strip:2 (session.mixers[0].devices[0].chains[1]:channel-strip)
            +                            active: c14, done_action: 2.0, gain: c15, gate: 1.0, out: 18.0
            +                        1024 supriya:patch-cable:2x2 (session.mixers[0].devices[0].chains[1]:output)
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            +                        1023 supriya:meters:2 (session.mixers[0].devices[0].chains[1]:output-levels)
            +                            in_: 18.0, out: 18.0
            +                1009 supriya:patch-cable:2x2:mix (session.mixers[0].devices[0]:output)
            +                    active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, mix: c5, out: 16.0
            +                1010 supriya:meters:2 (session.mixers[0].devices[0]:output-levels)
            +                    in_: 16.0, out: 6.0
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
