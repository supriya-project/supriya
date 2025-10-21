import asyncio
import dataclasses
from typing import Any

import pytest

from supriya.sessions import ChannelCount, Component, Mixer, Session, SynthConfig, Track
from supriya.typing import Inherit
from supriya.ugens import system  # lookup system.LAG_TIME to support monkeypatching

from .conftest import Scenario, does_not_raise


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "scenario",
    [
        Scenario(
            commands=[
                (None, "add_mixer", {"name": "Mixer One"}),
                ("mixers[0]", "add_track", {"name": "Track"}),
                (None, "add_mixer", {"name": "Mixer Two"}),
            ],
            subject="mixers[0]",
            expected_components_diff=lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,5 +1,3 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
            -        <Mixer 1 'Mixer One'>
            -            <Track 2 'Track'>
                     <Mixer 3 'Mixer Two'>
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -1,26 +1,4 @@
             <session.contexts[0]>
            -    NODE TREE 1000 group
            -        1001 group
            -            1007 group
            -                1008 group
            -                1011 supriya:meters:2
            -                    in_: 18.0, out: 7.0
            -                1009 group
            -                1010 supriya:channel-strip:2
            -                    active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
            -                1012 supriya:meters:2
            -                    in_: 18.0, out: 9.0
            -                1013 supriya:patch-cable:2x2
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            -        1004 supriya:meters:2
            -            in_: 16.0, out: 1.0
            -        1002 group
            -        1003 supriya:channel-strip:2
            -            active: 1.0, done_action: 2.0, gain: c0, gate: 1.0, out: 16.0
            -        1005 supriya:meters:2
            -            in_: 16.0, out: 3.0
            -        1006 supriya:patch-cable:2x2
            -            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 0.0
                 NODE TREE 1014 group
                     1015 group
                     1018 supriya:meters:2
            """,
            expected_messages="""
            - [None, [['/n_set', 1000, 'gate', 0.0], ['/n_set', 1003, 'done_action', 14.0]]]
            """,
        ),
        Scenario(
            commands=[
                (None, "add_mixer", {"name": "Mixer One"}),
                ("mixers[0]", "add_track", {"name": "Track"}),
                (None, "add_mixer", {"name": "Mixer Two"}),
            ],
            subject="mixers[1]",
            expected_components_diff="""
            --- initial
            +++ mutation
            @@ -2,4 +2,3 @@
                 <session.contexts[0]>
                     <Mixer 1 'Mixer One'>
                         <Track 2 'Track'>
            -        <Mixer 3 'Mixer Two'>
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -21,14 +21,3 @@
                         in_: 16.0, out: 3.0
                     1006 supriya:patch-cable:2x2
                         active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 0.0
            -    NODE TREE 1014 group
            -        1015 group
            -        1018 supriya:meters:2
            -            in_: 20.0, out: 12.0
            -        1016 group
            -        1017 supriya:channel-strip:2
            -            active: 1.0, done_action: 2.0, gain: c11, gate: 1.0, out: 20.0
            -        1019 supriya:meters:2
            -            in_: 20.0, out: 14.0
            -        1020 supriya:patch-cable:2x2
            -            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 0.0
            """,
            expected_messages="""
            - [None, [['/n_set', 1014, 'gate', 0.0], ['/n_set', 1017, 'done_action', 14.0]]]
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_Mixer_delete(
    online: bool,
    scenario: Scenario,
) -> None:
    async with scenario.run(annotation=None, online=online) as session:
        subject = session[scenario.subject]
        assert isinstance(subject, Mixer)
        await subject.delete()
    # N.B. The diff looks like the mixer immediately disappeared, but it hasn't.
    #      Session.dump_tree() just queries each mixer's group node, and
    #      because the mixer doesn't exist from the session's perspective, it
    #      doesn't query that group anymore.  We do this to save horizontal
    #      space, but querying the underlying context directly would show the
    #      nodes are still there, although about to be released.
    assert subject not in session.mixers
    assert subject.address == "mixers[?]"
    assert subject.context is None
    assert subject.parent is None
    assert subject.session is None


@dataclasses.dataclass(frozen=True)
class GainScenario(Scenario):
    expected_levels: list[tuple[str, list[float], list[float]]]
    gain: float


@pytest.mark.parametrize(
    "scenario",
    [
        GainScenario(
            commands=[
                (None, "add_mixer", {"name": "Self"}),
                (
                    "mixers[0]",
                    "add_device",
                    {"synth_configs": [SynthConfig(synthdef=system.build_dc_synthdef)]},
                ),
            ],
            subject="mixers[0]",
            gain=-6,
            expected_levels=[("Self", [0.0, 0.0], [0.5, 0.5])],
        ),
    ],
)
@pytest.mark.asyncio
async def test_Mixer_gain(
    scenario: GainScenario,
) -> None:
    async with scenario.run(online=True) as session:
        subject = session[scenario.subject]
        assert isinstance(subject, Mixer)
        subject.parameters["gain"].set(scenario.gain)
    await asyncio.sleep(system.LAG_TIME * 2)
    actual_levels = [
        (
            component.name,
            [round(x, 2) for x in component.input_levels],
            [round(x, 2) for x in component.output_levels],
        )
        for component in session.walk(Component)
        if isinstance(component, (Mixer, Track))
    ]
    assert actual_levels == scenario.expected_levels


@dataclasses.dataclass(frozen=True)
class SetChannelCountScenario(Scenario):
    channel_count: ChannelCount | Inherit
    maybe_raises: Any


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "scenario",
    [
        # 0
        # mixer: set channel count to 2
        # - no-op
        SetChannelCountScenario(
            id="set mixer to 2ch",
            commands=[
                (None, "add_mixer", {"name": "Self"}),
                ("mixers[0]", "add_track", {"name": "Track"}),
            ],
            subject="mixers[0]",
            channel_count=2,
            maybe_raises=does_not_raise,
            expected_tree_diff="",
            expected_messages="",
        ),
        # 1
        # mixer: set channel count to 4
        # - mixer changes to 4
        # - track changes to 4
        SetChannelCountScenario(
            id="set mixer to 4ch",
            commands=[
                (None, "add_mixer", {"name": "Self"}),
                ("mixers[0]", "add_track", {"name": "Track"}),
            ],
            subject="mixers[0]",
            channel_count=4,
            maybe_raises=does_not_raise,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -3,21 +3,29 @@
                     1001 group (session.mixers[0]:tracks)
                         1007 group (session.mixers[0].tracks[0]:group)
                             1008 group (session.mixers[0].tracks[0]:tracks)
            -                1011 supriya:meters:2 (session.mixers[0].tracks[0]:input-levels)
            -                    in_: 18.0, out: 7.0
            +                1019 supriya:meters:4 (session.mixers[0].tracks[0]:input-levels)
            +                    in_: 24.0, out: 19.0
                             1009 group (session.mixers[0].tracks[0]:devices)
                             1010 supriya:channel-strip:2 (session.mixers[0].tracks[0]:channel-strip)
            -                    active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
            -                1012 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
            -                    in_: 18.0, out: 9.0
            +                    active: c5, done_action: 2.0, gain: c6, gate: 0.0, out: 18.0
                             1013 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:output)
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            -        1004 supriya:meters:2 (session.mixers[0]:input-levels)
            -            in_: 16.0, out: 1.0
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 16.0
            +                1018 supriya:channel-strip:4 (session.mixers[0].tracks[0]:channel-strip)
            +                    active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 24.0
            +                1020 supriya:meters:4 (session.mixers[0].tracks[0]:output-levels)
            +                    in_: 24.0, out: 23.0
            +                1021 supriya:patch-cable:4x4 (session.mixers[0].tracks[0]:output)
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 24.0, out: 20.0
            +        1015 supriya:meters:4 (session.mixers[0]:input-levels)
            +            in_: 20.0, out: 11.0
                     1002 group (session.mixers[0]:devices)
                     1003 supriya:channel-strip:2 (session.mixers[0]:channel-strip)
            -            active: 1.0, done_action: 2.0, gain: c0, gate: 1.0, out: 16.0
            -        1005 supriya:meters:2 (session.mixers[0]:output-levels)
            -            in_: 16.0, out: 3.0
            +            active: 1.0, done_action: 2.0, gain: c0, gate: 0.0, out: 16.0
                     1006 supriya:patch-cable:2x2 (session.mixers[0]:output)
            -            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 0.0
            +            active: 1.0, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 16.0, out: 0.0
            +        1014 supriya:channel-strip:4 (session.mixers[0]:channel-strip)
            +            active: 1.0, done_action: 2.0, gain: c0, gate: 1.0, out: 20.0
            +        1016 supriya:meters:4 (session.mixers[0]:output-levels)
            +            in_: 20.0, out: 15.0
            +        1017 supriya:patch-cable:4x4 (session.mixers[0]:output)
            +            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 0.0
            """,
            expected_messages="""
            - ['/d_recv', <SynthDef: supriya:channel-strip:4>]
            - ['/d_recv', <SynthDef: supriya:meters:4>]
            - ['/d_recv', <SynthDef: supriya:patch-cable:4x4>]
            - ['/sync', 3]
            - ['/c_fill', 11, 4, 0.0, 15, 4, 0.0]
            - ['/c_fill', 19, 4, 0.0, 23, 4, 0.0]
            - [None,
               [['/s_new', 'supriya:channel-strip:4', 1014, 1, 1000, 'gain', 'c0', 'out', 20.0],
                ['/s_new', 'supriya:meters:4', 1015, 3, 1001, 'in_', 20.0, 'out', 11.0],
                ['/s_new', 'supriya:meters:4', 1016, 3, 1014, 'in_', 20.0, 'out', 15.0],
                ['/s_new', 'supriya:patch-cable:4x4', 1017, 1, 1000, 'in_', 20.0]]]
            - [None,
               [['/s_new', 'supriya:channel-strip:4', 1018, 1, 1007, 'active', 'c5', 'gain', 'c6', 'out', 24.0],
                ['/s_new', 'supriya:meters:4', 1019, 3, 1008, 'in_', 24.0, 'out', 19.0],
                ['/s_new', 'supriya:meters:4', 1020, 3, 1018, 'in_', 24.0, 'out', 23.0],
                ['/s_new', 'supriya:patch-cable:4x4', 1021, 1, 1007, 'active', 'c5', 'in_', 24.0, 'out', 20.0]]]
            - [None,
               [['/n_set', 1003, 'done_action', 2.0, 'gate', 0.0],
                ['/n_free', 1004],
                ['/n_free', 1005],
                ['/n_set', 1006, 'done_action', 2.0, 'gate', 0.0]]]
            - [None,
               [['/n_set', 1010, 'done_action', 2.0, 'gate', 0.0],
                ['/n_free', 1011],
                ['/n_free', 1012],
                ['/n_set', 1013, 'done_action', 2.0, 'gate', 0.0]]]
            """,
        ),
        # 2
        # mixer: set channel count to 4
        # - mixer changes to 4
        # - track changes to 4
        SetChannelCountScenario(
            id="set track to 2ch, set mixer to 4ch",
            commands=[
                (None, "add_mixer", {"name": "Self"}),
                ("mixers[0]", "add_track", {"name": "Track"}),
                ("mixers[0].tracks[0]", "set_channel_count", {"channel_count": 2}),
            ],
            subject="mixers[0]",
            channel_count=4,
            maybe_raises=does_not_raise,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -11,13 +11,19 @@
                             1012 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
                                 in_: 18.0, out: 9.0
                             1013 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:output)
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            -        1004 supriya:meters:2 (session.mixers[0]:input-levels)
            -            in_: 16.0, out: 1.0
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 16.0
            +                1018 supriya:patch-cable:2x4 (session.mixers[0].tracks[0]:output)
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            +        1015 supriya:meters:4 (session.mixers[0]:input-levels)
            +            in_: 20.0, out: 11.0
                     1002 group (session.mixers[0]:devices)
                     1003 supriya:channel-strip:2 (session.mixers[0]:channel-strip)
            -            active: 1.0, done_action: 2.0, gain: c0, gate: 1.0, out: 16.0
            -        1005 supriya:meters:2 (session.mixers[0]:output-levels)
            -            in_: 16.0, out: 3.0
            +            active: 1.0, done_action: 2.0, gain: c0, gate: 0.0, out: 16.0
                     1006 supriya:patch-cable:2x2 (session.mixers[0]:output)
            -            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 0.0
            +            active: 1.0, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 16.0, out: 0.0
            +        1014 supriya:channel-strip:4 (session.mixers[0]:channel-strip)
            +            active: 1.0, done_action: 2.0, gain: c0, gate: 1.0, out: 20.0
            +        1016 supriya:meters:4 (session.mixers[0]:output-levels)
            +            in_: 20.0, out: 15.0
            +        1017 supriya:patch-cable:4x4 (session.mixers[0]:output)
            +            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 0.0
            """,
            expected_messages="""
            - ['/d_recv', <SynthDef: supriya:channel-strip:4>]
            - ['/d_recv', <SynthDef: supriya:meters:4>]
            - ['/d_recv', <SynthDef: supriya:patch-cable:2x4>]
            - ['/d_recv', <SynthDef: supriya:patch-cable:4x4>]
            - ['/sync', 3]
            - ['/c_fill', 11, 4, 0.0, 15, 4, 0.0]
            - [None,
               [['/s_new', 'supriya:channel-strip:4', 1014, 1, 1000, 'gain', 'c0', 'out', 20.0],
                ['/s_new', 'supriya:meters:4', 1015, 3, 1001, 'in_', 20.0, 'out', 11.0],
                ['/s_new', 'supriya:meters:4', 1016, 3, 1014, 'in_', 20.0, 'out', 15.0],
                ['/s_new', 'supriya:patch-cable:4x4', 1017, 1, 1000, 'in_', 20.0]]]
            - ['/s_new', 'supriya:patch-cable:2x4', 1018, 1, 1007, 'active', 'c5', 'in_', 18.0, 'out', 20.0]
            - [None,
               [['/n_set', 1003, 'done_action', 2.0, 'gate', 0.0],
                ['/n_free', 1004],
                ['/n_free', 1005],
                ['/n_set', 1006, 'done_action', 2.0, 'gate', 0.0]]]
            - ['/n_set', 1013, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
    ],
    ids=lambda value: value.id,
)
@pytest.mark.asyncio
async def test_Mixer_set_channel_count(
    scenario: SetChannelCountScenario,
    online: bool,
) -> None:
    async with scenario.run(online=online) as session:
        subject = session[scenario.subject]
        assert isinstance(subject, Mixer)
        with scenario.maybe_raises:
            await subject.set_channel_count(channel_count=scenario.channel_count)
    assert subject.channel_count == scenario.channel_count


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.asyncio
async def test_Mixer_set_name(online: bool) -> None:
    session = Session()
    mixer = await session.add_mixer()
    if online:
        await session.boot()
    assert mixer.name is None
    for name in ("Foo", "Bar", "Baz"):
        mixer.set_name(name=name)
        assert mixer.name == name
    mixer.set_name(name=None)
    assert mixer.name is None
