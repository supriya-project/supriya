import dataclasses
from typing import Any, Literal

import pytest

from supriya.sessions import Chain, ChannelCount, PatchMode, Rack, Session, SynthConfig
from supriya.typing import Inherit
from supriya.ugens.system import build_dc_synthdef

from .conftest import Scenario, does_not_raise


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "scenario",
    [
        Scenario(
            id="add chain to rack w/ 1 chain",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_rack", {"name": "Self"}),
            ],
            subject="mixers[0].devices[0]",
            expected_components_diff=lambda session: """
            --- initial
            +++ mutation
            @@ -3,3 +3,4 @@
                     <Mixer 1 'Mixer'>
                         <Rack 2 'Self'>
                             <Chain 3 'Chain 1'>
            +                <Chain 4 'Chain 2'>
            """,
            expected_messages="""
            - [None, [['/c_set', 14, 1.0, 15, 0.0], ['/c_fill', 16, 2, 0.0, 18, 2, 0.0]]]
            - [None,
               [['/g_new', 1018, 3, 1011, 1019, 1, 1018],
                ['/s_new', 'supriya:patch-cable:2x2:replace', 1020, 2, 1019, 'in_', 16.0, 'out', 18.0],
                ['/s_new', 'supriya:meters:2', 1021, 3, 1020, 'in_', 18.0, 'out', 16.0],
                ['/s_new', 'supriya:channel-strip:2', 1022, 3, 1019, 'active', 'c14', 'gain', 'c15', 'out', 18.0],
                ['/s_new', 'supriya:meters:2', 1023, 3, 1022, 'in_', 18.0, 'out', 18.0],
                ['/s_new', 'supriya:patch-cable:2x2', 1024, 3, 1022, 'in_', 18.0, 'out', 20.0]]]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -18,6 +18,18 @@
                                         active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
                                     1016 supriya:meters:2 (session.mixers[0].devices[0].chains[0]:output-levels)
                                         in_: 18.0, out: 12.0
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
                             1009 supriya:patch-cable:2x2 (session.mixers[0].devices[0]:output)
                                 active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
                             1010 supriya:meters:2 (session.mixers[0].devices[0]:output-levels)
            """,
        ),
        Scenario(
            id="add chain to rack w/ 0 chains",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_rack", {"name": "Self"}),
                ("mixers[0].devices[0].chains[0]", "delete", {}),
            ],
            subject="mixers[0].devices[0]",
            expected_components_diff=lambda session: """
            --- initial
            +++ mutation
            @@ -2,3 +2,4 @@
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
                         <Rack 2 'Self'>
            +                <Chain 4 'Chain 1'>
            """,
            expected_messages="""
            - ['/d_recv', <SynthDef: supriya:patch-cable:2x2:replace>]
            - ['/sync', 3]
            - [None, [['/c_set', 8, 1.0, 9, 0.0], ['/c_fill', 10, 2, 0.0, 12, 2, 0.0]]]
            - [None,
               [['/g_new', 1011, 0, 1008, 1012, 1, 1011],
                ['/s_new', 'supriya:patch-cable:2x2:replace', 1013, 2, 1012, 'in_', 16.0, 'out', 18.0],
                ['/s_new', 'supriya:meters:2', 1014, 3, 1013, 'in_', 18.0, 'out', 10.0],
                ['/s_new', 'supriya:channel-strip:2', 1015, 3, 1012, 'active', 'c8', 'gain', 'c9', 'out', 18.0],
                ['/s_new', 'supriya:meters:2', 1016, 3, 1015, 'in_', 18.0, 'out', 12.0],
                ['/s_new', 'supriya:patch-cable:2x2', 1017, 3, 1015, 'in_', 18.0, 'out', 20.0]]]
            - ['/n_set', 1009, 'active', 1.0]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -6,8 +6,20 @@
                     1002 group (session.mixers[0]:devices)
                         1007 group (session.mixers[0].devices[0]:group)
                             1008 group (session.mixers[0].devices[0]:chains)
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
                             1009 supriya:patch-cable:2x2 (session.mixers[0].devices[0]:output)
            -                    active: 0.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
            +                    active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
                             1010 supriya:meters:2 (session.mixers[0].devices[0]:output-levels)
                                 in_: 16.0, out: 6.0
                     1003 supriya:channel-strip:2 (session.mixers[0]:channel-strip)
            """,
        ),
    ],
    ids=lambda scenario: scenario.id,
)
@pytest.mark.asyncio
async def test_Rack_add_chain(scenario: Scenario, online: bool) -> None:
    async with scenario.run(online=online) as session:
        subject = session[scenario.subject]
        assert isinstance(subject, Rack)
        chain = await subject.add_chain()
    assert isinstance(chain, Chain)
    assert chain in subject.chains
    assert chain.parent is subject
    assert subject.chains[-1] is chain


