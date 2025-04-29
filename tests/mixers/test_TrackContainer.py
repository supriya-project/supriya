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
            @@ -27,6 +27,10 @@
                             <TrackFeedback 14 session.mixers[0].tracks[2].feedback>
                             <TrackInput 15 session.mixers[0].tracks[2].input source=null>
                             <TrackOutput 16 session.mixers[0].tracks[2].output target=default>
            +            <Track 35 'Z' session.mixers[0].tracks[3]>
            +                <TrackFeedback 36 session.mixers[0].tracks[3].feedback>
            +                <TrackInput 37 session.mixers[0].tracks[3].input source=null>
            +                <TrackOutput 38 session.mixers[0].tracks[3].output target=default>
                         <MixerOutput 2 session.mixers[0].output>
                     <Mixer 3 'Q' session.mixers[1]>
                         <Track 29 'D' session.mixers[1].tracks[0]>
            """,
            """
            --- initial
            +++ mutation
            @@ -73,6 +73,17 @@
                                 in_: 30.0, out: 39.0
                             1049 supriya:patch-cable:2x2 (session.mixers[0].tracks[2].output:synth)
                                 active: c35, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 30.0, out: 16.0
            +            1066 group (session.mixers[0].tracks[3]:group)
            +                1067 group (session.mixers[0].tracks[3]:tracks)
            +                1070 supriya:meters:2 (session.mixers[0].tracks[3]:input-levels)
            +                    in_: 36.0, out: 54.0
            +                1068 group (session.mixers[0].tracks[3]:devices)
            +                1069 supriya:channel-strip:2 (session.mixers[0].tracks[3]:channel-strip)
            +                    active: c52, bus: 36.0, done_action: 2.0, gain: c53, gate: 1.0
            +                1071 supriya:meters:2 (session.mixers[0].tracks[3]:output-levels)
            +                    in_: 36.0, out: 56.0
            +                1072 supriya:patch-cable:2x2 (session.mixers[0].tracks[3].output:synth)
            +                    active: c52, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 36.0, out: 16.0
                     1004 supriya:meters:2 (session.mixers[0]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (session.mixers[0]:devices)
            """,
            """
            - [None,
               [['/c_set', 52, 1.0, 53, 0.0],
                ['/c_fill', 54, 2, 0.0, 56, 2, 0.0],
                ['/g_new', 1066, 1, 1001, 1067, 0, 1066, 1068, 1, 1066],
                ['/s_new', 'supriya:channel-strip:2', 1069, 1, 1066, 'active', 'c52', 'bus', 36.0, 'gain', 'c53'],
                ['/s_new', 'supriya:meters:2', 1070, 3, 1067, 'in_', 36.0, 'out', 54.0],
                ['/s_new', 'supriya:meters:2', 1071, 3, 1069, 'in_', 36.0, 'out', 56.0]]]
            - ['/s_new', 'supriya:patch-cable:2x2', 1072, 1, 1066, 'active', 'c52', 'in_', 36.0, 'out', 16.0]
            """,
        ),
        (
            "mixers[0].tracks[0]",
            """
            --- initial
            +++ mutation
            @@ -16,6 +16,10 @@
                                 <TrackFeedback 22 session.mixers[0].tracks[0].tracks[1].feedback>
                                 <TrackInput 23 session.mixers[0].tracks[0].tracks[1].input source=null>
                                 <TrackOutput 24 session.mixers[0].tracks[0].tracks[1].output target=default>
            +                <Track 35 'Z' session.mixers[0].tracks[0].tracks[2]>
            +                    <TrackFeedback 36 session.mixers[0].tracks[0].tracks[2].feedback>
            +                    <TrackInput 37 session.mixers[0].tracks[0].tracks[2].input source=null>
            +                    <TrackOutput 38 session.mixers[0].tracks[0].tracks[2].output target=default>
                             <TrackOutput 8 session.mixers[0].tracks[0].output target=default>
                             <TrackSend 33 session.mixers[0].tracks[0].sends[0] target=session.mixers[0].tracks[1]>
                         <Track 9 'B' session.mixers[0].tracks[1]>
            """,
            """
            --- initial
            +++ mutation
            @@ -38,6 +38,17 @@
                                         in_: 24.0, out: 27.0
                                     1032 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[1].output:synth)
                                         active: c23, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 24.0, out: 18.0
            +                    1066 group (session.mixers[0].tracks[0].tracks[2]:group)
            +                        1067 group (session.mixers[0].tracks[0].tracks[2]:tracks)
            +                        1070 supriya:meters:2 (session.mixers[0].tracks[0].tracks[2]:input-levels)
            +                            in_: 36.0, out: 54.0
            +                        1068 group (session.mixers[0].tracks[0].tracks[2]:devices)
            +                        1069 supriya:channel-strip:2 (session.mixers[0].tracks[0].tracks[2]:channel-strip)
            +                            active: c52, bus: 36.0, done_action: 2.0, gain: c53, gate: 1.0
            +                        1071 supriya:meters:2 (session.mixers[0].tracks[0].tracks[2]:output-levels)
            +                            in_: 36.0, out: 56.0
            +                        1072 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[2].output:synth)
            +                            active: c52, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 36.0, out: 18.0
                             1010 supriya:meters:2 (session.mixers[0].tracks[0]:input-levels)
                                 in_: 18.0, out: 7.0
                             1008 group (session.mixers[0].tracks[0]:devices)
            """,
            """
            - [None,
               [['/c_set', 52, 1.0, 53, 0.0],
                ['/c_fill', 54, 2, 0.0, 56, 2, 0.0],
                ['/g_new', 1066, 1, 1007, 1067, 0, 1066, 1068, 1, 1066],
                ['/s_new', 'supriya:channel-strip:2', 1069, 1, 1066, 'active', 'c52', 'bus', 36.0, 'gain', 'c53'],
                ['/s_new', 'supriya:meters:2', 1070, 3, 1067, 'in_', 36.0, 'out', 54.0],
                ['/s_new', 'supriya:meters:2', 1071, 3, 1069, 'in_', 36.0, 'out', 56.0]]]
            - ['/s_new', 'supriya:patch-cable:2x2', 1072, 1, 1066, 'active', 'c52', 'in_', 36.0, 'out', 18.0]
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
    session, initial_components, initial_tree = complex_session
    if online:
        await session.boot()
    target_ = session[target]
    assert isinstance(target_, TrackContainer)
    # Operation
    with capture(session["mixers[0]"].context) as messages:
        track = await target_.add_track(name="Z")
    # Post-conditions
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
