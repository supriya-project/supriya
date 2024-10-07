import contextlib
from typing import Dict, List

import pytest
from uqbar.strings import normalize

from supriya.mixers import Session
from supriya.mixers.mixers import Mixer
from supriya.mixers.tracks import Track, TrackContainer
from supriya.typing import DEFAULT

does_not_raise = contextlib.nullcontext()


@pytest.fixture
def track(mixer: Mixer) -> Track:
    return mixer.tracks[0]


@pytest.mark.asyncio
async def test_Track_activate(track: Track) -> None:
    await track.activate()


@pytest.mark.asyncio
async def test_Track_add_track(track: Track) -> None:
    await track.add_track()


@pytest.mark.asyncio
async def test_Track_deactivate(track: Track) -> None:
    await track.deactivate()


@pytest.mark.asyncio
async def test_Track_delete(track: Track) -> None:
    await track.delete()


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "parent, index, maybe_raises, expected_graph_order, expected_tree",
    [
        (
            "self",
            0,
            pytest.raises(RuntimeError),
            [0, 0],
            """
            {context}
                NODE TREE 1000 group (session.mixers[0]:group)
                    1001 group (session.mixers[0]:tracks)
                        1004 group (session.mixers[0].tracks[0]:group)
                            1005 group (session.mixers[0].tracks[0]:tracks)
                            1006 channel-strip-2 (session.mixers[0].tracks[0]:channel_strip)
                                active: 1.0, bus: 18.0, gain: 0.0, gate: 1.0
                            1007 patch-cable-2 (session.mixers[0].tracks[0]:output)
                                gate: 1.0, in_: 18.0, out: 16.0
                        1008 group (session.mixers[0].tracks[1]:group)
                            1009 group (session.mixers[0].tracks[1]:tracks)
                            1010 channel-strip-2 (session.mixers[0].tracks[1]:channel_strip)
                                active: 1.0, bus: 20.0, gain: 0.0, gate: 1.0
                            1011 patch-cable-2 (session.mixers[0].tracks[1]:output)
                                gate: 1.0, in_: 20.0, out: 16.0
                        1012 group (session.mixers[0].tracks[2]:group)
                            1013 group (session.mixers[0].tracks[2]:tracks)
                            1014 channel-strip-2 (session.mixers[0].tracks[2]:channel_strip)
                                active: 1.0, bus: 22.0, gain: 0.0, gate: 1.0
                            1015 patch-cable-2 (session.mixers[0].tracks[2]:output)
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
                            1023 patch-cable-2 (session.mixers[1].tracks[0]:output)
                                gate: 1.0, in_: 26.0, out: 24.0
                    1018 channel-strip-2 (session.mixers[1]:channel_strip)
                        active: 1.0, bus: 24.0, gain: 0.0, gate: 1.0
                    1019 patch-cable-2 (session.mixers[1]:output)
                        gate: 1.0, in_: 24.0, out: 0.0
            """,
        ),
        (
            "mixer",
            0,
            does_not_raise,
            [0, 0],
            """
            {context}
                NODE TREE 1000 group (session.mixers[0]:group)
                    1001 group (session.mixers[0]:tracks)
                        1004 group (session.mixers[0].tracks[0]:group)
                            1005 group (session.mixers[0].tracks[0]:tracks)
                            1006 channel-strip-2 (session.mixers[0].tracks[0]:channel_strip)
                                active: 1.0, bus: 18.0, gain: 0.0, gate: 1.0
                            1007 patch-cable-2 (session.mixers[0].tracks[0]:output)
                                gate: 1.0, in_: 18.0, out: 16.0
                        1008 group (session.mixers[0].tracks[1]:group)
                            1009 group (session.mixers[0].tracks[1]:tracks)
                            1010 channel-strip-2 (session.mixers[0].tracks[1]:channel_strip)
                                active: 1.0, bus: 20.0, gain: 0.0, gate: 1.0
                            1011 patch-cable-2 (session.mixers[0].tracks[1]:output)
                                gate: 1.0, in_: 20.0, out: 16.0
                        1012 group (session.mixers[0].tracks[2]:group)
                            1013 group (session.mixers[0].tracks[2]:tracks)
                            1014 channel-strip-2 (session.mixers[0].tracks[2]:channel_strip)
                                active: 1.0, bus: 22.0, gain: 0.0, gate: 1.0
                            1015 patch-cable-2 (session.mixers[0].tracks[2]:output)
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
                            1023 patch-cable-2 (session.mixers[1].tracks[0]:output)
                                gate: 1.0, in_: 26.0, out: 24.0
                    1018 channel-strip-2 (session.mixers[1]:channel_strip)
                        active: 1.0, bus: 24.0, gain: 0.0, gate: 1.0
                    1019 patch-cable-2 (session.mixers[1]:output)
                        gate: 1.0, in_: 24.0, out: 0.0
            """,
        ),
        (
            "mixer",
            1,
            does_not_raise,
            [0, 1],
            """
            {context}
                NODE TREE 1000 group (session.mixers[0]:group)
                    1001 group (session.mixers[0]:tracks)
                        1008 group (session.mixers[0].tracks[0]:group)
                            1009 group (session.mixers[0].tracks[0]:tracks)
                            1010 channel-strip-2 (session.mixers[0].tracks[0]:channel_strip)
                                active: 1.0, bus: 20.0, gain: 0.0, gate: 1.0
                            1011 patch-cable-2 (session.mixers[0].tracks[0]:output)
                                gate: 1.0, in_: 20.0, out: 16.0
                        1004 group (session.mixers[0].tracks[1]:group)
                            1005 group (session.mixers[0].tracks[1]:tracks)
                            1006 channel-strip-2 (session.mixers[0].tracks[1]:channel_strip)
                                active: 1.0, bus: 18.0, gain: 0.0, gate: 1.0
                            1007 patch-cable-2 (session.mixers[0].tracks[1]:output)
                                gate: 1.0, in_: 18.0, out: 16.0
                        1012 group (session.mixers[0].tracks[2]:group)
                            1013 group (session.mixers[0].tracks[2]:tracks)
                            1014 channel-strip-2 (session.mixers[0].tracks[2]:channel_strip)
                                active: 1.0, bus: 22.0, gain: 0.0, gate: 1.0
                            1015 patch-cable-2 (session.mixers[0].tracks[2]:output)
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
                            1023 patch-cable-2 (session.mixers[1].tracks[0]:output)
                                gate: 1.0, in_: 26.0, out: 24.0
                    1018 channel-strip-2 (session.mixers[1]:channel_strip)
                        active: 1.0, bus: 24.0, gain: 0.0, gate: 1.0
                    1019 patch-cable-2 (session.mixers[1]:output)
                        gate: 1.0, in_: 24.0, out: 0.0
            """,
        ),
        (
            "mixer",
            2,
            does_not_raise,
            [0, 2],
            """
            {context}
                NODE TREE 1000 group (session.mixers[0]:group)
                    1001 group (session.mixers[0]:tracks)
                        1008 group (session.mixers[0].tracks[0]:group)
                            1009 group (session.mixers[0].tracks[0]:tracks)
                            1010 channel-strip-2 (session.mixers[0].tracks[0]:channel_strip)
                                active: 1.0, bus: 20.0, gain: 0.0, gate: 1.0
                            1011 patch-cable-2 (session.mixers[0].tracks[0]:output)
                                gate: 1.0, in_: 20.0, out: 16.0
                        1012 group (session.mixers[0].tracks[1]:group)
                            1013 group (session.mixers[0].tracks[1]:tracks)
                            1014 channel-strip-2 (session.mixers[0].tracks[1]:channel_strip)
                                active: 1.0, bus: 22.0, gain: 0.0, gate: 1.0
                            1015 patch-cable-2 (session.mixers[0].tracks[1]:output)
                                gate: 1.0, in_: 22.0, out: 16.0
                        1004 group (session.mixers[0].tracks[2]:group)
                            1005 group (session.mixers[0].tracks[2]:tracks)
                            1006 channel-strip-2 (session.mixers[0].tracks[2]:channel_strip)
                                active: 1.0, bus: 18.0, gain: 0.0, gate: 1.0
                            1007 patch-cable-2 (session.mixers[0].tracks[2]:output)
                                gate: 1.0, in_: 18.0, out: 16.0
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
                            1023 patch-cable-2 (session.mixers[1].tracks[0]:output)
                                gate: 1.0, in_: 26.0, out: 24.0
                    1018 channel-strip-2 (session.mixers[1]:channel_strip)
                        active: 1.0, bus: 24.0, gain: 0.0, gate: 1.0
                    1019 patch-cable-2 (session.mixers[1]:output)
                        gate: 1.0, in_: 24.0, out: 0.0
            """,
        ),
        (
            "other",
            0,
            does_not_raise,
            [0, 0, 0],
            """
            {context}
                NODE TREE 1000 group (session.mixers[0]:group)
                    1001 group (session.mixers[0]:tracks)
                        1008 group (session.mixers[0].tracks[0]:group)
                            1009 group (session.mixers[0].tracks[0]:tracks)
                                1004 group (session.mixers[0].tracks[0].tracks[0]:group)
                                    1005 group (session.mixers[0].tracks[0].tracks[0]:tracks)
                                    1006 channel-strip-2 (session.mixers[0].tracks[0].tracks[0]:channel_strip)
                                        active: 1.0, bus: 18.0, gain: 0.0, gate: 1.0
                                    1007 patch-cable-2
                                        gate: 0.0, in_: 18.0, out: 16.0
                                    1024 patch-cable-2 (session.mixers[0].tracks[0].tracks[0]:output)
                                        gate: 1.0, in_: 18.0, out: 20.0
                            1010 channel-strip-2 (session.mixers[0].tracks[0]:channel_strip)
                                active: 1.0, bus: 20.0, gain: 0.0, gate: 1.0
                            1011 patch-cable-2 (session.mixers[0].tracks[0]:output)
                                gate: 1.0, in_: 20.0, out: 16.0
                        1012 group (session.mixers[0].tracks[1]:group)
                            1013 group (session.mixers[0].tracks[1]:tracks)
                            1014 channel-strip-2 (session.mixers[0].tracks[1]:channel_strip)
                                active: 1.0, bus: 22.0, gain: 0.0, gate: 1.0
                            1015 patch-cable-2 (session.mixers[0].tracks[1]:output)
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
                            1023 patch-cable-2 (session.mixers[1].tracks[0]:output)
                                gate: 1.0, in_: 26.0, out: 24.0
                    1018 channel-strip-2 (session.mixers[1]:channel_strip)
                        active: 1.0, bus: 24.0, gain: 0.0, gate: 1.0
                    1019 patch-cable-2 (session.mixers[1]:output)
                        gate: 1.0, in_: 24.0, out: 0.0
            """,
        ),
        (
            "other_other",
            0,
            does_not_raise,
            [0, 1, 0],
            """
            {context}
                NODE TREE 1000 group (session.mixers[0]:group)
                    1001 group (session.mixers[0]:tracks)
                        1008 group (session.mixers[0].tracks[0]:group)
                            1009 group (session.mixers[0].tracks[0]:tracks)
                            1010 channel-strip-2 (session.mixers[0].tracks[0]:channel_strip)
                                active: 1.0, bus: 20.0, gain: 0.0, gate: 1.0
                            1011 patch-cable-2 (session.mixers[0].tracks[0]:output)
                                gate: 1.0, in_: 20.0, out: 16.0
                        1012 group (session.mixers[0].tracks[1]:group)
                            1013 group (session.mixers[0].tracks[1]:tracks)
                                1004 group (session.mixers[0].tracks[1].tracks[0]:group)
                                    1005 group (session.mixers[0].tracks[1].tracks[0]:tracks)
                                    1006 channel-strip-2 (session.mixers[0].tracks[1].tracks[0]:channel_strip)
                                        active: 1.0, bus: 18.0, gain: 0.0, gate: 1.0
                                    1007 patch-cable-2
                                        gate: 0.0, in_: 18.0, out: 16.0
                                    1024 patch-cable-2 (session.mixers[0].tracks[1].tracks[0]:output)
                                        gate: 1.0, in_: 18.0, out: 22.0
                            1014 channel-strip-2 (session.mixers[0].tracks[1]:channel_strip)
                                active: 1.0, bus: 22.0, gain: 0.0, gate: 1.0
                            1015 patch-cable-2 (session.mixers[0].tracks[1]:output)
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
                            1023 patch-cable-2 (session.mixers[1].tracks[0]:output)
                                gate: 1.0, in_: 26.0, out: 24.0
                    1018 channel-strip-2 (session.mixers[1]:channel_strip)
                        active: 1.0, bus: 24.0, gain: 0.0, gate: 1.0
                    1019 patch-cable-2 (session.mixers[1]:output)
                        gate: 1.0, in_: 24.0, out: 0.0
            """,
        ),
        (
            "other_mixer",
            0,
            pytest.raises(RuntimeError),
            [0, 0],
            """
            {context}
                NODE TREE 1000 group (session.mixers[0]:group)
                    1001 group (session.mixers[0]:tracks)
                        1004 group (session.mixers[0].tracks[0]:group)
                            1005 group (session.mixers[0].tracks[0]:tracks)
                            1006 channel-strip-2 (session.mixers[0].tracks[0]:channel_strip)
                                active: 1.0, bus: 18.0, gain: 0.0, gate: 1.0
                            1007 patch-cable-2 (session.mixers[0].tracks[0]:output)
                                gate: 1.0, in_: 18.0, out: 16.0
                        1008 group (session.mixers[0].tracks[1]:group)
                            1009 group (session.mixers[0].tracks[1]:tracks)
                            1010 channel-strip-2 (session.mixers[0].tracks[1]:channel_strip)
                                active: 1.0, bus: 20.0, gain: 0.0, gate: 1.0
                            1011 patch-cable-2 (session.mixers[0].tracks[1]:output)
                                gate: 1.0, in_: 20.0, out: 16.0
                        1012 group (session.mixers[0].tracks[2]:group)
                            1013 group (session.mixers[0].tracks[2]:tracks)
                            1014 channel-strip-2 (session.mixers[0].tracks[2]:channel_strip)
                                active: 1.0, bus: 22.0, gain: 0.0, gate: 1.0
                            1015 patch-cable-2 (session.mixers[0].tracks[2]:output)
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
                            1023 patch-cable-2 (session.mixers[1].tracks[0]:output)
                                gate: 1.0, in_: 26.0, out: 24.0
                    1018 channel-strip-2 (session.mixers[1]:channel_strip)
                        active: 1.0, bus: 24.0, gain: 0.0, gate: 1.0
                    1019 patch-cable-2 (session.mixers[1]:output)
                        gate: 1.0, in_: 24.0, out: 0.0
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_Track_move(
    expected_graph_order: List[int],
    expected_tree: str,
    index: int,
    mixer: Mixer,
    online: bool,
    parent: str,
    maybe_raises,
    session: Session,
    track: Track,
) -> None:
    if online:
        await session.boot()
    targets: Dict[str, TrackContainer] = {
        "self": track,
        "mixer": mixer,
        "other": await mixer.add_track(),
        "other_other": await mixer.add_track(),
        "other_mixer": await session.add_mixer(),
    }
    with maybe_raises:
        await track.move(index=index, parent=targets[parent])
    assert track.graph_order == expected_graph_order
    if online:
        await session.sync()
        assert str(await session.dump_tree()) == normalize(
            expected_tree.format(context=repr(session.contexts[0]))
        )


@pytest.mark.parametrize("output", [None, DEFAULT])
@pytest.mark.asyncio
async def test_Track_set_output(output, track: Track) -> None:
    await track.set_output(output)


@pytest.mark.asyncio
async def test_Track_solo(track: Track) -> None:
    await track.solo()


@pytest.mark.asyncio
async def test_Track_ungroup(track: Track) -> None:
    await track.ungroup()


@pytest.mark.asyncio
async def test_Track_unsolo(track: Track) -> None:
    await track.unsolo()