@dataclasses.dataclass(frozen=True)
class SetChannelCountScenario(Scenario):
    channel_count: ChannelCount | Inherit
    maybe_raises: Any


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "scenario",
    [
        SetChannelCountScenario(
            id="rack -> 4",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_rack", {"name": "Self"}),
                (
                    "mixers[0].devices[0].chains[0]",
                    "add_device",
                    {"synth_configs": [SynthConfig(synthdef=build_dc_synthdef)]},
                ),
            ],
            subject="mixers[0].devices[0]",
            channel_count=4,
            maybe_raises=does_not_raise,
            expected_messages="""
            - ['/d_recv', <SynthDef: supriya:channel-strip:4>]
            - ['/d_recv', <SynthDef: supriya:dc:4>]
            - ['/d_recv', <SynthDef: supriya:meters:4>]
            - ['/d_recv', <SynthDef: supriya:patch-cable:2x4>]
            - ['/d_recv', <SynthDef: supriya:patch-cable:2x4:replace>]
            - ['/d_recv', <SynthDef: supriya:patch-cable:4x4>]
            - ['/sync', 3]
            - ['/c_fill', 16, 4, 0.0]
            - ['/c_fill', 20, 4, 0.0, 24, 4, 0.0]
            - ['/c_fill', 28, 4, 0.0]
            - ['/s_new', 'supriya:patch-cable:2x4', 1021, 3, 1008, 'in_', 26.0, 'out', 16.0]
            - [None,
               [['/s_new', 'supriya:patch-cable:2x4:replace', 1022, 2, 1012, 'in_', 16.0, 'out', 22.0],
                ['/s_new', 'supriya:meters:4', 1023, 3, 1022, 'in_', 22.0, 'out', 20.0],
                ['/s_new', 'supriya:channel-strip:4', 1024, 3, 1012, 'active', 'c8', 'gain', 'c9', 'out', 22.0],
                ['/s_new', 'supriya:meters:4', 1025, 3, 1024, 'in_', 22.0, 'out', 24.0],
                ['/s_new', 'supriya:patch-cable:4x4', 1026, 3, 1024, 'in_', 22.0, 'out', 26.0]]]
            - [None,
               [['/s_new', 'supriya:dc:4', 1027, 1, 1018, 'out', 22.0],
                ['/s_new', 'supriya:meters:4', 1028, 3, 1027, 'in_', 22.0, 'out', 28.0]]]
            - ['/n_set', 1009, 'done_action', 2.0, 'gate', 0.0]
            - [None,
               [['/n_set', 1013, 'done_action', 2.0, 'gate', 0.0],
                ['/n_free', 1014],
                ['/n_set', 1015, 'done_action', 2.0, 'gate', 0.0],
                ['/n_free', 1016],
                ['/n_set', 1017, 'done_action', 2.0, 'gate', 0.0]]]
            - [None, [['/n_set', 1019, 'done_action', 2.0, 'gate', 0.0], ['/n_free', 1020]]]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -8,23 +8,33 @@
                             1008 group (session.mixers[0].devices[0]:chains)
                                 1011 group (session.mixers[0].devices[0].chains[0]:group)
                                     1013 supriya:patch-cable:2x2:replace (session.mixers[0].devices[0].chains[0]:input)
            -                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 18.0
            -                        1014 supriya:meters:2 (session.mixers[0].devices[0].chains[0]:input-levels)
            -                            in_: 18.0, out: 10.0
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 16.0, out: 18.0
            +                        1022 supriya:patch-cable:2x4:replace (session.mixers[0].devices[0].chains[0]:input)
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 22.0
            +                        1023 supriya:meters:4 (session.mixers[0].devices[0].chains[0]:input-levels)
            +                            in_: 22.0, out: 20.0
                                     1012 group (session.mixers[0].devices[0].chains[0]:devices)
                                         1018 group (session.mixers[0].devices[0].chains[0].devices[0]:group)
                                             1019 supriya:dc:2 (session.mixers[0].devices[0].chains[0].devices[0]:synth-0)
            -                                    out: 18.0, active: 1.0, dc: 1.0, done_action: 2.0, gate: 1.0
            -                                1020 supriya:meters:2 (session.mixers[0].devices[0].chains[0].devices[0]:output-levels)
            -                                    in_: 18.0, out: 14.0
            +                                    out: 18.0, active: 1.0, dc: 1.0, done_action: 2.0, gate: 0.0
            +                                1027 supriya:dc:4 (session.mixers[0].devices[0].chains[0].devices[0]:synth-0)
            +                                    out: 22.0, active: 1.0, dc: 1.0, done_action: 2.0, gate: 1.0
            +                                1028 supriya:meters:4 (session.mixers[0].devices[0].chains[0].devices[0]:output-levels)
            +                                    in_: 22.0, out: 28.0
            +                        1024 supriya:channel-strip:4 (session.mixers[0].devices[0].chains[0]:channel-strip)
            +                            active: c8, done_action: 2.0, gain: c9, gate: 1.0, out: 22.0
            +                        1026 supriya:patch-cable:4x4 (session.mixers[0].devices[0].chains[0]:output)
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 26.0
            +                        1025 supriya:meters:4 (session.mixers[0].devices[0].chains[0]:output-levels)
            +                            in_: 22.0, out: 24.0
                                     1015 supriya:channel-strip:2 (session.mixers[0].devices[0].chains[0]:channel-strip)
            -                            active: c8, done_action: 2.0, gain: c9, gate: 1.0, out: 18.0
            +                            active: c8, done_action: 2.0, gain: c9, gate: 0.0, out: 18.0
                                     1017 supriya:patch-cable:2x2 (session.mixers[0].devices[0].chains[0]:output)
            -                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            -                        1016 supriya:meters:2 (session.mixers[0].devices[0].chains[0]:output-levels)
            -                            in_: 18.0, out: 12.0
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 20.0
            +                1021 supriya:patch-cable:2x4 (session.mixers[0].devices[0]:output)
            +                    active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 26.0, out: 16.0
                             1009 supriya:patch-cable:2x2 (session.mixers[0].devices[0]:output)
            -                    active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
            +                    active: 1.0, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 16.0
                             1010 supriya:meters:2 (session.mixers[0].devices[0]:output-levels)
                                 in_: 16.0, out: 6.0
                     1003 supriya:channel-strip:2 (session.mixers[0]:channel-strip)
            """,
        ),
    ],
    ids=lambda scenario: scenario.id,
)
@pytest.mark.asyncio
async def test_Rack_set_channel_count(
    scenario: SetChannelCountScenario, online: bool
) -> None:
    async with scenario.run(online=online) as session:
        subject = session[scenario.subject]
        assert isinstance(subject, Rack)
        with scenario.maybe_raises:
            await subject.set_channel_count(channel_count=scenario.channel_count)
    assert subject.channel_count == scenario.channel_count


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.asyncio
async def test_Rack_et_name(online: bool) -> None:
    session = Session()
    mixer = await session.add_mixer()
    rack = await mixer.add_rack()
    if online:
        await session.boot()
    assert rack.name is None
    for name in ("Foo", "Bar", "Baz"):
        rack.set_name(name=name)
        assert rack.name == name
    rack.set_name(name=None)
    assert rack.name is None


