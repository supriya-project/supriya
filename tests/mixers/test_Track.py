import contextlib
import difflib
from typing import Dict, List, Optional, Union

import pytest
from uqbar.strings import normalize

from supriya.mixers import Session
from supriya.mixers.mixers import Mixer
from supriya.mixers.tracks import Track, TrackContainer
from supriya.typing import DEFAULT, Default

does_not_raise = contextlib.nullcontext()


async def assert_diff(session: Session, expected_diff: str, initial_tree: str) -> None:
    await session.sync()
    actual_tree = str(await session.dump_tree()).replace(
        repr(session.contexts[0]), "{context}"
    )
    print("initial", normalize(initial_tree))
    print("actual", normalize(actual_tree))
    actual_diff = "".join(
        difflib.unified_diff(
            normalize(initial_tree).splitlines(True),
            actual_tree.splitlines(True),
            tofile="mutation",
            fromfile="initial",
        )
    )
    assert normalize(expected_diff) == normalize(actual_diff)


@contextlib.contextmanager
def capture(context):
    if context is None:
        return
    with context.osc_protocol.capture() as transcript:
        yield
    for x in transcript:
        print(x)


@pytest.fixture
def track(mixer: Mixer) -> Track:
    return mixer.tracks[0]


@pytest.mark.asyncio
async def test_Track_activate(track: Track) -> None:
    await track.activate()


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "postfader, target, expected_diff",
    [
        (
            True,
            "mixer",
            """
            --- initial
            +++ mutation
            @@ -5,6 +5,8 @@
                             1005 group (session.mixers[0].tracks[0]:tracks)
                             1006 channel-strip-2 (session.mixers[0].tracks[0]:channel_strip)
                                 active: 1.0, bus: 18.0, gain: 0.0, gate: 1.0
            +                1012 patch-cable-2 (session.mixers[0].tracks[0].send:synth)
            +                    gate: 1.0, in_: 18.0, out: 16.0
                             1007 patch-cable-2 (session.mixers[0].tracks[0].output:synth)
                                 gate: 1.0, in_: 18.0, out: 16.0
                         1008 group (session.mixers[0].tracks[1]:group)
            """,
        ),
        (
            True,
            "other",
            """
            --- initial
            +++ mutation
            @@ -5,6 +5,8 @@
                             1005 group (session.mixers[0].tracks[0]:tracks)
                             1006 channel-strip-2 (session.mixers[0].tracks[0]:channel_strip)
                                 active: 1.0, bus: 18.0, gain: 0.0, gate: 1.0
            +                1012 patch-cable-2 (session.mixers[0].tracks[0].send:synth)
            +                    gate: 1.0, in_: 18.0, out: 20.0
                             1007 patch-cable-2 (session.mixers[0].tracks[0].output:synth)
                                 gate: 1.0, in_: 18.0, out: 16.0
                         1008 group (session.mixers[0].tracks[1]:group)
            """,
        ),
        (
            False,
            "other",
            """
            --- initial
            +++ mutation
            @@ -3,6 +3,8 @@
                     1001 group (session.mixers[0]:tracks)
                         1004 group (session.mixers[0].tracks[0]:group)
                             1005 group (session.mixers[0].tracks[0]:tracks)
            +                1012 patch-cable-2 (session.mixers[0].tracks[0].send:synth)
            +                    gate: 1.0, in_: 18.0, out: 20.0
                             1006 channel-strip-2 (session.mixers[0].tracks[0]:channel_strip)
                                 active: 1.0, bus: 18.0, gain: 0.0, gate: 1.0
                             1007 patch-cable-2 (session.mixers[0].tracks[0].output:synth)
            """,
        ),
        (
            False,
            "self",
            """
            --- initial
            +++ mutation
            @@ -3,6 +3,8 @@
                     1001 group (session.mixers[0]:tracks)
                         1004 group (session.mixers[0].tracks[0]:group)
                             1005 group (session.mixers[0].tracks[0]:tracks)
            +                1012 patch-cable-2 (session.mixers[0].tracks[0].send:synth)
            +                    gate: 1.0, in_: 18.0, out: 18.0
                             1006 channel-strip-2 (session.mixers[0].tracks[0]:channel_strip)
                                 active: 1.0, bus: 18.0, gain: 0.0, gate: 1.0
                             1007 patch-cable-2 (session.mixers[0].tracks[0].output:synth)
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_Track_add_send(
    expected_diff: str,
    mixer: Mixer,
    online: bool,
    postfader: bool,
    session: Session,
    target: str,
    track: Track,
) -> None:
    # Pre-conditions
    if online:
        await session.boot()
    targets: Dict[str, TrackContainer] = {
        "mixer": mixer,
        "other": await mixer.add_track(),
        "self": track,
    }
    target_ = targets[target]
    # Operation
    send = await track.add_send(postfader=postfader, target=target_)
    # Post-conditions
    assert send in track.sends
    assert send.parent is track
    assert send.postfader == postfader
    assert send.target is target_
    assert track.sends[0] is send
    if not online:
        return
    await assert_diff(
        session,
        expected_diff,
        initial_tree="""
        {context}
            NODE TREE 1000 group (session.mixers[0]:group)
                1001 group (session.mixers[0]:tracks)
                    1004 group (session.mixers[0].tracks[0]:group)
                        1005 group (session.mixers[0].tracks[0]:tracks)
                        1006 channel-strip-2 (session.mixers[0].tracks[0]:channel_strip)
                            active: 1.0, bus: 18.0, gain: 0.0, gate: 1.0
                        1007 patch-cable-2 (session.mixers[0].tracks[0].output:synth)
                            gate: 1.0, in_: 18.0, out: 16.0
                    1008 group (session.mixers[0].tracks[1]:group)
                        1009 group (session.mixers[0].tracks[1]:tracks)
                        1010 channel-strip-2 (session.mixers[0].tracks[1]:channel_strip)
                            active: 1.0, bus: 20.0, gain: 0.0, gate: 1.0
                        1011 patch-cable-2 (session.mixers[0].tracks[1].output:synth)
                            gate: 1.0, in_: 20.0, out: 16.0
                1002 channel-strip-2 (session.mixers[0]:channel_strip)
                    active: 1.0, bus: 16.0, gain: 0.0, gate: 1.0
                1003 patch-cable-2 (session.mixers[0]:output)
                    gate: 1.0, in_: 16.0, out: 0.0
        """,
    )


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.asyncio
async def test_Track_add_track(
    online: bool,
    session: Session,
    track: Track,
) -> None:
    # Pre-conditions
    if online:
        await session.boot()
    # Operation
    child_track = await track.add_track()
    # Post-conditions
    assert child_track in track.tracks
    assert child_track.parent is track
    assert track.tracks[0] is child_track
    if not online:
        return
    await assert_diff(
        session,
        expected_diff="""
        --- initial
        +++ mutation
        @@ -3,6 +3,12 @@
                 1001 group (session.mixers[0]:tracks)
                     1004 group (session.mixers[0].tracks[0]:group)
                         1005 group (session.mixers[0].tracks[0]:tracks)
        +                    1008 group (session.mixers[0].tracks[0].tracks[0]:group)
        +                        1009 group (session.mixers[0].tracks[0].tracks[0]:tracks)
        +                        1010 channel-strip-2 (session.mixers[0].tracks[0].tracks[0]:channel_strip)
        +                            active: 1.0, bus: 20.0, gain: 0.0, gate: 1.0
        +                        1011 patch-cable-2 (session.mixers[0].tracks[0].tracks[0].output:synth)
        +                            gate: 1.0, in_: 20.0, out: 18.0
                         1006 channel-strip-2 (session.mixers[0].tracks[0]:channel_strip)
                             active: 1.0, bus: 18.0, gain: 0.0, gate: 1.0
                         1007 patch-cable-2 (session.mixers[0].tracks[0].output:synth)
        """,
        initial_tree="""
        {context}
            NODE TREE 1000 group (session.mixers[0]:group)
                1001 group (session.mixers[0]:tracks)
                    1004 group (session.mixers[0].tracks[0]:group)
                        1005 group (session.mixers[0].tracks[0]:tracks)
                        1006 channel-strip-2 (session.mixers[0].tracks[0]:channel_strip)
                            active: 1.0, bus: 18.0, gain: 0.0, gate: 1.0
                        1007 patch-cable-2 (session.mixers[0].tracks[0].output:synth)
                            gate: 1.0, in_: 18.0, out: 16.0
                1002 channel-strip-2 (session.mixers[0]:channel_strip)
                    active: 1.0, bus: 16.0, gain: 0.0, gate: 1.0
                1003 patch-cable-2 (session.mixers[0]:output)
                    gate: 1.0, in_: 16.0, out: 0.0
        """,
    )


@pytest.mark.asyncio
async def test_Track_deactivate(track: Track) -> None:
    await track.deactivate()


@pytest.mark.skip
@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "target, expected_diff",
    [
        ("parent", ""),
        ("self", ""),
        ("child", ""),
        ("sibling", ""),
    ],
)
@pytest.mark.asyncio
async def test_Track_delete(
    expected_diff: str,
    online: bool,
    mixer: Mixer,
    session: Session,
    target: str,
) -> None:
    # Pre-conditions
    if online:
        await session.boot()
    targets: Dict[str, Track] = {
        "parent": (parent := await mixer.add_track()),
        "self": (track := await parent.add_track()),
        "child": await track.add_track(),
        "sibling": (sibling := await mixer.add_track()),
    }
    await sibling.set_output(track)
    target_ = targets[target]
    parent_ = target_.parent
    # Operation
    await target_.delete()
    # Post-conditions
    assert parent_ and target_ not in parent_.children
    if not online:
        return
    await assert_diff(
        session,
        expected_diff,
        initial_tree="""
        {context}
            NODE TREE 1000 group (session.mixers[0]:group)
                1001 group (session.mixers[0]:tracks)
                    1004 group (session.mixers[0].tracks[0]:group)
                        1005 group (session.mixers[0].tracks[0]:tracks)
                        1006 channel-strip-2 (session.mixers[0].tracks[0]:channel_strip)
                            active: 1.0, bus: 18.0, gain: 0.0, gate: 1.0
                        1007 patch-cable-2 (session.mixers[0].tracks[0].output:synth)
                            gate: 1.0, in_: 18.0, out: 16.0
                    1008 group (session.mixers[0].tracks[1]:group)
                        1009 group (session.mixers[0].tracks[1]:tracks)
                            1012 group (session.mixers[0].tracks[1].tracks[0]:group)
                                1013 group (session.mixers[0].tracks[1].tracks[0]:tracks)
                                    1016 group (session.mixers[0].tracks[1].tracks[0].tracks[0]:group)
                                        1017 group (session.mixers[0].tracks[1].tracks[0].tracks[0]:tracks)
                                        1018 channel-strip-2 (session.mixers[0].tracks[1].tracks[0].tracks[0]:channel_strip)
                                            active: 1.0, bus: 24.0, gain: 0.0, gate: 1.0
                                        1019 patch-cable-2 (session.mixers[0].tracks[1].tracks[0].tracks[0].output:synth)
                                            gate: 1.0, in_: 24.0, out: 22.0
                                1014 channel-strip-2 (session.mixers[0].tracks[1].tracks[0]:channel_strip)
                                    active: 1.0, bus: 22.0, gain: 0.0, gate: 1.0
                                1015 patch-cable-2 (session.mixers[0].tracks[1].tracks[0].output:synth)
                                    gate: 1.0, in_: 22.0, out: 20.0
                        1010 channel-strip-2 (session.mixers[0].tracks[1]:channel_strip)
                            active: 1.0, bus: 20.0, gain: 0.0, gate: 1.0
                        1011 patch-cable-2 (session.mixers[0].tracks[1].output:synth)
                            gate: 1.0, in_: 20.0, out: 16.0
                    1020 group (session.mixers[0].tracks[2]:group)
                        1021 group (session.mixers[0].tracks[2]:tracks)
                        1022 channel-strip-2 (session.mixers[0].tracks[2]:channel_strip)
                            active: 1.0, bus: 26.0, gain: 0.0, gate: 1.0
                        1023 patch-cable-2
                            gate: 0.0, in_: 26.0, out: 16.0
                        1024 patch-cable-2 (session.mixers[0].tracks[2].output:synth)
                            gate: 1.0, in_: 26.0, out: 22.0
                1002 channel-strip-2 (session.mixers[0]:channel_strip)
                    active: 1.0, bus: 16.0, gain: 0.0, gate: 1.0
                1003 patch-cable-2 (session.mixers[0]:output)
                    gate: 1.0, in_: 16.0, out: 0.0
        """,
    )


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "parent, index, maybe_raises, expected_graph_order, expected_diff",
    [
        ("self", 0, pytest.raises(RuntimeError), [0, 0], ""),
        ("mixer", 0, does_not_raise, [0, 0], ""),
        (
            "mixer",
            1,
            does_not_raise,
            [0, 1],
            """
            --- initial
            +++ mutation
            @@ -1,18 +1,18 @@
             {context}
                 NODE TREE 1000 group (session.mixers[0]:group)
                     1001 group (session.mixers[0]:tracks)
            -            1004 group (session.mixers[0].tracks[0]:group)
            -                1005 group (session.mixers[0].tracks[0]:tracks)
            -                1006 channel-strip-2 (session.mixers[0].tracks[0]:channel_strip)
            +            1008 group (session.mixers[0].tracks[0]:group)
            +                1009 group (session.mixers[0].tracks[0]:tracks)
            +                1010 channel-strip-2 (session.mixers[0].tracks[0]:channel_strip)
            +                    active: 1.0, bus: 20.0, gain: 0.0, gate: 1.0
            +                1011 patch-cable-2 (session.mixers[0].tracks[0].output:synth)
            +                    gate: 1.0, in_: 20.0, out: 16.0
            +            1004 group (session.mixers[0].tracks[1]:group)
            +                1005 group (session.mixers[0].tracks[1]:tracks)
            +                1006 channel-strip-2 (session.mixers[0].tracks[1]:channel_strip)
                                 active: 1.0, bus: 18.0, gain: 0.0, gate: 1.0
            -                1007 patch-cable-2 (session.mixers[0].tracks[0].output:synth)
            +                1007 patch-cable-2 (session.mixers[0].tracks[1].output:synth)
                                 gate: 1.0, in_: 18.0, out: 16.0
            -            1008 group (session.mixers[0].tracks[1]:group)
            -                1009 group (session.mixers[0].tracks[1]:tracks)
            -                1010 channel-strip-2 (session.mixers[0].tracks[1]:channel_strip)
            -                    active: 1.0, bus: 20.0, gain: 0.0, gate: 1.0
            -                1011 patch-cable-2 (session.mixers[0].tracks[1].output:synth)
            -                    gate: 1.0, in_: 20.0, out: 16.0
                         1012 group (session.mixers[0].tracks[2]:group)
                             1013 group (session.mixers[0].tracks[2]:tracks)
                             1014 channel-strip-2 (session.mixers[0].tracks[2]:channel_strip)
            """,
        ),
        (
            "mixer",
            2,
            does_not_raise,
            [0, 2],
            """
            --- initial
            +++ mutation
            @@ -1,24 +1,24 @@
             {context}
                 NODE TREE 1000 group (session.mixers[0]:group)
                     1001 group (session.mixers[0]:tracks)
            -            1004 group (session.mixers[0].tracks[0]:group)
            -                1005 group (session.mixers[0].tracks[0]:tracks)
            -                1006 channel-strip-2 (session.mixers[0].tracks[0]:channel_strip)
            +            1008 group (session.mixers[0].tracks[0]:group)
            +                1009 group (session.mixers[0].tracks[0]:tracks)
            +                1010 channel-strip-2 (session.mixers[0].tracks[0]:channel_strip)
            +                    active: 1.0, bus: 20.0, gain: 0.0, gate: 1.0
            +                1011 patch-cable-2 (session.mixers[0].tracks[0].output:synth)
            +                    gate: 1.0, in_: 20.0, out: 16.0
            +            1012 group (session.mixers[0].tracks[1]:group)
            +                1013 group (session.mixers[0].tracks[1]:tracks)
            +                1014 channel-strip-2 (session.mixers[0].tracks[1]:channel_strip)
            +                    active: 1.0, bus: 22.0, gain: 0.0, gate: 1.0
            +                1015 patch-cable-2 (session.mixers[0].tracks[1].output:synth)
            +                    gate: 1.0, in_: 22.0, out: 16.0
            +            1004 group (session.mixers[0].tracks[2]:group)
            +                1005 group (session.mixers[0].tracks[2]:tracks)
            +                1006 channel-strip-2 (session.mixers[0].tracks[2]:channel_strip)
                                 active: 1.0, bus: 18.0, gain: 0.0, gate: 1.0
            -                1007 patch-cable-2 (session.mixers[0].tracks[0].output:synth)
            +                1007 patch-cable-2 (session.mixers[0].tracks[2].output:synth)
                                 gate: 1.0, in_: 18.0, out: 16.0
            -            1008 group (session.mixers[0].tracks[1]:group)
            -                1009 group (session.mixers[0].tracks[1]:tracks)
            -                1010 channel-strip-2 (session.mixers[0].tracks[1]:channel_strip)
            -                    active: 1.0, bus: 20.0, gain: 0.0, gate: 1.0
            -                1011 patch-cable-2 (session.mixers[0].tracks[1].output:synth)
            -                    gate: 1.0, in_: 20.0, out: 16.0
            -            1012 group (session.mixers[0].tracks[2]:group)
            -                1013 group (session.mixers[0].tracks[2]:tracks)
            -                1014 channel-strip-2 (session.mixers[0].tracks[2]:channel_strip)
            -                    active: 1.0, bus: 22.0, gain: 0.0, gate: 1.0
            -                1015 patch-cable-2 (session.mixers[0].tracks[2].output:synth)
            -                    gate: 1.0, in_: 22.0, out: 16.0
                     1002 channel-strip-2 (session.mixers[0]:channel_strip)
                         active: 1.0, bus: 16.0, gain: 0.0, gate: 1.0
                     1003 patch-cable-2 (session.mixers[0]:output)
            """,
        ),
        (
            "other",
            0,
            does_not_raise,
            [0, 0, 0],
            """
            --- initial
            +++ mutation
            @@ -1,23 +1,25 @@
             {context}
                 NODE TREE 1000 group (session.mixers[0]:group)
                     1001 group (session.mixers[0]:tracks)
            -            1004 group (session.mixers[0].tracks[0]:group)
            -                1005 group (session.mixers[0].tracks[0]:tracks)
            -                1006 channel-strip-2 (session.mixers[0].tracks[0]:channel_strip)
            -                    active: 1.0, bus: 18.0, gain: 0.0, gate: 1.0
            -                1007 patch-cable-2 (session.mixers[0].tracks[0].output:synth)
            -                    gate: 1.0, in_: 18.0, out: 16.0
            -            1008 group (session.mixers[0].tracks[1]:group)
            -                1009 group (session.mixers[0].tracks[1]:tracks)
            -                1010 channel-strip-2 (session.mixers[0].tracks[1]:channel_strip)
            +            1008 group (session.mixers[0].tracks[0]:group)
            +                1009 group (session.mixers[0].tracks[0]:tracks)
            +                    1004 group (session.mixers[0].tracks[0].tracks[0]:group)
            +                        1005 group (session.mixers[0].tracks[0].tracks[0]:tracks)
            +                        1006 channel-strip-2 (session.mixers[0].tracks[0].tracks[0]:channel_strip)
            +                            active: 1.0, bus: 18.0, gain: 0.0, gate: 1.0
            +                        1007 patch-cable-2
            +                            gate: 0.0, in_: 18.0, out: 16.0
            +                        1024 patch-cable-2 (session.mixers[0].tracks[0].tracks[0].output:synth)
            +                            gate: 1.0, in_: 18.0, out: 20.0
            +                1010 channel-strip-2 (session.mixers[0].tracks[0]:channel_strip)
                                 active: 1.0, bus: 20.0, gain: 0.0, gate: 1.0
            -                1011 patch-cable-2 (session.mixers[0].tracks[1].output:synth)
            +                1011 patch-cable-2 (session.mixers[0].tracks[0].output:synth)
                                 gate: 1.0, in_: 20.0, out: 16.0
            -            1012 group (session.mixers[0].tracks[2]:group)
            -                1013 group (session.mixers[0].tracks[2]:tracks)
            -                1014 channel-strip-2 (session.mixers[0].tracks[2]:channel_strip)
            +            1012 group (session.mixers[0].tracks[1]:group)
            +                1013 group (session.mixers[0].tracks[1]:tracks)
            +                1014 channel-strip-2 (session.mixers[0].tracks[1]:channel_strip)
                                 active: 1.0, bus: 22.0, gain: 0.0, gate: 1.0
            -                1015 patch-cable-2 (session.mixers[0].tracks[2].output:synth)
            +                1015 patch-cable-2 (session.mixers[0].tracks[1].output:synth)
                                 gate: 1.0, in_: 22.0, out: 16.0
                     1002 channel-strip-2 (session.mixers[0]:channel_strip)
                         active: 1.0, bus: 16.0, gain: 0.0, gate: 1.0
            """,
        ),
        (
            "other_other",
            0,
            does_not_raise,
            [0, 1, 0],
            """
            --- initial
            +++ mutation
            @@ -1,23 +1,25 @@
             {context}
                 NODE TREE 1000 group (session.mixers[0]:group)
                     1001 group (session.mixers[0]:tracks)
            -            1004 group (session.mixers[0].tracks[0]:group)
            -                1005 group (session.mixers[0].tracks[0]:tracks)
            -                1006 channel-strip-2 (session.mixers[0].tracks[0]:channel_strip)
            -                    active: 1.0, bus: 18.0, gain: 0.0, gate: 1.0
            -                1007 patch-cable-2 (session.mixers[0].tracks[0].output:synth)
            -                    gate: 1.0, in_: 18.0, out: 16.0
            -            1008 group (session.mixers[0].tracks[1]:group)
            -                1009 group (session.mixers[0].tracks[1]:tracks)
            -                1010 channel-strip-2 (session.mixers[0].tracks[1]:channel_strip)
            +            1008 group (session.mixers[0].tracks[0]:group)
            +                1009 group (session.mixers[0].tracks[0]:tracks)
            +                1010 channel-strip-2 (session.mixers[0].tracks[0]:channel_strip)
                                 active: 1.0, bus: 20.0, gain: 0.0, gate: 1.0
            -                1011 patch-cable-2 (session.mixers[0].tracks[1].output:synth)
            +                1011 patch-cable-2 (session.mixers[0].tracks[0].output:synth)
                                 gate: 1.0, in_: 20.0, out: 16.0
            -            1012 group (session.mixers[0].tracks[2]:group)
            -                1013 group (session.mixers[0].tracks[2]:tracks)
            -                1014 channel-strip-2 (session.mixers[0].tracks[2]:channel_strip)
            +            1012 group (session.mixers[0].tracks[1]:group)
            +                1013 group (session.mixers[0].tracks[1]:tracks)
            +                    1004 group (session.mixers[0].tracks[1].tracks[0]:group)
            +                        1005 group (session.mixers[0].tracks[1].tracks[0]:tracks)
            +                        1006 channel-strip-2 (session.mixers[0].tracks[1].tracks[0]:channel_strip)
            +                            active: 1.0, bus: 18.0, gain: 0.0, gate: 1.0
            +                        1007 patch-cable-2
            +                            gate: 0.0, in_: 18.0, out: 16.0
            +                        1024 patch-cable-2 (session.mixers[0].tracks[1].tracks[0].output:synth)
            +                            gate: 1.0, in_: 18.0, out: 22.0
            +                1014 channel-strip-2 (session.mixers[0].tracks[1]:channel_strip)
                                 active: 1.0, bus: 22.0, gain: 0.0, gate: 1.0
            -                1015 patch-cable-2 (session.mixers[0].tracks[2].output:synth)
            +                1015 patch-cable-2 (session.mixers[0].tracks[1].output:synth)
                                 gate: 1.0, in_: 22.0, out: 16.0
                     1002 channel-strip-2 (session.mixers[0]:channel_strip)
                         active: 1.0, bus: 16.0, gain: 0.0, gate: 1.0
            """,
        ),
        ("other_mixer", 0, pytest.raises(RuntimeError), [0, 0], ""),
    ],
)
@pytest.mark.asyncio
async def test_Track_move(
    expected_graph_order: List[int],
    expected_diff: str,
    index: int,
    mixer: Mixer,
    online: bool,
    parent: str,
    maybe_raises,
    session: Session,
    track: Track,
) -> None:
    # Pre-conditions
    if online:
        await session.boot()
    targets: Dict[str, TrackContainer] = {
        "self": track,
        "mixer": mixer,
        "other": await mixer.add_track(),
        "other_other": await mixer.add_track(),
        "other_mixer": await session.add_mixer(),
    }
    # Operation
    with maybe_raises:
        await track.move(index=index, parent=targets[parent])
    # Post-conditions
    assert track.graph_order == expected_graph_order
    if not online:
        return
    await assert_diff(
        session,
        expected_diff,
        initial_tree="""
        {context}
            NODE TREE 1000 group (session.mixers[0]:group)
                1001 group (session.mixers[0]:tracks)
                    1004 group (session.mixers[0].tracks[0]:group)
                        1005 group (session.mixers[0].tracks[0]:tracks)
                        1006 channel-strip-2 (session.mixers[0].tracks[0]:channel_strip)
                            active: 1.0, bus: 18.0, gain: 0.0, gate: 1.0
                        1007 patch-cable-2 (session.mixers[0].tracks[0].output:synth)
                            gate: 1.0, in_: 18.0, out: 16.0
                    1008 group (session.mixers[0].tracks[1]:group)
                        1009 group (session.mixers[0].tracks[1]:tracks)
                        1010 channel-strip-2 (session.mixers[0].tracks[1]:channel_strip)
                            active: 1.0, bus: 20.0, gain: 0.0, gate: 1.0
                        1011 patch-cable-2 (session.mixers[0].tracks[1].output:synth)
                            gate: 1.0, in_: 20.0, out: 16.0
                    1012 group (session.mixers[0].tracks[2]:group)
                        1013 group (session.mixers[0].tracks[2]:tracks)
                        1014 channel-strip-2 (session.mixers[0].tracks[2]:channel_strip)
                            active: 1.0, bus: 22.0, gain: 0.0, gate: 1.0
                        1015 patch-cable-2 (session.mixers[0].tracks[2].output:synth)
                            gate: 1.0, in_: 22.0, out: 16.0
                1002 channel-strip-2 (session.mixers[0]:channel_strip)
                    active: 1.0, bus: 16.0, gain: 0.0, gate: 1.0
                1003 patch-cable-2 (session.mixers[0]:output)
                    gate: 1.0, in_: 16.0, out: 0.0
            NODE TREE 1016 group (session.mixers[1]:group)
                1017 group (session.mixers[1]:tracks)
                    1020 group (session.mixers[1].tracks[0]:group)
                        1021 group (session.mixers[1].tracks[0]:tracks)
                        1022 channel-strip-2 (session.mixers[1].tracks[0]:channel_strip)
                            active: 1.0, bus: 26.0, gain: 0.0, gate: 1.0
                        1023 patch-cable-2 (session.mixers[1].tracks[0].output:synth)
                            gate: 1.0, in_: 26.0, out: 24.0
                1018 channel-strip-2 (session.mixers[1]:channel_strip)
                    active: 1.0, bus: 24.0, gain: 0.0, gate: 1.0
                1019 patch-cable-2 (session.mixers[1]:output)
                    gate: 1.0, in_: 24.0, out: 0.0
        """,
    )


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "output, maybe_raises, expected_diff",
    [
        (
            "none",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -13,8 +13,8 @@
                                                 gate: 1.0, in_: 22.0, out: 20.0
                                     1009 channel-strip-2 (session.mixers[0].tracks[0].tracks[0]:channel_strip)
                                         active: 1.0, bus: 20.0, gain: 0.0, gate: 1.0
            -                        1014 patch-cable-2 (session.mixers[0].tracks[0].tracks[0].output:synth)
            -                            gate: 1.0, in_: 20.0, out: 18.0
            +                        1014 patch-cable-2
            +                            gate: 0.0, in_: 20.0, out: 18.0
                             1006 channel-strip-2 (session.mixers[0].tracks[0]:channel_strip)
                                 active: 1.0, bus: 18.0, gain: 0.0, gate: 1.0
                             1015 patch-cable-2 (session.mixers[0].tracks[0].output:synth)
            """,
        ),
        (
            "default",
            does_not_raise,
            "",
        ),
        (
            "self",
            pytest.raises(RuntimeError),
            "",
        ),
        (
            "parent",
            does_not_raise,
            "",
        ),
        (
            "child",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -13,8 +13,10 @@
                                                 gate: 1.0, in_: 22.0, out: 20.0
                                     1009 channel-strip-2 (session.mixers[0].tracks[0].tracks[0]:channel_strip)
                                         active: 1.0, bus: 20.0, gain: 0.0, gate: 1.0
            -                        1014 patch-cable-2 (session.mixers[0].tracks[0].tracks[0].output:synth)
            -                            gate: 1.0, in_: 20.0, out: 18.0
            +                        1014 patch-cable-2
            +                            gate: 0.0, in_: 20.0, out: 18.0
            +                        1028 patch-cable-2 (session.mixers[0].tracks[0].tracks[0].output:synth)
            +                            gate: 1.0, in_: 20.0, out: 22.0
                             1006 channel-strip-2 (session.mixers[0].tracks[0]:channel_strip)
                                 active: 1.0, bus: 18.0, gain: 0.0, gate: 1.0
                             1015 patch-cable-2 (session.mixers[0].tracks[0].output:synth)
            """,
        ),
        (
            "mixer",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -13,8 +13,10 @@
                                                 gate: 1.0, in_: 22.0, out: 20.0
                                     1009 channel-strip-2 (session.mixers[0].tracks[0].tracks[0]:channel_strip)
                                         active: 1.0, bus: 20.0, gain: 0.0, gate: 1.0
            -                        1014 patch-cable-2 (session.mixers[0].tracks[0].tracks[0].output:synth)
            -                            gate: 1.0, in_: 20.0, out: 18.0
            +                        1014 patch-cable-2
            +                            gate: 0.0, in_: 20.0, out: 18.0
            +                        1028 patch-cable-2 (session.mixers[0].tracks[0].tracks[0].output:synth)
            +                            gate: 1.0, in_: 20.0, out: 16.0
                             1006 channel-strip-2 (session.mixers[0].tracks[0]:channel_strip)
                                 active: 1.0, bus: 18.0, gain: 0.0, gate: 1.0
                             1015 patch-cable-2 (session.mixers[0].tracks[0].output:synth)
            """,
        ),
        (
            "sibling",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -13,8 +13,10 @@
                                                 gate: 1.0, in_: 22.0, out: 20.0
                                     1009 channel-strip-2 (session.mixers[0].tracks[0].tracks[0]:channel_strip)
                                         active: 1.0, bus: 20.0, gain: 0.0, gate: 1.0
            -                        1014 patch-cable-2 (session.mixers[0].tracks[0].tracks[0].output:synth)
            -                            gate: 1.0, in_: 20.0, out: 18.0
            +                        1014 patch-cable-2
            +                            gate: 0.0, in_: 20.0, out: 18.0
            +                        1028 patch-cable-2 (session.mixers[0].tracks[0].tracks[0].output:synth)
            +                            gate: 1.0, in_: 20.0, out: 24.0
                             1006 channel-strip-2 (session.mixers[0].tracks[0]:channel_strip)
                                 active: 1.0, bus: 18.0, gain: 0.0, gate: 1.0
                             1015 patch-cable-2 (session.mixers[0].tracks[0].output:synth)
            """,
        ),
        (
            "other_mixer",
            pytest.raises(RuntimeError),
            "",
        ),
    ],
)
@pytest.mark.asyncio
async def test_Track_set_output(
    expected_diff: str,
    maybe_raises,
    mixer: Mixer,
    online: bool,
    output: str,
    session: Session,
    track: Track,
) -> None:
    # Pre-conditions
    subtrack = await track.add_track()
    subsubtrack = await subtrack.add_track()
    sibling = await mixer.add_track()
    if online or True:
        await session.boot()
    targets: Dict[str, Optional[Union[Default, TrackContainer]]] = {
        "child": subsubtrack,
        "default": DEFAULT,
        "mixer": mixer,
        "none": None,
        "other_mixer": await session.add_mixer(),
        "parent": track,
        "self": subtrack,
        "sibling": sibling,
    }
    print(str(await session.dump_tree()))
    # Operation
    with maybe_raises, capture(mixer.context):
        await subtrack.set_output(targets[output])
    # Post-conditions
    if not online:
        return
    await assert_diff(
        session,
        expected_diff,
        initial_tree="""
        {context}
            NODE TREE 1000 group (session.mixers[0]:group)
                1001 group (session.mixers[0]:tracks)
                    1004 group (session.mixers[0].tracks[0]:group)
                        1005 group (session.mixers[0].tracks[0]:tracks)
                            1007 group (session.mixers[0].tracks[0].tracks[0]:group)
                                1008 group (session.mixers[0].tracks[0].tracks[0]:tracks)
                                    1010 group (session.mixers[0].tracks[0].tracks[0].tracks[0]:group)
                                        1011 group (session.mixers[0].tracks[0].tracks[0].tracks[0]:tracks)
                                        1012 channel-strip-2 (session.mixers[0].tracks[0].tracks[0].tracks[0]:channel_strip)
                                            active: 1.0, bus: 22.0, gain: 0.0, gate: 1.0
                                        1013 patch-cable-2 (session.mixers[0].tracks[0].tracks[0].tracks[0].output:synth)
                                            gate: 1.0, in_: 22.0, out: 20.0
                                1009 channel-strip-2 (session.mixers[0].tracks[0].tracks[0]:channel_strip)
                                    active: 1.0, bus: 20.0, gain: 0.0, gate: 1.0
                                1014 patch-cable-2 (session.mixers[0].tracks[0].tracks[0].output:synth)
                                    gate: 1.0, in_: 20.0, out: 18.0
                        1006 channel-strip-2 (session.mixers[0].tracks[0]:channel_strip)
                            active: 1.0, bus: 18.0, gain: 0.0, gate: 1.0
                        1015 patch-cable-2 (session.mixers[0].tracks[0].output:synth)
                            gate: 1.0, in_: 18.0, out: 16.0
                    1016 group (session.mixers[0].tracks[1]:group)
                        1017 group (session.mixers[0].tracks[1]:tracks)
                        1018 channel-strip-2 (session.mixers[0].tracks[1]:channel_strip)
                            active: 1.0, bus: 24.0, gain: 0.0, gate: 1.0
                        1019 patch-cable-2 (session.mixers[0].tracks[1].output:synth)
                            gate: 1.0, in_: 24.0, out: 16.0
                1002 channel-strip-2 (session.mixers[0]:channel_strip)
                    active: 1.0, bus: 16.0, gain: 0.0, gate: 1.0
                1003 patch-cable-2 (session.mixers[0]:output)
                    gate: 1.0, in_: 16.0, out: 0.0
            NODE TREE 1020 group (session.mixers[1]:group)
                1021 group (session.mixers[1]:tracks)
                    1024 group (session.mixers[1].tracks[0]:group)
                        1025 group (session.mixers[1].tracks[0]:tracks)
                        1026 channel-strip-2 (session.mixers[1].tracks[0]:channel_strip)
                            active: 1.0, bus: 28.0, gain: 0.0, gate: 1.0
                        1027 patch-cable-2 (session.mixers[1].tracks[0].output:synth)
                            gate: 1.0, in_: 28.0, out: 26.0
                1022 channel-strip-2 (session.mixers[1]:channel_strip)
                    active: 1.0, bus: 26.0, gain: 0.0, gate: 1.0
                1023 patch-cable-2 (session.mixers[1]:output)
                    gate: 1.0, in_: 26.0, out: 0.0
        """,
    )


@pytest.mark.asyncio
async def test_Track_solo(track: Track) -> None:
    await track.solo()


@pytest.mark.asyncio
async def test_Track_ungroup(track: Track) -> None:
    await track.ungroup()


@pytest.mark.asyncio
async def test_Track_unsolo(track: Track) -> None:
    await track.unsolo()
