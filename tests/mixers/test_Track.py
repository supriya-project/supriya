import asyncio

import pytest
from uqbar.strings import normalize

from supriya import BusGroup
from supriya.mixers import Session
from supriya.mixers.mixers import Mixer
from supriya.mixers.tracks import Track, TrackContainer, TrackSend
from supriya.typing import DEFAULT, Default

from .conftest import assert_diff, capture, debug_tree, does_not_raise, format_messages


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "postfader, source, target, maybe_raises, expected_diff, expected_commands",
    [
        (
            True,
            "mixers[0].tracks[1]",
            "mixers[0]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -56,6 +56,8 @@
                             1036 group (session.mixers[0].tracks[1]:devices)
                             1037 supriya:channel-strip:2 (session.mixers[0].tracks[1]:channel-strip)
                                 active: c29, bus: 26.0, gain: c30, gate: 1.0
            +                1066 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].sends[1]:synth)
            +                    active: c29, gain: 0.0, gate: 1.0, in_: 26.0, out: 16.0
                             1042 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].sends[0]:synth)
                                 active: c29, gain: 0.0, gate: 1.0, in_: 26.0, out: 28.0
                             1039 supriya:meters:2 (session.mixers[0].tracks[1]:output-levels)
            """,
            """
            - ['/s_new', 'supriya:patch-cable:2x2', 1066, 3, 1037, 'active', 'c29', 'in_', 26.0, 'out', 16.0]
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
            @@ -56,6 +56,8 @@
                             1036 group (session.mixers[0].tracks[1]:devices)
                             1037 supriya:channel-strip:2 (session.mixers[0].tracks[1]:channel-strip)
                                 active: c29, bus: 26.0, gain: c30, gate: 1.0
            +                1066 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].sends[1]:synth)
            +                    active: c29, gain: 0.0, gate: 1.0, in_: 26.0, out: 30.0
                             1042 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].sends[0]:synth)
                                 active: c29, gain: 0.0, gate: 1.0, in_: 26.0, out: 28.0
                             1039 supriya:meters:2 (session.mixers[0].tracks[1]:output-levels)
            """,
            """
            - ['/s_new', 'supriya:patch-cable:2x2', 1066, 3, 1037, 'active', 'c29', 'in_', 26.0, 'out', 30.0]
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
            @@ -54,6 +54,8 @@
                             1038 supriya:meters:2 (session.mixers[0].tracks[1]:input-levels)
                                 in_: 26.0, out: 31.0
                             1036 group (session.mixers[0].tracks[1]:devices)
            +                1066 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].sends[1]:synth)
            +                    active: c29, gain: 0.0, gate: 1.0, in_: 26.0, out: 30.0
                             1037 supriya:channel-strip:2 (session.mixers[0].tracks[1]:channel-strip)
                                 active: c29, bus: 26.0, gain: c30, gate: 1.0
                             1042 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].sends[0]:synth)
            """,
            """
            - ['/s_new', 'supriya:patch-cable:2x2', 1066, 2, 1037, 'active', 'c29', 'in_', 26.0, 'out', 30.0]
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
            @@ -50,10 +50,14 @@
                             1033 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].output:synth)
                                 active: c5, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
                         1034 group (session.mixers[0].tracks[1]:group)
            +                1066 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[1].feedback:synth)
            +                    active: c29, gain: 0.0, gate: 1.0, in_: 36.0, out: 26.0
                             1035 group (session.mixers[0].tracks[1]:tracks)
                             1038 supriya:meters:2 (session.mixers[0].tracks[1]:input-levels)
                                 in_: 26.0, out: 31.0
                             1036 group (session.mixers[0].tracks[1]:devices)
            +                1067 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].sends[1]:synth)
            +                    active: c29, gain: 0.0, gate: 1.0, in_: 26.0, out: 36.0
                             1037 supriya:channel-strip:2 (session.mixers[0].tracks[1]:channel-strip)
                                 active: c29, bus: 26.0, gain: c30, gate: 1.0
                             1042 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].sends[0]:synth)
            """,
            """
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1066, 0, 1034, 'active', 'c29', 'in_', 36.0, 'out', 26.0]
            - ['/s_new', 'supriya:patch-cable:2x2', 1067, 2, 1037, 'active', 'c29', 'in_', 26.0, 'out', 36.0]
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
            @@ -50,6 +50,8 @@
                             1033 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].output:synth)
                                 active: c5, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
                         1034 group (session.mixers[0].tracks[1]:group)
            +                1066 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[1].feedback:synth)
            +                    active: c29, gain: 0.0, gate: 1.0, in_: 36.0, out: 26.0
                             1035 group (session.mixers[0].tracks[1]:tracks)
                             1038 supriya:meters:2 (session.mixers[0].tracks[1]:input-levels)
                                 in_: 26.0, out: 31.0
            @@ -69,6 +71,8 @@
                             1045 group (session.mixers[0].tracks[2]:devices)
                             1046 supriya:channel-strip:2 (session.mixers[0].tracks[2]:channel-strip)
                                 active: c35, bus: 30.0, gain: c36, gate: 1.0
            +                1067 supriya:patch-cable:2x2 (session.mixers[0].tracks[2].sends[0]:synth)
            +                    active: c35, gain: 0.0, gate: 1.0, in_: 30.0, out: 36.0
                             1048 supriya:meters:2 (session.mixers[0].tracks[2]:output-levels)
                                 in_: 30.0, out: 39.0
                             1049 supriya:patch-cable:2x2 (session.mixers[0].tracks[2].output:synth)
            """,
            """
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1066, 0, 1034, 'active', 'c29', 'in_', 36.0, 'out', 26.0]
            - ['/s_new', 'supriya:patch-cable:2x2', 1067, 3, 1046, 'active', 'c35', 'in_', 30.0, 'out', 36.0]
            """,
        ),
        (
            True,
            "mixers[0].tracks[1]",
            "mixers[1].tracks[0]",
            pytest.raises(RuntimeError),
            "",
            "",
        ),
    ],
)
@pytest.mark.asyncio
async def test_Track_add_send(
    complex_session: tuple[Session, str],
    expected_commands: str,
    expected_diff: str,
    maybe_raises,
    online: bool,
    postfader: bool,
    source: str,
    target: str,
) -> None:
    # Pre-conditions
    session, initial_tree = complex_session
    if online:
        await session.boot()
    source_ = session[source]
    target_ = session[target]
    assert isinstance(source_, Track)
    assert isinstance(target_, TrackContainer)
    if online:
        await debug_tree(session)
    # Operation
    send: TrackSend | None = None
    with maybe_raises, capture(session["mixers[0]"].context) as commands:
        send = await source_.add_send(postfader=postfader, target=target_)
    # Post-conditions
    if send is not None:
        assert isinstance(send, TrackSend)
        assert send in source_.sends
        assert send.parent is source_
        assert send.postfader == postfader
        assert send.target is target_
        assert source_.sends[-1] is send
    if not online:
        return
    await assert_diff(
        session,
        expected_diff,
        expected_initial_tree=initial_tree,
    )
    assert format_messages(commands) == normalize(expected_commands)


@pytest.mark.xfail
@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "target, expected_diff, expected_commands",
    [],
)
@pytest.mark.asyncio
async def test_Track_delete(
    expected_commands: str,
    expected_diff: str,
    online: bool,
    mixer: Mixer,
    complex_session: tuple[Session, str],
    target: str,
) -> None:
    # TODO: rewrite this with complex_session and track lookups
    # Pre-conditions
    session, _ = complex_session
    if online:
        await session.boot()
    target_ = session[target]
    assert isinstance(target_, Track)
    parent_ = target_.parent
    # Operation
    with capture(mixer.context) as commands:
        await target_.delete()
    # Post-conditions
    assert parent_ and target_ not in parent_.children
    if not online:
        raise Exception
    await assert_diff(
        session,
        expected_diff,
        expected_initial_tree="""
        """,
    )
    assert format_messages(commands) == normalize(expected_commands)
    raise Exception


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "target, parent, index, maybe_raises, expected_graph_order, expected_diff, expected_commands",
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
            @@ -1,6 +1,21 @@
             <session.contexts[0]>
                 NODE TREE 1000 group
                     1001 group
            +            1034 group
            +                1066 supriya:fb-patch-cable:2x2
            +                    active: c29, gain: 0.0, gate: 1.0, in_: 36.0, out: 26.0
            +                1035 group
            +                1038 supriya:meters:2
            +                    in_: 26.0, out: 31.0
            +                1036 group
            +                1037 supriya:channel-strip:2
            +                    active: c29, bus: 26.0, gain: c30, gate: 1.0
            +                1042 supriya:patch-cable:2x2
            +                    active: c29, gain: 0.0, gate: 1.0, in_: 26.0, out: 28.0
            +                1039 supriya:meters:2
            +                    in_: 26.0, out: 33.0
            +                1040 supriya:patch-cable:2x2
            +                    active: c29, gain: 0.0, gate: 1.0, in_: 26.0, out: 16.0
                         1006 group
                             1007 group
                                 1012 group
            @@ -43,25 +58,14 @@
                             1008 group
                             1009 supriya:channel-strip:2
                                 active: c5, bus: 18.0, gain: c6, gate: 1.0
            +                1067 supriya:patch-cable:2x2
            +                    active: c5, gain: 0.0, gate: 1.0, in_: 18.0, out: 36.0
                             1051 supriya:patch-cable:2x2
            -                    active: c5, gain: 0.0, gate: 1.0, in_: 18.0, out: 26.0
            +                    active: c5, gain: 0.0, gate: 0.0, in_: 18.0, out: 26.0
                             1011 supriya:meters:2
                                 in_: 18.0, out: 9.0
                             1033 supriya:patch-cable:2x2
                                 active: c5, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            -            1034 group
            -                1035 group
            -                1038 supriya:meters:2
            -                    in_: 26.0, out: 31.0
            -                1036 group
            -                1037 supriya:channel-strip:2
            -                    active: c29, bus: 26.0, gain: c30, gate: 1.0
            -                1042 supriya:patch-cable:2x2
            -                    active: c29, gain: 0.0, gate: 1.0, in_: 26.0, out: 28.0
            -                1039 supriya:meters:2
            -                    in_: 26.0, out: 33.0
            -                1040 supriya:patch-cable:2x2
            -                    active: c29, gain: 0.0, gate: 1.0, in_: 26.0, out: 16.0
                         1043 group
                             1044 group
                             1047 supriya:meters:2
            """,
            """
            - ['/n_after', 1006, 1034]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1066, 0, 1034, 'active', 'c29', 'in_', 36.0, 'out', 26.0]
            - [None,
               [['/n_set', 1051, 'gate', 0.0],
                ['/s_new', 'supriya:patch-cable:2x2', 1067, 3, 1009, 'active', 'c5', 'in_', 18.0, 'out', 36.0]]]
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
            @@ -1,11 +1,28 @@
             <session.contexts[0]>
                 NODE TREE 1000 group
                     1001 group
            +            1034 group
            +                1067 supriya:fb-patch-cable:2x2
            +                    active: c29, gain: 0.0, gate: 1.0, in_: 28.0, out: 26.0
            +                1035 group
            +                1038 supriya:meters:2
            +                    in_: 26.0, out: 31.0
            +                1036 group
            +                1037 supriya:channel-strip:2
            +                    active: c29, bus: 26.0, gain: c30, gate: 1.0
            +                1066 supriya:patch-cable:2x2
            +                    active: c29, gain: 0.0, gate: 1.0, in_: 26.0, out: 20.0
            +                1042 supriya:patch-cable:2x2
            +                    active: c29, gain: 0.0, gate: 0.0, in_: 26.0, out: 28.0
            +                1039 supriya:meters:2
            +                    in_: 26.0, out: 33.0
            +                1040 supriya:patch-cable:2x2
            +                    active: c29, gain: 0.0, gate: 1.0, in_: 26.0, out: 16.0
                         1006 group
                             1007 group
                                 1012 group
                                     1041 supriya:fb-patch-cable:2x2
            -                            active: c11, gain: 0.0, gate: 1.0, in_: 28.0, out: 20.0
            +                            active: c11, gain: 0.0, gate: 0.0, in_: 28.0, out: 20.0
                                     1013 group
                                         1018 group
                                             1019 group
            @@ -43,25 +60,14 @@
                             1008 group
                             1009 supriya:channel-strip:2
                                 active: c5, bus: 18.0, gain: c6, gate: 1.0
            +                1068 supriya:patch-cable:2x2
            +                    active: c5, gain: 0.0, gate: 1.0, in_: 18.0, out: 28.0
                             1051 supriya:patch-cable:2x2
            -                    active: c5, gain: 0.0, gate: 1.0, in_: 18.0, out: 26.0
            +                    active: c5, gain: 0.0, gate: 0.0, in_: 18.0, out: 26.0
                             1011 supriya:meters:2
                                 in_: 18.0, out: 9.0
                             1033 supriya:patch-cable:2x2
                                 active: c5, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            -            1034 group
            -                1035 group
            -                1038 supriya:meters:2
            -                    in_: 26.0, out: 31.0
            -                1036 group
            -                1037 supriya:channel-strip:2
            -                    active: c29, bus: 26.0, gain: c30, gate: 1.0
            -                1042 supriya:patch-cable:2x2
            -                    active: c29, gain: 0.0, gate: 1.0, in_: 26.0, out: 28.0
            -                1039 supriya:meters:2
            -                    in_: 26.0, out: 33.0
            -                1040 supriya:patch-cable:2x2
            -                    active: c29, gain: 0.0, gate: 1.0, in_: 26.0, out: 16.0
                         1043 group
                             1044 group
                             1047 supriya:meters:2
            """,
            """
            - ['/g_head', 1001, 1034]
            - ['/n_set', 1041, 'gate', 0.0]
            - [None,
               [['/n_set', 1042, 'gate', 0.0],
                ['/s_new', 'supriya:patch-cable:2x2', 1066, 3, 1037, 'active', 'c29', 'in_', 26.0, 'out', 20.0]]]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1067, 0, 1034, 'active', 'c29', 'in_', 28.0, 'out', 26.0]
            - [None,
               [['/n_set', 1051, 'gate', 0.0],
                ['/s_new', 'supriya:patch-cable:2x2', 1068, 3, 1009, 'active', 'c5', 'in_', 18.0, 'out', 28.0]]]
            """,
        ),
        ("mixers[0].tracks[1]", "mixers[0]", 1, does_not_raise, (0, 1), "", ""),
        (
            "mixers[0].tracks[1]",
            "mixers[0]",
            2,
            does_not_raise,
            (0, 2),
            """
            --- initial
            +++ mutation
            @@ -49,6 +49,17 @@
                                 in_: 18.0, out: 9.0
                             1033 supriya:patch-cable:2x2
                                 active: c5, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            +            1043 group
            +                1044 group
            +                1047 supriya:meters:2
            +                    in_: 30.0, out: 37.0
            +                1045 group
            +                1046 supriya:channel-strip:2
            +                    active: c35, bus: 30.0, gain: c36, gate: 1.0
            +                1048 supriya:meters:2
            +                    in_: 30.0, out: 39.0
            +                1049 supriya:patch-cable:2x2
            +                    active: c35, gain: 0.0, gate: 1.0, in_: 30.0, out: 16.0
                         1034 group
                             1035 group
                             1038 supriya:meters:2
            @@ -62,17 +73,6 @@
                                 in_: 26.0, out: 33.0
                             1040 supriya:patch-cable:2x2
                                 active: c29, gain: 0.0, gate: 1.0, in_: 26.0, out: 16.0
            -            1043 group
            -                1044 group
            -                1047 supriya:meters:2
            -                    in_: 30.0, out: 37.0
            -                1045 group
            -                1046 supriya:channel-strip:2
            -                    active: c35, bus: 30.0, gain: c36, gate: 1.0
            -                1048 supriya:meters:2
            -                    in_: 30.0, out: 39.0
            -                1049 supriya:patch-cable:2x2
            -                    active: c35, gain: 0.0, gate: 1.0, in_: 30.0, out: 16.0
                     1004 supriya:meters:2
                         in_: 16.0, out: 1.0
                     1002 group
            """,
            """
            - ['/n_after', 1034, 1043]
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
        ),
        (
            "mixers[0].tracks[1]",
            "mixers[0].tracks[0]",
            0,
            does_not_raise,
            (0, 0, 2),
            """
            --- initial
            +++ mutation
            @@ -3,9 +3,28 @@
                     1001 group
                         1006 group
                             1007 group
            +                    1034 group
            +                        1068 supriya:fb-patch-cable:2x2
            +                            active: c29, gain: 0.0, gate: 1.0, in_: 28.0, out: 26.0
            +                        1035 group
            +                        1038 supriya:meters:2
            +                            in_: 26.0, out: 31.0
            +                        1036 group
            +                        1037 supriya:channel-strip:2
            +                            active: c29, bus: 26.0, gain: c30, gate: 1.0
            +                        1067 supriya:patch-cable:2x2
            +                            active: c29, gain: 0.0, gate: 1.0, in_: 26.0, out: 20.0
            +                        1042 supriya:patch-cable:2x2
            +                            active: c29, gain: 0.0, gate: 0.0, in_: 26.0, out: 28.0
            +                        1039 supriya:meters:2
            +                            in_: 26.0, out: 33.0
            +                        1040 supriya:patch-cable:2x2
            +                            active: c29, gain: 0.0, gate: 0.0, in_: 26.0, out: 16.0
            +                        1066 supriya:patch-cable:2x2
            +                            active: c29, gain: 0.0, gate: 1.0, in_: 26.0, out: 18.0
                                 1012 group
                                     1041 supriya:fb-patch-cable:2x2
            -                            active: c11, gain: 0.0, gate: 1.0, in_: 28.0, out: 20.0
            +                            active: c11, gain: 0.0, gate: 0.0, in_: 28.0, out: 20.0
                                     1013 group
                                         1018 group
                                             1019 group
            @@ -43,25 +62,14 @@
                             1008 group
                             1009 supriya:channel-strip:2
                                 active: c5, bus: 18.0, gain: c6, gate: 1.0
            +                1069 supriya:patch-cable:2x2
            +                    active: c5, gain: 0.0, gate: 1.0, in_: 18.0, out: 28.0
                             1051 supriya:patch-cable:2x2
            -                    active: c5, gain: 0.0, gate: 1.0, in_: 18.0, out: 26.0
            +                    active: c5, gain: 0.0, gate: 0.0, in_: 18.0, out: 26.0
                             1011 supriya:meters:2
                                 in_: 18.0, out: 9.0
                             1033 supriya:patch-cable:2x2
                                 active: c5, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            -            1034 group
            -                1035 group
            -                1038 supriya:meters:2
            -                    in_: 26.0, out: 31.0
            -                1036 group
            -                1037 supriya:channel-strip:2
            -                    active: c29, bus: 26.0, gain: c30, gate: 1.0
            -                1042 supriya:patch-cable:2x2
            -                    active: c29, gain: 0.0, gate: 1.0, in_: 26.0, out: 28.0
            -                1039 supriya:meters:2
            -                    in_: 26.0, out: 33.0
            -                1040 supriya:patch-cable:2x2
            -                    active: c29, gain: 0.0, gate: 1.0, in_: 26.0, out: 16.0
                         1043 group
                             1044 group
                             1047 supriya:meters:2
            """,
            """
            - ['/g_head', 1007, 1034]
            - [None,
               [['/n_set', 1040, 'gate', 0.0],
                ['/s_new', 'supriya:patch-cable:2x2', 1066, 1, 1034, 'active', 'c29', 'in_', 26.0, 'out', 18.0]]]
            - ['/n_set', 1041, 'gate', 0.0]
            - [None,
               [['/n_set', 1042, 'gate', 0.0],
                ['/s_new', 'supriya:patch-cable:2x2', 1067, 3, 1037, 'active', 'c29', 'in_', 26.0, 'out', 20.0]]]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1068, 0, 1034, 'active', 'c29', 'in_', 28.0, 'out', 26.0]
            - [None,
               [['/n_set', 1051, 'gate', 0.0],
                ['/s_new', 'supriya:patch-cable:2x2', 1069, 3, 1009, 'active', 'c5', 'in_', 18.0, 'out', 28.0]]]
            """,
        ),
        (
            "mixers[0].tracks[1]",
            "mixers[0].tracks[0].tracks[0]",
            0,
            does_not_raise,
            (0, 0, 2, 2),
            """
            --- initial
            +++ mutation
            @@ -5,8 +5,27 @@
                             1007 group
                                 1012 group
                                     1041 supriya:fb-patch-cable:2x2
            -                            active: c11, gain: 0.0, gate: 1.0, in_: 28.0, out: 20.0
            +                            active: c11, gain: 0.0, gate: 0.0, in_: 28.0, out: 20.0
                                     1013 group
            +                            1034 group
            +                                1068 supriya:fb-patch-cable:2x2
            +                                    active: c29, gain: 0.0, gate: 1.0, in_: 28.0, out: 26.0
            +                                1035 group
            +                                1038 supriya:meters:2
            +                                    in_: 26.0, out: 31.0
            +                                1036 group
            +                                1037 supriya:channel-strip:2
            +                                    active: c29, bus: 26.0, gain: c30, gate: 1.0
            +                                1067 supriya:patch-cable:2x2
            +                                    active: c29, gain: 0.0, gate: 1.0, in_: 26.0, out: 20.0
            +                                1042 supriya:patch-cable:2x2
            +                                    active: c29, gain: 0.0, gate: 0.0, in_: 26.0, out: 28.0
            +                                1039 supriya:meters:2
            +                                    in_: 26.0, out: 33.0
            +                                1040 supriya:patch-cable:2x2
            +                                    active: c29, gain: 0.0, gate: 0.0, in_: 26.0, out: 16.0
            +                                1066 supriya:patch-cable:2x2
            +                                    active: c29, gain: 0.0, gate: 1.0, in_: 26.0, out: 20.0
                                         1018 group
                                             1019 group
                                             1022 supriya:meters:2
            @@ -43,25 +62,14 @@
                             1008 group
                             1009 supriya:channel-strip:2
                                 active: c5, bus: 18.0, gain: c6, gate: 1.0
            +                1069 supriya:patch-cable:2x2
            +                    active: c5, gain: 0.0, gate: 1.0, in_: 18.0, out: 28.0
                             1051 supriya:patch-cable:2x2
            -                    active: c5, gain: 0.0, gate: 1.0, in_: 18.0, out: 26.0
            +                    active: c5, gain: 0.0, gate: 0.0, in_: 18.0, out: 26.0
                             1011 supriya:meters:2
                                 in_: 18.0, out: 9.0
                             1033 supriya:patch-cable:2x2
                                 active: c5, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            -            1034 group
            -                1035 group
            -                1038 supriya:meters:2
            -                    in_: 26.0, out: 31.0
            -                1036 group
            -                1037 supriya:channel-strip:2
            -                    active: c29, bus: 26.0, gain: c30, gate: 1.0
            -                1042 supriya:patch-cable:2x2
            -                    active: c29, gain: 0.0, gate: 1.0, in_: 26.0, out: 28.0
            -                1039 supriya:meters:2
            -                    in_: 26.0, out: 33.0
            -                1040 supriya:patch-cable:2x2
            -                    active: c29, gain: 0.0, gate: 1.0, in_: 26.0, out: 16.0
                         1043 group
                             1044 group
                             1047 supriya:meters:2
            """,
            """
            - ['/g_head', 1013, 1034]
            - [None,
               [['/n_set', 1040, 'gate', 0.0],
                ['/s_new', 'supriya:patch-cable:2x2', 1066, 1, 1034, 'active', 'c29', 'in_', 26.0, 'out', 20.0]]]
            - ['/n_set', 1041, 'gate', 0.0]
            - [None,
               [['/n_set', 1042, 'gate', 0.0],
                ['/s_new', 'supriya:patch-cable:2x2', 1067, 3, 1037, 'active', 'c29', 'in_', 26.0, 'out', 20.0]]]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1068, 0, 1034, 'active', 'c29', 'in_', 28.0, 'out', 26.0]
            - [None,
               [['/n_set', 1051, 'gate', 0.0],
                ['/s_new', 'supriya:patch-cable:2x2', 1069, 3, 1009, 'active', 'c5', 'in_', 18.0, 'out', 28.0]]]
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
        ),
        (
            "mixers[0].tracks[1]",
            "mixers[0].tracks[2]",
            0,
            does_not_raise,
            (0, 1, 2),
            """
            --- initial
            +++ mutation
            @@ -49,21 +49,23 @@
                                 in_: 18.0, out: 9.0
                             1033 supriya:patch-cable:2x2
                                 active: c5, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            -            1034 group
            -                1035 group
            -                1038 supriya:meters:2
            -                    in_: 26.0, out: 31.0
            -                1036 group
            -                1037 supriya:channel-strip:2
            -                    active: c29, bus: 26.0, gain: c30, gate: 1.0
            -                1042 supriya:patch-cable:2x2
            -                    active: c29, gain: 0.0, gate: 1.0, in_: 26.0, out: 28.0
            -                1039 supriya:meters:2
            -                    in_: 26.0, out: 33.0
            -                1040 supriya:patch-cable:2x2
            -                    active: c29, gain: 0.0, gate: 1.0, in_: 26.0, out: 16.0
                         1043 group
                             1044 group
            +                    1034 group
            +                        1035 group
            +                        1038 supriya:meters:2
            +                            in_: 26.0, out: 31.0
            +                        1036 group
            +                        1037 supriya:channel-strip:2
            +                            active: c29, bus: 26.0, gain: c30, gate: 1.0
            +                        1042 supriya:patch-cable:2x2
            +                            active: c29, gain: 0.0, gate: 1.0, in_: 26.0, out: 28.0
            +                        1039 supriya:meters:2
            +                            in_: 26.0, out: 33.0
            +                        1040 supriya:patch-cable:2x2
            +                            active: c29, gain: 0.0, gate: 0.0, in_: 26.0, out: 16.0
            +                        1066 supriya:patch-cable:2x2
            +                            active: c29, gain: 0.0, gate: 1.0, in_: 26.0, out: 30.0
                             1047 supriya:meters:2
                                 in_: 30.0, out: 37.0
                             1045 group
            """,
            """
            - ['/g_head', 1044, 1034]
            - [None,
               [['/n_set', 1040, 'gate', 0.0],
                ['/s_new', 'supriya:patch-cable:2x2', 1066, 1, 1034, 'active', 'c29', 'in_', 26.0, 'out', 30.0]]]
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
            @@ -1,6 +1,17 @@
             <session.contexts[0]>
                 NODE TREE 1000 group
                     1001 group
            +            1043 group
            +                1044 group
            +                1047 supriya:meters:2
            +                    in_: 30.0, out: 37.0
            +                1045 group
            +                1046 supriya:channel-strip:2
            +                    active: c35, bus: 30.0, gain: c36, gate: 1.0
            +                1048 supriya:meters:2
            +                    in_: 30.0, out: 39.0
            +                1049 supriya:patch-cable:2x2
            +                    active: c35, gain: 0.0, gate: 1.0, in_: 30.0, out: 16.0
                         1006 group
                             1007 group
                                 1012 group
            @@ -62,17 +73,6 @@
                                 in_: 26.0, out: 33.0
                             1040 supriya:patch-cable:2x2
                                 active: c29, gain: 0.0, gate: 1.0, in_: 26.0, out: 16.0
            -            1043 group
            -                1044 group
            -                1047 supriya:meters:2
            -                    in_: 30.0, out: 37.0
            -                1045 group
            -                1046 supriya:channel-strip:2
            -                    active: c35, bus: 30.0, gain: c36, gate: 1.0
            -                1048 supriya:meters:2
            -                    in_: 30.0, out: 39.0
            -                1049 supriya:patch-cable:2x2
            -                    active: c35, gain: 0.0, gate: 1.0, in_: 30.0, out: 16.0
                     1004 supriya:meters:2
                         in_: 16.0, out: 1.0
                     1002 group
            """,
            """
            - ['/g_head', 1001, 1043]
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
        ),
    ],
)
@pytest.mark.asyncio
async def test_Track_move(
    complex_session: tuple[Session, str],
    expected_commands: str,
    expected_graph_order: list[int],
    expected_diff: str,
    index: int,
    online: bool,
    parent: str,
    target: str,
    maybe_raises,
) -> None:
    # Pre-conditions
    print("Pre-conditions")
    session, _ = complex_session
    if online:
        await session.boot()
        initial_tree = await debug_tree(session, annotated=False)
    target_ = session[target]
    parent_ = session[parent]
    assert isinstance(target_, Track)
    assert isinstance(parent_, TrackContainer)
    # Operation
    print("Operation")
    with maybe_raises, capture(session["mixers[0]"].context) as commands:
        await target_.move(index=index, parent=parent_)
    # Post-conditions
    print("Post-conditions")
    assert target_.graph_order == expected_graph_order
    if not online:
        return
    await assert_diff(
        session,
        expected_diff,
        expected_initial_tree=initial_tree,
        annotated=False,
    )
    assert format_messages(commands) == normalize(expected_commands)


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "source, target, maybe_raises, expected_diff, expected_commands",
    [
        # none
        (
            "mixers[0].tracks[0].tracks[0]",
            None,
            does_not_raise,
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
        ),
        # parent
        # TODO: This should feedback, because the reader is calculated before
        #       the writer.
        (
            "mixers[0].tracks[0].tracks[0]",
            "mixers[0].tracks[0]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -6,6 +6,8 @@
                                 1012 group (session.mixers[0].tracks[0].tracks[0]:group)
                                     1041 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].feedback:synth)
                                         active: c11, gain: 0.0, gate: 1.0, in_: 28.0, out: 20.0
            +                        1066 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].input:synth)
            +                            active: c11, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
                                     1013 group (session.mixers[0].tracks[0].tracks[0]:tracks)
                                         1018 group (session.mixers[0].tracks[0].tracks[0].tracks[0]:group)
                                             1019 group (session.mixers[0].tracks[0].tracks[0].tracks[0]:tracks)
            """,
            """
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1066, 2, 1013, 'active', 'c11', 'in_', 18.0, 'out', 20.0]
            """,
        ),
        # child
        (
            "mixers[0].tracks[0].tracks[0]",
            "mixers[0].tracks[0].tracks[0].tracks[0]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -6,6 +6,8 @@
                                 1012 group (session.mixers[0].tracks[0].tracks[0]:group)
                                     1041 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].feedback:synth)
                                         active: c11, gain: 0.0, gate: 1.0, in_: 28.0, out: 20.0
            +                        1066 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].input:synth)
            +                            active: c11, gain: 0.0, gate: 1.0, in_: 22.0, out: 20.0
                                     1013 group (session.mixers[0].tracks[0].tracks[0]:tracks)
                                         1018 group (session.mixers[0].tracks[0].tracks[0].tracks[0]:group)
                                             1019 group (session.mixers[0].tracks[0].tracks[0].tracks[0]:tracks)
            """,
            """
            - ['/s_new', 'supriya:patch-cable:2x2', 1066, 2, 1013, 'active', 'c11', 'in_', 22.0, 'out', 20.0]
            """,
        ),
        # auntie
        # TODO: This should feedback, because the reader is calculated before
        #       the writer.
        (
            "mixers[0].tracks[0].tracks[0]",
            "mixers[0].tracks[1]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -6,6 +6,8 @@
                                 1012 group (session.mixers[0].tracks[0].tracks[0]:group)
                                     1041 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].feedback:synth)
                                         active: c11, gain: 0.0, gate: 1.0, in_: 28.0, out: 20.0
            +                        1066 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].input:synth)
            +                            active: c11, gain: 0.0, gate: 1.0, in_: 26.0, out: 20.0
                                     1013 group (session.mixers[0].tracks[0].tracks[0]:tracks)
                                         1018 group (session.mixers[0].tracks[0].tracks[0].tracks[0]:group)
                                             1019 group (session.mixers[0].tracks[0].tracks[0].tracks[0]:tracks)
            """,
            """
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1066, 2, 1013, 'active', 'c11', 'in_', 26.0, 'out', 20.0]
            """,
        ),
        # sibling, reversed
        # NOTE: Does not need to feedback.
        (
            "mixers[0].tracks[1]",
            "mixers[0].tracks[0]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -50,6 +50,8 @@
                             1033 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].output:synth)
                                 active: c5, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
                         1034 group (session.mixers[0].tracks[1]:group)
            +                1066 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].input:synth)
            +                    active: c29, gain: 0.0, gate: 1.0, in_: 18.0, out: 26.0
                             1035 group (session.mixers[0].tracks[1]:tracks)
                             1038 supriya:meters:2 (session.mixers[0].tracks[1]:input-levels)
                                 in_: 26.0, out: 31.0
            """,
            """
            - ['/s_new', 'supriya:patch-cable:2x2', 1066, 2, 1035, 'active', 'c29', 'in_', 18.0, 'out', 26.0]
            """,
        ),
        # sibling
        # TODO: This should feedback, because the reader is calculated before
        #       the writer.
        (
            "mixers[0].tracks[0].tracks[0]",
            "mixers[0].tracks[0].tracks[1]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -6,6 +6,8 @@
                                 1012 group (session.mixers[0].tracks[0].tracks[0]:group)
                                     1041 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].feedback:synth)
                                         active: c11, gain: 0.0, gate: 1.0, in_: 28.0, out: 20.0
            +                        1066 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].input:synth)
            +                            active: c11, gain: 0.0, gate: 1.0, in_: 24.0, out: 20.0
                                     1013 group (session.mixers[0].tracks[0].tracks[0]:tracks)
                                         1018 group (session.mixers[0].tracks[0].tracks[0].tracks[0]:group)
                                             1019 group (session.mixers[0].tracks[0].tracks[0].tracks[0]:tracks)
            """,
            """
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1066, 2, 1013, 'active', 'c11', 'in_', 24.0, 'out', 20.0]
            """,
        ),
        # other mixer
        (
            "mixers[0].tracks[0]",
            "mixers[1].tracks[0]",
            pytest.raises(RuntimeError),
            "",
            "",
        ),
    ],
)
@pytest.mark.asyncio
async def test_Track_set_input(
    complex_session: tuple[Session, str],
    expected_commands: str,
    expected_diff: str,
    maybe_raises,
    online: bool,
    source: str,
    target: str | tuple[int, int] | None,
) -> None:
    # Pre-conditions
    session, initial_tree = complex_session
    if online:
        await session.boot()
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
    with maybe_raises, capture(session["mixers[0]"].context) as commands:
        await source_.set_input(target_)
    # Post-conditions
    if not online:
        return
    await assert_diff(
        session,
        expected_diff,
        expected_initial_tree=initial_tree,
    )
    assert format_messages(commands) == normalize(expected_commands)


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "actions, expected_state, expected_commands",
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
async def test_Track_set_muted(
    actions: list[tuple[str, list[bool]]],
    complex_session: tuple[Session, str],
    expected_commands: str,
    expected_state: list[tuple[str, tuple[float, ...], bool]],
    online: bool,
) -> None:
    # Pre-conditions
    session, _ = complex_session
    if online:
        await session.boot()
        await session.mixers[0].tracks[0].tracks[0].tracks[0].add_device()
        await session.mixers[0].tracks[1].sends[0].delete()
        await asyncio.sleep(0.25)
        initial_tree = await debug_tree(session)
    # Operation
    with capture(session["mixers[0]"].context) as commands:
        for target, args in actions:
            target_ = session[target]
            assert isinstance(target_, Track)
            await target_.set_muted(*args)
    # Post-conditions
    if not online:
        return
    await assert_diff(
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
    assert format_messages(commands) == normalize(expected_commands)


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "source, target, maybe_raises, expected_diff, expected_commands",
    [
        # none
        (
            "mixers[0].tracks[0].tracks[0]",
            None,
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -25,8 +25,8 @@
                                         active: c11, bus: 20.0, gain: c12, gate: 1.0
                                     1017 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:output-levels)
                                         in_: 20.0, out: 15.0
            -                        1025 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].output:synth)
            -                            active: c11, gain: 0.0, gate: 1.0, in_: 20.0, out: 18.0
            +                        1025 supriya:patch-cable:2x2
            +                            active: c11, gain: 0.0, gate: 0.0, in_: 20.0, out: 18.0
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
        ),
        # self
        (
            "mixers[0].tracks[0].tracks[0]",
            "mixers[0].tracks[0].tracks[0]",
            pytest.raises(RuntimeError),
            "",
            "",
        ),
        # parent: no-op
        (
            "mixers[0].tracks[0].tracks[0]",
            "mixers[0].tracks[0]",
            does_not_raise,
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
            @@ -8,6 +8,8 @@
                                         active: c11, gain: 0.0, gate: 1.0, in_: 28.0, out: 20.0
                                     1013 group (session.mixers[0].tracks[0].tracks[0]:tracks)
                                         1018 group (session.mixers[0].tracks[0].tracks[0].tracks[0]:group)
            +                                1066 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].tracks[0].feedback:synth)
            +                                    active: c17, gain: 0.0, gate: 1.0, in_: 36.0, out: 22.0
                                             1019 group (session.mixers[0].tracks[0].tracks[0].tracks[0]:tracks)
                                             1022 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0].tracks[0]:input-levels)
                                                 in_: 22.0, out: 19.0
            @@ -25,8 +27,10 @@
                                         active: c11, bus: 20.0, gain: c12, gate: 1.0
                                     1017 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:output-levels)
                                         in_: 20.0, out: 15.0
            -                        1025 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].output:synth)
            -                            active: c11, gain: 0.0, gate: 1.0, in_: 20.0, out: 18.0
            +                        1025 supriya:patch-cable:2x2
            +                            active: c11, gain: 0.0, gate: 0.0, in_: 20.0, out: 18.0
            +                        1067 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].output:synth)
            +                            active: c11, gain: 0.0, gate: 1.0, in_: 20.0, out: 36.0
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
            @@ -25,8 +25,10 @@
                                         active: c11, bus: 20.0, gain: c12, gate: 1.0
                                     1017 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:output-levels)
                                         in_: 20.0, out: 15.0
            -                        1025 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].output:synth)
            -                            active: c11, gain: 0.0, gate: 1.0, in_: 20.0, out: 18.0
            +                        1025 supriya:patch-cable:2x2
            +                            active: c11, gain: 0.0, gate: 0.0, in_: 20.0, out: 18.0
            +                        1066 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].output:synth)
            +                            active: c11, gain: 0.0, gate: 1.0, in_: 20.0, out: 26.0
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
        # mixer: no-op
        (
            "mixers[0].tracks[0]",
            "mixers[0]",
            does_not_raise,
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
            @@ -25,8 +25,10 @@
                                         active: c11, bus: 20.0, gain: c12, gate: 1.0
                                     1017 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:output-levels)
                                         in_: 20.0, out: 15.0
            -                        1025 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].output:synth)
            -                            active: c11, gain: 0.0, gate: 1.0, in_: 20.0, out: 18.0
            +                        1025 supriya:patch-cable:2x2
            +                            active: c11, gain: 0.0, gate: 0.0, in_: 20.0, out: 18.0
            +                        1066 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].output:synth)
            +                            active: c11, gain: 0.0, gate: 1.0, in_: 20.0, out: 24.0
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
        ),
    ],
)
@pytest.mark.asyncio
async def test_Track_set_output(
    complex_session: tuple[Session, str],
    expected_commands: str,
    expected_diff: str,
    maybe_raises,
    online: bool,
    source: str,
    target: Default | str | tuple[int, int] | None,
) -> None:
    # Pre-conditions
    session, initial_tree = complex_session
    if online:
        await session.boot()
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
    with maybe_raises, capture(session["mixers[0]"].context) as commands:
        await source_.set_output(target_)
    # Post-conditions
    if not online:
        return
    await assert_diff(
        session,
        expected_diff,
        expected_initial_tree=initial_tree,
    )
    assert format_messages(commands) == normalize(expected_commands)


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "actions, expected_state, expected_commands",
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
async def test_Track_set_soloed(
    actions: list[tuple[str, list[bool]]],
    complex_session: tuple[Session, str],
    expected_commands: str,
    expected_state: list[tuple[str, tuple[float, ...], bool]],
    online: bool,
) -> None:
    # Pre-conditions
    session, initial_tree = complex_session
    if online:
        await session.boot()
        await session.mixers[0].tracks[0].tracks[0].tracks[0].add_device()
        await session.mixers[0].tracks[1].sends[0].delete()
        await asyncio.sleep(0.25)
        initial_tree = await debug_tree(session)
    # Operation
    with capture(session["mixers[0]"].context) as commands:
        for target, args in actions:
            target_ = session[target]
            assert isinstance(target_, Track)
            await target_.set_soloed(*args)
    # Post-conditions
    if not online:
        return
    await assert_diff(
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
    assert format_messages(commands) == normalize(expected_commands)


@pytest.mark.xfail
@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "expected_diff, expected_commands",
    [
        ("", ""),
    ],
)
@pytest.mark.asyncio
async def test_Track_ungroup(
    complex_session: tuple[Session, str],
    expected_commands: str,
    expected_diff: str,
    online: bool,
    target: str,
) -> None:
    # Pre-conditions
    session, initial_tree = complex_session
    if online:
        await session.boot()
    target_ = session[target]
    assert isinstance(target_, Track)
    # Operation
    with capture(session["mixers[0]"].context) as commands:
        await target_.ungroup()
    # Post-conditions
    if not online:
        raise Exception
    await assert_diff(
        session,
        expected_diff,
        expected_initial_tree="""
        """,
    )
    assert format_messages(commands) == normalize(expected_commands)
    raise Exception