@dataclasses.dataclass(frozen=True)
class SetReadModeScenario(Scenario):
    mode: Literal[PatchMode.IGNORE, PatchMode.REPLACE]


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "scenario",
    [
        SetReadModeScenario(
            id="mode:replace, mode -> ignore",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_rack", {"name": "Self"}),
            ],
            subject="mixers[0].devices[0]",
            mode=PatchMode.IGNORE,
            expected_components_diff="",
            expected_messages="""
            - ['/d_recv', <SynthDef: supriya:zero:2>]
            - ['/sync', 3]
            - ['/s_new', 'supriya:zero:2', 1018, 2, 1012, 'out', 18.0]
            - [None, [['/n_set', 1013, 'done_action', 2.0, 'gate', 0.0], ['/n_free', 1014]]]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -8,9 +8,9 @@
                             1008 group (session.mixers[0].devices[0]:chains)
                                 1011 group (session.mixers[0].devices[0].chains[0]:group)
                                     1013 supriya:patch-cable:2x2:replace (session.mixers[0].devices[0].chains[0]:input)
            -                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 18.0
            -                        1014 supriya:meters:2 (session.mixers[0].devices[0].chains[0]:input-levels)
            -                            in_: 18.0, out: 10.0
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 16.0, out: 18.0
            +                        1018 supriya:zero:2 (session.mixers[0].devices[0].chains[0]:input)
            +                            out: 18.0
                                     1012 group (session.mixers[0].devices[0].chains[0]:devices)
                                     1015 supriya:channel-strip:2 (session.mixers[0].devices[0].chains[0]:channel-strip)
                                         active: c8, done_action: 2.0, gain: c9, gate: 1.0, out: 18.0
            """,
        ),
        SetReadModeScenario(
            id="mode:ignore, mode -> replace",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_rack", {"name": "Self"}),
                ("mixers[0].devices[0]", "set_read_mode", {"mode": PatchMode.IGNORE}),
            ],
            subject="mixers[0].devices[0]",
            mode=PatchMode.REPLACE,
            expected_components_diff="",
            expected_messages="""
            - ['/d_recv', <SynthDef: supriya:patch-cable:2x2:replace>]
            - ['/sync', 3]
            - ['/c_fill', 12, 2, 0.0]
            - [None,
               [['/s_new', 'supriya:patch-cable:2x2:replace', 1017, 2, 1012, 'in_', 16.0, 'out', 18.0],
                ['/s_new', 'supriya:meters:2', 1018, 3, 1017, 'in_', 18.0, 'out', 12.0]]]
            - ['/n_free', 1013]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -7,8 +7,10 @@
                         1007 group (session.mixers[0].devices[0]:group)
                             1008 group (session.mixers[0].devices[0]:chains)
                                 1011 group (session.mixers[0].devices[0].chains[0]:group)
            -                        1013 supriya:zero:2 (session.mixers[0].devices[0].chains[0]:input)
            -                            out: 18.0
            +                        1017 supriya:patch-cable:2x2:replace (session.mixers[0].devices[0].chains[0]:input)
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 18.0
            +                        1018 supriya:meters:2 (session.mixers[0].devices[0].chains[0]:input-levels)
            +                            in_: 18.0, out: 12.0
                                     1012 group (session.mixers[0].devices[0].chains[0]:devices)
                                     1014 supriya:channel-strip:2 (session.mixers[0].devices[0].chains[0]:channel-strip)
                                         active: c8, done_action: 2.0, gain: c9, gate: 1.0, out: 18.0
            """,
        ),
        SetReadModeScenario(
            id="mode:ignore, mode -> ignore, no-op",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_rack", {"name": "Self"}),
                ("mixers[0].devices[0]", "set_read_mode", {"mode": PatchMode.IGNORE}),
            ],
            subject="mixers[0].devices[0]",
            mode=PatchMode.IGNORE,
            expected_components_diff="",
            expected_tree_diff="",
            expected_messages="",
        ),
        SetReadModeScenario(
            id="mode:replace, mode -> replace, no-op",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_rack", {"name": "Self"}),
            ],
            subject="mixers[0].devices[0]",
            mode=PatchMode.REPLACE,
            expected_components_diff="",
            expected_tree_diff="",
            expected_messages="",
        ),
    ],
    ids=lambda scenario: scenario.id,
)
@pytest.mark.asyncio
async def test_Rack_set_read_mode(scenario: SetReadModeScenario, online: bool) -> None:
    async with scenario.run(online=online) as session:
        subject = session[scenario.subject]
        assert isinstance(subject, Rack)
        await subject.set_read_mode(mode=scenario.mode)
    assert subject.read_mode == scenario.mode


