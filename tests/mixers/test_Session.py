import pytest
from uqbar.strings import normalize

from supriya.enums import BootStatus
from supriya.mixers import Session

from .conftest import (
    assert_components_diff,
    assert_tree_diff,
    capture,
    debug_components,
    debug_tree,
    format_messages,
)


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.asyncio
async def test_Session_add_context(
    basic_session: tuple[Session, str, str],
    online: bool,
) -> None:
    # Pre-conditions
    session, initial_components, initial_tree = basic_session
    if online:
        await session.boot()
    assert len(session.contexts) == 1
    # Operation
    context = await session.add_context()
    # Post-conditions
    assert len(session.contexts) == 2
    assert context in session.contexts
    assert context.boot_status == session.status
    assert_components_diff(
        session,
        """
        --- initial
        +++ mutation
        @@ -6,3 +6,4 @@
                         <TrackInput 5 session.mixers[0].tracks[0].input source=null>
                         <TrackOutput 6 session.mixers[0].tracks[0].output target=default>
                     <MixerOutput 2 session.mixers[0].output>
        +    <session.contexts[1]>
        """,
        initial_components,
    )
    if not online:
        return
    await assert_tree_diff(
        session,
        """
        --- initial
        +++ mutation
        @@ -21,3 +21,4 @@
                     in_: 16.0, out: 3.0
                 1013 supriya:patch-cable:2x2 (session.mixers[0].output:synth)
                     active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 0.0
        +<session.contexts[1]>
        """,
        initial_tree,
    )


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "reuse_context, expected_components_diff, expected_tree_diff, expected_messages",
    [
        (
            False,
            """
            """,
            """
            --- initial
            +++ mutation
            @@ -21,3 +21,15 @@
                         in_: 16.0, out: 3.0
                     1013 supriya:patch-cable:2x2 (session.mixers[0].output:synth)
                         active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 0.0
            +<session.contexts[1]>
            +    NODE TREE 1000 group (session.mixers[1]:group)
            +        1001 group (session.mixers[1]:tracks)
            +        1004 supriya:meters:2 (session.mixers[1]:input-levels)
            +            in_: 16.0, out: 1.0
            +        1002 group (session.mixers[1]:devices)
            +        1003 supriya:channel-strip:2 (session.mixers[1]:channel-strip)
            +            active: 1.0, bus: 16.0, done_action: 2.0, gain: c0, gate: 1.0
            +        1005 supriya:meters:2 (session.mixers[1]:output-levels)
            +            in_: 16.0, out: 3.0
            +        1006 supriya:patch-cable:2x2 (session.mixers[1].output:synth)
            +            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 0.0
            """,
            r"""
            - ['/d_recv', <SynthDef: supriya:channel-strip:2>]
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/d_recv', <SynthDef: supriya:meters:2>]
            - ['/d_recv', <SynthDef: supriya:patch-cable:2x2>]
            - ['/sync', 1]
            - [None,
               [['/c_set', 0, 0.0],
                ['/c_fill', 1, 2, 0.0, 3, 2, 0.0],
                ['/g_new', 1000, 1, 1, 1001, 0, 1000, 1002, 1, 1000],
                ['/s_new', 'supriya:channel-strip:2', 1003, 1, 1000, 'bus', 16.0, 'gain', 'c0'],
                ['/s_new', 'supriya:meters:2', 1004, 3, 1001, 'in_', 16.0, 'out', 1.0],
                ['/s_new', 'supriya:meters:2', 1005, 3, 1003, 'in_', 16.0, 'out', 3.0]]]
            - ['/s_new', 'supriya:patch-cable:2x2', 1006, 1, 1000, 'in_', 16.0, 'out', 0.0]
            """,
        ),
        (
            True,
            """
            """,
            """
            --- initial
            +++ mutation
            @@ -21,3 +21,15 @@
                         in_: 16.0, out: 3.0
                     1013 supriya:patch-cable:2x2 (session.mixers[0].output:synth)
                         active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 0.0
            +    NODE TREE 1014 group (session.mixers[1]:group)
            +        1015 group (session.mixers[1]:tracks)
            +        1018 supriya:meters:2 (session.mixers[1]:input-levels)
            +            in_: 20.0, out: 12.0
            +        1016 group (session.mixers[1]:devices)
            +        1017 supriya:channel-strip:2 (session.mixers[1]:channel-strip)
            +            active: 1.0, bus: 20.0, done_action: 2.0, gain: c11, gate: 1.0
            +        1019 supriya:meters:2 (session.mixers[1]:output-levels)
            +            in_: 20.0, out: 14.0
            +        1020 supriya:patch-cable:2x2 (session.mixers[1].output:synth)
            +            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 0.0
            +<session.contexts[1]>
            """,
            """
            - [None,
               [['/c_set', 11, 0.0],
                ['/c_fill', 12, 2, 0.0, 14, 2, 0.0],
                ['/g_new', 1014, 1, 1, 1015, 0, 1014, 1016, 1, 1014],
                ['/s_new', 'supriya:channel-strip:2', 1017, 1, 1014, 'bus', 20.0, 'gain', 'c11'],
                ['/s_new', 'supriya:meters:2', 1018, 3, 1015, 'in_', 20.0, 'out', 12.0],
                ['/s_new', 'supriya:meters:2', 1019, 3, 1017, 'in_', 20.0, 'out', 14.0]]]
            - ['/s_new', 'supriya:patch-cable:2x2', 1020, 1, 1014, 'in_', 20.0, 'out', 0.0]
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_Session_add_mixer(
    basic_session: tuple[Session, str, str],
    expected_components_diff: str,
    expected_messages: str,
    expected_tree_diff: str,
    online: bool,
    reuse_context: bool,
) -> None:
    # Pre-conditions
    session, initial_components, initial_tree = basic_session
    if online:
        await session.boot()
    await session.add_context()
    assert len(session.mixers) == 1
    # Operation
    with capture(
        session.contexts[0] if reuse_context else session.contexts[1]
    ) as messages:
        await session.add_mixer(context=None if reuse_context else session.contexts[1])
    # Post-conditions
    assert len(session.mixers) == 2
    assert_components_diff(session, expected_components_diff, initial_components)
    if not online:
        return
    await assert_tree_diff(
        session,
        expected_tree_diff,
        expected_initial_tree=initial_tree,
    )
    assert format_messages(messages) == normalize(expected_messages)


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.asyncio
async def test_Session_boot(
    basic_session: tuple[Session, str, str],
    online: bool,
) -> None:
    # Pre-conditions
    session, initial_components, initial_tree = basic_session
    assert session.status == BootStatus.OFFLINE
    if online:
        await session.boot()
        assert session.status == BootStatus.ONLINE
    # Operation
    await session.boot()  # idempotent
    # Post-conditions
    assert session.status == BootStatus.ONLINE
    assert_components_diff(session, "", initial_components)
    await assert_tree_diff(
        session,
        "",
        expected_initial_tree=initial_tree,
    )


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "context_index, expected_components_diff, expected_tree_diff",
    [
        (
            0,
            """
            """,
            """
            --- initial
            +++ mutation
            @@ -1,24 +1 @@
             <session.contexts[0]>
            -    NODE TREE 1000 group (session.mixers[0]:group)
            -        1001 group (session.mixers[0]:tracks)
            -            1006 group (session.mixers[0].tracks[0]:group)
            -                1007 group (session.mixers[0].tracks[0]:tracks)
            -                1010 supriya:meters:2 (session.mixers[0].tracks[0]:input-levels)
            -                    in_: 18.0, out: 7.0
            -                1008 group (session.mixers[0].tracks[0]:devices)
            -                1009 supriya:channel-strip:2 (session.mixers[0].tracks[0]:channel-strip)
            -                    active: c5, bus: 18.0, done_action: 2.0, gain: c6, gate: 1.0
            -                1011 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
            -                    in_: 18.0, out: 9.0
            -                1012 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].output:synth)
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            -        1004 supriya:meters:2 (session.mixers[0]:input-levels)
            -            in_: 16.0, out: 1.0
            -        1002 group (session.mixers[0]:devices)
            -        1003 supriya:channel-strip:2 (session.mixers[0]:channel-strip)
            -            active: 1.0, bus: 16.0, done_action: 2.0, gain: c0, gate: 1.0
            -        1005 supriya:meters:2 (session.mixers[0]:output-levels)
            -            in_: 16.0, out: 3.0
            -        1013 supriya:patch-cable:2x2 (session.mixers[0].output:synth)
            -            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 0.0
            -<session.contexts[1]>
            """,
        ),
        (
            1,
            """
            --- initial
            +++ mutation
            @@ -1,11 +1,11 @@
             <Session 0>
                 <session.contexts[0]>
            +        <Mixer 7 'Q' session.mixers[1]>
            +            <MixerOutput 8 session.mixers[1].output>
            +    <session.contexts[1]>
                     <Mixer 1 'P' session.mixers[0]>
                         <Track 3 'A' session.mixers[0].tracks[0]>
                             <TrackFeedback 4 session.mixers[0].tracks[0].feedback>
                             <TrackInput 5 session.mixers[0].tracks[0].input source=null>
                             <TrackOutput 6 session.mixers[0].tracks[0].output target=default>
                         <MixerOutput 2 session.mixers[0].output>
            -        <Mixer 7 'Q' session.mixers[1]>
            -            <MixerOutput 8 session.mixers[1].output>
            -    <session.contexts[1]>
            """,
            """
            --- initial
            +++ mutation
            @@ -21,4 +21,3 @@
                         in_: 16.0, out: 3.0
                     1013 supriya:patch-cable:2x2 (session.mixers[0].output:synth)
                         active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 0.0
            -<session.contexts[1]>
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_Session_delete_context(
    basic_session: tuple[Session, str, str],
    context_index: int,
    expected_components_diff: str,
    expected_tree_diff: str,
    online: bool,
) -> None:
    # Pre-conditions
    session, _, _ = basic_session
    await session.add_context()
    initial_components = debug_components(session)
    if online:
        await session.boot()
        initial_tree = await debug_tree(session)
    # Operation
    await session.delete_context(session.contexts[context_index])
    # Post-conditions
    assert len(session.contexts) == 1
    assert_components_diff(session, expected_components_diff, initial_components)
    if not online:
        return
    await assert_tree_diff(
        session,
        expected_tree_diff,
        expected_initial_tree=initial_tree,
    )


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.asyncio
async def test_Session_quit(
    basic_session: tuple[Session, str, str],
    online: bool,
) -> None:
    # Pre-conditions
    session, initial_components, _ = basic_session
    assert session.status == BootStatus.OFFLINE
    if online:
        await session.boot()
        assert session.status == BootStatus.ONLINE
    # Operation
    await session.quit()
    # Post-conditions
    assert session.status == BootStatus.OFFLINE
    assert_components_diff(session, "", initial_components)


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "mixer_index, context_index, expected_components_diff, expected_tree_diff",
    [
        (0, 0, "", ""),
        (
            0,
            1,
            """
            --- initial
            +++ mutation
            @@ -1,11 +1,11 @@
             <Session 0>
                 <session.contexts[0]>
            +        <Mixer 7 'Q' session.mixers[1]>
            +            <MixerOutput 8 session.mixers[1].output>
            +    <session.contexts[1]>
                     <Mixer 1 'P' session.mixers[0]>
                         <Track 3 'A' session.mixers[0].tracks[0]>
                             <TrackFeedback 4 session.mixers[0].tracks[0].feedback>
                             <TrackInput 5 session.mixers[0].tracks[0].input source=null>
                             <TrackOutput 6 session.mixers[0].tracks[0].output target=default>
                         <MixerOutput 2 session.mixers[0].output>
            -        <Mixer 7 'Q' session.mixers[1]>
            -            <MixerOutput 8 session.mixers[1].output>
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
            +            active: 1.0, bus: 20.0, done_action: 2.0, gain: c11, gate: 1.0
            +        1019 supriya:meters:2 (session.mixers[1]:output-levels)
            +            in_: 20.0, out: 14.0
            +        1020 supriya:patch-cable:2x2 (session.mixers[1].output:synth)
            +            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 0.0
            +<session.contexts[1]>
                 NODE TREE 1000 group (session.mixers[0]:group)
                     1001 group (session.mixers[0]:tracks)
                         1006 group (session.mixers[0].tracks[0]:group)
            @@ -21,15 +33,3 @@
                         in_: 16.0, out: 3.0
                     1013 supriya:patch-cable:2x2 (session.mixers[0].output:synth)
                         active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 0.0
            -    NODE TREE 1014 group (session.mixers[1]:group)
            -        1015 group (session.mixers[1]:tracks)
            -        1018 supriya:meters:2 (session.mixers[1]:input-levels)
            -            in_: 20.0, out: 12.0
            -        1016 group (session.mixers[1]:devices)
            -        1017 supriya:channel-strip:2 (session.mixers[1]:channel-strip)
            -            active: 1.0, bus: 20.0, done_action: 2.0, gain: c11, gate: 1.0
            -        1019 supriya:meters:2 (session.mixers[1]:output-levels)
            -            in_: 20.0, out: 14.0
            -        1020 supriya:patch-cable:2x2 (session.mixers[1].output:synth)
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
            @@ -6,6 +6,6 @@
                             <TrackInput 5 session.mixers[0].tracks[0].input source=null>
                             <TrackOutput 6 session.mixers[0].tracks[0].output target=default>
                         <MixerOutput 2 session.mixers[0].output>
            +    <session.contexts[1]>
                     <Mixer 7 'Q' session.mixers[1]>
                         <MixerOutput 8 session.mixers[1].output>
            -    <session.contexts[1]>
            """,
            """
            --- initial
            +++ mutation
            @@ -21,15 +21,15 @@
                         in_: 16.0, out: 3.0
                     1013 supriya:patch-cable:2x2 (session.mixers[0].output:synth)
                         active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 0.0
            -    NODE TREE 1014 group (session.mixers[1]:group)
            -        1015 group (session.mixers[1]:tracks)
            -        1018 supriya:meters:2 (session.mixers[1]:input-levels)
            -            in_: 20.0, out: 12.0
            -        1016 group (session.mixers[1]:devices)
            -        1017 supriya:channel-strip:2 (session.mixers[1]:channel-strip)
            -            active: 1.0, bus: 20.0, done_action: 2.0, gain: c11, gate: 1.0
            -        1019 supriya:meters:2 (session.mixers[1]:output-levels)
            -            in_: 20.0, out: 14.0
            -        1020 supriya:patch-cable:2x2 (session.mixers[1].output:synth)
            -            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 0.0
             <session.contexts[1]>
            +    NODE TREE 1000 group (session.mixers[1]:group)
            +        1001 group (session.mixers[1]:tracks)
            +        1004 supriya:meters:2 (session.mixers[1]:input-levels)
            +            in_: 16.0, out: 1.0
            +        1002 group (session.mixers[1]:devices)
            +        1003 supriya:channel-strip:2 (session.mixers[1]:channel-strip)
            +            active: 1.0, bus: 16.0, done_action: 2.0, gain: c0, gate: 1.0
            +        1005 supriya:meters:2 (session.mixers[1]:output-levels)
            +            in_: 16.0, out: 3.0
            +        1006 supriya:patch-cable:2x2 (session.mixers[1].output:synth)
            +            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 0.0
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_Session_set_mixer_context(
    basic_session: tuple[Session, str, str],
    context_index: int,
    expected_components_diff: str,
    expected_tree_diff: str,
    mixer_index: int,
    online: bool,
) -> None:
    # Pre-conditions
    session, _, _ = basic_session
    await session.add_mixer(name="Q")
    await session.add_context()
    assert len(session.contexts) == 2
    assert len(session.mixers) == 2
    if online:
        await session.boot()
    initial_components = debug_components(session)
    if online:
        initial_tree = await debug_tree(session, label="actual initial tree")
    # Operation
    await session.set_mixer_context(
        mixer=session.mixers[mixer_index], context=session.contexts[context_index]
    )
    # Post-conditions
    assert_components_diff(session, expected_components_diff, initial_components)
    if not online:
        return
    await assert_tree_diff(
        session,
        expected_tree_diff,
        expected_initial_tree=initial_tree,
    )
