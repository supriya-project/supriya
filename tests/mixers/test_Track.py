import asyncio

import pytest
from uqbar.strings import normalize

from supriya import BusGroup
from supriya.mixers import Session
from supriya.mixers.synthdefs import get_lag_time
from supriya.mixers.tracks import Track, TrackContainer, TrackSend
from supriya.typing import DEFAULT, Default

from .conftest import (
    assert_components_diff,
    assert_tree_diff,
    capture,
    compute_tree_diff,
    debug_components,
    debug_tree,
    does_not_raise,
    format_messages,
)


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "postfader, source, target, maybe_raises, expected_components_diff, expected_tree_diff, expected_messages",
    [
        (
            True,
            "mixers[0].tracks[1]",
            "mixers[0]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -8,6 +8,7 @@
                             <TrackSend 10 target=<Track 4 'B'>>
                         <Track 4 'B'>
                             <TrackSend 11 target=<Track 6 'A1'>>
            +                <TrackSend 12 target=<Mixer 1 'P'>>
                         <Track 5 'C'>
                     <Mixer 2 'Q'>
                         <Track 9 'D'>
            """,
            """
            --- initial
            +++ mutation
            @@ -56,6 +56,8 @@
                             1039 group (session.mixers[0].tracks[1]:devices)
                             1040 supriya:channel-strip:2 (session.mixers[0].tracks[1]:channel-strip)
                                 active: c29, done_action: 2.0, gain: c30, gate: 1.0, out: 28.0
            +                1066 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].sends[1]:synth)
            +                    active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 28.0, out: 16.0
                             1044 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].sends[0]:synth)
                                 active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 28.0, out: 22.0
                             1042 supriya:meters:2 (session.mixers[0].tracks[1]:output-levels)
            """,
            """
            - ['/s_new', 'supriya:patch-cable:2x2', 1066, 3, 1040, 'active', 'c29', 'in_', 28.0, 'out', 16.0]
            """,
        ),
        (
            True,
            "mixers[0].tracks[1]",
            "mixers[0].tracks[2]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -8,6 +8,7 @@
                             <TrackSend 10 target=<Track 4 'B'>>
                         <Track 4 'B'>
                             <TrackSend 11 target=<Track 6 'A1'>>
            +                <TrackSend 12 target=<Track 5 'C'>>
                         <Track 5 'C'>
                     <Mixer 2 'Q'>
                         <Track 9 'D'>
            """,
            """
            --- initial
            +++ mutation
            @@ -56,6 +56,8 @@
                             1039 group (session.mixers[0].tracks[1]:devices)
                             1040 supriya:channel-strip:2 (session.mixers[0].tracks[1]:channel-strip)
                                 active: c29, done_action: 2.0, gain: c30, gate: 1.0, out: 28.0
            +                1066 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].sends[1]:synth)
            +                    active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 28.0, out: 30.0
                             1044 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].sends[0]:synth)
                                 active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 28.0, out: 22.0
                             1042 supriya:meters:2 (session.mixers[0].tracks[1]:output-levels)
            """,
            """
            - ['/s_new', 'supriya:patch-cable:2x2', 1066, 3, 1040, 'active', 'c29', 'in_', 28.0, 'out', 30.0]
            """,
        ),
        (
            False,
            "mixers[0].tracks[1]",
            "mixers[0].tracks[2]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -8,6 +8,7 @@
                             <TrackSend 10 target=<Track 4 'B'>>
                         <Track 4 'B'>
                             <TrackSend 11 target=<Track 6 'A1'>>
            +                <TrackSend 12 target=<Track 5 'C'>>
                         <Track 5 'C'>
                     <Mixer 2 'Q'>
                         <Track 9 'D'>
            """,
            """
            --- initial
            +++ mutation
            @@ -54,6 +54,8 @@
                             1041 supriya:meters:2 (session.mixers[0].tracks[1]:input-levels)
                                 in_: 28.0, out: 31.0
                             1039 group (session.mixers[0].tracks[1]:devices)
            +                1066 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].sends[1]:synth)
            +                    active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 28.0, out: 30.0
                             1040 supriya:channel-strip:2 (session.mixers[0].tracks[1]:channel-strip)
                                 active: c29, done_action: 2.0, gain: c30, gate: 1.0, out: 28.0
                             1044 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].sends[0]:synth)
            """,
            """
            - ['/s_new', 'supriya:patch-cable:2x2', 1066, 2, 1040, 'active', 'c29', 'in_', 28.0, 'out', 30.0]
            """,
        ),
        (
            False,
            "mixers[0].tracks[1]",
            "mixers[0].tracks[1]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -8,6 +8,7 @@
                             <TrackSend 10 target=<Track 4 'B'>>
                         <Track 4 'B'>
                             <TrackSend 11 target=<Track 6 'A1'>>
            +                <TrackSend 12 target=<Track 4 'B'>>
                         <Track 5 'C'>
                     <Mixer 2 'Q'>
                         <Track 9 'D'>
            """,
            """
            --- initial
            +++ mutation
            @@ -50,10 +50,14 @@
                             1013 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:output)
                                 active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
                         1037 group (session.mixers[0].tracks[1]:group)
            +                1067 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[1]:feedback)
            +                    active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 36.0, out: 28.0
                             1038 group (session.mixers[0].tracks[1]:tracks)
                             1041 supriya:meters:2 (session.mixers[0].tracks[1]:input-levels)
                                 in_: 28.0, out: 31.0
                             1039 group (session.mixers[0].tracks[1]:devices)
            +                1066 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].sends[1]:synth)
            +                    active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 28.0, out: 36.0
                             1040 supriya:channel-strip:2 (session.mixers[0].tracks[1]:channel-strip)
                                 active: c29, done_action: 2.0, gain: c30, gate: 1.0, out: 28.0
                             1044 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].sends[0]:synth)
            """,
            """
            - ['/s_new', 'supriya:patch-cable:2x2', 1066, 2, 1040, 'active', 'c29', 'in_', 28.0, 'out', 36.0]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1067, 0, 1037, 'active', 'c29', 'in_', 36.0, 'out', 28.0]
            """,
        ),
        (
            True,
            "mixers[0].tracks[2]",
            "mixers[0].tracks[1]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -9,5 +9,6 @@
                         <Track 4 'B'>
                             <TrackSend 11 target=<Track 6 'A1'>>
                         <Track 5 'C'>
            +                <TrackSend 12 target=<Track 4 'B'>>
                     <Mixer 2 'Q'>
                         <Track 9 'D'>
            """,
            """
            --- initial
            +++ mutation
            @@ -50,6 +50,8 @@
                             1013 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:output)
                                 active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
                         1037 group (session.mixers[0].tracks[1]:group)
            +                1067 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[1]:feedback)
            +                    active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 36.0, out: 28.0
                             1038 group (session.mixers[0].tracks[1]:tracks)
                             1041 supriya:meters:2 (session.mixers[0].tracks[1]:input-levels)
                                 in_: 28.0, out: 31.0
            @@ -69,6 +71,8 @@
                             1047 group (session.mixers[0].tracks[2]:devices)
                             1048 supriya:channel-strip:2 (session.mixers[0].tracks[2]:channel-strip)
                                 active: c35, done_action: 2.0, gain: c36, gate: 1.0, out: 30.0
            +                1066 supriya:patch-cable:2x2 (session.mixers[0].tracks[2].sends[0]:synth)
            +                    active: c35, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 30.0, out: 36.0
                             1050 supriya:meters:2 (session.mixers[0].tracks[2]:output-levels)
                                 in_: 30.0, out: 39.0
                             1051 supriya:patch-cable:2x2 (session.mixers[0].tracks[2]:output)
            """,
            """
            - ['/s_new', 'supriya:patch-cable:2x2', 1066, 3, 1048, 'active', 'c35', 'in_', 30.0, 'out', 36.0]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1067, 0, 1037, 'active', 'c29', 'in_', 36.0, 'out', 28.0]
            """,
        ),
        (
            True,
            "mixers[0].tracks[1]",
            "mixers[1].tracks[0]",
            pytest.raises(RuntimeError),
            "",
            "",
            "",
        ),
    ],
)
@pytest.mark.asyncio
async def test_Track_add_send(
    complex_session: tuple[Session, str, str],
    expected_components_diff: str,
    expected_messages: str,
    expected_tree_diff: str,
    maybe_raises,
    online: bool,
    postfader: bool,
    source: str,
    target: str,
) -> None:
    # Pre-conditions
    print("Pre-conditions")
    session, initial_components, initial_tree = complex_session
    if online:
        await session.boot()
        await session.sync()
    source_ = session[source]
    target_ = session[target]
    assert isinstance(source_, Track)
    assert isinstance(target_, TrackContainer)
    if online:
        await debug_tree(session)
    send: TrackSend | None = None
    # Operation
    print("Operation")
    with maybe_raises, capture(session["mixers[0]"].context) as messages:
        send = await source_.add_send(postfader=postfader, target=target_)
    # Post-conditions
    print("Post-conditions")
    if send is not None:
        assert isinstance(send, TrackSend)
        assert send in source_.sends
        assert send.parent is source_
        assert send.postfader == postfader
        assert send.target is target_
        assert source_.sends[-1] is send
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
    "target, commands, expected_components_diff, expected_tree_diff, expected_messages",
    [
        # just a track
        (
            "mixers[0].tracks[0]",
            [],
            """
            --- initial
            +++ mutation
            @@ -1,4 +1,3 @@
             <Session 0>
                 <session.contexts[0]>
                     <Mixer 1 'P'>
            -            <Track 2 'A'>
            """,
            """
            --- initial
            +++ mutation
            @@ -7,11 +7,11 @@
                                 in_: 18.0, out: 7.0
                             1009 group
                             1010 supriya:channel-strip:2
            -                    active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
            +                    active: c5, done_action: 14.0, gain: c6, gate: 0.0, out: 18.0
                             1012 supriya:meters:2
                                 in_: 18.0, out: 9.0
                             1013 supriya:patch-cable:2x2
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 16.0
                     1004 supriya:meters:2
                         in_: 16.0, out: 1.0
                     1002 group
            """,
            """
            - [None, [['/n_set', 1007, 'gate', 0.0], ['/n_set', 1010, 'done_action', 14.0]]]
            """,
        ),
        # parent track with child
        (
            "mixers[0].tracks[0]",
            [
                ("mixers[0].tracks[0]", "add_track", "B"),
            ],
            """
            --- initial
            +++ mutation
            @@ -1,5 +1,3 @@
             <Session 0>
                 <session.contexts[0]>
                     <Mixer 1 'P'>
            -            <Track 2 'A'>
            -                <Track 3 'B'>
            """,
            """
            --- initial
            +++ mutation
            @@ -9,20 +9,20 @@
                                         in_: 20.0, out: 13.0
                                     1016 group
                                     1017 supriya:channel-strip:2
            -                            active: c11, done_action: 2.0, gain: c12, gate: 1.0, out: 20.0
            +                            active: c11, done_action: 2.0, gain: c12, gate: 0.0, out: 20.0
                                     1019 supriya:meters:2
                                         in_: 20.0, out: 15.0
                                     1020 supriya:patch-cable:2x2
            -                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 18.0
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 18.0
                             1011 supriya:meters:2
                                 in_: 18.0, out: 7.0
                             1009 group
                             1010 supriya:channel-strip:2
            -                    active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
            +                    active: c5, done_action: 14.0, gain: c6, gate: 0.0, out: 18.0
                             1012 supriya:meters:2
                                 in_: 18.0, out: 9.0
                             1013 supriya:patch-cable:2x2
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 16.0
                     1004 supriya:meters:2
                         in_: 16.0, out: 1.0
                     1002 group
            """,
            """
            - [None, [['/n_set', 1007, 'gate', 0.0], ['/n_set', 1010, 'done_action', 14.0]]]
            """,
        ),
        # in-tree send to self
        (
            "mixers[0].tracks[0]",
            [("mixers[0].tracks[0]", "add_send", "mixers[0].tracks[0]")],
            """
            --- initial
            +++ mutation
            @@ -1,5 +1,3 @@
             <Session 0>
                 <session.contexts[0]>
                     <Mixer 1 'P'>
            -            <Track 2 'A'>
            -                <TrackSend 3 target=<Track 2 'A'>>
            """,
            """
            --- initial
            +++ mutation
            @@ -3,19 +3,19 @@
                     1001 group
                         1007 group
                             1014 supriya:fb-patch-cable:2x2
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 18.0
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 18.0
                             1008 group
                             1011 supriya:meters:2
                                 in_: 18.0, out: 7.0
                             1009 group
                             1010 supriya:channel-strip:2
            -                    active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
            +                    active: c5, done_action: 14.0, gain: c6, gate: 0.0, out: 18.0
                             1015 supriya:patch-cable:2x2
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 20.0
                             1012 supriya:meters:2
                                 in_: 18.0, out: 9.0
                             1013 supriya:patch-cable:2x2
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 16.0
                     1004 supriya:meters:2
                         in_: 16.0, out: 1.0
                     1002 group
            """,
            """
            - [None, [['/n_set', 1007, 'gate', 0.0], ['/n_set', 1010, 'done_action', 14.0], ['/n_set', 1014, 'gate', 0.0]]]
            """,
        ),
        # in-tree send to out-of-tree stack
        (
            "mixers[0].tracks[1]",
            [
                ("mixers[0]", "add_track", "B"),
                ("mixers[0].tracks[1]", "add_send", "mixers[0].tracks[0]"),
            ],
            """
            --- initial
            +++ mutation
            @@ -2,5 +2,3 @@
                 <session.contexts[0]>
                     <Mixer 1 'P'>
                         <Track 2 'A'>
            -            <Track 3 'B'>
            -                <TrackSend 4 target=<Track 2 'A'>>
            """,
            """
            --- initial
            +++ mutation
            @@ -3,7 +3,7 @@
                     1001 group
                         1007 group
                             1014 supriya:fb-patch-cable:2x2
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 18.0
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 18.0
                             1008 group
                             1011 supriya:meters:2
                                 in_: 18.0, out: 7.0
            @@ -20,13 +20,13 @@
                                 in_: 22.0, out: 13.0
                             1017 group
                             1018 supriya:channel-strip:2
            -                    active: c11, done_action: 2.0, gain: c12, gate: 1.0, out: 22.0
            +                    active: c11, done_action: 14.0, gain: c12, gate: 0.0, out: 22.0
                             1022 supriya:patch-cable:2x2
            -                    active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 20.0
            +                    active: c11, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 22.0, out: 20.0
                             1020 supriya:meters:2
                                 in_: 22.0, out: 15.0
                             1021 supriya:patch-cable:2x2
            -                    active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 16.0
            +                    active: c11, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 22.0, out: 16.0
                     1004 supriya:meters:2
                         in_: 16.0, out: 1.0
                     1002 group
            """,
            """
            - [None, [['/n_set', 1015, 'gate', 0.0], ['/n_set', 1018, 'done_action', 14.0]]]
            - ['/n_set', 1014, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        # out-of-tree send to in-tree track
        (
            "mixers[0].tracks[1]",
            [
                ("mixers[0]", "add_track", "B"),
                ("mixers[0].tracks[0]", "add_send", "mixers[0].tracks[1]"),
            ],
            """
            --- initial
            +++ mutation
            @@ -2,5 +2,3 @@
                 <session.contexts[0]>
                     <Mixer 1 'P'>
                         <Track 2 'A'>
            -                <TrackSend 4 target=<Track 3 'B'>>
            -            <Track 3 'B'>
            """,
            """
            --- initial
            +++ mutation
            @@ -9,7 +9,7 @@
                             1010 supriya:channel-strip:2
                                 active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
                             1014 supriya:patch-cable:2x2
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 20.0
                             1012 supriya:meters:2
                                 in_: 18.0, out: 9.0
                             1013 supriya:patch-cable:2x2
            @@ -20,11 +20,11 @@
                                 in_: 20.0, out: 13.0
                             1017 group
                             1018 supriya:channel-strip:2
            -                    active: c11, done_action: 2.0, gain: c12, gate: 1.0, out: 20.0
            +                    active: c11, done_action: 14.0, gain: c12, gate: 0.0, out: 20.0
                             1020 supriya:meters:2
                                 in_: 20.0, out: 15.0
                             1021 supriya:patch-cable:2x2
            -                    active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
            +                    active: c11, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 16.0
                     1004 supriya:meters:2
                         in_: 16.0, out: 1.0
                     1002 group
            """,
            """
            - [None, [['/n_set', 1015, 'gate', 0.0], ['/n_set', 1018, 'done_action', 14.0]]]
            - ['/n_set', 1014, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        # out-of-tree send to in-tree child track
        (
            "mixers[0].tracks[1]",
            [
                ("mixers[0]", "add_track", "B"),
                ("mixers[0].tracks[1]", "add_track", "C"),
                ("mixers[0].tracks[0]", "add_send", "mixers[0].tracks[1].tracks[0]"),
            ],
            """
            --- initial
            +++ mutation
            @@ -2,6 +2,3 @@
                 <session.contexts[0]>
                     <Mixer 1 'P'>
                         <Track 2 'A'>
            -                <TrackSend 5 target=<Track 4 'C'>>
            -            <Track 3 'B'>
            -                <Track 4 'C'>
            """,
            """
            --- initial
            +++ mutation
            @@ -9,7 +9,7 @@
                             1010 supriya:channel-strip:2
                                 active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
                             1014 supriya:patch-cable:2x2
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 22.0
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 22.0
                             1012 supriya:meters:2
                                 in_: 18.0, out: 9.0
                             1013 supriya:patch-cable:2x2
            @@ -22,20 +22,20 @@
                                         in_: 22.0, out: 19.0
                                     1024 group
                                     1025 supriya:channel-strip:2
            -                            active: c17, done_action: 2.0, gain: c18, gate: 1.0, out: 22.0
            +                            active: c17, done_action: 2.0, gain: c18, gate: 0.0, out: 22.0
                                     1027 supriya:meters:2
                                         in_: 22.0, out: 21.0
                                     1028 supriya:patch-cable:2x2
            -                            active: c17, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 20.0
            +                            active: c17, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 22.0, out: 20.0
                             1019 supriya:meters:2
                                 in_: 20.0, out: 13.0
                             1017 group
                             1018 supriya:channel-strip:2
            -                    active: c11, done_action: 2.0, gain: c12, gate: 1.0, out: 20.0
            +                    active: c11, done_action: 14.0, gain: c12, gate: 0.0, out: 20.0
                             1020 supriya:meters:2
                                 in_: 20.0, out: 15.0
                             1021 supriya:patch-cable:2x2
            -                    active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
            +                    active: c11, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 16.0
                     1004 supriya:meters:2
                         in_: 16.0, out: 1.0
                     1002 group
            """,
            """
            - [None, [['/n_set', 1015, 'gate', 0.0], ['/n_set', 1018, 'done_action', 14.0]]]
            - ['/n_set', 1014, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        # out-of-tree track output
        (
            "mixers[0].tracks[1]",
            [
                ("mixers[0]", "add_track", "B"),
                ("mixers[0].tracks[0]", "set_output", "mixers[0].tracks[1]"),
            ],
            """
            --- initial
            +++ mutation
            @@ -2,4 +2,3 @@
                 <session.contexts[0]>
                     <Mixer 1 'P'>
                         <Track 2 'A'>
            -            <Track 3 'B'>
            """,
            """
            --- initial
            +++ mutation
            @@ -11,18 +11,18 @@
                             1012 supriya:meters:2
                                 in_: 18.0, out: 9.0
                             1013 supriya:patch-cable:2x2
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 16.0
                         1014 group
                             1015 group
                             1018 supriya:meters:2
                                 in_: 20.0, out: 13.0
                             1016 group
                             1017 supriya:channel-strip:2
            -                    active: c11, done_action: 2.0, gain: c12, gate: 1.0, out: 20.0
            +                    active: c11, done_action: 14.0, gain: c12, gate: 0.0, out: 20.0
                             1019 supriya:meters:2
                                 in_: 20.0, out: 15.0
                             1020 supriya:patch-cable:2x2
            -                    active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
            +                    active: c11, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 16.0
                     1004 supriya:meters:2
                         in_: 16.0, out: 1.0
                     1002 group
            """,
            """
            - [None, [['/n_set', 1014, 'gate', 0.0], ['/n_set', 1017, 'done_action', 14.0]]]
            - ['/n_set', 1013, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        # out-of-tree track input
        (
            "mixers[0].tracks[1]",
            [
                ("mixers[0]", "add_track", "B"),
                ("mixers[0].tracks[0]", "set_input", "mixers[0].tracks[1]"),
            ],
            """
            --- initial
            +++ mutation
            @@ -2,4 +2,3 @@
                 <session.contexts[0]>
                     <Mixer 1 'P'>
                         <Track 2 'A'>
            -            <Track 3 'B'>
            """,
            """
            --- initial
            +++ mutation
            @@ -3,7 +3,7 @@
                     1001 group
                         1007 group
                             1013 supriya:fb-patch-cable:2x2
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 18.0
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 18.0
                             1008 group
                             1011 supriya:meters:2
                                 in_: 18.0, out: 7.0
            @@ -20,11 +20,11 @@
                                 in_: 20.0, out: 13.0
                             1017 group
                             1018 supriya:channel-strip:2
            -                    active: c11, done_action: 2.0, gain: c12, gate: 1.0, out: 20.0
            +                    active: c11, done_action: 14.0, gain: c12, gate: 0.0, out: 20.0
                             1020 supriya:meters:2
                                 in_: 20.0, out: 15.0
                             1021 supriya:patch-cable:2x2
            -                    active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
            +                    active: c11, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 16.0
                     1004 supriya:meters:2
                         in_: 16.0, out: 1.0
                     1002 group
            """,
            """
            - [None, [['/n_set', 1015, 'gate', 0.0], ['/n_set', 1018, 'done_action', 14.0]]]
            - ['/n_set', 1013, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_Track_delete(
    basic_session: tuple[Session, str, str],
    commands: list[tuple[str, str, str | None]],
    expected_components_diff: str,
    expected_tree_diff: str,
    expected_messages: str,
    online: bool,
    target: str,
) -> None:
    # TODO: rewrite this with complex_session and track lookups
    # Pre-conditions
    print("Pre-conditions")
    session, _, _ = basic_session
    for command in commands:
        procedure = getattr(session[command[0]], command[1])
        if command[2]:
            if session._PATH_REGEX.match(command[2]):
                await procedure(session[command[2]])
            else:
                await procedure(command[2])
        else:
            await procedure()
    if online:
        await session.boot()
        await session.sync()
        initial_tree = await debug_tree(session, annotated=False)
    initial_components = debug_components(session)
    target_ = session[target]
    assert isinstance(target_, Track)
    parent_ = target_.parent
    # Operation
    print("Operation")
    with capture(session["mixers[0]"].context) as messages:
        await target_.delete()
    # Post-conditions
    print("Post-conditions")
    if online:
        actual_tree_diff = await compute_tree_diff(
            session,
            initial_tree,
            annotated=False,
        )
        assert actual_tree_diff == normalize(expected_tree_diff)
        assert format_messages(messages) == normalize(expected_messages)
    assert parent_ and target_ not in parent_.children
    assert_components_diff(session, expected_components_diff, initial_components)


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "target, parent, index, maybe_raises, expected_graph_order, expected_components_diff, expected_tree_diff, expected_messages",
    [
        (
            "mixers[0].tracks[0]",
            "mixers[0]",
            1,
            does_not_raise,
            (0, 1),
            """
            --- initial
            +++ mutation
            @@ -1,13 +1,13 @@
             <Session 0>
                 <session.contexts[0]>
                     <Mixer 1 'P'>
            +            <Track 4 'B'>
            +                <TrackSend 11 target=<Track 6 'A1'>>
                         <Track 3 'A'>
                             <Track 6 'A1'>
                                 <Track 8 'A11'>
                             <Track 7 'A2'>
                             <TrackSend 10 target=<Track 4 'B'>>
            -            <Track 4 'B'>
            -                <TrackSend 11 target=<Track 6 'A1'>>
                         <Track 5 'C'>
                     <Mixer 2 'Q'>
                         <Track 9 'D'>
            """,
            """
            --- initial
            +++ mutation
            @@ -1,6 +1,21 @@
             <session.contexts[0]>
                 NODE TREE 1000 group
                     1001 group
            +            1037 group
            +                1066 supriya:fb-patch-cable:2x2
            +                    active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 36.0, out: 28.0
            +                1038 group
            +                1041 supriya:meters:2
            +                    in_: 28.0, out: 31.0
            +                1039 group
            +                1040 supriya:channel-strip:2
            +                    active: c29, done_action: 2.0, gain: c30, gate: 1.0, out: 28.0
            +                1044 supriya:patch-cable:2x2
            +                    active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 28.0, out: 22.0
            +                1042 supriya:meters:2
            +                    in_: 28.0, out: 33.0
            +                1043 supriya:patch-cable:2x2
            +                    active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 28.0, out: 16.0
                         1007 group
                             1008 group
                                 1014 group
            @@ -49,19 +64,6 @@
                                 in_: 18.0, out: 9.0
                             1013 supriya:patch-cable:2x2
                                 active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            -            1037 group
            -                1038 group
            -                1041 supriya:meters:2
            -                    in_: 28.0, out: 31.0
            -                1039 group
            -                1040 supriya:channel-strip:2
            -                    active: c29, done_action: 2.0, gain: c30, gate: 1.0, out: 28.0
            -                1044 supriya:patch-cable:2x2
            -                    active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 28.0, out: 22.0
            -                1042 supriya:meters:2
            -                    in_: 28.0, out: 33.0
            -                1043 supriya:patch-cable:2x2
            -                    active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 28.0, out: 16.0
                         1045 group
                             1046 group
                             1049 supriya:meters:2
            """,
            # TODO: The /g_head is redundant, but not sure how to get rid of it
            # as tracks have no knowledge of the change to the other tracks.
            """
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1066, 0, 1037, 'active', 'c29', 'in_', 36.0, 'out', 28.0]
            - ['/n_after', 1007, 1037]
            - ['/g_head', 1001, 1037]
            """,
        ),
        (
            "mixers[0].tracks[0]",
            "mixers[0].tracks[0].tracks[0]",
            0,
            pytest.raises(RuntimeError),
            (0, 0),
            "",
            "",
            "",
        ),
        (
            "mixers[0].tracks[1]",
            "mixers[0]",
            0,
            does_not_raise,
            (0, 0),
            """
            --- initial
            +++ mutation
            @@ -1,13 +1,13 @@
             <Session 0>
                 <session.contexts[0]>
                     <Mixer 1 'P'>
            +            <Track 4 'B'>
            +                <TrackSend 11 target=<Track 6 'A1'>>
                         <Track 3 'A'>
                             <Track 6 'A1'>
                                 <Track 8 'A11'>
                             <Track 7 'A2'>
                             <TrackSend 10 target=<Track 4 'B'>>
            -            <Track 4 'B'>
            -                <TrackSend 11 target=<Track 6 'A1'>>
                         <Track 5 'C'>
                     <Mixer 2 'Q'>
                         <Track 9 'D'>
            """,
            """
            --- initial
            +++ mutation
            @@ -1,11 +1,26 @@
             <session.contexts[0]>
                 NODE TREE 1000 group
                     1001 group
            +            1037 group
            +                1066 supriya:fb-patch-cable:2x2
            +                    active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 36.0, out: 28.0
            +                1038 group
            +                1041 supriya:meters:2
            +                    in_: 28.0, out: 31.0
            +                1039 group
            +                1040 supriya:channel-strip:2
            +                    active: c29, done_action: 2.0, gain: c30, gate: 1.0, out: 28.0
            +                1044 supriya:patch-cable:2x2
            +                    active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 28.0, out: 22.0
            +                1042 supriya:meters:2
            +                    in_: 28.0, out: 33.0
            +                1043 supriya:patch-cable:2x2
            +                    active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 28.0, out: 16.0
                         1007 group
                             1008 group
                                 1014 group
                                     1021 supriya:fb-patch-cable:2x2
            -                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 20.0
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 22.0, out: 20.0
                                     1015 group
                                         1022 group
                                             1023 group
            @@ -49,19 +64,6 @@
                                 in_: 18.0, out: 9.0
                             1013 supriya:patch-cable:2x2
                                 active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            -            1037 group
            -                1038 group
            -                1041 supriya:meters:2
            -                    in_: 28.0, out: 31.0
            -                1039 group
            -                1040 supriya:channel-strip:2
            -                    active: c29, done_action: 2.0, gain: c30, gate: 1.0, out: 28.0
            -                1044 supriya:patch-cable:2x2
            -                    active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 28.0, out: 22.0
            -                1042 supriya:meters:2
            -                    in_: 28.0, out: 33.0
            -                1043 supriya:patch-cable:2x2
            -                    active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 28.0, out: 16.0
                         1045 group
                             1046 group
                             1049 supriya:meters:2
            """,
            """
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1066, 0, 1037, 'active', 'c29', 'in_', 36.0, 'out', 28.0]
            - ['/g_head', 1001, 1037]
            - ['/n_set', 1021, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        ("mixers[0].tracks[1]", "mixers[0]", 1, does_not_raise, (0, 1), "", "", ""),
        (
            "mixers[0].tracks[1]",
            "mixers[0]",
            2,
            does_not_raise,
            (0, 2),
            """
            --- initial
            +++ mutation
            @@ -6,8 +6,8 @@
                                 <Track 8 'A11'>
                             <Track 7 'A2'>
                             <TrackSend 10 target=<Track 4 'B'>>
            +            <Track 5 'C'>
                         <Track 4 'B'>
                             <TrackSend 11 target=<Track 6 'A1'>>
            -            <Track 5 'C'>
                     <Mixer 2 'Q'>
                         <Track 9 'D'>
            """,
            """
            --- initial
            +++ mutation
            @@ -49,6 +49,17 @@
                                 in_: 18.0, out: 9.0
                             1013 supriya:patch-cable:2x2
                                 active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            +            1045 group
            +                1046 group
            +                1049 supriya:meters:2
            +                    in_: 30.0, out: 37.0
            +                1047 group
            +                1048 supriya:channel-strip:2
            +                    active: c35, done_action: 2.0, gain: c36, gate: 1.0, out: 30.0
            +                1050 supriya:meters:2
            +                    in_: 30.0, out: 39.0
            +                1051 supriya:patch-cable:2x2
            +                    active: c35, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 30.0, out: 16.0
                         1037 group
                             1038 group
                             1041 supriya:meters:2
            @@ -62,17 +73,6 @@
                                 in_: 28.0, out: 33.0
                             1043 supriya:patch-cable:2x2
                                 active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 28.0, out: 16.0
            -            1045 group
            -                1046 group
            -                1049 supriya:meters:2
            -                    in_: 30.0, out: 37.0
            -                1047 group
            -                1048 supriya:channel-strip:2
            -                    active: c35, done_action: 2.0, gain: c36, gate: 1.0, out: 30.0
            -                1050 supriya:meters:2
            -                    in_: 30.0, out: 39.0
            -                1051 supriya:patch-cable:2x2
            -                    active: c35, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 30.0, out: 16.0
                     1004 supriya:meters:2
                         in_: 16.0, out: 1.0
                     1002 group
            """,
            """
            - ['/n_after', 1037, 1045]
            """,
        ),
        (
            "mixers[0].tracks[1]",
            "mixers[0]",
            3,
            pytest.raises(RuntimeError),
            (0, 1),
            "",
            "",
            "",
        ),
        (
            "mixers[0].tracks[1]",
            "mixers[0].tracks[0]",
            0,
            does_not_raise,
            (0, 0, 0),
            """
            --- initial
            +++ mutation
            @@ -2,12 +2,12 @@
                 <session.contexts[0]>
                     <Mixer 1 'P'>
                         <Track 3 'A'>
            +                <Track 4 'B'>
            +                    <TrackSend 11 target=<Track 6 'A1'>>
                             <Track 6 'A1'>
                                 <Track 8 'A11'>
                             <Track 7 'A2'>
                             <TrackSend 10 target=<Track 4 'B'>>
            -            <Track 4 'B'>
            -                <TrackSend 11 target=<Track 6 'A1'>>
                         <Track 5 'C'>
                     <Mixer 2 'Q'>
                         <Track 9 'D'>
            """,
            """
            --- initial
            +++ mutation
            @@ -3,9 +3,24 @@
                     1001 group
                         1007 group
                             1008 group
            +                    1037 group
            +                        1066 supriya:fb-patch-cable:2x2
            +                            active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 36.0, out: 28.0
            +                        1038 group
            +                        1041 supriya:meters:2
            +                            in_: 28.0, out: 31.0
            +                        1039 group
            +                        1040 supriya:channel-strip:2
            +                            active: c29, done_action: 2.0, gain: c30, gate: 1.0, out: 28.0
            +                        1044 supriya:patch-cable:2x2
            +                            active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 28.0, out: 22.0
            +                        1042 supriya:meters:2
            +                            in_: 28.0, out: 33.0
            +                        1043 supriya:patch-cable:2x2
            +                            active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 28.0, out: 16.0
                                 1014 group
                                     1021 supriya:fb-patch-cable:2x2
            -                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 20.0
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 22.0, out: 20.0
                                     1015 group
                                         1022 group
                                             1023 group
            @@ -49,19 +64,6 @@
                                 in_: 18.0, out: 9.0
                             1013 supriya:patch-cable:2x2
                                 active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            -            1037 group
            -                1038 group
            -                1041 supriya:meters:2
            -                    in_: 28.0, out: 31.0
            -                1039 group
            -                1040 supriya:channel-strip:2
            -                    active: c29, done_action: 2.0, gain: c30, gate: 1.0, out: 28.0
            -                1044 supriya:patch-cable:2x2
            -                    active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 28.0, out: 22.0
            -                1042 supriya:meters:2
            -                    in_: 28.0, out: 33.0
            -                1043 supriya:patch-cable:2x2
            -                    active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 28.0, out: 16.0
                         1045 group
                             1046 group
                             1049 supriya:meters:2
            """,
            """
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1066, 0, 1037, 'active', 'c29', 'in_', 36.0, 'out', 28.0]
            - ['/g_head', 1008, 1037]
            - ['/n_after', 1014, 1037]
            - ['/n_set', 1021, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        (
            "mixers[0].tracks[1]",
            "mixers[0].tracks[0].tracks[0]",
            0,
            does_not_raise,
            (0, 0, 0, 0),
            """
            --- initial
            +++ mutation
            @@ -3,11 +3,11 @@
                     <Mixer 1 'P'>
                         <Track 3 'A'>
                             <Track 6 'A1'>
            +                    <Track 4 'B'>
            +                        <TrackSend 11 target=<Track 6 'A1'>>
                                 <Track 8 'A11'>
                             <Track 7 'A2'>
                             <TrackSend 10 target=<Track 4 'B'>>
            -            <Track 4 'B'>
            -                <TrackSend 11 target=<Track 6 'A1'>>
                         <Track 5 'C'>
                     <Mixer 2 'Q'>
                         <Track 9 'D'>
            """,
            """
            --- initial
            +++ mutation
            @@ -5,8 +5,23 @@
                             1008 group
                                 1014 group
                                     1021 supriya:fb-patch-cable:2x2
            -                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 20.0
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 22.0, out: 20.0
                                     1015 group
            +                            1037 group
            +                                1066 supriya:fb-patch-cable:2x2
            +                                    active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 36.0, out: 28.0
            +                                1038 group
            +                                1041 supriya:meters:2
            +                                    in_: 28.0, out: 31.0
            +                                1039 group
            +                                1040 supriya:channel-strip:2
            +                                    active: c29, done_action: 2.0, gain: c30, gate: 1.0, out: 28.0
            +                                1044 supriya:patch-cable:2x2
            +                                    active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 28.0, out: 22.0
            +                                1042 supriya:meters:2
            +                                    in_: 28.0, out: 33.0
            +                                1043 supriya:patch-cable:2x2
            +                                    active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 28.0, out: 16.0
                                         1022 group
                                             1023 group
                                             1026 supriya:meters:2
            @@ -49,19 +64,6 @@
                                 in_: 18.0, out: 9.0
                             1013 supriya:patch-cable:2x2
                                 active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            -            1037 group
            -                1038 group
            -                1041 supriya:meters:2
            -                    in_: 28.0, out: 31.0
            -                1039 group
            -                1040 supriya:channel-strip:2
            -                    active: c29, done_action: 2.0, gain: c30, gate: 1.0, out: 28.0
            -                1044 supriya:patch-cable:2x2
            -                    active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 28.0, out: 22.0
            -                1042 supriya:meters:2
            -                    in_: 28.0, out: 33.0
            -                1043 supriya:patch-cable:2x2
            -                    active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 28.0, out: 16.0
                         1045 group
                             1046 group
                             1049 supriya:meters:2
            """,
            """
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1066, 0, 1037, 'active', 'c29', 'in_', 36.0, 'out', 28.0]
            - ['/g_head', 1015, 1037]
            - ['/n_set', 1021, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        (
            "mixers[0].tracks[1]",
            "mixers[0].tracks[1]",
            0,
            pytest.raises(RuntimeError),
            (0, 1),
            "",
            "",
            "",
        ),
        (
            "mixers[0].tracks[1]",
            "mixers[0].tracks[2]",
            0,
            does_not_raise,
            (0, 1, 0),
            """
            --- initial
            +++ mutation
            @@ -6,8 +6,8 @@
                                 <Track 8 'A11'>
                             <Track 7 'A2'>
                             <TrackSend 10 target=<Track 4 'B'>>
            -            <Track 4 'B'>
            -                <TrackSend 11 target=<Track 6 'A1'>>
                         <Track 5 'C'>
            +                <Track 4 'B'>
            +                    <TrackSend 11 target=<Track 6 'A1'>>
                     <Mixer 2 'Q'>
                         <Track 9 'D'>
            """,
            """
            --- initial
            +++ mutation
            @@ -49,21 +49,21 @@
                                 in_: 18.0, out: 9.0
                             1013 supriya:patch-cable:2x2
                                 active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            -            1037 group
            -                1038 group
            -                1041 supriya:meters:2
            -                    in_: 28.0, out: 31.0
            -                1039 group
            -                1040 supriya:channel-strip:2
            -                    active: c29, done_action: 2.0, gain: c30, gate: 1.0, out: 28.0
            -                1044 supriya:patch-cable:2x2
            -                    active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 28.0, out: 22.0
            -                1042 supriya:meters:2
            -                    in_: 28.0, out: 33.0
            -                1043 supriya:patch-cable:2x2
            -                    active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 28.0, out: 16.0
                         1045 group
                             1046 group
            +                    1037 group
            +                        1038 group
            +                        1041 supriya:meters:2
            +                            in_: 28.0, out: 31.0
            +                        1039 group
            +                        1040 supriya:channel-strip:2
            +                            active: c29, done_action: 2.0, gain: c30, gate: 1.0, out: 28.0
            +                        1044 supriya:patch-cable:2x2
            +                            active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 28.0, out: 22.0
            +                        1042 supriya:meters:2
            +                            in_: 28.0, out: 33.0
            +                        1043 supriya:patch-cable:2x2
            +                            active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 28.0, out: 16.0
                             1049 supriya:meters:2
                                 in_: 30.0, out: 37.0
                             1047 group
            """,
            """
            - ['/g_head', 1046, 1037]
            - ['/n_after', 1045, 1007]
            """,
        ),
        (
            "mixers[0].tracks[2]",
            "mixers[0]",
            0,
            does_not_raise,
            (0, 0),
            """
            --- initial
            +++ mutation
            @@ -1,6 +1,7 @@
             <Session 0>
                 <session.contexts[0]>
                     <Mixer 1 'P'>
            +            <Track 5 'C'>
                         <Track 3 'A'>
                             <Track 6 'A1'>
                                 <Track 8 'A11'>
            @@ -8,6 +9,5 @@
                             <TrackSend 10 target=<Track 4 'B'>>
                         <Track 4 'B'>
                             <TrackSend 11 target=<Track 6 'A1'>>
            -            <Track 5 'C'>
                     <Mixer 2 'Q'>
                         <Track 9 'D'>
            """,
            """
            --- initial
            +++ mutation
            @@ -1,6 +1,17 @@
             <session.contexts[0]>
                 NODE TREE 1000 group
                     1001 group
            +            1045 group
            +                1046 group
            +                1049 supriya:meters:2
            +                    in_: 30.0, out: 37.0
            +                1047 group
            +                1048 supriya:channel-strip:2
            +                    active: c35, done_action: 2.0, gain: c36, gate: 1.0, out: 30.0
            +                1050 supriya:meters:2
            +                    in_: 30.0, out: 39.0
            +                1051 supriya:patch-cable:2x2
            +                    active: c35, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 30.0, out: 16.0
                         1007 group
                             1008 group
                                 1014 group
            @@ -62,17 +73,6 @@
                                 in_: 28.0, out: 33.0
                             1043 supriya:patch-cable:2x2
                                 active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 28.0, out: 16.0
            -            1045 group
            -                1046 group
            -                1049 supriya:meters:2
            -                    in_: 30.0, out: 37.0
            -                1047 group
            -                1048 supriya:channel-strip:2
            -                    active: c35, done_action: 2.0, gain: c36, gate: 1.0, out: 30.0
            -                1050 supriya:meters:2
            -                    in_: 30.0, out: 39.0
            -                1051 supriya:patch-cable:2x2
            -                    active: c35, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 30.0, out: 16.0
                     1004 supriya:meters:2
                         in_: 16.0, out: 1.0
                     1002 group
            """,
            """
            - ['/g_head', 1001, 1045]
            """,
        ),
        (
            "mixers[0].tracks[1]",
            "mixers[1]",
            0,
            pytest.raises(RuntimeError),
            (0, 1),
            "",
            "",
            "",
        ),
    ],
)
@pytest.mark.asyncio
async def test_Track_move(
    complex_session: tuple[Session, str, str],
    expected_components_diff: str,
    expected_graph_order: list[int],
    expected_messages: str,
    expected_tree_diff: str,
    index: int,
    maybe_raises,
    online: bool,
    parent: str,
    target: str,
) -> None:
    # Pre-conditions
    print("Pre-conditions")
    session, initial_components, _ = complex_session
    if online:
        await session.boot()
        await session.sync()
        initial_tree = await debug_tree(session, annotated=False)
    target_ = session[target]
    parent_ = session[parent]
    assert isinstance(target_, Track)
    assert isinstance(parent_, TrackContainer)
    # Operation
    print("Operation")
    with maybe_raises, capture(session["mixers[0]"].context) as messages:
        await target_.move(index=index, parent=parent_)
    # Post-conditions
    print("Post-conditions")
    assert target_.graph_order == expected_graph_order
    assert_components_diff(session, expected_components_diff, initial_components)
    if not online:
        return
    await assert_tree_diff(
        session,
        expected_tree_diff,
        expected_initial_tree=initial_tree,
        annotated=False,
    )
    assert format_messages(messages) == normalize(expected_messages)


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "source, target, maybe_raises, expected_components_diff, expected_tree_diff, expected_messages",
    [
        # none
        (
            "mixers[0].tracks[0].tracks[0]",
            None,
            does_not_raise,
            "",
            "",
            "",
        ),
        # self
        (
            "mixers[0].tracks[0].tracks[0]",
            "mixers[0].tracks[0].tracks[0]",
            pytest.raises(RuntimeError),
            "",
            "",
            "",
        ),
        # parent
        # TODO: This should feedback, because the reader is calculated before
        #       the writer.
        (
            "mixers[0].tracks[0].tracks[0]",
            "mixers[0].tracks[0]",
            does_not_raise,
            """
            """,
            """
            """,
            """
            """,
        #   """
        #   --- initial
        #   +++ mutation
        #   @@ -6,7 +6,7 @@
        #                    <TrackInput 7 session.mixers[0].tracks[0].input source=null>
        #                    <Track 17 'A1'>
        #                        <TrackFeedback 18 session.mixers[0].tracks[0].tracks[0].feedback>
        #   -                    <TrackInput 19 session.mixers[0].tracks[0].tracks[0].input source=null>
        #   +                    <TrackInput 19 session.mixers[0].tracks[0].tracks[0].input source=session.mixers[0].tracks[0]>
        #                        <Track 25 'A11'>
        #                            <TrackFeedback 26 session.mixers[0].tracks[0].tracks[0].tracks[0].feedback>
        #                            <TrackInput 27 session.mixers[0].tracks[0].tracks[0].tracks[0].input source=null>
        #   """,
        #   """
        #   --- initial
        #   +++ mutation
        #   @@ -6,6 +6,8 @@
        #                        1012 group (session.mixers[0].tracks[0].tracks[0]:group)
        #                            1041 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].feedback:synth)
        #                                active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 28.0, out: 20.0
        #   +                        1066 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].input:synth)
        #   +                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
        #                            1013 group (session.mixers[0].tracks[0].tracks[0]:tracks)
        #                                1018 group (session.mixers[0].tracks[0].tracks[0].tracks[0]:group)
        #                                    1019 group (session.mixers[0].tracks[0].tracks[0].tracks[0]:tracks)
        #   """,
        #   """
        #   - ['/s_new', 'supriya:fb-patch-cable:2x2', 1066, 2, 1013, 'active', 'c11', 'in_', 18.0, 'out', 20.0]
        #   """,
        ),
        # child
        (
            "mixers[0].tracks[0].tracks[0]",
            "mixers[0].tracks[0].tracks[0].tracks[0]",
            does_not_raise,
            """
            """,
            """
            """,
            """
            """,
        #   """
        #   --- initial
        #   +++ mutation
        #   @@ -6,7 +6,7 @@
        #                    <TrackInput 7 session.mixers[0].tracks[0].input source=null>
        #                    <Track 17 'A1'>
        #                        <TrackFeedback 18 session.mixers[0].tracks[0].tracks[0].feedback>
        #   -                    <TrackInput 19 session.mixers[0].tracks[0].tracks[0].input source=null>
        #   +                    <TrackInput 19 session.mixers[0].tracks[0].tracks[0].input source=session.mixers[0].tracks[0].tracks[0].tracks[0]>
        #                        <Track 25 'A11'>
        #                            <TrackFeedback 26 session.mixers[0].tracks[0].tracks[0].tracks[0].feedback>
        #                            <TrackInput 27 session.mixers[0].tracks[0].tracks[0].tracks[0].input source=null>
        #   """,
        #   """
        #   --- initial
        #   +++ mutation
        #   @@ -6,6 +6,8 @@
        #                        1012 group (session.mixers[0].tracks[0].tracks[0]:group)
        #                            1041 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].feedback:synth)
        #                                active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 28.0, out: 20.0
        #   +                        1066 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].input:synth)
        #   +                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 20.0
        #                            1013 group (session.mixers[0].tracks[0].tracks[0]:tracks)
        #                                1018 group (session.mixers[0].tracks[0].tracks[0].tracks[0]:group)
        #                                    1019 group (session.mixers[0].tracks[0].tracks[0].tracks[0]:tracks)
        #   """,
        #   """
        #   - ['/s_new', 'supriya:patch-cable:2x2', 1066, 2, 1013, 'active', 'c11', 'in_', 22.0, 'out', 20.0]
        #   """,
        ),
        # auntie
        # TODO: This should feedback, because the reader is calculated before
        #       the writer.
        (
            "mixers[0].tracks[0].tracks[0]",
            "mixers[0].tracks[1]",
            does_not_raise,
            """
            """,
            """
            """,
            """
            """,
        #   """
        #   --- initial
        #   +++ mutation
        #   @@ -6,7 +6,7 @@
        #                    <TrackInput 7 session.mixers[0].tracks[0].input source=null>
        #                    <Track 17 'A1'>
        #                        <TrackFeedback 18 session.mixers[0].tracks[0].tracks[0].feedback>
        #   -                    <TrackInput 19 session.mixers[0].tracks[0].tracks[0].input source=null>
        #   +                    <TrackInput 19 session.mixers[0].tracks[0].tracks[0].input source=session.mixers[0].tracks[1]>
        #                        <Track 25 'A11'>
        #                            <TrackFeedback 26 session.mixers[0].tracks[0].tracks[0].tracks[0].feedback>
        #                            <TrackInput 27 session.mixers[0].tracks[0].tracks[0].tracks[0].input source=null>
        #   """,
        #   """
        #   --- initial
        #   +++ mutation
        #   @@ -6,6 +6,8 @@
        #                        1012 group (session.mixers[0].tracks[0].tracks[0]:group)
        #                            1041 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].feedback:synth)
        #                                active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 28.0, out: 20.0
        #   +                        1066 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].input:synth)
        #   +                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 26.0, out: 20.0
        #                            1013 group (session.mixers[0].tracks[0].tracks[0]:tracks)
        #                                1018 group (session.mixers[0].tracks[0].tracks[0].tracks[0]:group)
        #                                    1019 group (session.mixers[0].tracks[0].tracks[0].tracks[0]:tracks)
        #   """,
        #   """
        #   - ['/s_new', 'supriya:fb-patch-cable:2x2', 1066, 2, 1013, 'active', 'c11', 'in_', 26.0, 'out', 20.0]
        #   """,
        ),
        # sibling, reversed
        # NOTE: Does not need to feedback.
        (
            "mixers[0].tracks[1]",
            "mixers[0].tracks[0]",
            does_not_raise,
            """
            """,
            """
            """,
            """
            """,
        #   """
        #   --- initial
        #   +++ mutation
        #   @@ -20,7 +20,7 @@
        #                    <TrackSend 33 target=<Track 4 'B'>>
        #                <Track 9 'B'>
        #                    <TrackFeedback 10 session.mixers[0].tracks[1].feedback>
        #   -                <TrackInput 11 session.mixers[0].tracks[1].input source=null>
        #   +                <TrackInput 11 session.mixers[0].tracks[1].input source=session.mixers[0].tracks[0]>
        #                    <TrackOutput 12 session.mixers[0].tracks[1].output target=default>
        #                    <TrackSend 34 target=<Track 6 'A1'>>
        #                <Track 13 'C'>
        #   """,
        #   """
        #   --- initial
        #   +++ mutation
        #   @@ -50,6 +50,8 @@
        #                    1033 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].output:synth)
        #                        active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
        #                1034 group (session.mixers[0].tracks[1]:group)
        #   +                1066 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].input:synth)
        #   +                    active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 26.0
        #                    1035 group (session.mixers[0].tracks[1]:tracks)
        #                    1038 supriya:meters:2 (session.mixers[0].tracks[1]:input-levels)
        #                        in_: 26.0, out: 31.0
        #   """,
        #   """
        #   - ['/s_new', 'supriya:patch-cable:2x2', 1066, 2, 1035, 'active', 'c29', 'in_', 18.0, 'out', 26.0]
        #   """,
        ),
        # sibling
        # TODO: This should feedback, because the reader is calculated before
        #       the writer.
        (
            "mixers[0].tracks[0].tracks[0]",
            "mixers[0].tracks[0].tracks[1]",
            does_not_raise,
            """
            """,
            """
            """,
            """
            """,
        #   """
        #   --- initial
        #   +++ mutation
        #   @@ -6,7 +6,7 @@
        #                    <TrackInput 7 session.mixers[0].tracks[0].input source=null>
        #                    <Track 17 'A1'>
        #                        <TrackFeedback 18 session.mixers[0].tracks[0].tracks[0].feedback>
        #   -                    <TrackInput 19 session.mixers[0].tracks[0].tracks[0].input source=null>
        #   +                    <TrackInput 19 session.mixers[0].tracks[0].tracks[0].input source=session.mixers[0].tracks[0].tracks[1]>
        #                        <Track 25 'A11'>
        #                            <TrackFeedback 26 session.mixers[0].tracks[0].tracks[0].tracks[0].feedback>
        #                            <TrackInput 27 session.mixers[0].tracks[0].tracks[0].tracks[0].input source=null>
        #   """,
        #   """
        #   --- initial
        #   +++ mutation
        #   @@ -6,6 +6,8 @@
        #                        1012 group (session.mixers[0].tracks[0].tracks[0]:group)
        #                            1041 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].feedback:synth)
        #                                active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 28.0, out: 20.0
        #   +                        1066 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].input:synth)
        #   +                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 24.0, out: 20.0
        #                            1013 group (session.mixers[0].tracks[0].tracks[0]:tracks)
        #                                1018 group (session.mixers[0].tracks[0].tracks[0].tracks[0]:group)
        #                                    1019 group (session.mixers[0].tracks[0].tracks[0].tracks[0]:tracks)
        #   """,
        #   """
        #   - ['/s_new', 'supriya:fb-patch-cable:2x2', 1066, 2, 1013, 'active', 'c11', 'in_', 24.0, 'out', 20.0]
        #   """,
        ),
        # other mixer
        (
            "mixers[0].tracks[0]",
            "mixers[1].tracks[0]",
            pytest.raises(RuntimeError),
            "",
            "",
            "",
        ),
    ],
)
@pytest.mark.asyncio
@pytest.mark.xfail
async def test_Track_set_input(
    complex_session: tuple[Session, str, str],
    expected_components_diff: str,
    expected_tree_diff: str,
    expected_messages: str,
    maybe_raises,
    online: bool,
    source: str,
    target: str | tuple[int, int] | None,
) -> None:
    # Pre-conditions
    session, initial_components, initial_tree = complex_session
    if online:
        await session.boot()
        await session.sync()
    source_ = session[source]
    assert isinstance(source_, Track)
    target_: BusGroup | Track | None = None
    # TODO: Because the context could be null, we need the "promise" of a bus group.
    if isinstance(target, str):
        target_component = session[target]
        assert isinstance(target_component, Track)
        target_ = target_component
    # elif isinstance(target, tuple):
    #     index, count = target
    #     target_ = BusGroup(
    #         context=session["mixers[0]"].context,
    #         calculation_rate=CalculationRate.AUDIO,
    #         id_=index,
    #         count=count,
    #     )
    # Operation
    with maybe_raises, capture(session["mixers[0]"].context) as messages:
        await source_.set_input(target_)
    # Post-conditions
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
    "actions, expected_state, expected_messages",
    [
        (
            [("mixers[0].tracks[0]", [True])],
            [
                ("m[0].t[0]", (0.0, 0.0), False),
                ("m[0].t[0].t[0]", (1.0, 1.0), True),
                ("m[0].t[0].t[0].t[0]", (1.0, 1.0), True),
                ("m[0].t[0].t[1]", (0.0, 0.0), True),
                ("m[0].t[1]", (0.0, 0.0), True),
                ("m[0].t[2]", (0.0, 0.0), True),
                ("m[1].t[0]", (0.0, 0.0), True),
            ],
            """
            - ['/c_set', 5, 0.0]
            """,
        ),
        (
            [("mixers[0].tracks[0].tracks[0]", [True])],
            [
                ("m[0].t[0]", (0.0, 0.0), True),
                ("m[0].t[0].t[0]", (0.0, 0.0), False),
                ("m[0].t[0].t[0].t[0]", (1.0, 1.0), True),
                ("m[0].t[0].t[1]", (0.0, 0.0), True),
                ("m[0].t[1]", (0.0, 0.0), True),
                ("m[0].t[2]", (0.0, 0.0), True),
                ("m[1].t[0]", (0.0, 0.0), True),
            ],
            """
            - ['/c_set', 11, 0.0]
            """,
        ),
    ],
)
@pytest.mark.asyncio
@pytest.mark.xfail
async def test_Track_set_muted(
    actions: list[tuple[str, list[bool]]],
    complex_session: tuple[Session, str, str],
    expected_messages: str,
    expected_state: list[tuple[str, tuple[float, ...], bool]],
    online: bool,
) -> None:
    # Pre-conditions
    session, _, _ = complex_session
    if online:
        await session.mixers[0].tracks[0].tracks[0].tracks[0].add_device()
        await session.mixers[0].tracks[1].sends[0].delete()
        await session.boot()
        await session.sync()
        initial_tree = await debug_tree(session)
    # Operation
    with capture(session["mixers[0]"].context) as messages:
        for target, args in actions:
            target_ = session[target]
            assert isinstance(target_, Track)
            await target_.set_muted(*args)
    # Post-conditions
    if not online:
        return
    await asyncio.sleep(get_lag_time() * 2)
    await assert_tree_diff(
        session,
        "",
        expected_initial_tree=initial_tree,
    )
    assert [
        (
            track.short_address,
            tuple(round(x, 6) for x in track.output_levels),
            track.is_active,
        )
        for track in session._walk(Track)
        if isinstance(track, Track)
    ] == expected_state
    assert format_messages(messages) == normalize(expected_messages)


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "source, target, maybe_raises, expected_components_diff, expected_tree_diff, expected_messages",
    [
        # none
        (
            "mixers[0].tracks[0].tracks[0]",
            None,
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -11,7 +11,7 @@
                                     <TrackFeedback 26 session.mixers[0].tracks[0].tracks[0].tracks[0].feedback>
                                     <TrackInput 27 session.mixers[0].tracks[0].tracks[0].tracks[0].input source=null>
                                     <TrackOutput 28 session.mixers[0].tracks[0].tracks[0].tracks[0].output target=default>
            -                    <TrackOutput 20 session.mixers[0].tracks[0].tracks[0].output target=default>
            +                    <TrackOutput 20 session.mixers[0].tracks[0].tracks[0].output target=null>
                             <Track 21 'A2'>
                                 <TrackFeedback 22 session.mixers[0].tracks[0].tracks[1].feedback>
                                 <TrackInput 23 session.mixers[0].tracks[0].tracks[1].input source=null>
            """,
            """
            --- initial
            +++ mutation
            @@ -25,8 +25,8 @@
                                         active: c11, bus: 20.0, done_action: 2.0, gain: c12, gate: 1.0
                                     1017 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:output-levels)
                                         in_: 20.0, out: 15.0
            -                        1025 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].output:synth)
            -                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 18.0
            +                        1025 supriya:patch-cable:2x2
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 18.0
                                 1026 group (session.mixers[0].tracks[0].tracks[1]:group)
                                     1027 group (session.mixers[0].tracks[0].tracks[1]:tracks)
                                     1030 supriya:meters:2 (session.mixers[0].tracks[0].tracks[1]:input-levels)
            """,
            """
            - ['/n_set', 1025, 'gate', 0.0]
            """,
        ),
        # default: no-op
        (
            "mixers[0].tracks[0].tracks[0]",
            DEFAULT,
            does_not_raise,
            "",
            "",
            "",
        ),
        # self
        (
            "mixers[0].tracks[0].tracks[0]",
            "mixers[0].tracks[0].tracks[0]",
            pytest.raises(RuntimeError),
            "",
            "",
            "",
        ),
        # parent: no-op, but does pin target
        (
            "mixers[0].tracks[0].tracks[0]",
            "mixers[0].tracks[0]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -11,7 +11,7 @@
                                     <TrackFeedback 26 session.mixers[0].tracks[0].tracks[0].tracks[0].feedback>
                                     <TrackInput 27 session.mixers[0].tracks[0].tracks[0].tracks[0].input source=null>
                                     <TrackOutput 28 session.mixers[0].tracks[0].tracks[0].tracks[0].output target=default>
            -                    <TrackOutput 20 session.mixers[0].tracks[0].tracks[0].output target=default>
            +                    <TrackOutput 20 session.mixers[0].tracks[0].tracks[0].output target=session.mixers[0].tracks[0]>
                             <Track 21 'A2'>
                                 <TrackFeedback 22 session.mixers[0].tracks[0].tracks[1].feedback>
                                 <TrackInput 23 session.mixers[0].tracks[0].tracks[1].input source=null>
            """,
            "",
            "",
        ),
        # child
        (
            "mixers[0].tracks[0].tracks[0]",
            "mixers[0].tracks[0].tracks[0].tracks[0]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -11,7 +11,7 @@
                                     <TrackFeedback 26 session.mixers[0].tracks[0].tracks[0].tracks[0].feedback>
                                     <TrackInput 27 session.mixers[0].tracks[0].tracks[0].tracks[0].input source=null>
                                     <TrackOutput 28 session.mixers[0].tracks[0].tracks[0].tracks[0].output target=default>
            -                    <TrackOutput 20 session.mixers[0].tracks[0].tracks[0].output target=default>
            +                    <TrackOutput 20 session.mixers[0].tracks[0].tracks[0].output target=session.mixers[0].tracks[0].tracks[0].tracks[0]>
                             <Track 21 'A2'>
                                 <TrackFeedback 22 session.mixers[0].tracks[0].tracks[1].feedback>
                                 <TrackInput 23 session.mixers[0].tracks[0].tracks[1].input source=null>
            """,
            """
            --- initial
            +++ mutation
            @@ -8,6 +8,8 @@
                                         active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 28.0, out: 20.0
                                     1013 group (session.mixers[0].tracks[0].tracks[0]:tracks)
                                         1018 group (session.mixers[0].tracks[0].tracks[0].tracks[0]:group)
            +                                1066 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].tracks[0].feedback:synth)
            +                                    active: c17, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 36.0, out: 22.0
                                             1019 group (session.mixers[0].tracks[0].tracks[0].tracks[0]:tracks)
                                             1022 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0].tracks[0]:input-levels)
                                                 in_: 22.0, out: 19.0
            @@ -25,8 +27,10 @@
                                         active: c11, bus: 20.0, done_action: 2.0, gain: c12, gate: 1.0
                                     1017 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:output-levels)
                                         in_: 20.0, out: 15.0
            -                        1025 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].output:synth)
            -                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 18.0
            +                        1025 supriya:patch-cable:2x2
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 18.0
            +                        1067 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].output:synth)
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 36.0
                                 1026 group (session.mixers[0].tracks[0].tracks[1]:group)
                                     1027 group (session.mixers[0].tracks[0].tracks[1]:tracks)
                                     1030 supriya:meters:2 (session.mixers[0].tracks[0].tracks[1]:input-levels)
            """,
            """
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1066, 0, 1018, 'active', 'c17', 'in_', 36.0, 'out', 22.0]
            - [None,
               [['/n_set', 1025, 'gate', 0.0],
                ['/s_new', 'supriya:patch-cable:2x2', 1067, 1, 1012, 'active', 'c11', 'in_', 20.0, 'out', 36.0]]]
            """,
        ),
        # auntie
        (
            "mixers[0].tracks[0].tracks[0]",
            "mixers[0].tracks[1]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -11,7 +11,7 @@
                                     <TrackFeedback 26 session.mixers[0].tracks[0].tracks[0].tracks[0].feedback>
                                     <TrackInput 27 session.mixers[0].tracks[0].tracks[0].tracks[0].input source=null>
                                     <TrackOutput 28 session.mixers[0].tracks[0].tracks[0].tracks[0].output target=default>
            -                    <TrackOutput 20 session.mixers[0].tracks[0].tracks[0].output target=default>
            +                    <TrackOutput 20 session.mixers[0].tracks[0].tracks[0].output target=<Track 4 'B'>>
                             <Track 21 'A2'>
                                 <TrackFeedback 22 session.mixers[0].tracks[0].tracks[1].feedback>
                                 <TrackInput 23 session.mixers[0].tracks[0].tracks[1].input source=null>
            """,
            """
            --- initial
            +++ mutation
            @@ -25,8 +25,10 @@
                                         active: c11, bus: 20.0, done_action: 2.0, gain: c12, gate: 1.0
                                     1017 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:output-levels)
                                         in_: 20.0, out: 15.0
            -                        1025 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].output:synth)
            -                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 18.0
            +                        1025 supriya:patch-cable:2x2
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 18.0
            +                        1066 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].output:synth)
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 26.0
                                 1026 group (session.mixers[0].tracks[0].tracks[1]:group)
                                     1027 group (session.mixers[0].tracks[0].tracks[1]:tracks)
                                     1030 supriya:meters:2 (session.mixers[0].tracks[0].tracks[1]:input-levels)
            """,
            """
            - [None,
               [['/n_set', 1025, 'gate', 0.0],
                ['/s_new', 'supriya:patch-cable:2x2', 1066, 1, 1012, 'active', 'c11', 'in_', 20.0, 'out', 26.0]]]
            """,
        ),
        # mixer: no-op but does pin target
        (
            "mixers[0].tracks[0]",
            "mixers[0]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -16,7 +16,7 @@
                                 <TrackFeedback 22 session.mixers[0].tracks[0].tracks[1].feedback>
                                 <TrackInput 23 session.mixers[0].tracks[0].tracks[1].input source=null>
                                 <TrackOutput 24 session.mixers[0].tracks[0].tracks[1].output target=default>
            -                <TrackOutput 8 session.mixers[0].tracks[0].output target=default>
            +                <TrackOutput 8 session.mixers[0].tracks[0].output target=session.mixers[0]>
                             <TrackSend 33 target=<Track 4 'B'>>
                         <Track 9 'B'>
                             <TrackFeedback 10 session.mixers[0].tracks[1].feedback>
            """,
            "",
            "",
        ),
        # sibling
        (
            "mixers[0].tracks[0].tracks[0]",
            "mixers[0].tracks[0].tracks[1]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -11,7 +11,7 @@
                                     <TrackFeedback 26 session.mixers[0].tracks[0].tracks[0].tracks[0].feedback>
                                     <TrackInput 27 session.mixers[0].tracks[0].tracks[0].tracks[0].input source=null>
                                     <TrackOutput 28 session.mixers[0].tracks[0].tracks[0].tracks[0].output target=default>
            -                    <TrackOutput 20 session.mixers[0].tracks[0].tracks[0].output target=default>
            +                    <TrackOutput 20 session.mixers[0].tracks[0].tracks[0].output target=session.mixers[0].tracks[0].tracks[1]>
                             <Track 21 'A2'>
                                 <TrackFeedback 22 session.mixers[0].tracks[0].tracks[1].feedback>
                                 <TrackInput 23 session.mixers[0].tracks[0].tracks[1].input source=null>
            """,
            """
            --- initial
            +++ mutation
            @@ -25,8 +25,10 @@
                                         active: c11, bus: 20.0, done_action: 2.0, gain: c12, gate: 1.0
                                     1017 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:output-levels)
                                         in_: 20.0, out: 15.0
            -                        1025 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].output:synth)
            -                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 18.0
            +                        1025 supriya:patch-cable:2x2
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 18.0
            +                        1066 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].output:synth)
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 24.0
                                 1026 group (session.mixers[0].tracks[0].tracks[1]:group)
                                     1027 group (session.mixers[0].tracks[0].tracks[1]:tracks)
                                     1030 supriya:meters:2 (session.mixers[0].tracks[0].tracks[1]:input-levels)
            """,
            """
            - [None,
               [['/n_set', 1025, 'gate', 0.0],
                ['/s_new', 'supriya:patch-cable:2x2', 1066, 1, 1012, 'active', 'c11', 'in_', 20.0, 'out', 24.0]]]
            """,
        ),
        # other mixer
        (
            "mixers[0].tracks[0]",
            "mixers[1].tracks[0]",
            pytest.raises(RuntimeError),
            "",
            "",
            "",
        ),
    ],
)
@pytest.mark.asyncio
@pytest.mark.xfail
async def test_Track_set_output(
    complex_session: tuple[Session, str, str],
    expected_components_diff: str,
    expected_tree_diff: str,
    expected_messages: str,
    maybe_raises,
    online: bool,
    source: str,
    target: Default | str | tuple[int, int] | None,
) -> None:
    # Pre-conditions
    session, initial_components, initial_tree = complex_session
    if online:
        await session.boot()
        await session.sync()
    source_ = session[source]
    assert isinstance(source_, Track)
    target_: BusGroup | Default | TrackContainer | None = None
    if isinstance(target, Default):
        target_ = DEFAULT
    elif isinstance(target, str):
        target_component = session[target]
        assert isinstance(target_component, TrackContainer)
        target_ = target_component
    # TODO: Because the context could be null, we need the "promise" of a bus group.
    # elif isinstance(target, tuple):
    #     index, count = target
    #     target_ = BusGroup(
    #         context=session["mixers[0]"].context,
    #         calculation_rate=CalculationRate.AUDIO,
    #         id_=index,
    #         count=count,
    #     )
    # Operation
    with maybe_raises, capture(session["mixers[0]"].context) as messages:
        await source_.set_output(target_)
    # Post-conditions
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
    "actions, expected_state, expected_messages",
    [
        (
            [
                ("mixers[0].tracks[0]", [True]),
            ],
            [
                ("m[0].t[0]", (1.0, 1.0), True),
                ("m[0].t[0].t[0]", (1.0, 1.0), True),
                ("m[0].t[0].t[0].t[0]", (1.0, 1.0), True),
                ("m[0].t[0].t[1]", (0.0, 0.0), True),
                ("m[0].t[1]", (0.0, 0.0), False),
                ("m[0].t[2]", (0.0, 0.0), False),
                ("m[1].t[0]", (0.0, 0.0), True),
            ],
            """
            - ['/c_set', 5, 1.0]
            - ['/c_set', 11, 1.0]
            - ['/c_set', 17, 1.0]
            - ['/c_set', 23, 1.0]
            - ['/c_set', 29, 0.0]
            - ['/c_set', 35, 0.0]
            """,
        ),
        (
            [
                ("mixers[0].tracks[0].tracks[0]", [True]),
            ],
            [
                ("m[0].t[0]", (0.0, 0.0), False),
                ("m[0].t[0].t[0]", (1.0, 1.0), True),
                ("m[0].t[0].t[0].t[0]", (1.0, 1.0), True),
                ("m[0].t[0].t[1]", (0.0, 0.0), False),
                ("m[0].t[1]", (0.0, 0.0), False),
                ("m[0].t[2]", (0.0, 0.0), False),
                ("m[1].t[0]", (0.0, 0.0), True),
            ],
            """
            - ['/c_set', 5, 0.0]
            - ['/c_set', 11, 1.0]
            - ['/c_set', 17, 1.0]
            - ['/c_set', 23, 0.0]
            - ['/c_set', 29, 0.0]
            - ['/c_set', 35, 0.0]
            """,
        ),
        (
            [
                ("mixers[0].tracks[0]", [True]),
                ("mixers[0].tracks[1]", [True, False]),
            ],
            [
                ("m[0].t[0]", (1.0, 1.0), True),
                ("m[0].t[0].t[0]", (1.0, 1.0), True),
                ("m[0].t[0].t[0].t[0]", (1.0, 1.0), True),
                ("m[0].t[0].t[1]", (0.0, 0.0), True),
                ("m[0].t[1]", (1.0, 1.0), True),
                ("m[0].t[2]", (0.0, 0.0), False),
                ("m[1].t[0]", (0.0, 0.0), True),
            ],
            """
            - ['/c_set', 5, 1.0]
            - ['/c_set', 11, 1.0]
            - ['/c_set', 17, 1.0]
            - ['/c_set', 23, 1.0]
            - ['/c_set', 29, 0.0]
            - ['/c_set', 35, 0.0]
            - ['/c_set', 5, 1.0]
            - ['/c_set', 11, 1.0]
            - ['/c_set', 17, 1.0]
            - ['/c_set', 23, 1.0]
            - ['/c_set', 29, 1.0]
            - ['/c_set', 35, 0.0]
            """,
        ),
    ],
)
@pytest.mark.asyncio
@pytest.mark.xfail
async def test_Track_set_soloed(
    actions: list[tuple[str, list[bool]]],
    complex_session: tuple[Session, str, str],
    expected_messages: str,
    expected_state: list[tuple[str, tuple[float, ...], bool]],
    online: bool,
) -> None:
    # Pre-conditions
    session, initial_components, initial_tree = complex_session
    if online:
        await session.mixers[0].tracks[0].tracks[0].tracks[0].add_device()
        await session.mixers[0].tracks[1].sends[0].delete()
        await session.boot()
        await session.sync()
        initial_tree = await debug_tree(session)
    # Operation
    with capture(session["mixers[0]"].context) as messages:
        for target, args in actions:
            target_ = session[target]
            assert isinstance(target_, Track)
            await target_.set_soloed(*args)
    # Post-conditions
    if not online:
        return
    await asyncio.sleep(get_lag_time() * 2)
    await assert_tree_diff(
        session,
        "",
        expected_initial_tree=initial_tree,
    )
    assert [
        (
            track.short_address,
            tuple(round(x, 6) for x in track.output_levels),
            track.is_active,
        )
        for track in session._walk(Track)
        if isinstance(track, Track)
    ] == expected_state
    assert format_messages(messages) == normalize(expected_messages)


@pytest.mark.xfail
@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "expected_tree_diff, expected_messages",
    [
        ("", ""),
    ],
)
@pytest.mark.asyncio
@pytest.mark.xfail
async def test_Track_ungroup(
    complex_session: tuple[Session, str, str],
    expected_tree_diff: str,
    expected_messages: str,
    online: bool,
    target: str,
) -> None:
    # Pre-conditions
    session, initial_components, initial_tree = complex_session
    if online:
        await session.boot()
        await session.sync()
    target_ = session[target]
    assert isinstance(target_, Track)
    # Operation
    with capture(session["mixers[0]"].context) as messages:
        await target_.ungroup()
    # Post-conditions
    if not online:
        raise Exception
    await assert_tree_diff(
        session,
        expected_tree_diff,
        expected_initial_tree="""
        """,
    )
    assert format_messages(messages) == normalize(expected_messages)
    raise Exception