@dataclasses.dataclass(frozen=True)
class SetWriteModeScenario(Scenario):
    mode: PatchMode


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "scenario",
    [
        SetWriteModeScenario(
            id="mode:sum, mode -> replace",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_rack", {"name": "Self"}),
            ],
            subject="mixers[0].devices[0]",
            mode=PatchMode.IGNORE,
            expected_components_diff="",
            expected_messages="""
            - ['/d_recv', <SynthDef: supriya:patch-cable:2x2:mix>]
            - ['/sync', 3]
            - ['/s_new', 'supriya:patch-cable:2x2:mix', 1018, 3, 1008, 'active', 0.0, 'in_', 20.0, 'out', 16.0]
            - ['/n_set', 1009, 'done_action', 2.0, 'gate', 0.0]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -18,8 +18,10 @@
                                         active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
                                     1016 supriya:meters:2 (session.mixers[0].devices[0].chains[0]:output-levels)
                                         in_: 18.0, out: 12.0
            +                1018 supriya:patch-cable:2x2:mix (session.mixers[0].devices[0]:output)
            +                    active: 0.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, mix: 0.0, out: 16.0
                             1009 supriya:patch-cable:2x2 (session.mixers[0].devices[0]:output)
            -                    active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
            +                    active: 1.0, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 16.0
                             1010 supriya:meters:2 (session.mixers[0].devices[0]:output-levels)
                                 in_: 16.0, out: 6.0
                     1003 supriya:channel-strip:2 (session.mixers[0]:channel-strip)
            """,
        ),
        SetWriteModeScenario(
            id="mode:sum, mode -> mix",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_rack", {"name": "Self"}),
            ],
            subject="mixers[0].devices[0]",
            mode=PatchMode.MIX,
            expected_components_diff="",
            expected_messages="""
            - ['/d_recv', <SynthDef: supriya:patch-cable:2x2:mix>]
            - ['/sync', 3]
            - ['/s_new', 'supriya:patch-cable:2x2:mix', 1018, 3, 1008, 'in_', 20.0, 'mix', 'c5', 'out', 16.0]
            - ['/n_set', 1009, 'done_action', 2.0, 'gate', 0.0]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -18,8 +18,10 @@
                                         active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
                                     1016 supriya:meters:2 (session.mixers[0].devices[0].chains[0]:output-levels)
                                         in_: 18.0, out: 12.0
            +                1018 supriya:patch-cable:2x2:mix (session.mixers[0].devices[0]:output)
            +                    active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, mix: c5, out: 16.0
                             1009 supriya:patch-cable:2x2 (session.mixers[0].devices[0]:output)
            -                    active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
            +                    active: 1.0, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 16.0
                             1010 supriya:meters:2 (session.mixers[0].devices[0]:output-levels)
                                 in_: 16.0, out: 6.0
                     1003 supriya:channel-strip:2 (session.mixers[0]:channel-strip)
            """,
        ),
        SetWriteModeScenario(
            id="mode:sum, mode -> replace",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_rack", {"name": "Self"}),
            ],
            subject="mixers[0].devices[0]",
            mode=PatchMode.REPLACE,
            expected_components_diff="",
            expected_messages="""
            - ['/s_new', 'supriya:patch-cable:2x2:replace', 1018, 3, 1008, 'in_', 20.0, 'out', 16.0]
            - ['/n_set', 1009, 'done_action', 2.0, 'gate', 0.0]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -18,8 +18,10 @@
                                         active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
                                     1016 supriya:meters:2 (session.mixers[0].devices[0].chains[0]:output-levels)
                                         in_: 18.0, out: 12.0
            +                1018 supriya:patch-cable:2x2:replace (session.mixers[0].devices[0]:output)
            +                    active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
                             1009 supriya:patch-cable:2x2 (session.mixers[0].devices[0]:output)
            -                    active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
            +                    active: 1.0, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 16.0
                             1010 supriya:meters:2 (session.mixers[0].devices[0]:output-levels)
                                 in_: 16.0, out: 6.0
                     1003 supriya:channel-strip:2 (session.mixers[0]:channel-strip)
            """,
        ),
    ],
    ids=lambda scenario: scenario.id,
)
@pytest.mark.asyncio
async def test_Rack_set_write_mode(
    scenario: SetWriteModeScenario, online: bool
) -> None:
    async with scenario.run(online=online) as session:
        subject = session[scenario.subject]
        assert isinstance(subject, Rack)
        await subject.set_write_mode(mode=scenario.mode)
    assert subject.write_mode == scenario.mode


