import dataclasses
from typing import Callable

import pytest

from supriya import CalculationRate, SynthDef
from supriya.sessions import (
    ChannelCount,
    Device,
    DeviceContainer,
    FloatField,
    Names,
    ParameterConfig,
    Rack,
    Session,
    SidechainConfig,
    SynthConfig,
)
from supriya.typing import INHERIT
from supriya.ugens import In, ReplaceOut, SynthDefBuilder

from .conftest import Scenario, run_test


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
            target="mixers[0]",
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
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -4,6 +4,9 @@
                     1004 supriya:meters:2 (session.mixers[0]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (session.mixers[0]:devices)
            +            1007 group (session.mixers[0].devices[0]:group)
            +                1008 test:effect:2 (session.mixers[0].devices[0]:synth-0)
            +                    bus: 16.0, multiplier: 1.0, offset: 0.0
                     1003 supriya:channel-strip:2 (session.mixers[0]:channel-strip)
                         active: 1.0, done_action: 2.0, gain: c0, gate: 1.0, out: 16.0
                     1005 supriya:meters:2 (session.mixers[0]:output-levels)
            """,
            expected_messages="""
            - ['/d_recv', <SynthDef: test:effect:2>]
            - ['/sync', 3]
            - [None, [['/g_new', 1007, 0, 1002], ['/s_new', 'test:effect:2', 1008, 1, 1007, 'bus', 16.0]]]
            """,
        ),
        # effect with one synth, two parameter specs
        AddDeviceScenario(
            commands=[(None, "add_mixer", {"name": "Mixer"})],
            target="mixers[0]",
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
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -4,6 +4,9 @@
                     1004 supriya:meters:2 (session.mixers[0]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (session.mixers[0]:devices)
            +            1007 group (session.mixers[0].devices[0]:group)
            +                1008 test:effect:2 (session.mixers[0].devices[0]:synth-0)
            +                    bus: 16.0, multiplier: c6, offset: c5
                     1003 supriya:channel-strip:2 (session.mixers[0]:channel-strip)
                         active: 1.0, done_action: 2.0, gain: c0, gate: 1.0, out: 16.0
                     1005 supriya:meters:2 (session.mixers[0]:output-levels)
            """,
            expected_messages="""
            - ['/d_recv', <SynthDef: test:effect:2>]
            - ['/sync', 3]
            - ['/c_set', 5, 0.25, 6, 0.5]
            - [None,
               [['/g_new', 1007, 0, 1002],
                ['/s_new', 'test:effect:2', 1008, 1, 1007, 'bus', 16.0, 'multiplier', 'c6', 'offset', 'c5']]]
            """,
        ),
        # effect with one synth, one default-channeled sidechain
        AddDeviceScenario(
            commands=[(None, "add_mixer", {"name": "Mixer"})],
            target="mixers[0]",
            parameter_configs=[],
            sidechain_configs=[SidechainConfig(name=Names.SIDECHAIN, channel_count=INHERIT)],
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
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -4,6 +4,9 @@
                     1004 supriya:meters:2 (session.mixers[0]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (session.mixers[0]:devices)
            +            1007 group (session.mixers[0].devices[0]:group)
            +                1008 test:sidechain:2 (session.mixers[0].devices[0]:synth-0)
            +                    bus: 16.0, multiplier: 1.0, offset: 0.0, sidechain_bus: 18.0
                     1003 supriya:channel-strip:2 (session.mixers[0]:channel-strip)
                         active: 1.0, done_action: 2.0, gain: c0, gate: 1.0, out: 16.0
                     1005 supriya:meters:2 (session.mixers[0]:output-levels)
            """,
            expected_messages="""
            - ['/d_recv', <SynthDef: test:sidechain:2>]
            - ['/sync', 3]
            - [None, [['/g_new', 1007, 0, 1002], ['/s_new', 'test:sidechain:2', 1008, 1, 1007, 'bus', 16.0, 'sidechain_bus', 18.0]]]
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_DeviceContainer_add_device(
    scenario: AddDeviceScenario,
    online: bool,
) -> None:
    async with run_test(
        commands=scenario.commands,
        expected_components_diff=scenario.expected_components_diff,
        expected_messages=scenario.expected_messages,
        expected_tree_diff=scenario.expected_tree_diff,
        online=online,
    ) as session:
        target = session[scenario.target]
        assert isinstance(target, DeviceContainer)
        device = await target.add_device(
            name="Device",
            parameter_configs=scenario.parameter_configs,
            sidechain_configs=scenario.sidechain_configs,
            synth_configs=scenario.synth_configs,
        )
    assert isinstance(device, Device)
    assert device in target.devices
    assert device.parent is target
    assert target.devices[0] is device


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "scenario",
    # "commands, target, expected_components_diff, expected_tree_diff, expected_messages",
    [
        Scenario(
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Track"}),
            ],
            target="mixers[0]",
            expected_components_diff="""
            --- initial
            +++ mutation
            @@ -2,3 +2,5 @@
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
                         <Track 2 'Track'>
            +            <Rack 3 'Rack'>
            +                <Chain 4>
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -15,6 +15,16 @@
                     1004 supriya:meters:2 (session.mixers[0]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (session.mixers[0]:devices)
            +            1014 group (session.mixers[0].devices[0]:group)
            +                1016 supriya:patch-cable:2x2:replace (session.mixers[0].devices[0]:input)
            +                    active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 20.0
            +                1015 group (session.mixers[0].devices[0]:chains)
            +                    1018 group (session.mixers[0].devices[0].chains[0]:group)
            +                        1019 group (session.mixers[0].devices[0].chains[0]:devices)
            +                        1020 supriya:channel-strip:2 (session.mixers[0].devices[0].chains[0]:channel-strip)
            +                            active: c12, done_action: 2.0, gain: c13, gate: 1.0, out: 20.0
            +                1017 supriya:patch-cable:2x2 (session.mixers[0].devices[0]:output)
            +                    active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
                     1003 supriya:channel-strip:2 (session.mixers[0]:channel-strip)
                         active: 1.0, done_action: 2.0, gain: c0, gate: 1.0, out: 16.0
                     1005 supriya:meters:2 (session.mixers[0]:output-levels)
            """,
            expected_messages="""
            - ['/d_recv', <SynthDef: supriya:patch-cable:2x2:replace>]
            - ['/sync', 3]
            - ['/c_set', 11, 1.0]
            - [None, [['/c_set', 12, 1.0, 13, 0.0], ['/c_fill', 14, 2, 0.0, 16, 2, 0.0]]]
            - [None,
               [['/g_new', 1014, 0, 1002, 1015, 0, 1014],
                ['/s_new', 'supriya:patch-cable:2x2:replace', 1016, 2, 1015, 'in_', 16.0, 'out', 20.0],
                ['/s_new', 'supriya:patch-cable:2x2', 1017, 3, 1015, 'in_', 20.0, 'out', 16.0]]]
            - [None,
               [['/g_new', 1018, 0, 1015, 1019, 1, 1018],
                ['/s_new', 'supriya:channel-strip:2', 1020, 1, 1018, 'active', 'c12', 'gain', 'c13', 'out', 20.0]]]
            """,
        )
    ],
)
@pytest.mark.asyncio
async def test_DeviceContainer_add_rack(
    scenario: Scenario,
    online: bool,
) -> None:
    async with run_test(
        commands=scenario.commands,
        expected_components_diff=scenario.expected_components_diff,
        expected_messages=scenario.expected_messages,
        expected_tree_diff=scenario.expected_tree_diff,
        online=online,
    ) as session:
        target = session[scenario.target]
        assert isinstance(target, DeviceContainer)
        rack = await target.add_rack(
            name="Rack",
        )
    assert isinstance(rack, Rack)
    assert rack in target.devices
    assert rack.parent is target
    assert target.devices[0] is rack
