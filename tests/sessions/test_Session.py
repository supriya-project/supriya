from typing import Callable

import pytest

from supriya.enums import BootStatus
from supriya.osc import find_free_port
from supriya.scsynth import Options
from supriya.sessions import Session

from .conftest import run_test


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "commands, expected_components_diff, expected_tree_diff",
    [
        (
            [
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Track"}),
            ],
            """
            --- initial
            +++ mutation
            @@ -2,3 +2,4 @@
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
                         <Track 2 'Track'>
            +    <session.contexts[1]>
            """,
            """
            --- initial
            +++ mutation
            @@ -21,3 +21,4 @@
                         in_: 16.0, out: 3.0
                     1006 supriya:patch-cable:2x2 (session.mixers[0]:output)
                         active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 0.0
            +<session.contexts[1]>
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_Session_add_context(
    commands: list[tuple[str | None, str, dict | None]],
    expected_components_diff: Callable[[Session], str] | str,
    expected_tree_diff: str,
    online: bool,
) -> None:
    async with run_test(
        commands=commands,
        expected_components_diff=expected_components_diff,
        expected_tree_diff=expected_tree_diff,
        online=online,
    ) as session:
        assert len(session.contexts) == 1
        # unique port ensure unique context index in debug_components
        context = await session.add_context(Options(port=find_free_port()))
    assert len(session.contexts) == 2
    assert context in session.contexts
    assert context.boot_status == session.boot_status


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "commands, reuse_context, expected_components_diff, expected_tree_diff, expected_messages",
    [
        (
            [
                (None, "add_mixer", {"name": "Mixer"}),
                (None, "add_context", {"options": Options(port=find_free_port())}),
                ("mixers[0]", "add_track", {"name": "Track"}),
            ],
            False,
            """
            --- initial
            +++ mutation
            @@ -3,3 +3,4 @@
                     <Mixer 1 'Mixer'>
                         <Track 2 'Track'>
                 <session.contexts[1]>
            +        <Mixer 3>
            """,
            """
            --- initial
            +++ mutation
            @@ -22,3 +22,14 @@
                     1006 supriya:patch-cable:2x2 (session.mixers[0]:output)
                         active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 0.0
             <session.contexts[1]>
            +    NODE TREE 1000 group (session.mixers[1]:group)
            +        1001 group (session.mixers[1]:tracks)
            +        1004 supriya:meters:2 (session.mixers[1]:input-levels)
            +            in_: 16.0, out: 1.0
            +        1002 group (session.mixers[1]:devices)
            +        1003 supriya:channel-strip:2 (session.mixers[1]:channel-strip)
            +            active: 1.0, done_action: 2.0, gain: c0, gate: 1.0, out: 16.0
            +        1005 supriya:meters:2 (session.mixers[1]:output-levels)
            +            in_: 16.0, out: 3.0
            +        1006 supriya:patch-cable:2x2 (session.mixers[1]:output)
            +            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 0.0
            """,
            r"""
            - ['/d_recv', <SynthDef: supriya:channel-strip:2>]
            - ['/d_recv', <SynthDef: supriya:meters:2>]
            - ['/d_recv', <SynthDef: supriya:patch-cable:2x2>]
            - ['/sync', 2]
            - [None, [['/c_set', 0, 0.0], ['/c_fill', 1, 2, 0.0, 3, 2, 0.0]]]
            - [None,
               [['/g_new', 1000, 0, 1, 1001, 0, 1000, 1002, 1, 1000],
                ['/s_new', 'supriya:channel-strip:2', 1003, 1, 1000, 'gain', 'c0', 'out', 16.0],
                ['/s_new', 'supriya:meters:2', 1004, 3, 1001, 'in_', 16.0, 'out', 1.0],
                ['/s_new', 'supriya:meters:2', 1005, 3, 1003, 'in_', 16.0, 'out', 3.0],
                ['/s_new', 'supriya:patch-cable:2x2', 1006, 1, 1000, 'in_', 16.0]]]
            """,
        ),
        (
            [
                (None, "add_mixer", {"name": "Mixer"}),
                (None, "add_context", {"options": Options(port=find_free_port())}),
                ("mixers[0]", "add_track", {"name": "Track"}),
            ],
            True,
            """
            --- initial
            +++ mutation
            @@ -2,4 +2,5 @@
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
                         <Track 2 'Track'>
            +        <Mixer 3>
                 <session.contexts[1]>
            """,
            """
            --- initial
            +++ mutation
            @@ -21,4 +21,15 @@
                         in_: 16.0, out: 3.0
                     1006 supriya:patch-cable:2x2 (session.mixers[0]:output)
                         active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 0.0
            +    NODE TREE 1014 group (session.mixers[1]:group)
            +        1015 group (session.mixers[1]:tracks)
            +        1018 supriya:meters:2 (session.mixers[1]:input-levels)
            +            in_: 20.0, out: 12.0
            +        1016 group (session.mixers[1]:devices)
            +        1017 supriya:channel-strip:2 (session.mixers[1]:channel-strip)
            +            active: 1.0, done_action: 2.0, gain: c11, gate: 1.0, out: 20.0
            +        1019 supriya:meters:2 (session.mixers[1]:output-levels)
            +            in_: 20.0, out: 14.0
            +        1020 supriya:patch-cable:2x2 (session.mixers[1]:output)
            +            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 0.0
             <session.contexts[1]>
            """,
            """
            - [None, [['/c_set', 11, 0.0], ['/c_fill', 12, 2, 0.0, 14, 2, 0.0]]]
            - [None,
               [['/g_new', 1014, 0, 1, 1015, 0, 1014, 1016, 1, 1014],
                ['/s_new', 'supriya:channel-strip:2', 1017, 1, 1014, 'gain', 'c11', 'out', 20.0],
                ['/s_new', 'supriya:meters:2', 1018, 3, 1015, 'in_', 20.0, 'out', 12.0],
                ['/s_new', 'supriya:meters:2', 1019, 3, 1017, 'in_', 20.0, 'out', 14.0],
                ['/s_new', 'supriya:patch-cable:2x2', 1020, 1, 1014, 'in_', 20.0]]]
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_Session_add_mixer(
    commands: list[tuple[str | None, str, dict | None]],
    expected_components_diff: Callable[[Session], str] | str,
    expected_messages: str,
    expected_tree_diff: str,
    online: bool,
    reuse_context: bool,
) -> None:
    async with run_test(
        commands=commands,
        context_index=0 if reuse_context else 1,
        expected_components_diff=expected_components_diff,
        expected_messages=expected_messages,
        expected_tree_diff=expected_tree_diff,
        online=online,
    ) as session:
        assert len(session.contexts) == 2
        assert len(session.mixers) == 1
        await session.add_mixer(context=None if reuse_context else session.contexts[1])
    assert len(session.mixers) == 2


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "commands",
    [
        [
            (None, "add_mixer", {"name": "Mixer"}),
            ("mixers[0]", "add_track", {"name": "Track"}),
        ],
    ],
)
@pytest.mark.asyncio
async def test_Session_boot(
    commands: list[tuple[str | None, str, dict | None]],
    online: bool,
) -> None:
    async with run_test(commands=commands, online=online) as session:
        await session.boot()  # idempotent
    assert session.boot_status == BootStatus.ONLINE


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "commands",
    [
        [
            (None, "add_mixer", {"name": "Mixer"}),
            ("mixers[0]", "add_track", {"name": "Track"}),
            (None, "add_context", {"options": Options(port=find_free_port())}),
        ],
    ],
)
@pytest.mark.parametrize(
    "context_index, expected_components_diff, expected_tree_diff",
    [
        (
            0,
            lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,5 +1,2 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
            -        <Mixer 1 'Mixer'>
            -            <Track 2 'Track'>
            -    <session.contexts[1]>
            """,
            """
            --- initial
            +++ mutation
            @@ -1,24 +1 @@
             <session.contexts[0]>
            -    NODE TREE 1000 group (session.mixers[0]:group)
            -        1001 group (session.mixers[0]:tracks)
            -            1007 group (session.mixers[0].tracks[0]:group)
            -                1008 group (session.mixers[0].tracks[0]:tracks)
            -                1011 supriya:meters:2 (session.mixers[0].tracks[0]:input-levels)
            -                    in_: 18.0, out: 7.0
            -                1009 group (session.mixers[0].tracks[0]:devices)
            -                1010 supriya:channel-strip:2 (session.mixers[0].tracks[0]:channel-strip)
            -                    active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
            -                1012 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
            -                    in_: 18.0, out: 9.0
            -                1013 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:output)
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            -        1004 supriya:meters:2 (session.mixers[0]:input-levels)
            -            in_: 16.0, out: 1.0
            -        1002 group (session.mixers[0]:devices)
            -        1003 supriya:channel-strip:2 (session.mixers[0]:channel-strip)
            -            active: 1.0, done_action: 2.0, gain: c0, gate: 1.0, out: 16.0
            -        1005 supriya:meters:2 (session.mixers[0]:output-levels)
            -            in_: 16.0, out: 3.0
            -        1006 supriya:patch-cable:2x2 (session.mixers[0]:output)
            -            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 0.0
            -<session.contexts[1]>
            """,
        ),
        (
            1,
            """
            --- initial
            +++ mutation
            @@ -2,4 +2,3 @@
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
                         <Track 2 'Track'>
            -    <session.contexts[1]>
            """,
            """
            --- initial
            +++ mutation
            @@ -21,4 +21,3 @@
                         in_: 16.0, out: 3.0
                     1006 supriya:patch-cable:2x2 (session.mixers[0]:output)
                         active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 0.0
            -<session.contexts[1]>
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_Session_delete_context(
    commands: list[tuple[str | None, str, dict | None]],
    context_index: int,
    expected_components_diff: Callable[[Session], str] | str,
    expected_tree_diff: str,
    online: bool,
) -> None:
    async with run_test(
        commands=commands,
        expected_components_diff=expected_components_diff,
        expected_messages=None,
        expected_tree_diff=expected_tree_diff,
        online=online,
    ) as session:
        await session.delete_context(session.contexts[context_index])
    assert len(session.contexts) == 1


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "commands, expected_messages",
    [
        (
            [
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Track"}),
            ],
            """
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
            - ['/quit']
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_Session_quit(
    commands: list[tuple[str | None, str, dict | None]],
    expected_messages: str,
    online: bool,
) -> None:
    async with run_test(
        commands=commands,
        expected_messages=expected_messages,
        expected_tree_diff=None,
        online=online,
    ) as session:
        await session.quit()  # idempotent
    assert session.boot_status == BootStatus.OFFLINE


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "commands",
    [
        [
            (None, "add_mixer", {"name": "Mixer One"}),
            ("mixers[0]", "add_track", {"name": "Track"}),
            (None, "add_mixer", {"name": "Mixer Two"}),
            (None, "add_context", {"options": Options(port=find_free_port())}),
        ],
    ],
)
@pytest.mark.parametrize(
    "mixer_index, context_index, expected_components_diff, expected_tree_diff",
    [
        (0, 0, "", ""),
        (
            0,
            1,
            lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,6 +1,6 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
            +        <Mixer 3 'Mixer Two'>
            +    <session.contexts[1]>
                     <Mixer 1 'Mixer One'>
                         <Track 2 'Track'>
            -        <Mixer 3 'Mixer Two'>
            -    <session.contexts[1]>
            """,
            """
            --- initial
            +++ mutation
            @@ -1,4 +1,16 @@
             <session.contexts[0]>
            +    NODE TREE 1014 group (session.mixers[1]:group)
            +        1015 group (session.mixers[1]:tracks)
            +        1018 supriya:meters:2 (session.mixers[1]:input-levels)
            +            in_: 20.0, out: 12.0
            +        1016 group (session.mixers[1]:devices)
            +        1017 supriya:channel-strip:2 (session.mixers[1]:channel-strip)
            +            active: 1.0, done_action: 2.0, gain: c11, gate: 1.0, out: 20.0
            +        1019 supriya:meters:2 (session.mixers[1]:output-levels)
            +            in_: 20.0, out: 14.0
            +        1020 supriya:patch-cable:2x2 (session.mixers[1]:output)
            +            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 0.0
            +<session.contexts[1]>
                 NODE TREE 1000 group (session.mixers[0]:group)
                     1001 group (session.mixers[0]:tracks)
                         1007 group (session.mixers[0].tracks[0]:group)
            @@ -21,15 +33,3 @@
                         in_: 16.0, out: 3.0
                     1006 supriya:patch-cable:2x2 (session.mixers[0]:output)
                         active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 0.0
            -    NODE TREE 1014 group (session.mixers[1]:group)
            -        1015 group (session.mixers[1]:tracks)
            -        1018 supriya:meters:2 (session.mixers[1]:input-levels)
            -            in_: 20.0, out: 12.0
            -        1016 group (session.mixers[1]:devices)
            -        1017 supriya:channel-strip:2 (session.mixers[1]:channel-strip)
            -            active: 1.0, done_action: 2.0, gain: c11, gate: 1.0, out: 20.0
            -        1019 supriya:meters:2 (session.mixers[1]:output-levels)
            -            in_: 20.0, out: 14.0
            -        1020 supriya:patch-cable:2x2 (session.mixers[1]:output)
            -            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 0.0
            -<session.contexts[1]>
            """,
        ),
        (1, 0, "", ""),
        (
            1,
            1,
            """
            --- initial
            +++ mutation
            @@ -2,5 +2,5 @@
                 <session.contexts[0]>
                     <Mixer 1 'Mixer One'>
                         <Track 2 'Track'>
            +    <session.contexts[1]>
                     <Mixer 3 'Mixer Two'>
            -    <session.contexts[1]>
            """,
            """
            --- initial
            +++ mutation
            @@ -21,15 +21,15 @@
                         in_: 16.0, out: 3.0
                     1006 supriya:patch-cable:2x2 (session.mixers[0]:output)
                         active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 0.0
            -    NODE TREE 1014 group (session.mixers[1]:group)
            -        1015 group (session.mixers[1]:tracks)
            -        1018 supriya:meters:2 (session.mixers[1]:input-levels)
            -            in_: 20.0, out: 12.0
            -        1016 group (session.mixers[1]:devices)
            -        1017 supriya:channel-strip:2 (session.mixers[1]:channel-strip)
            -            active: 1.0, done_action: 2.0, gain: c11, gate: 1.0, out: 20.0
            -        1019 supriya:meters:2 (session.mixers[1]:output-levels)
            -            in_: 20.0, out: 14.0
            -        1020 supriya:patch-cable:2x2 (session.mixers[1]:output)
            -            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 0.0
             <session.contexts[1]>
            +    NODE TREE 1000 group (session.mixers[1]:group)
            +        1001 group (session.mixers[1]:tracks)
            +        1004 supriya:meters:2 (session.mixers[1]:input-levels)
            +            in_: 16.0, out: 1.0
            +        1002 group (session.mixers[1]:devices)
            +        1003 supriya:channel-strip:2 (session.mixers[1]:channel-strip)
            +            active: 1.0, done_action: 2.0, gain: c0, gate: 1.0, out: 16.0
            +        1005 supriya:meters:2 (session.mixers[1]:output-levels)
            +            in_: 16.0, out: 3.0
            +        1006 supriya:patch-cable:2x2 (session.mixers[1]:output)
            +            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 0.0
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_Session_set_mixer_context(
    commands: list[tuple[str | None, str, dict | None]],
    context_index: int,
    expected_components_diff: Callable[[Session], str] | str,
    expected_tree_diff: str,
    mixer_index: int,
    online: bool,
) -> None:
    async with run_test(
        commands=commands,
        expected_components_diff=expected_components_diff,
        expected_messages=None,
        expected_tree_diff=expected_tree_diff,
        online=online,
    ) as session:
        assert len(session.contexts) == 2
        assert len(session.mixers) == 2
        await session.set_mixer_context(
            mixer=session.mixers[mixer_index], context=session.contexts[context_index]
        )
