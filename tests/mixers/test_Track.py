import asyncio

import pytest
from uqbar.strings import normalize

from supriya import BusGroup
from supriya.mixers import Session
from supriya.mixers.synthdefs import get_lag_time
from supriya.mixers.tracks import Track, TrackContainer, TrackSend
from supriya.typing import DEFAULT, Default

from .conftest import (
    apply_commands,
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
    "commands, postfader, source, target, maybe_raises, expected_components_diff, expected_tree_diff, expected_messages",
    [
        # send to other mixer: raises
        (
            [
                (None, "add_mixer", None),
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", None),
                ("mixers[1]", "add_track", None),
            ],
            True,
            "mixers[0].tracks[0]",
            "mixers[1].tracks[0]",
            pytest.raises(RuntimeError),
            """
            """,
            """
            """,
            """
            """,
        ),
        # send to self
        # - track: expect :feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", "Self"),
            ],
            True,
            "mixers[0].tracks[0]",
            "mixers[0].tracks[0]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -2,3 +2,4 @@
                 <session.contexts[0]>
                     <Mixer 1>
                         <Track 2 'Self'>
            +                <TrackSend 3 postfader target=<Track 2 'Self'>>
            """,
            """
            --- initial
            +++ mutation
            @@ -2,12 +2,16 @@
                 NODE TREE 1000 group (session.mixers[0]:group)
                     1001 group (session.mixers[0]:tracks)
                         1007 group (session.mixers[0].tracks[0]:group)
            +                1015 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0]:feedback)
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 18.0
                             1008 group (session.mixers[0].tracks[0]:tracks)
                             1011 supriya:meters:2 (session.mixers[0].tracks[0]:input-levels)
                                 in_: 18.0, out: 7.0
                             1009 group (session.mixers[0].tracks[0]:devices)
                             1010 supriya:channel-strip:2 (session.mixers[0].tracks[0]:channel-strip)
                                 active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
            +                1014 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].sends[0]:synth)
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
                             1012 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
                                 in_: 18.0, out: 9.0
                             1013 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:output)
            """,
            """
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 4]
            - ['/s_new', 'supriya:patch-cable:2x2', 1014, 3, 1010, 'active', 'c5', 'in_', 18.0, 'out', 20.0]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1015, 0, 1007, 'active', 'c5', 'in_', 20.0, 'out', 18.0]
            """,
        ),
        # send to younger sibling
        # - sibling: do not expect :feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", "Self"),
                ("mixers[0]", "add_track", "Younger Sibling"),
            ],
            True,
            "mixers[0].tracks[0]",
            "mixers[0].tracks[1]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -2,4 +2,5 @@
                 <session.contexts[0]>
                     <Mixer 1>
                         <Track 2 'Self'>
            +                <TrackSend 4 postfader target=<Track 3 'Younger Sibling'>>
                         <Track 3 'Younger Sibling'>
            """,
            """
            --- initial
            +++ mutation
            @@ -8,6 +8,8 @@
                             1009 group (session.mixers[0].tracks[0]:devices)
                             1010 supriya:channel-strip:2 (session.mixers[0].tracks[0]:channel-strip)
                                 active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
            +                1021 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].sends[0]:synth)
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
                             1012 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
                                 in_: 18.0, out: 9.0
                             1013 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:output)
            """,
            """
            - ['/s_new', 'supriya:patch-cable:2x2', 1021, 3, 1010, 'active', 'c5', 'in_', 18.0, 'out', 20.0]
            """,
        ),
        # send to younger sibling, prefader
        # - sibling: do not expect :feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", "Self"),
                ("mixers[0]", "add_track", "Younger Sibling"),
            ],
            False,
            "mixers[0].tracks[0]",
            "mixers[0].tracks[1]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -2,4 +2,5 @@
                 <session.contexts[0]>
                     <Mixer 1>
                         <Track 2 'Self'>
            +                <TrackSend 4 prefader target=<Track 3 'Younger Sibling'>>
                         <Track 3 'Younger Sibling'>
            """,
            """
            --- initial
            +++ mutation
            @@ -6,6 +6,8 @@
                             1011 supriya:meters:2 (session.mixers[0].tracks[0]:input-levels)
                                 in_: 18.0, out: 7.0
                             1009 group (session.mixers[0].tracks[0]:devices)
            +                1021 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].sends[0]:synth)
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
                             1010 supriya:channel-strip:2 (session.mixers[0].tracks[0]:channel-strip)
                                 active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
                             1012 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
            """,
            """
            - ['/s_new', 'supriya:patch-cable:2x2', 1021, 2, 1010, 'active', 'c5', 'in_', 18.0, 'out', 20.0]
            """,
        ),
        # send to older sibling
        # - sibling: expect :feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", "Older Sibling"),
                ("mixers[0]", "add_track", "Self"),
            ],
            True,
            "mixers[0].tracks[1]",
            "mixers[0].tracks[0]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -3,3 +3,4 @@
                     <Mixer 1>
                         <Track 2 'Older Sibling'>
                         <Track 3 'Self'>
            +                <TrackSend 4 postfader target=<Track 2 'Older Sibling'>>
            """,
            """
            --- initial
            +++ mutation
            @@ -2,6 +2,8 @@
                 NODE TREE 1000 group (session.mixers[0]:group)
                     1001 group (session.mixers[0]:tracks)
                         1007 group (session.mixers[0].tracks[0]:group)
            +                1022 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0]:feedback)
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 18.0
                             1008 group (session.mixers[0].tracks[0]:tracks)
                             1011 supriya:meters:2 (session.mixers[0].tracks[0]:input-levels)
                                 in_: 18.0, out: 7.0
            @@ -19,6 +21,8 @@
                             1016 group (session.mixers[0].tracks[1]:devices)
                             1017 supriya:channel-strip:2 (session.mixers[0].tracks[1]:channel-strip)
                                 active: c11, done_action: 2.0, gain: c12, gate: 1.0, out: 20.0
            +                1021 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].sends[0]:synth)
            +                    active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 22.0
                             1019 supriya:meters:2 (session.mixers[0].tracks[1]:output-levels)
                                 in_: 20.0, out: 15.0
                             1020 supriya:patch-cable:2x2 (session.mixers[0].tracks[1]:output)
            """,
            """
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 4]
            - ['/s_new', 'supriya:patch-cable:2x2', 1021, 3, 1017, 'active', 'c11', 'in_', 20.0, 'out', 22.0]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1022, 0, 1007, 'active', 'c5', 'in_', 22.0, 'out', 18.0]
            """,
        ),
        # send to child
        # - child: expect :feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", "Self"),
                ("mixers[0].tracks[0]", "add_track", "Child"),
            ],
            True,
            "mixers[0].tracks[0]",
            "mixers[0].tracks[0].tracks[0]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -3,3 +3,4 @@
                     <Mixer 1>
                         <Track 2 'Self'>
                             <Track 3 'Child'>
            +                <TrackSend 4 postfader target=<Track 3 'Child'>>
            """,
            """
            --- initial
            +++ mutation
            @@ -4,6 +4,8 @@
                         1007 group (session.mixers[0].tracks[0]:group)
                             1008 group (session.mixers[0].tracks[0]:tracks)
                                 1014 group (session.mixers[0].tracks[0].tracks[0]:group)
            +                        1022 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0]:feedback)
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 20.0
                                     1015 group (session.mixers[0].tracks[0].tracks[0]:tracks)
                                     1018 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:input-levels)
                                         in_: 20.0, out: 13.0
            @@ -19,6 +21,8 @@
                             1009 group (session.mixers[0].tracks[0]:devices)
                             1010 supriya:channel-strip:2 (session.mixers[0].tracks[0]:channel-strip)
                                 active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
            +                1021 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].sends[0]:synth)
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 22.0
                             1012 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
                                 in_: 18.0, out: 9.0
                             1013 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:output)
            """,
            """
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 4]
            - ['/s_new', 'supriya:patch-cable:2x2', 1021, 3, 1010, 'active', 'c5', 'in_', 18.0, 'out', 22.0]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1022, 0, 1014, 'active', 'c11', 'in_', 22.0, 'out', 20.0]
            """,
        ),
        # send to parent
        # - parent: do not expect :feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", "Parent"),
                ("mixers[0].tracks[0]", "add_track", "Self"),
            ],
            True,
            "mixers[0].tracks[0].tracks[0]",
            "mixers[0].tracks[0]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -3,3 +3,4 @@
                     <Mixer 1>
                         <Track 2 'Parent'>
                             <Track 3 'Self'>
            +                    <TrackSend 4 postfader target=<Track 2 'Parent'>>
            """,
            """
            --- initial
            +++ mutation
            @@ -10,6 +10,8 @@
                                     1016 group (session.mixers[0].tracks[0].tracks[0]:devices)
                                     1017 supriya:channel-strip:2 (session.mixers[0].tracks[0].tracks[0]:channel-strip)
                                         active: c11, done_action: 2.0, gain: c12, gate: 1.0, out: 20.0
            +                        1021 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].sends[0]:synth)
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 18.0
                                     1019 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:output-levels)
                                         in_: 20.0, out: 15.0
                                     1020 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0]:output)
            """,
            """
            - ['/s_new', 'supriya:patch-cable:2x2', 1021, 3, 1017, 'active', 'c11', 'in_', 20.0, 'out', 18.0]
            """,
        ),
        # send to grandparent
        # - grandparent: do not expect :feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", "Grandarent"),
                ("mixers[0].tracks[0]", "add_track", "Parent"),
                ("mixers[0].tracks[0].tracks[0]", "add_track", "Self"),
            ],
            True,
            "mixers[0].tracks[0].tracks[0].tracks[0]",
            "mixers[0].tracks[0]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -4,3 +4,4 @@
                         <Track 2 'Grandarent'>
                             <Track 3 'Parent'>
                                 <Track 4 'Self'>
            +                        <TrackSend 5 postfader target=<Track 2 'Grandarent'>>
            """,
            """
            --- initial
            +++ mutation
            @@ -12,6 +12,8 @@
                                             1023 group (session.mixers[0].tracks[0].tracks[0].tracks[0]:devices)
                                             1024 supriya:channel-strip:2 (session.mixers[0].tracks[0].tracks[0].tracks[0]:channel-strip)
                                                 active: c17, done_action: 2.0, gain: c18, gate: 1.0, out: 22.0
            +                                1028 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].tracks[0].sends[0]:synth)
            +                                    active: c17, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 18.0
                                             1026 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0].tracks[0]:output-levels)
                                                 in_: 22.0, out: 21.0
                                             1027 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].tracks[0]:output)
            """,
            """
            - ['/s_new', 'supriya:patch-cable:2x2', 1028, 3, 1024, 'active', 'c17', 'in_', 22.0, 'out', 18.0]
            """,
        ),
        # send to grandchild
        # - grandchild: expect :feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", "Self"),
                ("mixers[0].tracks[0]", "add_track", "Child"),
                ("mixers[0].tracks[0].tracks[0]", "add_track", "Grandchild"),
            ],
            True,
            "mixers[0].tracks[0]",
            "mixers[0].tracks[0].tracks[0].tracks[0]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -4,3 +4,4 @@
                         <Track 2 'Self'>
                             <Track 3 'Child'>
                                 <Track 4 'Grandchild'>
            +                <TrackSend 5 postfader target=<Track 4 'Grandchild'>>
            """,
            """
            --- initial
            +++ mutation
            @@ -6,6 +6,8 @@
                                 1014 group (session.mixers[0].tracks[0].tracks[0]:group)
                                     1015 group (session.mixers[0].tracks[0].tracks[0]:tracks)
                                         1021 group (session.mixers[0].tracks[0].tracks[0].tracks[0]:group)
            +                                1029 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].tracks[0]:feedback)
            +                                    active: c17, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 24.0, out: 22.0
                                             1022 group (session.mixers[0].tracks[0].tracks[0].tracks[0]:tracks)
                                             1025 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0].tracks[0]:input-levels)
                                                 in_: 22.0, out: 19.0
            @@ -30,6 +32,8 @@
                             1009 group (session.mixers[0].tracks[0]:devices)
                             1010 supriya:channel-strip:2 (session.mixers[0].tracks[0]:channel-strip)
                                 active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
            +                1028 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].sends[0]:synth)
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 24.0
                             1012 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
                                 in_: 18.0, out: 9.0
                             1013 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:output)
            """,
            """
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 4]
            - ['/s_new', 'supriya:patch-cable:2x2', 1028, 3, 1010, 'active', 'c5', 'in_', 18.0, 'out', 24.0]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1029, 0, 1021, 'active', 'c17', 'in_', 24.0, 'out', 22.0]
            """,
        ),
        # send to older auntie
        # - auntie: expect :feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", "Older Auntie"),
                ("mixers[0]", "add_track", "Parent"),
                ("mixers[0].tracks[1]", "add_track", "Self"),
            ],
            True,
            "mixers[0].tracks[1].tracks[0]",
            "mixers[0].tracks[0]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -4,3 +4,4 @@
                         <Track 2 'Older Auntie'>
                         <Track 3 'Parent'>
                             <Track 4 'Self'>
            +                    <TrackSend 5 postfader target=<Track 2 'Older Auntie'>>
            """,
            """
            --- initial
            +++ mutation
            @@ -2,6 +2,8 @@
                 NODE TREE 1000 group (session.mixers[0]:group)
                     1001 group (session.mixers[0]:tracks)
                         1007 group (session.mixers[0].tracks[0]:group)
            +                1029 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0]:feedback)
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 24.0, out: 18.0
                             1008 group (session.mixers[0].tracks[0]:tracks)
                             1011 supriya:meters:2 (session.mixers[0].tracks[0]:input-levels)
                                 in_: 18.0, out: 7.0
            @@ -21,6 +23,8 @@
                                     1023 group (session.mixers[0].tracks[1].tracks[0]:devices)
                                     1024 supriya:channel-strip:2 (session.mixers[0].tracks[1].tracks[0]:channel-strip)
                                         active: c17, done_action: 2.0, gain: c18, gate: 1.0, out: 22.0
            +                        1028 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].tracks[0].sends[0]:synth)
            +                            active: c17, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 24.0
                                     1026 supriya:meters:2 (session.mixers[0].tracks[1].tracks[0]:output-levels)
                                         in_: 22.0, out: 21.0
                                     1027 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].tracks[0]:output)
            """,
            """
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 4]
            - ['/s_new', 'supriya:patch-cable:2x2', 1028, 3, 1024, 'active', 'c17', 'in_', 22.0, 'out', 24.0]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1029, 0, 1007, 'active', 'c5', 'in_', 24.0, 'out', 18.0]
            """,
        ),
        # send to younger auntie
        # - auntie: do not expect :feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", "Parent"),
                ("mixers[0]", "add_track", "Younger Auntie"),
                ("mixers[0].tracks[0]", "add_track", "Self"),
            ],
            True,
            "mixers[0].tracks[0].tracks[0]",
            "mixers[0].tracks[1]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -3,4 +3,5 @@
                     <Mixer 1>
                         <Track 2 'Parent'>
                             <Track 4 'Self'>
            +                    <TrackSend 5 postfader target=<Track 3 'Younger Auntie'>>
                         <Track 3 'Younger Auntie'>
            """,
            """
            --- initial
            +++ mutation
            @@ -10,6 +10,8 @@
                                     1016 group (session.mixers[0].tracks[0].tracks[0]:devices)
                                     1017 supriya:channel-strip:2 (session.mixers[0].tracks[0].tracks[0]:channel-strip)
                                         active: c11, done_action: 2.0, gain: c12, gate: 1.0, out: 20.0
            +                        1028 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].sends[0]:synth)
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 22.0
                                     1019 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:output-levels)
                                         in_: 20.0, out: 15.0
                                     1020 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0]:output)
            """,
            """
            - ['/s_new', 'supriya:patch-cable:2x2', 1028, 3, 1017, 'active', 'c11', 'in_', 20.0, 'out', 22.0]
            """,
        ),
        # send to older cousin
        # - older cousin: expect :feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", "Auntie"),
                ("mixers[0]", "add_track", "Parent"),
                ("mixers[0].tracks[0]", "add_track", "Older Cousin"),
                ("mixers[0].tracks[1]", "add_track", "Self"),
            ],
            True,
            "mixers[0].tracks[1].tracks[0]",
            "mixers[0].tracks[0].tracks[0]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -5,3 +5,4 @@
                             <Track 4 'Older Cousin'>
                         <Track 3 'Parent'>
                             <Track 5 'Self'>
            +                    <TrackSend 6 postfader target=<Track 4 'Older Cousin'>>
            """,
            """
            --- initial
            +++ mutation
            @@ -4,6 +4,8 @@
                         1007 group (session.mixers[0].tracks[0]:group)
                             1008 group (session.mixers[0].tracks[0]:tracks)
                                 1014 group (session.mixers[0].tracks[0].tracks[0]:group)
            +                        1036 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0]:feedback)
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 26.0, out: 20.0
                                     1015 group (session.mixers[0].tracks[0].tracks[0]:tracks)
                                     1018 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:input-levels)
                                         in_: 20.0, out: 13.0
            @@ -32,6 +34,8 @@
                                     1030 group (session.mixers[0].tracks[1].tracks[0]:devices)
                                     1031 supriya:channel-strip:2 (session.mixers[0].tracks[1].tracks[0]:channel-strip)
                                         active: c23, done_action: 2.0, gain: c24, gate: 1.0, out: 24.0
            +                        1035 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].tracks[0].sends[0]:synth)
            +                            active: c23, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 24.0, out: 26.0
                                     1033 supriya:meters:2 (session.mixers[0].tracks[1].tracks[0]:output-levels)
                                         in_: 24.0, out: 27.0
                                     1034 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].tracks[0]:output)
            """,
            """
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 4]
            - ['/s_new', 'supriya:patch-cable:2x2', 1035, 3, 1031, 'active', 'c23', 'in_', 24.0, 'out', 26.0]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1036, 0, 1014, 'active', 'c11', 'in_', 26.0, 'out', 20.0]
            """,
        ),
        # send to younger cousin
        # - younger cousin: do not expect :feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", "Parent"),
                ("mixers[0]", "add_track", "Auntie"),
                ("mixers[0].tracks[0]", "add_track", "Self"),
                ("mixers[0].tracks[1]", "add_track", "Younger Cousin"),
            ],
            True,
            "mixers[0].tracks[0].tracks[0]",
            "mixers[0].tracks[1].tracks[0]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -3,5 +3,6 @@
                     <Mixer 1>
                         <Track 2 'Parent'>
                             <Track 4 'Self'>
            +                    <TrackSend 6 postfader target=<Track 5 'Younger Cousin'>>
                         <Track 3 'Auntie'>
                             <Track 5 'Younger Cousin'>
            """,
            """
            --- initial
            +++ mutation
            @@ -10,6 +10,8 @@
                                     1016 group (session.mixers[0].tracks[0].tracks[0]:devices)
                                     1017 supriya:channel-strip:2 (session.mixers[0].tracks[0].tracks[0]:channel-strip)
                                         active: c11, done_action: 2.0, gain: c12, gate: 1.0, out: 20.0
            +                        1035 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].sends[0]:synth)
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 24.0
                                     1019 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:output-levels)
                                         in_: 20.0, out: 15.0
                                     1020 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0]:output)
            """,
            """
            - ['/s_new', 'supriya:patch-cable:2x2', 1035, 3, 1017, 'active', 'c11', 'in_', 20.0, 'out', 24.0]
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_Track_add_send(
    commands: list[tuple[str | None, str, str | None]],
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
    session = Session()
    await apply_commands(session, commands)
    initial_components = debug_components(session)
    if online:
        await session.boot()
        await session.sync()
        initial_tree = await debug_tree(session)
        print(initial_tree)
    source_ = session[source]
    target_ = session[target]
    assert isinstance(source_, Track)
    assert isinstance(target_, TrackContainer)
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
            @@ -1,5 +1,4 @@
             <Session 0>
                 <session.contexts[0]>
                     <Mixer 1 'P'>
            -            <Track 2 'A' output=<Track 3 'B'>>
            -            <Track 3 'B'>
            +            <Track 2 'A' output=None>
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
            @@ -1,5 +1,4 @@
             <Session 0>
                 <session.contexts[0]>
                     <Mixer 1 'P'>
            -            <Track 2 'A' input=<Track 3 'B'>>
            -            <Track 3 'B'>
            +            <Track 2 'A'>
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
    commands: list[tuple[str | None, str, str | None]],
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
    await apply_commands(session, commands)
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
        # self: not allowed
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
            --- initial
            +++ mutation
            @@ -2,7 +2,7 @@
                 <session.contexts[0]>
                     <Mixer 1 'P'>
                         <Track 3 'A'>
            -                <Track 6 'A1'>
            +                <Track 6 'A1' input=<Track 3 'A'>>
                                 <Track 8 'A11'>
                             <Track 7 'A2'>
                             <TrackSend 10 target=<Track 4 'B'>>
            """,
            # TODO: This shouldn't trigger feedback in 1067
            """
            --- initial
            +++ mutation
            @@ -2,8 +2,12 @@
                 NODE TREE 1000 group (session.mixers[0]:group)
                     1001 group (session.mixers[0]:tracks)
                         1007 group (session.mixers[0].tracks[0]:group)
            +                1067 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0]:feedback)
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 36.0, out: 18.0
                             1008 group (session.mixers[0].tracks[0]:tracks)
                                 1014 group (session.mixers[0].tracks[0].tracks[0]:group)
            +                        1066 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0]:input)
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
                                     1021 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0]:feedback)
                                         active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 20.0
                                     1015 group (session.mixers[0].tracks[0].tracks[0]:tracks)
            """,
            """
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1066, 0, 1014, 'active', 'c11', 'in_', 18.0, 'out', 20.0]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1067, 0, 1007, 'active', 'c5', 'in_', 36.0, 'out', 18.0]
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
            @@ -2,7 +2,7 @@
                 <session.contexts[0]>
                     <Mixer 1 'P'>
                         <Track 3 'A'>
            -                <Track 6 'A1'>
            +                <Track 6 'A1' input=<Track 8 'A11'>>
                                 <Track 8 'A11'>
                             <Track 7 'A2'>
                             <TrackSend 10 target=<Track 4 'B'>>
            """,
            # TODO: Track[6] should have the fb-patch-cable, and no feedback at 1067
            """
            --- initial
            +++ mutation
            @@ -4,10 +4,14 @@
                         1007 group (session.mixers[0].tracks[0]:group)
                             1008 group (session.mixers[0].tracks[0]:tracks)
                                 1014 group (session.mixers[0].tracks[0].tracks[0]:group)
            +                        1066 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0]:input)
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 24.0, out: 20.0
                                     1021 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0]:feedback)
                                         active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 20.0
                                     1015 group (session.mixers[0].tracks[0].tracks[0]:tracks)
                                         1022 group (session.mixers[0].tracks[0].tracks[0].tracks[0]:group)
            +                                1067 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].tracks[0]:feedback)
            +                                    active: c17, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 36.0, out: 24.0
                                             1023 group (session.mixers[0].tracks[0].tracks[0].tracks[0]:tracks)
                                             1026 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0].tracks[0]:input-levels)
                                                 in_: 24.0, out: 19.0           """,
            """
            - ['/s_new', 'supriya:patch-cable:2x2', 1066, 0, 1014, 'active', 'c11', 'in_', 24.0, 'out', 20.0]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1067, 0, 1022, 'active', 'c17', 'in_', 36.0, 'out', 24.0]
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
            @@ -2,7 +2,7 @@
                 <session.contexts[0]>
                     <Mixer 1 'P'>
                         <Track 3 'A'>
            -                <Track 6 'A1'>
            +                <Track 6 'A1' input=<Track 4 'B'>>
                                 <Track 8 'A11'>
                             <Track 7 'A2'>
                             <TrackSend 10 target=<Track 4 'B'>>
            """,
            """
            --- initial
            +++ mutation
            @@ -4,6 +4,8 @@
                         1007 group (session.mixers[0].tracks[0]:group)
                             1008 group (session.mixers[0].tracks[0]:tracks)
                                 1014 group (session.mixers[0].tracks[0].tracks[0]:group)
            +                        1066 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0]:input)
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 28.0, out: 20.0
                                     1021 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0]:feedback)
                                         active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 20.0
                                     1015 group (session.mixers[0].tracks[0].tracks[0]:tracks)
            """,
            """
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1066, 0, 1014, 'active', 'c11', 'in_', 28.0, 'out', 20.0]
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
            @@ -6,7 +6,7 @@
                                 <Track 8 'A11'>
                             <Track 7 'A2'>
                             <TrackSend 10 target=<Track 4 'B'>>
            -            <Track 4 'B'>
            +            <Track 4 'B' input=<Track 3 'A'>>
                             <TrackSend 11 target=<Track 6 'A1'>>
                         <Track 5 'C'>
                     <Mixer 2 'Q'>
            """,
            # TODO: Should not trigger feedback at 1067
            """
            --- initial
            +++ mutation
            @@ -2,6 +2,8 @@
                 NODE TREE 1000 group (session.mixers[0]:group)
                     1001 group (session.mixers[0]:tracks)
                         1007 group (session.mixers[0].tracks[0]:group)
            +                1067 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0]:feedback)
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 36.0, out: 18.0
                             1008 group (session.mixers[0].tracks[0]:tracks)
                                 1014 group (session.mixers[0].tracks[0].tracks[0]:group)
                                     1021 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0]:feedback)
            @@ -50,6 +52,8 @@
                             1013 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:output)
                                 active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
                         1037 group (session.mixers[0].tracks[1]:group)
            +                1066 supriya:patch-cable:2x2 (session.mixers[0].tracks[1]:input)
            +                    active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 28.0
                             1038 group (session.mixers[0].tracks[1]:tracks)
                             1041 supriya:meters:2 (session.mixers[0].tracks[1]:input-levels)
                                 in_: 28.0, out: 31.0
            """,
            """
            - ['/s_new', 'supriya:patch-cable:2x2', 1066, 0, 1037, 'active', 'c29', 'in_', 18.0, 'out', 28.0]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1067, 0, 1007, 'active', 'c5', 'in_', 36.0, 'out', 18.0]
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
            @@ -2,7 +2,7 @@
                 <session.contexts[0]>
                     <Mixer 1 'P'>
                         <Track 3 'A'>
            -                <Track 6 'A1'>
            +                <Track 6 'A1' input=<Track 7 'A2'>>
                                 <Track 8 'A11'>
                             <Track 7 'A2'>
                             <TrackSend 10 target=<Track 4 'B'>>
            """,
            """
            --- initial
            +++ mutation
            @@ -4,6 +4,8 @@
                         1007 group (session.mixers[0].tracks[0]:group)
                             1008 group (session.mixers[0].tracks[0]:tracks)
                                 1014 group (session.mixers[0].tracks[0].tracks[0]:group)
            +                        1066 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0]:input)
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 26.0, out: 20.0
                                     1021 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0]:feedback)
                                         active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 20.0
                                     1015 group (session.mixers[0].tracks[0].tracks[0]:tracks)
            """,
            """
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1066, 0, 1014, 'active', 'c11', 'in_', 26.0, 'out', 20.0]
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
    if isinstance(target, str):
        target_component = session[target]
        assert isinstance(target_component, Track)
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
            """,
            """
            """,
            """
            """,
            #   """
            #   --- initial
            #   +++ mutation
            #   @@ -11,7 +11,7 @@
            #                            <TrackFeedback 26 session.mixers[0].tracks[0].tracks[0].tracks[0].feedback>
            #                            <TrackInput 27 session.mixers[0].tracks[0].tracks[0].tracks[0].input source=null>
            #                            <TrackOutput 28 session.mixers[0].tracks[0].tracks[0].tracks[0].output target=default>
            #   -                    <TrackOutput 20 session.mixers[0].tracks[0].tracks[0].output target=default>
            #   +                    <TrackOutput 20 session.mixers[0].tracks[0].tracks[0].output target=null>
            #                    <Track 21 'A2'>
            #                        <TrackFeedback 22 session.mixers[0].tracks[0].tracks[1].feedback>
            #                        <TrackInput 23 session.mixers[0].tracks[0].tracks[1].input source=null>
            #   """,
            #   """
            #   --- initial
            #   +++ mutation
            #   @@ -25,8 +25,8 @@
            #                                active: c11, bus: 20.0, done_action: 2.0, gain: c12, gate: 1.0
            #                            1017 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:output-levels)
            #                                in_: 20.0, out: 15.0
            #   -                        1025 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].output:synth)
            #   -                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 18.0
            #   +                        1025 supriya:patch-cable:2x2
            #   +                            active: c11, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 18.0
            #                        1026 group (session.mixers[0].tracks[0].tracks[1]:group)
            #                            1027 group (session.mixers[0].tracks[0].tracks[1]:tracks)
            #                            1030 supriya:meters:2 (session.mixers[0].tracks[0].tracks[1]:input-levels)
            #   """,
            #   """
            #   - ['/n_set', 1025, 'gate', 0.0]
            #   """,
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
        # self: not allowed
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
            """,
            """
            """,
            """
            """,
            #   """
            #   --- initial
            #   +++ mutation
            #   @@ -11,7 +11,7 @@
            #                            <TrackFeedback 26 session.mixers[0].tracks[0].tracks[0].tracks[0].feedback>
            #                            <TrackInput 27 session.mixers[0].tracks[0].tracks[0].tracks[0].input source=null>
            #                            <TrackOutput 28 session.mixers[0].tracks[0].tracks[0].tracks[0].output target=default>
            #   -                    <TrackOutput 20 session.mixers[0].tracks[0].tracks[0].output target=default>
            #   +                    <TrackOutput 20 session.mixers[0].tracks[0].tracks[0].output target=session.mixers[0].tracks[0]>
            #                    <Track 21 'A2'>
            #                        <TrackFeedback 22 session.mixers[0].tracks[0].tracks[1].feedback>
            #                        <TrackInput 23 session.mixers[0].tracks[0].tracks[1].input source=null>
            #   """,
            #   "",
            #   "",
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
            #   @@ -11,7 +11,7 @@
            #                            <TrackFeedback 26 session.mixers[0].tracks[0].tracks[0].tracks[0].feedback>
            #                            <TrackInput 27 session.mixers[0].tracks[0].tracks[0].tracks[0].input source=null>
            #                            <TrackOutput 28 session.mixers[0].tracks[0].tracks[0].tracks[0].output target=default>
            #   -                    <TrackOutput 20 session.mixers[0].tracks[0].tracks[0].output target=default>
            #   +                    <TrackOutput 20 session.mixers[0].tracks[0].tracks[0].output target=session.mixers[0].tracks[0].tracks[0].tracks[0]>
            #                    <Track 21 'A2'>
            #                        <TrackFeedback 22 session.mixers[0].tracks[0].tracks[1].feedback>
            #                        <TrackInput 23 session.mixers[0].tracks[0].tracks[1].input source=null>
            #   """,
            #   """
            #   --- initial
            #   +++ mutation
            #   @@ -8,6 +8,8 @@
            #                                active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 28.0, out: 20.0
            #                            1013 group (session.mixers[0].tracks[0].tracks[0]:tracks)
            #                                1018 group (session.mixers[0].tracks[0].tracks[0].tracks[0]:group)
            #   +                                1066 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].tracks[0].feedback:synth)
            #   +                                    active: c17, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 36.0, out: 22.0
            #                                    1019 group (session.mixers[0].tracks[0].tracks[0].tracks[0]:tracks)
            #                                    1022 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0].tracks[0]:input-levels)
            #                                        in_: 22.0, out: 19.0
            #   @@ -25,8 +27,10 @@
            #                                active: c11, bus: 20.0, done_action: 2.0, gain: c12, gate: 1.0
            #                            1017 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:output-levels)
            #                                in_: 20.0, out: 15.0
            #   -                        1025 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].output:synth)
            #   -                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 18.0
            #   +                        1025 supriya:patch-cable:2x2
            #   +                            active: c11, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 18.0
            #   +                        1067 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].output:synth)
            #   +                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 36.0
            #                        1026 group (session.mixers[0].tracks[0].tracks[1]:group)
            #                            1027 group (session.mixers[0].tracks[0].tracks[1]:tracks)
            #                            1030 supriya:meters:2 (session.mixers[0].tracks[0].tracks[1]:input-levels)
            #   """,
            #   """
            #   - ['/s_new', 'supriya:fb-patch-cable:2x2', 1066, 0, 1018, 'active', 'c17', 'in_', 36.0, 'out', 22.0]
            #   - [None,
            #      [['/n_set', 1025, 'gate', 0.0],
            #       ['/s_new', 'supriya:patch-cable:2x2', 1067, 1, 1012, 'active', 'c11', 'in_', 20.0, 'out', 36.0]]]
            #   """,
        ),
        # auntie
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
            #   @@ -11,7 +11,7 @@
            #                            <TrackFeedback 26 session.mixers[0].tracks[0].tracks[0].tracks[0].feedback>
            #                            <TrackInput 27 session.mixers[0].tracks[0].tracks[0].tracks[0].input source=null>
            #                            <TrackOutput 28 session.mixers[0].tracks[0].tracks[0].tracks[0].output target=default>
            #   -                    <TrackOutput 20 session.mixers[0].tracks[0].tracks[0].output target=default>
            #   +                    <TrackOutput 20 session.mixers[0].tracks[0].tracks[0].output target=<Track 4 'B'>>
            #                    <Track 21 'A2'>
            #                        <TrackFeedback 22 session.mixers[0].tracks[0].tracks[1].feedback>
            #                        <TrackInput 23 session.mixers[0].tracks[0].tracks[1].input source=null>
            #   """,
            #   """
            #   --- initial
            #   +++ mutation
            #   @@ -25,8 +25,10 @@
            #                                active: c11, bus: 20.0, done_action: 2.0, gain: c12, gate: 1.0
            #                            1017 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:output-levels)
            #                                in_: 20.0, out: 15.0
            #   -                        1025 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].output:synth)
            #   -                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 18.0
            #   +                        1025 supriya:patch-cable:2x2
            #   +                            active: c11, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 18.0
            #   +                        1066 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].output:synth)
            #   +                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 26.0
            #                        1026 group (session.mixers[0].tracks[0].tracks[1]:group)
            #                            1027 group (session.mixers[0].tracks[0].tracks[1]:tracks)
            #                            1030 supriya:meters:2 (session.mixers[0].tracks[0].tracks[1]:input-levels)
            #   """,
            #   """
            #   - [None,
            #      [['/n_set', 1025, 'gate', 0.0],
            #       ['/s_new', 'supriya:patch-cable:2x2', 1066, 1, 1012, 'active', 'c11', 'in_', 20.0, 'out', 26.0]]]
            #   """,
        ),
        # mixer: no-op but does pin target
        (
            "mixers[0].tracks[0]",
            "mixers[0]",
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
            #   @@ -16,7 +16,7 @@
            #                        <TrackFeedback 22 session.mixers[0].tracks[0].tracks[1].feedback>
            #                        <TrackInput 23 session.mixers[0].tracks[0].tracks[1].input source=null>
            #                        <TrackOutput 24 session.mixers[0].tracks[0].tracks[1].output target=default>
            #   -                <TrackOutput 8 session.mixers[0].tracks[0].output target=default>
            #   +                <TrackOutput 8 session.mixers[0].tracks[0].output target=session.mixers[0]>
            #                    <TrackSend 33 target=<Track 4 'B'>>
            #                <Track 9 'B'>
            #                    <TrackFeedback 10 session.mixers[0].tracks[1].feedback>
            #   """,
            #   "",
            #   "",
        ),
        # sibling
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
            #   @@ -11,7 +11,7 @@
            #                            <TrackFeedback 26 session.mixers[0].tracks[0].tracks[0].tracks[0].feedback>
            #                            <TrackInput 27 session.mixers[0].tracks[0].tracks[0].tracks[0].input source=null>
            #                            <TrackOutput 28 session.mixers[0].tracks[0].tracks[0].tracks[0].output target=default>
            #   -                    <TrackOutput 20 session.mixers[0].tracks[0].tracks[0].output target=default>
            #   +                    <TrackOutput 20 session.mixers[0].tracks[0].tracks[0].output target=session.mixers[0].tracks[0].tracks[1]>
            #                    <Track 21 'A2'>
            #                        <TrackFeedback 22 session.mixers[0].tracks[0].tracks[1].feedback>
            #                        <TrackInput 23 session.mixers[0].tracks[0].tracks[1].input source=null>
            #   """,
            #   """
            #   --- initial
            #   +++ mutation
            #   @@ -25,8 +25,10 @@
            #                                active: c11, bus: 20.0, done_action: 2.0, gain: c12, gate: 1.0
            #                            1017 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:output-levels)
            #                                in_: 20.0, out: 15.0
            #   -                        1025 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].output:synth)
            #   -                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 18.0
            #   +                        1025 supriya:patch-cable:2x2
            #   +                            active: c11, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 18.0
            #   +                        1066 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].output:synth)
            #   +                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 24.0
            #                        1026 group (session.mixers[0].tracks[0].tracks[1]:group)
            #                            1027 group (session.mixers[0].tracks[0].tracks[1]:tracks)
            #                            1030 supriya:meters:2 (session.mixers[0].tracks[0].tracks[1]:input-levels)
            #   """,
            #   """
            #   - [None,
            #      [['/n_set', 1025, 'gate', 0.0],
            #       ['/s_new', 'supriya:patch-cable:2x2', 1066, 1, 1012, 'active', 'c11', 'in_', 20.0, 'out', 24.0]]]
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
