import pytest
from uqbar.strings import normalize

from supriya.mixers import Session
from supriya.mixers.tracks import Track, TrackContainer

from .conftest import assert_components_diff, assert_tree_diff, capture, format_messages


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "target, expected_components_diff, expected_tree_diff, expected_messages",
    [
        (
            "mixers[0]",
            """
            --- initial
            +++ mutation
            @@ -9,5 +9,6 @@
                         <Track 4 'B'>
                             <TrackSend 11 target=<Track 6 'A1'>>
                         <Track 5 'C'>
            +            <Track 12 'Z'>
                     <Mixer 2 'Q'>
                         <Track 9 'D'>
            """,
            """
            --- initial
            +++ mutation
            @@ -73,6 +73,17 @@
                                 in_: 30.0, out: 39.0
                             1051 supriya:patch-cable:2x2 (session.mixers[0].tracks[2]:output)
                                 active: c35, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 30.0, out: 16.0
            +            1066 group (session.mixers[0].tracks[3]:group)
            +                1067 group (session.mixers[0].tracks[3]:tracks)
            +                1070 supriya:meters:2 (session.mixers[0].tracks[3]:input-levels)
            +                    in_: 36.0, out: 54.0
            +                1068 group (session.mixers[0].tracks[3]:devices)
            +                1069 supriya:channel-strip:2 (session.mixers[0].tracks[3]:channel-strip)
            +                    active: c52, done_action: 2.0, gain: c53, gate: 1.0, out: 36.0
            +                1071 supriya:meters:2 (session.mixers[0].tracks[3]:output-levels)
            +                    in_: 36.0, out: 56.0
            +                1072 supriya:patch-cable:2x2 (session.mixers[0].tracks[3]:output)
            +                    active: c52, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 36.0, out: 16.0
                     1004 supriya:meters:2 (session.mixers[0]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (session.mixers[0]:devices)
            """,
            """
            - [None, [['/c_set', 52, 1.0, 53, 0.0], ['/c_fill', 54, 2, 0.0, 56, 2, 0.0]]]
            - [None,
               [['/g_new', 1066, 3, 1045, 1067, 0, 1066, 1068, 1, 1066],
                ['/s_new', 'supriya:channel-strip:2', 1069, 1, 1066, 'active', 'c52', 'gain', 'c53', 'out', 36.0],
                ['/s_new', 'supriya:meters:2', 1070, 3, 1067, 'in_', 36.0, 'out', 54.0],
                ['/s_new', 'supriya:meters:2', 1071, 3, 1069, 'in_', 36.0, 'out', 56.0],
                ['/s_new', 'supriya:patch-cable:2x2', 1072, 1, 1066, 'active', 'c52', 'in_', 36.0, 'out', 16.0]]]
            """,
        ),
        (
            "mixers[0].tracks[0]",
            """
            --- initial
            +++ mutation
            @@ -5,6 +5,7 @@
                             <Track 6 'A1'>
                                 <Track 8 'A11'>
                             <Track 7 'A2'>
            +                <Track 12 'Z'>
                             <TrackSend 10 target=<Track 4 'B'>>
                         <Track 4 'B'>
                             <TrackSend 11 target=<Track 6 'A1'>>
            """,
            """
            --- initial
            +++ mutation
            @@ -38,6 +38,17 @@
                                         in_: 26.0, out: 27.0
                                     1035 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[1]:output)
                                         active: c23, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 26.0, out: 18.0
            +                    1066 group (session.mixers[0].tracks[0].tracks[2]:group)
            +                        1067 group (session.mixers[0].tracks[0].tracks[2]:tracks)
            +                        1070 supriya:meters:2 (session.mixers[0].tracks[0].tracks[2]:input-levels)
            +                            in_: 36.0, out: 54.0
            +                        1068 group (session.mixers[0].tracks[0].tracks[2]:devices)
            +                        1069 supriya:channel-strip:2 (session.mixers[0].tracks[0].tracks[2]:channel-strip)
            +                            active: c52, done_action: 2.0, gain: c53, gate: 1.0, out: 36.0
            +                        1071 supriya:meters:2 (session.mixers[0].tracks[0].tracks[2]:output-levels)
            +                            in_: 36.0, out: 56.0
            +                        1072 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[2]:output)
            +                            active: c52, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 36.0, out: 18.0
                             1011 supriya:meters:2 (session.mixers[0].tracks[0]:input-levels)
                                 in_: 18.0, out: 7.0
                             1009 group (session.mixers[0].tracks[0]:devices)
            """,
            """
            - [None, [['/c_set', 52, 1.0, 53, 0.0], ['/c_fill', 54, 2, 0.0, 56, 2, 0.0]]]
            - [None,
               [['/g_new', 1066, 3, 1029, 1067, 0, 1066, 1068, 1, 1066],
                ['/s_new', 'supriya:channel-strip:2', 1069, 1, 1066, 'active', 'c52', 'gain', 'c53', 'out', 36.0],
                ['/s_new', 'supriya:meters:2', 1070, 3, 1067, 'in_', 36.0, 'out', 54.0],
                ['/s_new', 'supriya:meters:2', 1071, 3, 1069, 'in_', 36.0, 'out', 56.0],
                ['/s_new', 'supriya:patch-cable:2x2', 1072, 1, 1066, 'active', 'c52', 'in_', 36.0, 'out', 18.0]]]
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_TrackContainer_add_track(
    complex_session: tuple[Session, str, str],
    expected_components_diff: str,
    expected_messages: str,
    expected_tree_diff: str,
    online: bool,
    target: str,
) -> None:
    # Pre-conditions
    print("Pre-conditions")
    session, initial_components, initial_tree = complex_session
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
    "target, index, count, maybe_raises, expected_components_diff, expected_tree_diff, expected_messages",
    [],
)
@pytest.mark.asyncio
async def test_TrackContainer_group(
    complex_session: tuple[Session, str, str],
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
    session, initial_components, initial_tree = complex_session
    if online:
        await session.boot()
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