@dataclasses.dataclass(frozen=True)
class UngroupScenario(Scenario):
    maybe_raises: Any


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "scenario",
    [
        UngroupScenario(
            id="0 chains",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_rack", {"name": "Self"}),
                ("mixers[0].devices[0].chains[0]", "delete", {}),
            ],
            subject="mixers[0].devices[0]",
            maybe_raises=does_not_raise,
            expected_components_diff=lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,4 +1,3 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
            -            <Rack 2 'Self'>
            """,
            expected_messages="""
            - [None, [['/n_set', 1007, 'gate', 0.0], ['/n_set', 1009, 'done_action', 14.0]]]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -7,7 +7,7 @@
                         1007 group (devices[2]:group)
                             1008 group (devices[2]:chains)
                             1009 supriya:patch-cable:2x2 (devices[2]:output)
            -                    active: 0.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
            +                    active: 0.0, done_action: 14.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 16.0
                             1010 supriya:meters:2 (devices[2]:output-levels)
                                 in_: 16.0, out: 6.0
                     1003 supriya:channel-strip:2 (mixers[1]:channel-strip)
            """,
        ),
        UngroupScenario(
            id="1 chain",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_rack", {"name": "Self"}),
                (
                    "mixers[0].devices[0].chains[0]",
                    "add_device",
                    {"synth_configs": [SynthConfig(synthdef=build_dc_synthdef)]},
                ),
            ],
            subject="mixers[0].devices[0]",
            maybe_raises=does_not_raise,
            expected_components_diff=lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,6 +1,4 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
            -            <Rack 2 'Self'>
            -                <Chain 3 'Chain 1'>
            -                    <Device 4>
            +            <Device 4>
            """,
            expected_messages="""
            - [None,
               [['/s_new', 'supriya:dc:2', 1021, 1, 1018, 'out', 16.0],
                ['/s_new', 'supriya:meters:2', 1022, 3, 1021, 'in_', 16.0, 'out', 14.0]]]
            - ['/n_after', 1018, 1007]
            - [None, [['/n_set', 1007, 'gate', 0.0], ['/n_set', 1009, 'done_action', 14.0]]]
            - [None, [['/n_set', 1019, 'done_action', 2.0, 'gate', 0.0], ['/n_free', 1020]]]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -8,25 +8,27 @@
                             1008 group (devices[2]:chains)
                                 1011 group (chains[3]:group)
                                     1013 supriya:patch-cable:2x2:replace (chains[3]:input)
            -                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 18.0
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 16.0, out: 18.0
                                     1014 supriya:meters:2 (chains[3]:input-levels)
                                         in_: 18.0, out: 10.0
                                     1012 group (chains[3]:devices)
            -                            1018 group (devices[4]:group)
            -                                1019 supriya:dc:2 (devices[4]:synth-0)
            -                                    out: 18.0, active: 1.0, dc: 1.0, done_action: 2.0, gate: 1.0
            -                                1020 supriya:meters:2 (devices[4]:output-levels)
            -                                    in_: 18.0, out: 14.0
                                     1015 supriya:channel-strip:2 (chains[3]:channel-strip)
            -                            active: c8, done_action: 2.0, gain: c9, gate: 1.0, out: 18.0
            +                            active: c8, done_action: 2.0, gain: c9, gate: 0.0, out: 18.0
                                     1017 supriya:patch-cable:2x2 (chains[3]:output)
            -                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 20.0
                                     1016 supriya:meters:2 (chains[3]:output-levels)
                                         in_: 18.0, out: 12.0
                             1009 supriya:patch-cable:2x2 (devices[2]:output)
            -                    active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
            +                    active: 1.0, done_action: 14.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 16.0
                             1010 supriya:meters:2 (devices[2]:output-levels)
                                 in_: 16.0, out: 6.0
            +            1018 group (devices[4]:group)
            +                1019 supriya:dc:2 (devices[4]:synth-0)
            +                    out: 18.0, active: 1.0, dc: 1.0, done_action: 2.0, gate: 0.0
            +                1021 supriya:dc:2 (devices[4]:synth-0)
            +                    out: 16.0, active: 1.0, dc: 1.0, done_action: 2.0, gate: 1.0
            +                1022 supriya:meters:2 (devices[4]:output-levels)
            +                    in_: 16.0, out: 14.0
                     1003 supriya:channel-strip:2 (mixers[1]:channel-strip)
                         active: 1.0, done_action: 2.0, gain: c0, gate: 1.0, out: 16.0
                     1005 supriya:meters:2 (mixers[1]:output-levels)
            """,
        ),
        UngroupScenario(
            id="2 chains: raises",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_rack", {"name": "Self"}),
                ("mixers[0].devices[0]", "add_chain", {}),
                (
                    "mixers[0].devices[0].chains[0]",
                    "add_device",
                    {"synth_configs": [SynthConfig(synthdef=build_dc_synthdef)]},
                ),
                (
                    "mixers[0].devices[0].chains[1]",
                    "add_device",
                    {"synth_configs": [SynthConfig(synthdef=build_dc_synthdef)]},
                ),
            ],
            subject="mixers[0].devices[0]",
            maybe_raises=pytest.raises(RuntimeError),
            expected_components_diff=lambda session: "",
            expected_messages="",
            expected_tree_diff="",
        ),
    ],
    ids=lambda scenario: scenario.id,
)
@pytest.mark.asyncio
async def test_Rack_ungroup(scenario: UngroupScenario, online: bool) -> None:
    async with scenario.run(annotation_style="numeric", online=online) as session:
        subject = session[scenario.subject]
        assert isinstance(subject, Rack)
        with scenario.maybe_raises:
            await subject.ungroup()
