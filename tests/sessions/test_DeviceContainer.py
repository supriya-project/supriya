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
from supriya.typing import DEFAULT
from supriya.ugens import In, ReplaceOut, SynthDefBuilder

from .conftest import run_test


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


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    (
        "commands, target, parameter_configs, sidechain_configs, synth_configs, "
        "expected_components_diff, expected_tree_diff, expected_messages"
    ),
    [
        # effect with one synth, no parameter specs
        (
            [(None, "add_mixer", {"name": "Mixer"})],
            "mixers[0]",
            None,
            None,
            [
                SynthConfig(synthdef=build_effect_synthdef),
            ],
            lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,3 +1,4 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
            +            <Device 2 'Device'>
            """,
            """
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
            """
            - ['/d_recv', <SynthDef: test:effect:2>]
            - ['/sync', 3]
            - [None, [['/g_new', 1007, 0, 1002], ['/s_new', 'test:effect:2', 1008, 1, 1007, 'bus', 16.0]]]
            """,
        ),
        # effect with one synth, two parameter specs
        (
            [(None, "add_mixer", {"name": "Mixer"})],
            "mixers[0]",
            [
                ParameterConfig(
                    name="mult", field=FloatField(default=0.5, has_bus=True)
                ),
                ParameterConfig(
                    name="add", field=FloatField(default=0.25, has_bus=True)
                ),
            ],
            None,
            [
                SynthConfig(
                    synthdef=build_effect_synthdef,
                    parameters={
                        "multiplier": (CalculationRate.CONTROL, "mult"),
                        "offset": (CalculationRate.CONTROL, "add"),
                    },
                ),
            ],
            lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,3 +1,4 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
            +            <Device 2 'Device'>
            """,
            """
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
            """
            - ['/d_recv', <SynthDef: test:effect:2>]
            - ['/sync', 3]
            - ['/c_set', 5, 0.25, 6, 0.5]
            - [None,
               [['/g_new', 1007, 0, 1002],
                ['/s_new', 'test:effect:2', 1008, 1, 1007, 'bus', 16.0, 'multiplier', 'c6', 'offset', 'c5']]]
            """,
        ),
        # effect with one synth, one default-channeled sidechain
        (
            [(None, "add_mixer", {"name": "Mixer"})],
            "mixers[0]",
            [],
            [SidechainConfig(name=Names.SIDECHAIN, channel_count=DEFAULT)],
            [
                SynthConfig(
                    synthdef=build_sidechain_synthdef,
                    parameters={
                        "sidechain_bus": (CalculationRate.AUDIO, Names.SIDECHAIN),
                    },
                ),
            ],
            lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,3 +1,4 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
            +            <Device 2 'Device'>
            """,
            """
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
            """
            - ['/d_recv', <SynthDef: test:sidechain:2>]
            - ['/sync', 3]
            - [None, [['/g_new', 1007, 0, 1002], ['/s_new', 'test:sidechain:2', 1008, 1, 1007, 'bus', 16.0, 'sidechain_bus', 18.0]]]
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_DeviceContainer_add_device(
    commands: list[tuple[str | None, str, dict | None]],
    expected_components_diff: Callable[[Session], str] | str,
    expected_messages: str,
    expected_tree_diff: str,
    online: bool,
    parameter_configs: list[ParameterConfig] | None,
    sidechain_configs: list[SidechainConfig] | None,
    synth_configs: list[SynthConfig],
    target: str,
) -> None:
    async with run_test(
        commands=commands,
        expected_components_diff=expected_components_diff,
        expected_messages=expected_messages,
        expected_tree_diff=expected_tree_diff,
        online=online,
    ) as session:
        target_ = session[target]
        assert isinstance(target_, DeviceContainer)
        device = await target_.add_device(
            name="Device",
            parameter_configs=parameter_configs,
            sidechain_configs=sidechain_configs,
            synth_configs=synth_configs,
        )
    assert isinstance(device, Device)
    assert device in target_.devices
    assert device.parent is target_
    assert target_.devices[0] is device


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "commands, target, expected_components_diff, expected_tree_diff, expected_messages",
    [
        (
            [
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Track"}),
            ],
            "mixers[0]",
            """
            --- initial
            +++ mutation
            @@ -2,3 +2,5 @@
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
                         <Track 2 'Track'>
            +            <Rack 3 'Rack'>
            +                <Chain 4>
            """,
            """
            --- initial
            +++ mutation
            @@ -15,6 +15,12 @@
                     1004 supriya:meters:2 (session.mixers[0]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (session.mixers[0]:devices)
            +            1014 group (session.mixers[0].devices[0]:group)
            +                1015 group (session.mixers[0].devices[0]:chains)
            +                    1016 group (session.mixers[0].devices[0].chains[0]:group)
            +                        1017 group (session.mixers[0].devices[0].chains[0]:devices)
            +                        1018 supriya:channel-strip:2 (session.mixers[0].devices[0].chains[0]:channel-strip)
            +                            active: c11, done_action: 2.0, gain: c12, gate: 1.0, out: 22.0
                     1003 supriya:channel-strip:2 (session.mixers[0]:channel-strip)
                         active: 1.0, done_action: 2.0, gain: c0, gate: 1.0, out: 16.0
                     1005 supriya:meters:2 (session.mixers[0]:output-levels)
            """,
            """
            - [None, [['/c_set', 11, 1.0, 12, 0.0], ['/c_fill', 13, 2, 0.0, 15, 2, 0.0]]]
            - ['/g_new', 1014, 0, 1002, 1015, 0, 1014]
            - [None,
               [['/g_new', 1016, 0, 1015, 1017, 1, 1016],
                ['/s_new', 'supriya:channel-strip:2', 1018, 1, 1016, 'active', 'c11', 'gain', 'c12', 'out', 22.0]]]
            """,
        )
    ],
)
@pytest.mark.asyncio
async def test_DeviceContainer_add_rack(
    commands: list[tuple[str | None, str, dict | None]],
    expected_components_diff: Callable[[Session], str] | str,
    expected_messages: str,
    expected_tree_diff: str,
    online: bool,
    target: str,
) -> None:
    async with run_test(
        commands=commands,
        expected_components_diff=expected_components_diff,
        expected_messages=expected_messages,
        expected_tree_diff=expected_tree_diff,
        online=online,
    ) as session:
        target_ = session[target]
        assert isinstance(target_, DeviceContainer)
        rack = await target_.add_rack(
            name="Rack",
        )
    assert isinstance(rack, Rack)
    assert rack in target_.devices
    assert rack.parent is target_
    assert target_.devices[0] is rack
