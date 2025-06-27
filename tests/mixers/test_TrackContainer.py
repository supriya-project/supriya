import pytest
from uqbar.strings import normalize

from supriya.mixers import Session
from supriya.mixers.tracks import Track, TrackContainer

from .conftest import (
    apply_commands,
    assert_components_diff,
    assert_tree_diff,
    capture,
    debug_components,
    debug_tree,
    format_messages,
)


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "target, expected_components_diff, expected_tree_diff, expected_messages",
    [
        (
            "mixers[0]",
            """
            --- initial
            +++ mutation
            @@ -2,3 +2,4 @@
                 <session.contexts[0]>
                     <Mixer 1 'P'>
                         <Track 2 'A'>
            +            <Track 3 'Z'>
            """,
            """
            --- initial
            +++ mutation
            @@ -12,6 +12,17 @@
                                 in_: 18.0, out: 9.0
                             1013 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:output)
                                 active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            +            1014 group (session.mixers[0].tracks[1]:group)
            +                1015 group (session.mixers[0].tracks[1]:tracks)
            +                1018 supriya:meters:2 (session.mixers[0].tracks[1]:input-levels)
            +                    in_: 20.0, out: 13.0
            +                1016 group (session.mixers[0].tracks[1]:devices)
            +                1017 supriya:channel-strip:2 (session.mixers[0].tracks[1]:channel-strip)
            +                    active: c11, done_action: 2.0, gain: c12, gate: 1.0, out: 20.0
            +                1019 supriya:meters:2 (session.mixers[0].tracks[1]:output-levels)
            +                    in_: 20.0, out: 15.0
            +                1020 supriya:patch-cable:2x2 (session.mixers[0].tracks[1]:output)
            +                    active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
                     1004 supriya:meters:2 (session.mixers[0]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (session.mixers[0]:devices)
            """,
            """
            - [None, [['/c_set', 11, 1.0, 12, 0.0], ['/c_fill', 13, 2, 0.0, 15, 2, 0.0]]]
            - [None,
               [['/g_new', 1014, 3, 1007, 1015, 0, 1014, 1016, 1, 1014],
                ['/s_new', 'supriya:channel-strip:2', 1017, 1, 1014, 'active', 'c11', 'gain', 'c12', 'out', 20.0],
                ['/s_new', 'supriya:meters:2', 1018, 3, 1015, 'in_', 20.0, 'out', 13.0],
                ['/s_new', 'supriya:meters:2', 1019, 3, 1017, 'in_', 20.0, 'out', 15.0],
                ['/s_new', 'supriya:patch-cable:2x2', 1020, 1, 1014, 'active', 'c11', 'in_', 20.0, 'out', 16.0]]]
            """,
        ),
        (
            "mixers[0].tracks[0]",
            """
            --- initial
            +++ mutation
            @@ -2,3 +2,4 @@
                 <session.contexts[0]>
                     <Mixer 1 'P'>
                         <Track 2 'A'>
            +                <Track 3 'Z'>
            """,
            """
            --- initial
            +++ mutation
            @@ -3,6 +3,17 @@
                     1001 group (session.mixers[0]:tracks)
                         1007 group (session.mixers[0].tracks[0]:group)
                             1008 group (session.mixers[0].tracks[0]:tracks)
            +                    1014 group (session.mixers[0].tracks[0].tracks[0]:group)
            +                        1015 group (session.mixers[0].tracks[0].tracks[0]:tracks)
            +                        1018 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:input-levels)
            +                            in_: 20.0, out: 13.0
            +                        1016 group (session.mixers[0].tracks[0].tracks[0]:devices)
            +                        1017 supriya:channel-strip:2 (session.mixers[0].tracks[0].tracks[0]:channel-strip)
            +                            active: c11, done_action: 2.0, gain: c12, gate: 1.0, out: 20.0
            +                        1019 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:output-levels)
            +                            in_: 20.0, out: 15.0
            +                        1020 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0]:output)
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 18.0
                             1011 supriya:meters:2 (session.mixers[0].tracks[0]:input-levels)
                                 in_: 18.0, out: 7.0
                             1009 group (session.mixers[0].tracks[0]:devices)
            """,
            """
            - [None, [['/c_set', 11, 1.0, 12, 0.0], ['/c_fill', 13, 2, 0.0, 15, 2, 0.0]]]
            - [None,
               [['/g_new', 1014, 0, 1008, 1015, 0, 1014, 1016, 1, 1014],
                ['/s_new', 'supriya:channel-strip:2', 1017, 1, 1014, 'active', 'c11', 'gain', 'c12', 'out', 20.0],
                ['/s_new', 'supriya:meters:2', 1018, 3, 1015, 'in_', 20.0, 'out', 13.0],
                ['/s_new', 'supriya:meters:2', 1019, 3, 1017, 'in_', 20.0, 'out', 15.0],
                ['/s_new', 'supriya:patch-cable:2x2', 1020, 1, 1014, 'active', 'c11', 'in_', 20.0, 'out', 18.0]]]
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_TrackContainer_add_track(
    basic_session: tuple[Session, str, str],
    expected_components_diff: str,
    expected_messages: str,
    expected_tree_diff: str,
    online: bool,
    target: str,
) -> None:
    # Pre-conditions
    print("Pre-conditions")
    session, initial_components, initial_tree = basic_session
    if online:
        await session.boot()
    target_ = session[target]
    assert isinstance(target_, TrackContainer)
    # Operation
    print("Operation")
    with capture(session["mixers[0]"].context) as messages:
        track = await target_.add_track(name="Z")
    # Post-conditions
    print("Post-conditions")
    assert isinstance(track, Track)
    assert track in target_.tracks
    assert track.parent is target_
    assert target_.tracks[-1] is track
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
@pytest.mark.parametrize(
    "commands, target, index, count, maybe_raises, expected_components_diff, expected_tree_diff, expected_messages",
    [],
)
@pytest.mark.asyncio
async def test_TrackContainer_group(
    commands: list[tuple[str | None, str, dict | None]],
    count: int,
    expected_components_diff: str,
    expected_messages: str,
    expected_tree_diff: str,
    index: int,
    maybe_raises,
    online: bool,
    target: str,
) -> None:
    # Pre-conditions
    print("Pre-conditions")
    session = Session()
    await apply_commands(session, commands)
    initial_components = debug_components(session)
    if online:
        await session.boot()
        await session.sync()
        initial_tree = await debug_tree(session, annotated=False)
    target_ = session[target]
    assert isinstance(target_, TrackContainer)
    # Operation
    print("Operation")
    with maybe_raises, capture(session["mixers[0]"].context) as messages:
        track = await target_.group(index=index, count=count)
    # Post-conditions
    print("Post-conditions")
    assert isinstance(track, Track)
    assert track in target_.tracks
    assert track.parent is target_
    assert target_.tracks[index] is track
    assert_components_diff(session, expected_components_diff, initial_components)
    if not online:
        return
    await assert_tree_diff(
        session,
        expected_tree_diff,
        expected_initial_tree=initial_tree,
    )
    assert format_messages(messages) == normalize(expected_messages)
