import dataclasses

import pytest

from supriya.sessions import Track, TrackContainer

from .conftest import Scenario


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "scenario",
    [
        Scenario(
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Track"}),
            ],
            subject="mixers[0]",
            expected_components_diff="""
            --- initial
            +++ mutation
            @@ -2,3 +2,4 @@
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
                         <Track 2 'Track'>
            +            <Track 3 'Child Track'>
            """,
            expected_tree_diff="""
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
            expected_messages="""
            - [None, [['/c_set', 11, 1.0, 12, 0.0], ['/c_fill', 13, 2, 0.0, 15, 2, 0.0]]]
            - [None,
               [['/g_new', 1014, 3, 1007, 1015, 0, 1014, 1016, 1, 1014],
                ['/s_new', 'supriya:channel-strip:2', 1017, 1, 1014, 'active', 'c11', 'gain', 'c12', 'out', 20.0],
                ['/s_new', 'supriya:meters:2', 1018, 3, 1015, 'in_', 20.0, 'out', 13.0],
                ['/s_new', 'supriya:meters:2', 1019, 3, 1017, 'in_', 20.0, 'out', 15.0],
                ['/s_new', 'supriya:patch-cable:2x2', 1020, 1, 1014, 'active', 'c11', 'in_', 20.0, 'out', 16.0]]]
            """,
        ),
        Scenario(
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Track"}),
            ],
            subject="mixers[0].tracks[0]",
            expected_components_diff="""
            --- initial
            +++ mutation
            @@ -2,3 +2,4 @@
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
                         <Track 2 'Track'>
            +                <Track 3 'Child Track'>
            """,
            expected_tree_diff="""
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
            expected_messages="""
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
    scenario: Scenario,
    online: bool,
) -> None:
    async with scenario.run(online=online) as session:
        subject = session[scenario.subject]
        assert isinstance(subject, TrackContainer)
        track = await subject.add_track(name="Child Track")
    assert isinstance(track, Track)
    assert track in subject.tracks
    assert track.parent is subject
    assert subject.tracks[-1] is track


@dataclasses.dataclass(frozen=True)
class GroupTracksScenario(Scenario):
    count: int
    index: int


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "scenario",
    [
        # mixers can group
        GroupTracksScenario(
            commands=[
                (None, "add_mixer", {"name": "Self"}),
                ("mixers[0]", "add_track", {"name": "Track One"}),
                ("mixers[0]", "add_track", {"name": "Track Two"}),
            ],
            subject="mixers[0]",
            index=0,
            count=2,
            expected_components_diff=lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,5 +1,6 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1 'Self'>
            -            <Track 2 'Track One'>
            -            <Track 3 'Track Two'>
            +            <Track 4 'Group Track'>
            +                <Track 2 'Track One'>
            +                <Track 3 'Track Two'>
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -1,28 +1,43 @@
             <session.contexts[0]>
                 NODE TREE 1000 group (mixers[1]:group)
                     1001 group (mixers[1]:tracks)
            -            1007 group (tracks[2]:group)
            -                1008 group (tracks[2]:tracks)
            -                1011 supriya:meters:2 (tracks[2]:input-levels)
            -                    in_: 18.0, out: 7.0
            -                1009 group (tracks[2]:devices)
            -                1010 supriya:channel-strip:2 (tracks[2]:channel-strip)
            -                    active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
            -                1012 supriya:meters:2 (tracks[2]:output-levels)
            -                    in_: 18.0, out: 9.0
            -                1013 supriya:patch-cable:2x2 (tracks[2]:output)
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            -            1014 group (tracks[3]:group)
            -                1015 group (tracks[3]:tracks)
            -                1018 supriya:meters:2 (tracks[3]:input-levels)
            -                    in_: 20.0, out: 13.0
            -                1016 group (tracks[3]:devices)
            -                1017 supriya:channel-strip:2 (tracks[3]:channel-strip)
            -                    active: c11, done_action: 2.0, gain: c12, gate: 1.0, out: 20.0
            -                1019 supriya:meters:2 (tracks[3]:output-levels)
            -                    in_: 20.0, out: 15.0
            -                1020 supriya:patch-cable:2x2 (tracks[3]:output)
            -                    active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
            +            1021 group (tracks[4]:group)
            +                1022 group (tracks[4]:tracks)
            +                    1007 group (tracks[2]:group)
            +                        1008 group (tracks[2]:tracks)
            +                        1011 supriya:meters:2 (tracks[2]:input-levels)
            +                            in_: 18.0, out: 7.0
            +                        1009 group (tracks[2]:devices)
            +                        1010 supriya:channel-strip:2 (tracks[2]:channel-strip)
            +                            active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
            +                        1012 supriya:meters:2 (tracks[2]:output-levels)
            +                            in_: 18.0, out: 9.0
            +                        1013 supriya:patch-cable:2x2 (tracks[2]:output)
            +                            active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 16.0
            +                        1028 supriya:patch-cable:2x2 (tracks[2]:output)
            +                            active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 22.0
            +                    1014 group (tracks[3]:group)
            +                        1015 group (tracks[3]:tracks)
            +                        1018 supriya:meters:2 (tracks[3]:input-levels)
            +                            in_: 20.0, out: 13.0
            +                        1016 group (tracks[3]:devices)
            +                        1017 supriya:channel-strip:2 (tracks[3]:channel-strip)
            +                            active: c11, done_action: 2.0, gain: c12, gate: 1.0, out: 20.0
            +                        1019 supriya:meters:2 (tracks[3]:output-levels)
            +                            in_: 20.0, out: 15.0
            +                        1020 supriya:patch-cable:2x2 (tracks[3]:output)
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 16.0
            +                        1029 supriya:patch-cable:2x2 (tracks[3]:output)
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 22.0
            +                1025 supriya:meters:2 (tracks[4]:input-levels)
            +                    in_: 22.0, out: 19.0
            +                1023 group (tracks[4]:devices)
            +                1024 supriya:channel-strip:2 (tracks[4]:channel-strip)
            +                    active: c17, done_action: 2.0, gain: c18, gate: 1.0, out: 22.0
            +                1026 supriya:meters:2 (tracks[4]:output-levels)
            +                    in_: 22.0, out: 21.0
            +                1027 supriya:patch-cable:2x2 (tracks[4]:output)
            +                    active: c17, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 16.0
                     1004 supriya:meters:2 (mixers[1]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (mixers[1]:devices)
            """,
            expected_messages="""
            - [None, [['/c_set', 17, 1.0, 18, 0.0], ['/c_fill', 19, 2, 0.0, 21, 2, 0.0]]]
            - [None,
               [['/g_new', 1021, 0, 1001, 1022, 0, 1021, 1023, 1, 1021],
                ['/s_new', 'supriya:channel-strip:2', 1024, 1, 1021, 'active', 'c17', 'gain', 'c18', 'out', 22.0],
                ['/s_new', 'supriya:meters:2', 1025, 3, 1022, 'in_', 22.0, 'out', 19.0],
                ['/s_new', 'supriya:meters:2', 1026, 3, 1024, 'in_', 22.0, 'out', 21.0],
                ['/s_new', 'supriya:patch-cable:2x2', 1027, 1, 1021, 'active', 'c17', 'in_', 22.0, 'out', 16.0]]]
            - ['/s_new', 'supriya:patch-cable:2x2', 1028, 1, 1007, 'active', 'c5', 'in_', 18.0, 'out', 22.0]
            - ['/s_new', 'supriya:patch-cable:2x2', 1029, 1, 1014, 'active', 'c11', 'in_', 20.0, 'out', 22.0]
            - ['/g_head', 1022, 1007]
            - ['/n_after', 1014, 1007]
            - ['/n_set', 1013, 'done_action', 2.0, 'gate', 0.0]
            - ['/n_set', 1020, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        # tracks can group
        GroupTracksScenario(
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Track One"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Track Two"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Track Three"}),
            ],
            subject="mixers[0].tracks[0]",
            index=1,
            count=2,
            expected_components_diff="""
            --- initial
            +++ mutation
            @@ -3,5 +3,6 @@
                     <Mixer 1 'Mixer'>
                         <Track 2 'Self'>
                             <Track 3 'Track One'>
            -                <Track 4 'Track Two'>
            -                <Track 5 'Track Three'>
            +                <Track 6 'Group Track'>
            +                    <Track 4 'Track Two'>
            +                    <Track 5 'Track Three'>
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -14,28 +14,43 @@
                                         in_: 20.0, out: 15.0
                                     1020 supriya:patch-cable:2x2 (tracks[3]:output)
                                         active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 18.0
            -                    1021 group (tracks[4]:group)
            -                        1022 group (tracks[4]:tracks)
            -                        1025 supriya:meters:2 (tracks[4]:input-levels)
            -                            in_: 22.0, out: 19.0
            -                        1023 group (tracks[4]:devices)
            -                        1024 supriya:channel-strip:2 (tracks[4]:channel-strip)
            -                            active: c17, done_action: 2.0, gain: c18, gate: 1.0, out: 22.0
            -                        1026 supriya:meters:2 (tracks[4]:output-levels)
            -                            in_: 22.0, out: 21.0
            -                        1027 supriya:patch-cable:2x2 (tracks[4]:output)
            -                            active: c17, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 18.0
            -                    1028 group (tracks[5]:group)
            -                        1029 group (tracks[5]:tracks)
            -                        1032 supriya:meters:2 (tracks[5]:input-levels)
            -                            in_: 24.0, out: 25.0
            -                        1030 group (tracks[5]:devices)
            -                        1031 supriya:channel-strip:2 (tracks[5]:channel-strip)
            -                            active: c23, done_action: 2.0, gain: c24, gate: 1.0, out: 24.0
            -                        1033 supriya:meters:2 (tracks[5]:output-levels)
            -                            in_: 24.0, out: 27.0
            -                        1034 supriya:patch-cable:2x2 (tracks[5]:output)
            -                            active: c23, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 24.0, out: 18.0
            +                    1035 group (tracks[6]:group)
            +                        1036 group (tracks[6]:tracks)
            +                            1021 group (tracks[4]:group)
            +                                1022 group (tracks[4]:tracks)
            +                                1025 supriya:meters:2 (tracks[4]:input-levels)
            +                                    in_: 22.0, out: 19.0
            +                                1023 group (tracks[4]:devices)
            +                                1024 supriya:channel-strip:2 (tracks[4]:channel-strip)
            +                                    active: c17, done_action: 2.0, gain: c18, gate: 1.0, out: 22.0
            +                                1026 supriya:meters:2 (tracks[4]:output-levels)
            +                                    in_: 22.0, out: 21.0
            +                                1027 supriya:patch-cable:2x2 (tracks[4]:output)
            +                                    active: c17, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 22.0, out: 18.0
            +                                1042 supriya:patch-cable:2x2 (tracks[4]:output)
            +                                    active: c17, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 26.0
            +                            1028 group (tracks[5]:group)
            +                                1029 group (tracks[5]:tracks)
            +                                1032 supriya:meters:2 (tracks[5]:input-levels)
            +                                    in_: 24.0, out: 25.0
            +                                1030 group (tracks[5]:devices)
            +                                1031 supriya:channel-strip:2 (tracks[5]:channel-strip)
            +                                    active: c23, done_action: 2.0, gain: c24, gate: 1.0, out: 24.0
            +                                1033 supriya:meters:2 (tracks[5]:output-levels)
            +                                    in_: 24.0, out: 27.0
            +                                1034 supriya:patch-cable:2x2 (tracks[5]:output)
            +                                    active: c23, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 24.0, out: 18.0
            +                                1043 supriya:patch-cable:2x2 (tracks[5]:output)
            +                                    active: c23, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 24.0, out: 26.0
            +                        1039 supriya:meters:2 (tracks[6]:input-levels)
            +                            in_: 26.0, out: 31.0
            +                        1037 group (tracks[6]:devices)
            +                        1038 supriya:channel-strip:2 (tracks[6]:channel-strip)
            +                            active: c29, done_action: 2.0, gain: c30, gate: 1.0, out: 26.0
            +                        1040 supriya:meters:2 (tracks[6]:output-levels)
            +                            in_: 26.0, out: 33.0
            +                        1041 supriya:patch-cable:2x2 (tracks[6]:output)
            +                            active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 26.0, out: 18.0
                             1011 supriya:meters:2 (tracks[2]:input-levels)
                                 in_: 18.0, out: 7.0
                             1009 group (tracks[2]:devices)
            """,
            expected_messages="""
            - [None, [['/c_set', 29, 1.0, 30, 0.0], ['/c_fill', 31, 2, 0.0, 33, 2, 0.0]]]
            - [None,
               [['/g_new', 1035, 3, 1014, 1036, 0, 1035, 1037, 1, 1035],
                ['/s_new', 'supriya:channel-strip:2', 1038, 1, 1035, 'active', 'c29', 'gain', 'c30', 'out', 26.0],
                ['/s_new', 'supriya:meters:2', 1039, 3, 1036, 'in_', 26.0, 'out', 31.0],
                ['/s_new', 'supriya:meters:2', 1040, 3, 1038, 'in_', 26.0, 'out', 33.0],
                ['/s_new', 'supriya:patch-cable:2x2', 1041, 1, 1035, 'active', 'c29', 'in_', 26.0, 'out', 18.0]]]
            - ['/s_new', 'supriya:patch-cable:2x2', 1042, 1, 1021, 'active', 'c17', 'in_', 22.0, 'out', 26.0]
            - ['/s_new', 'supriya:patch-cable:2x2', 1043, 1, 1028, 'active', 'c23', 'in_', 24.0, 'out', 26.0]
            - ['/g_head', 1036, 1021]
            - ['/n_after', 1028, 1021]
            - ['/n_set', 1027, 'done_action', 2.0, 'gate', 0.0]
            - ['/n_set', 1034, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        # no children: raise
        GroupTracksScenario(
            commands=[
                (None, "add_mixer", {"name": "Self"}),
            ],
            subject="mixers[0]",
            index=0,
            count=1,
            expected_exception=RuntimeError,
            expected_components_diff="",
            expected_tree_diff="",
            expected_messages="",
        ),
        # index less than zero: raise
        GroupTracksScenario(
            commands=[
                (None, "add_mixer", {"name": "Self"}),
                ("mixers[0]", "add_track", {"name": "Track One"}),
                ("mixers[0]", "add_track", {"name": "Track Two"}),
            ],
            subject="mixers[0]",
            index=-1,
            count=1,
            expected_exception=RuntimeError,
            expected_components_diff="",
            expected_tree_diff="",
            expected_messages="",
        ),
        # index plus count greater than length: raise
        GroupTracksScenario(
            commands=[
                (None, "add_mixer", {"name": "Self"}),
                ("mixers[0]", "add_track", {"name": "Track One"}),
                ("mixers[0]", "add_track", {"name": "Track Two"}),
            ],
            subject="mixers[0]",
            index=0,
            count=666,
            expected_exception=RuntimeError,
            expected_components_diff="",
            expected_tree_diff="",
            expected_messages="",
        ),
    ],
)
@pytest.mark.asyncio
async def test_TrackContainer_group_tracks(
    scenario: GroupTracksScenario,
    online: bool,
) -> None:
    async with scenario.run(annotation_style="numeric", online=online) as session:
        subject = session[scenario.subject]
        assert isinstance(subject, TrackContainer)
        group_track = await subject.group_tracks(
            index=scenario.index, count=scenario.count, name="Group Track"
        )
    if scenario.expected_exception:
        return
    assert isinstance(group_track, Track)
    assert group_track in subject.tracks
    assert group_track.parent is subject
    assert subject.tracks[scenario.index] is group_track
