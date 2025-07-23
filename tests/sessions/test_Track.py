import asyncio
from typing import Callable

import pytest

from supriya import BusGroup
from supriya.sessions import (
    Component,
    Mixer,
    Session,
    SignalTesterDevice,
    Track,
    TrackContainer,
    TrackSend,
)
from supriya.sessions.constants import ChannelCount
from supriya.typing import DEFAULT, Default
from supriya.ugens import system  # lookup system.LAG_TIME to support monkeypatching

from .conftest import apply_commands, does_not_raise, run_test


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "commands, postfader, send_from, send_to, maybe_raises, expected_components_diff, expected_tree_diff, expected_messages",
    [
        # 0
        # send to other mixer
        # - raises
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
        # 1
        # send to other mixer
        # send to self
        # - track: expect :feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Self"}),
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
            +                    active: c5, done_action: 2.0, gain: c11, gate: 1.0, in_: 18.0, out: 20.0
                             1012 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
                                 in_: 18.0, out: 9.0
                             1013 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:output)
            """,
            """
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 3]
            - ['/c_set', 11, 0.0]
            - ['/s_new', 'supriya:patch-cable:2x2', 1014, 3, 1010, 'active', 'c5', 'gain', 'c11', 'in_', 18.0, 'out', 20.0]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1015, 0, 1007, 'active', 'c5', 'in_', 20.0, 'out', 18.0]
            """,
        ),
        # 2
        # send to other mixer
        # send to older sibling
        # - sibling: expect :feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Older Sibling"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
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
            +                    active: c11, done_action: 2.0, gain: c17, gate: 1.0, in_: 20.0, out: 22.0
                             1019 supriya:meters:2 (session.mixers[0].tracks[1]:output-levels)
                                 in_: 20.0, out: 15.0
                             1020 supriya:patch-cable:2x2 (session.mixers[0].tracks[1]:output)
            """,
            """
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 3]
            - ['/c_set', 17, 0.0]
            - ['/s_new', 'supriya:patch-cable:2x2', 1021, 3, 1017, 'active', 'c11', 'gain', 'c17', 'in_', 20.0, 'out', 22.0]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1022, 0, 1007, 'active', 'c5', 'in_', 22.0, 'out', 18.0]
            """,
        ),
        # 3
        # send to younger sibling
        # - sibling: do not expect :feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0]", "add_track", {"name": "Younger Sibling"}),
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
            +                    active: c5, done_action: 2.0, gain: c17, gate: 1.0, in_: 18.0, out: 20.0
                             1012 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
                                 in_: 18.0, out: 9.0
                             1013 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:output)
            """,
            """
            - ['/c_set', 17, 0.0]
            - ['/s_new', 'supriya:patch-cable:2x2', 1021, 3, 1010, 'active', 'c5', 'gain', 'c17', 'in_', 18.0, 'out', 20.0]
            """,
        ),
        # 4
        # send to younger sibling, prefader
        # - sibling: do not expect :feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0]", "add_track", {"name": "Younger Sibling"}),
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
            +                    active: c5, done_action: 2.0, gain: c17, gate: 1.0, in_: 18.0, out: 20.0
                             1010 supriya:channel-strip:2 (session.mixers[0].tracks[0]:channel-strip)
                                 active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
                             1012 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
            """,
            """
            - ['/c_set', 17, 0.0]
            - ['/s_new', 'supriya:patch-cable:2x2', 1021, 2, 1010, 'active', 'c5', 'gain', 'c17', 'in_', 18.0, 'out', 20.0]
            """,
        ),
        # 5
        # send to child
        # - child: expect :feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Child"}),
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
            +                    active: c5, done_action: 2.0, gain: c17, gate: 1.0, in_: 18.0, out: 22.0
                             1012 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
                                 in_: 18.0, out: 9.0
                             1013 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:output)
            """,
            """
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 3]
            - ['/c_set', 17, 0.0]
            - ['/s_new', 'supriya:patch-cable:2x2', 1021, 3, 1010, 'active', 'c5', 'gain', 'c17', 'in_', 18.0, 'out', 22.0]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1022, 0, 1014, 'active', 'c11', 'in_', 22.0, 'out', 20.0]
            """,
        ),
        # 6
        # send to parent
        # - parent: do not expect :feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Parent"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Self"}),
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
            +                            active: c11, done_action: 2.0, gain: c17, gate: 1.0, in_: 20.0, out: 18.0
                                     1019 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:output-levels)
                                         in_: 20.0, out: 15.0
                                     1020 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0]:output)
            """,
            """
            - ['/c_set', 17, 0.0]
            - ['/s_new', 'supriya:patch-cable:2x2', 1021, 3, 1017, 'active', 'c11', 'gain', 'c17', 'in_', 20.0, 'out', 18.0]
            """,
        ),
        # 7
        # send to grandparent
        # - grandparent: do not expect :feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Grandparent"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Parent"}),
                ("mixers[0].tracks[0].tracks[0]", "add_track", {"name": "Self"}),
            ],
            True,
            "mixers[0].tracks[0].tracks[0].tracks[0]",
            "mixers[0].tracks[0]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -4,3 +4,4 @@
                         <Track 2 'Grandparent'>
                             <Track 3 'Parent'>
                                 <Track 4 'Self'>
            +                        <TrackSend 5 postfader target=<Track 2 'Grandparent'>>
            """,
            """
            --- initial
            +++ mutation
            @@ -12,6 +12,8 @@
                                             1023 group (session.mixers[0].tracks[0].tracks[0].tracks[0]:devices)
                                             1024 supriya:channel-strip:2 (session.mixers[0].tracks[0].tracks[0].tracks[0]:channel-strip)
                                                 active: c17, done_action: 2.0, gain: c18, gate: 1.0, out: 22.0
            +                                1028 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].tracks[0].sends[0]:synth)
            +                                    active: c17, done_action: 2.0, gain: c23, gate: 1.0, in_: 22.0, out: 18.0
                                             1026 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0].tracks[0]:output-levels)
                                                 in_: 22.0, out: 21.0
                                             1027 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].tracks[0]:output)
            """,
            """
            - ['/c_set', 23, 0.0]
            - ['/s_new', 'supriya:patch-cable:2x2', 1028, 3, 1024, 'active', 'c17', 'gain', 'c23', 'in_', 22.0, 'out', 18.0]
            """,
        ),
        # 8
        # send to grandchild
        # - grandchild: expect :feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Child"}),
                ("mixers[0].tracks[0].tracks[0]", "add_track", {"name": "Grandchild"}),
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
            +                    active: c5, done_action: 2.0, gain: c23, gate: 1.0, in_: 18.0, out: 24.0
                             1012 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
                                 in_: 18.0, out: 9.0
                             1013 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:output)
            """,
            """
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 3]
            - ['/c_set', 23, 0.0]
            - ['/s_new', 'supriya:patch-cable:2x2', 1028, 3, 1010, 'active', 'c5', 'gain', 'c23', 'in_', 18.0, 'out', 24.0]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1029, 0, 1021, 'active', 'c17', 'in_', 24.0, 'out', 22.0]
            """,
        ),
        # 9
        # send to older auntie
        # - auntie: expect :feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Older Auntie"}),
                ("mixers[0]", "add_track", {"name": "Parent"}),
                ("mixers[0].tracks[1]", "add_track", {"name": "Self"}),
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
            +                            active: c17, done_action: 2.0, gain: c23, gate: 1.0, in_: 22.0, out: 24.0
                                     1026 supriya:meters:2 (session.mixers[0].tracks[1].tracks[0]:output-levels)
                                         in_: 22.0, out: 21.0
                                     1027 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].tracks[0]:output)
            """,
            """
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 3]
            - ['/c_set', 23, 0.0]
            - ['/s_new', 'supriya:patch-cable:2x2', 1028, 3, 1024, 'active', 'c17', 'gain', 'c23', 'in_', 22.0, 'out', 24.0]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1029, 0, 1007, 'active', 'c5', 'in_', 24.0, 'out', 18.0]
            """,
        ),
        # 10
        # send to younger auntie
        # - auntie: do not expect :feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Parent"}),
                ("mixers[0]", "add_track", {"name": "Younger Auntie"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Self"}),
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
            +                            active: c11, done_action: 2.0, gain: c23, gate: 1.0, in_: 20.0, out: 22.0
                                     1019 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:output-levels)
                                         in_: 20.0, out: 15.0
                                     1020 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0]:output)
            """,
            """
            - ['/c_set', 23, 0.0]
            - ['/s_new', 'supriya:patch-cable:2x2', 1028, 3, 1017, 'active', 'c11', 'gain', 'c23', 'in_', 20.0, 'out', 22.0]
            """,
        ),
        # 11
        # send to older cousin
        # - older cousin: expect :feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Older Auntie"}),
                ("mixers[0]", "add_track", {"name": "Parent"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Older Cousin"}),
                ("mixers[0].tracks[1]", "add_track", {"name": "Self"}),
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
            +                            active: c23, done_action: 2.0, gain: c29, gate: 1.0, in_: 24.0, out: 26.0
                                     1033 supriya:meters:2 (session.mixers[0].tracks[1].tracks[0]:output-levels)
                                         in_: 24.0, out: 27.0
                                     1034 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].tracks[0]:output)
            """,
            """
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 3]
            - ['/c_set', 29, 0.0]
            - ['/s_new', 'supriya:patch-cable:2x2', 1035, 3, 1031, 'active', 'c23', 'gain', 'c29', 'in_', 24.0, 'out', 26.0]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1036, 0, 1014, 'active', 'c11', 'in_', 26.0, 'out', 20.0]
            """,
        ),
        # 12
        # send to younger cousin
        # - younger cousin: do not expect :feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Parent"}),
                ("mixers[0]", "add_track", {"name": "Younger Auntie"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Self"}),
                ("mixers[0].tracks[1]", "add_track", {"name": "Younger Cousin"}),
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
                         <Track 3 'Younger Auntie'>
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
            +                            active: c11, done_action: 2.0, gain: c29, gate: 1.0, in_: 20.0, out: 24.0
                                     1019 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:output-levels)
                                         in_: 20.0, out: 15.0
                                     1020 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0]:output)
            """,
            """
            - ['/c_set', 29, 0.0]
            - ['/s_new', 'supriya:patch-cable:2x2', 1035, 3, 1017, 'active', 'c11', 'gain', 'c29', 'in_', 20.0, 'out', 24.0]
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_Track_add_send(
    commands: list[tuple[str | None, str, dict | None]],
    expected_components_diff: Callable[[Session], str] | str,
    expected_messages: str,
    expected_tree_diff: str,
    maybe_raises,
    online: bool,
    postfader: bool,
    send_from: str,
    send_to: str,
) -> None:
    async with run_test(
        commands=commands,
        expected_components_diff=expected_components_diff,
        expected_messages=expected_messages,
        expected_tree_diff=expected_tree_diff,
        online=online,
    ) as session:
        send_from_ = session[send_from]
        send_to_ = session[send_to]
        assert isinstance(send_from_, Track)
        assert isinstance(send_to_, TrackContainer)
        send: TrackSend | None = None
        with maybe_raises:
            send = await send_from_.add_send(postfader=postfader, target=send_to_)
    if send is None:
        return
    assert isinstance(send, TrackSend)
    assert send in send_from_.sends
    assert send.parent is send_from_
    assert send.postfader == postfader
    assert send.target is send_to_
    assert send_from_.sends[-1] is send


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "commands, target, expected_components_diff, expected_tree_diff, expected_messages",
    [
        # 0
        # just a track
        (
            [
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
            ],
            "mixers[0].tracks[0]",
            lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,4 +1,3 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
            -            <Track 2 'Self'>
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
        # 1
        # parent track with child
        (
            [
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Child"}),
            ],
            "mixers[0].tracks[0]",
            lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,5 +1,3 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
            -            <Track 2 'Self'>
            -                <Track 3 'Child'>
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
        # 2
        # child track
        (
            [
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Parent"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Self"}),
            ],
            "mixers[0].tracks[0].tracks[0]",
            """
            --- initial
            +++ mutation
            @@ -2,4 +2,3 @@
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
                         <Track 2 'Parent'>
            -                <Track 3 'Self'>
            """,
            """
            --- initial
            +++ mutation
            @@ -9,11 +9,11 @@
                                         in_: 20.0, out: 13.0
                                     1016 group
                                     1017 supriya:channel-strip:2
            -                            active: c11, done_action: 2.0, gain: c12, gate: 1.0, out: 20.0
            +                            active: c11, done_action: 14.0, gain: c12, gate: 0.0, out: 20.0
                                     1019 supriya:meters:2
                                         in_: 20.0, out: 15.0
                                     1020 supriya:patch-cable:2x2
            -                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 18.0
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 18.0
                             1011 supriya:meters:2
                                 in_: 18.0, out: 7.0
                             1009 group
            """,
            """
            - [None, [['/n_set', 1014, 'gate', 0.0], ['/n_set', 1017, 'done_action', 14.0]]]
            """,
        ),
        # 3
        # in-tree send to self
        (
            [
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0].tracks[0]", "add_send", {"target": "mixers[0].tracks[0]"}),
            ],
            "mixers[0].tracks[0]",
            lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,5 +1,3 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
            -            <Track 2 'Self'>
            -                <TrackSend 3 postfader target=<Track 2 'Self'>>
            """,
            """
            --- initial
            +++ mutation
            @@ -3,19 +3,19 @@
                     1001 group
                         1007 group
                             1014 supriya:fb-patch-cable:2x2
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 20.0
                             1008 group
                             1011 supriya:meters:2
                                 in_: 20.0, out: 7.0
                             1009 group
                             1010 supriya:channel-strip:2
            -                    active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 20.0
            +                    active: c5, done_action: 14.0, gain: c6, gate: 0.0, out: 20.0
                             1015 supriya:patch-cable:2x2
            -                    active: c5, done_action: 2.0, gain: c11, gate: 1.0, in_: 20.0, out: 18.0
            +                    active: c5, done_action: 2.0, gain: c11, gate: 0.0, in_: 20.0, out: 18.0
                             1012 supriya:meters:2
                                 in_: 20.0, out: 9.0
                             1013 supriya:patch-cable:2x2
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 16.0
                     1004 supriya:meters:2
                         in_: 16.0, out: 1.0
                     1002 group
            """,
            """
            - [None, [['/n_set', 1007, 'gate', 0.0], ['/n_set', 1010, 'done_action', 14.0], ['/n_set', 1014, 'gate', 0.0]]]
            """,
        ),
        # 4
        # in-tree send to out-of-tree stack
        (
            [
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0]", "add_track", {"name": "Other"}),
                ("mixers[0].tracks[0]", "add_send", {"target": "mixers[0].tracks[1]"}),
            ],
            "mixers[0].tracks[0]",
            lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,6 +1,4 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
            -            <Track 2 'Self'>
            -                <TrackSend 4 postfader target=<Track 3 'Other'>>
                         <Track 3 'Other'>
            """,
            """
            --- initial
            +++ mutation
            @@ -7,13 +7,13 @@
                                 in_: 18.0, out: 7.0
                             1009 group
                             1010 supriya:channel-strip:2
            -                    active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
            +                    active: c5, done_action: 14.0, gain: c6, gate: 0.0, out: 18.0
                             1014 supriya:patch-cable:2x2
            -                    active: c5, done_action: 2.0, gain: c11, gate: 1.0, in_: 18.0, out: 20.0
            +                    active: c5, done_action: 2.0, gain: c11, gate: 0.0, in_: 18.0, out: 20.0
                             1012 supriya:meters:2
                                 in_: 18.0, out: 9.0
                             1013 supriya:patch-cable:2x2
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 16.0
                         1015 group
                             1016 group
                             1019 supriya:meters:2
            """,
            """
            - [None, [['/n_set', 1007, 'gate', 0.0], ['/n_set', 1010, 'done_action', 14.0]]]
            """,
        ),
        # 5
        # out-of-tree send to in-tree track
        (
            [
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0]", "add_track", {"name": "Other"}),
                ("mixers[0].tracks[1]", "add_send", {"target": "mixers[0].tracks[0]"}),
            ],
            "mixers[0].tracks[0]",
            lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,6 +1,4 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
            -            <Track 2 'Self'>
                         <Track 3 'Other'>
            -                <TrackSend 4 postfader target=<Track 2 'Self'>>
            """,
            """
            --- initial
            +++ mutation
            @@ -3,17 +3,17 @@
                     1001 group
                         1007 group
                             1014 supriya:fb-patch-cable:2x2
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 20.0
                             1008 group
                             1011 supriya:meters:2
                                 in_: 20.0, out: 7.0
                             1009 group
                             1010 supriya:channel-strip:2
            -                    active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 20.0
            +                    active: c5, done_action: 14.0, gain: c6, gate: 0.0, out: 20.0
                             1012 supriya:meters:2
                                 in_: 20.0, out: 9.0
                             1013 supriya:patch-cable:2x2
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 16.0
                         1015 group
                             1016 group
                             1019 supriya:meters:2
            @@ -22,7 +22,7 @@
                             1018 supriya:channel-strip:2
                                 active: c11, done_action: 2.0, gain: c12, gate: 1.0, out: 22.0
                             1022 supriya:patch-cable:2x2
            -                    active: c11, done_action: 2.0, gain: c17, gate: 1.0, in_: 22.0, out: 18.0
            +                    active: c11, done_action: 2.0, gain: c17, gate: 0.0, in_: 22.0, out: 18.0
                             1020 supriya:meters:2
                                 in_: 22.0, out: 15.0
                             1021 supriya:patch-cable:2x2
            """,
            """
            - [None, [['/n_set', 1007, 'gate', 0.0], ['/n_set', 1010, 'done_action', 14.0], ['/n_set', 1014, 'gate', 0.0]]]
            - ['/n_set', 1022, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        # 6
        # out-of-tree send to in-tree child track
        (
            [
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0]", "add_track", {"name": "Other"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Child"}),
                (
                    "mixers[0].tracks[1]",
                    "add_send",
                    {"target": "mixers[0].tracks[0].tracks[0]"},
                ),
            ],
            "mixers[0].tracks[0]",
            lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,7 +1,4 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
            -            <Track 2 'Self'>
            -                <Track 4 'Child'>
                         <Track 3 'Other'>
            -                <TrackSend 5 postfader target=<Track 4 'Child'>>
            """,
            """
            --- initial
            +++ mutation
            @@ -5,26 +5,26 @@
                             1008 group
                                 1014 group
                                     1021 supriya:fb-patch-cable:2x2
            -                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 22.0
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 22.0
                                     1015 group
                                     1018 supriya:meters:2
                                         in_: 22.0, out: 13.0
                                     1016 group
                                     1017 supriya:channel-strip:2
            -                            active: c11, done_action: 2.0, gain: c12, gate: 1.0, out: 22.0
            +                            active: c11, done_action: 2.0, gain: c12, gate: 0.0, out: 22.0
                                     1019 supriya:meters:2
                                         in_: 22.0, out: 15.0
                                     1020 supriya:patch-cable:2x2
            -                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 18.0
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 22.0, out: 18.0
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
                         1022 group
                             1023 group
                             1026 supriya:meters:2
            @@ -33,7 +33,7 @@
                             1025 supriya:channel-strip:2
                                 active: c17, done_action: 2.0, gain: c18, gate: 1.0, out: 24.0
                             1029 supriya:patch-cable:2x2
            -                    active: c17, done_action: 2.0, gain: c23, gate: 1.0, in_: 24.0, out: 20.0
            +                    active: c17, done_action: 2.0, gain: c23, gate: 0.0, in_: 24.0, out: 20.0
                             1027 supriya:meters:2
                                 in_: 24.0, out: 21.0
                             1028 supriya:patch-cable:2x2
            """,
            """
            - [None, [['/n_set', 1007, 'gate', 0.0], ['/n_set', 1010, 'done_action', 14.0]]]
            - ['/n_set', 1029, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        # 7
        # out-of-tree track output
        (
            [
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0]", "add_track", {"name": "Other"}),
                (
                    "mixers[0].tracks[1]",
                    "set_output",
                    {"output": "mixers[0].tracks[0]"},
                ),
            ],
            "mixers[0].tracks[0]",
            lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,5 +1,4 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
            -            <Track 2 'Self'>
            -            <Track 3 'Other' output=<Track 2 'Self'>>
            +            <Track 3 'Other' output=None>
            """,
            """
            --- initial
            +++ mutation
            @@ -3,17 +3,17 @@
                     1001 group
                         1007 group
                             1014 supriya:fb-patch-cable:2x2
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 20.0
                             1008 group
                             1011 supriya:meters:2
                                 in_: 20.0, out: 7.0
                             1009 group
                             1010 supriya:channel-strip:2
            -                    active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 20.0
            +                    active: c5, done_action: 14.0, gain: c6, gate: 0.0, out: 20.0
                             1012 supriya:meters:2
                                 in_: 20.0, out: 9.0
                             1013 supriya:patch-cable:2x2
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 16.0
                         1015 group
                             1016 group
                             1019 supriya:meters:2
            @@ -24,7 +24,7 @@
                             1020 supriya:meters:2
                                 in_: 22.0, out: 15.0
                             1021 supriya:patch-cable:2x2
            -                    active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 18.0
            +                    active: c11, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 22.0, out: 18.0
                     1004 supriya:meters:2
                         in_: 16.0, out: 1.0
                     1002 group
            """,
            """
            - [None, [['/n_set', 1007, 'gate', 0.0], ['/n_set', 1010, 'done_action', 14.0], ['/n_set', 1014, 'gate', 0.0]]]
            - ['/n_set', 1021, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        # 8
        # out-of-tree track input
        (
            [
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0]", "add_track", {"name": "Other"}),
                ("mixers[0].tracks[1]", "set_input", {"input_": "mixers[0].tracks[0]"}),
            ],
            "mixers[0].tracks[0]",
            lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,5 +1,4 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
            -            <Track 2 'Self'>
            -            <Track 3 'Other' input=<Track 2 'Self'>>
            +            <Track 3 'Other'>
            """,
            """
            --- initial
            +++ mutation
            @@ -7,14 +7,14 @@
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
                         1014 group
                             1020 supriya:patch-cable:2x2
            -                    active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            +                    active: c11, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 20.0
                             1015 group
                             1018 supriya:meters:2
                                 in_: 20.0, out: 13.0
            """,
            """
            - [None, [['/n_set', 1007, 'gate', 0.0], ['/n_set', 1010, 'done_action', 14.0]]]
            - ['/n_set', 1020, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_Track_delete(
    commands: list[tuple[str | None, str, dict | None]],
    expected_components_diff: Callable[[Session], str] | str,
    expected_tree_diff: str,
    expected_messages: str,
    online: bool,
    target: str,
) -> None:
    async with run_test(
        annotation=None,
        commands=commands,
        expected_components_diff=expected_components_diff,
        expected_messages=expected_messages,
        expected_tree_diff=expected_tree_diff,
        online=online,
    ) as session:
        target_ = session[target]
        assert isinstance(target_, Track)
        parent = target_.parent
        await target_.delete()
    assert parent
    assert target_ not in parent.tracks
    assert target_.address == "tracks[?]"
    assert target_.context is None
    assert target_.parent is None
    assert target_.mixer is None
    assert target_.session is None


@pytest.mark.parametrize(
    "commands, target, gain, expected_levels",
    [
        (
            [
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
                (
                    "mixers[0].tracks[0]",
                    "add_device",
                    {"device_class": SignalTesterDevice},
                ),
            ],
            "mixers[0].tracks[0]",
            -6,
            [
                ("Mixer", [0.5, 0.5], [0.5, 0.5]),
                ("Self", [0.0, 0.0], [0.5, 0.5]),
            ],
        ),
        (
            [
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Child Track"}),
                (
                    "mixers[0].tracks[0].tracks[0]",
                    "add_device",
                    {"device_class": SignalTesterDevice},
                ),
            ],
            "mixers[0].tracks[0]",
            -6,
            [
                ("Mixer", [0.5, 0.5], [0.5, 0.5]),
                ("Self", [1.0, 1.0], [0.5, 0.5]),
                ("Child Track", [0.0, 0.0], [1.0, 1.0]),
            ],
        ),
        (
            [
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Child Track"}),
                (
                    "mixers[0].tracks[0].tracks[0]",
                    "add_device",
                    {"device_class": SignalTesterDevice},
                ),
                ("mixers[0].tracks[0]", "set_parameter", {"name": "gain", "value": -6}),
            ],
            "mixers[0].tracks[0].tracks[0]",
            -6,
            [
                ("Mixer", [0.25, 0.25], [0.25, 0.25]),
                ("Self", [0.5, 0.5], [0.25, 0.25]),
                ("Child Track", [0.0, 0.0], [0.5, 0.5]),
            ],
        ),
    ],
)
@pytest.mark.asyncio
async def test_Track_gain(
    commands: list[tuple[str | None, str, dict | None]],
    expected_levels: list[tuple[str, list[float], list[float]]],
    gain: float,
    target: str,
) -> None:
    async with run_test(
        annotation=None,
        commands=commands,
        online=True,
    ) as session:
        target_ = session[target]
        assert isinstance(target_, Track)
        target_.parameters["gain"].set(gain)
    await asyncio.sleep(system.LAG_TIME * 2)
    actual_levels = [
        (
            component.name,
            [round(x, 2) for x in component.input_levels],
            [round(x, 2) for x in component.output_levels],
        )
        for component in session.walk(Component)
        if isinstance(component, (Mixer, Track))
    ]
    assert actual_levels == expected_levels


# @pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "commands, target, parent, index, maybe_raises, expected_graph_order, expected_components_diff, expected_tree_diff, expected_messages",
    [
        # 0
        # move to other mixer: raises
        (
            [
                (None, "add_mixer", {"name": "Mixer One"}),
                (None, "add_mixer", {"name": "Mixer Two"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
            ],
            "mixers[0].tracks[0]",
            "mixers[1]",
            0,
            pytest.raises(RuntimeError),
            (0, 0),
            "",
            "",
            "",
        ),
        # 1
        # move under child: raises
        (
            [
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Child"}),
            ],
            "mixers[0].tracks[0]",
            "mixers[0].tracks[0].tracks[0]",
            0,
            pytest.raises(RuntimeError),
            (0, 0),
            "",
            "",
            "",
        ),
        # 2
        # move to same parent, index too low: raises
        (
            [
                (None, "add_mixer", {"name": "Mixer One"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
            ],
            "mixers[0].tracks[0]",
            "mixers[0]",
            -1,
            pytest.raises(RuntimeError),
            (0, 0),
            "",
            "",
            "",
        ),
        # 3
        # move to same parent, index too high: raises
        (
            [
                (None, "add_mixer", {"name": "Mixer One"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
            ],
            "mixers[0].tracks[0]",
            "mixers[0]",
            2,
            pytest.raises(RuntimeError),
            (0, 0),
            "",
            "",
            "",
        ),
        # 4
        # move to same parent, same index: no-op
        (
            [
                (None, "add_mixer", {"name": "Mixer One"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
            ],
            "mixers[0].tracks[0]",
            "mixers[0]",
            0,
            does_not_raise,
            (0, 0),
            "",
            "",
            "",
        ),
        # 5
        # move after younger sibling
        (
            [
                (None, "add_mixer", {"name": "Mixer One"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0]", "add_track", {"name": "Younger Sibling"}),
            ],
            "mixers[0].tracks[0]",
            "mixers[0]",
            1,
            does_not_raise,
            (0, 1),
            lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,5 +1,5 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1 'Mixer One'>
            +            <Track 3 'Younger Sibling'>
                         <Track 2 'Self'>
            -            <Track 3 'Younger Sibling'>
            """,
            """
            --- initial
            +++ mutation
            @@ -1,6 +1,17 @@
             <session.contexts[0]>
                 NODE TREE 1000 group (mixers[1]:group)
                     1001 group (mixers[1]:tracks)
            +            1014 group (tracks[3]:group)
            +                1015 group (tracks[3]:tracks)
            +                1018 supriya:meters:2 (tracks[3]:input-levels)
            +                    in_: 20.0, out: 13.0
            +                1016 group (tracks[3]:devices)
            +                1017 supriya:channel-strip:2 (tracks[3]:channel-strip)
            +                    active: c11, done_action: 2.0, gain: c12, gate: 1.0, out: 20.0
            +                1019 supriya:meters:2 (tracks[3]:output-levels)
            +                    in_: 20.0, out: 15.0
            +                1020 supriya:patch-cable:2x2 (tracks[3]:output)
            +                    active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
                         1007 group (tracks[2]:group)
                             1008 group (tracks[2]:tracks)
                             1011 supriya:meters:2 (tracks[2]:input-levels)
            @@ -12,17 +23,6 @@
                                 in_: 18.0, out: 9.0
                             1013 supriya:patch-cable:2x2 (tracks[2]:output)
                                 active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
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
                     1004 supriya:meters:2 (mixers[1]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (mixers[1]:devices)
            """,
            """
            - ['/n_after', 1007, 1014]
            """,
        ),
        # 6
        # move before older sibling
        (
            [
                (None, "add_mixer", {"name": "Mixer One"}),
                ("mixers[0]", "add_track", {"name": "Eldest Sibling"}),
                ("mixers[0]", "add_track", {"name": "Older Sibling"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
            ],
            "mixers[0].tracks[2]",
            "mixers[0]",
            0,
            does_not_raise,
            (0, 0),
            lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,6 +1,6 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1 'Mixer One'>
            +            <Track 4 'Self'>
                         <Track 2 'Eldest Sibling'>
                         <Track 3 'Older Sibling'>
            -            <Track 4 'Self'>
            """,
            """
            --- initial
            +++ mutation
            @@ -1,6 +1,17 @@
             <session.contexts[0]>
                 NODE TREE 1000 group (mixers[1]:group)
                     1001 group (mixers[1]:tracks)
            +            1021 group (tracks[4]:group)
            +                1022 group (tracks[4]:tracks)
            +                1025 supriya:meters:2 (tracks[4]:input-levels)
            +                    in_: 22.0, out: 19.0
            +                1023 group (tracks[4]:devices)
            +                1024 supriya:channel-strip:2 (tracks[4]:channel-strip)
            +                    active: c17, done_action: 2.0, gain: c18, gate: 1.0, out: 22.0
            +                1026 supriya:meters:2 (tracks[4]:output-levels)
            +                    in_: 22.0, out: 21.0
            +                1027 supriya:patch-cable:2x2 (tracks[4]:output)
            +                    active: c17, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 16.0
                         1007 group (tracks[2]:group)
                             1008 group (tracks[2]:tracks)
                             1011 supriya:meters:2 (tracks[2]:input-levels)
            @@ -23,17 +34,6 @@
                                 in_: 20.0, out: 15.0
                             1020 supriya:patch-cable:2x2 (tracks[3]:output)
                                 active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
            -            1021 group (tracks[4]:group)
            -                1022 group (tracks[4]:tracks)
            -                1025 supriya:meters:2 (tracks[4]:input-levels)
            -                    in_: 22.0, out: 19.0
            -                1023 group (tracks[4]:devices)
            -                1024 supriya:channel-strip:2 (tracks[4]:channel-strip)
            -                    active: c17, done_action: 2.0, gain: c18, gate: 1.0, out: 22.0
            -                1026 supriya:meters:2 (tracks[4]:output-levels)
            -                    in_: 22.0, out: 21.0
            -                1027 supriya:patch-cable:2x2 (tracks[4]:output)
            -                    active: c17, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 16.0
                     1004 supriya:meters:2 (mixers[1]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (mixers[1]:devices)
            """,
            """
            - ['/g_head', 1001, 1021]
            """,
        ),
        # 7
        # move under sibling
        (
            [
                (None, "add_mixer", {"name": "Mixer One"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0]", "add_track", {"name": "Younger Sibling"}),
            ],
            "mixers[0].tracks[0]",
            "mixers[0].tracks[1]",
            0,
            does_not_raise,
            (0, 0, 0),
            lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,5 +1,5 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1 'Mixer One'>
            -            <Track 2 'Self'>
                         <Track 3 'Younger Sibling'>
            +                <Track 2 'Self'>
            """,
            """
            --- initial
            +++ mutation
            @@ -1,19 +1,21 @@
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
                         1014 group (tracks[3]:group)
                             1015 group (tracks[3]:tracks)
            +                    1007 group (tracks[2]:group)
            +                        1008 group (tracks[2]:tracks)
            +                        1011 supriya:meters:2 (tracks[2]:input-levels)
            +                            in_: 18.0, out: 7.0
            +                        1009 group (tracks[2]:devices)
            +                        1010 supriya:channel-strip:2 (tracks[2]:channel-strip)
            +                            active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
            +                        1012 supriya:meters:2 (tracks[2]:output-levels)
            +                            in_: 18.0, out: 9.0
            +                        1013 supriya:patch-cable:2x2
            +                            active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 16.0
            +                        1021 supriya:patch-cable:2x2 (tracks[2]:output)
            +                            active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
                             1018 supriya:meters:2 (tracks[3]:input-levels)
                                 in_: 20.0, out: 13.0
                             1016 group (tracks[3]:devices)
            """,
            """
            - ['/s_new', 'supriya:patch-cable:2x2', 1021, 1, 1007, 'active', 'c5', 'in_', 18.0, 'out', 20.0]
            - ['/g_head', 1015, 1007]
            - ['/g_head', 1001, 1014]
            - ['/n_set', 1013, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        # 8
        # move after younger sibling, with sends in self.
        (
            [
                (None, "add_mixer", {"name": "Mixer One"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0]", "add_track", {"name": "Younger Sibling"}),
                ("mixers[0].tracks[0]", "add_send", {"target": "mixers[0].tracks[1]"}),
            ],
            "mixers[0].tracks[0]",
            "mixers[0]",
            1,
            does_not_raise,
            (0, 1),
            lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,6 +1,6 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1 'Mixer One'>
            +            <Track 3 'Younger Sibling'>
                         <Track 2 'Self'>
                             <TrackSend 4 postfader target=<Track 3 'Younger Sibling'>>
            -            <Track 3 'Younger Sibling'>
            """,
            """
            --- initial
            +++ mutation
            @@ -1,20 +1,9 @@
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
            -                1014 supriya:patch-cable:2x2 (sends[4]:synth)
            -                    active: c5, done_action: 2.0, gain: c11, gate: 1.0, in_: 18.0, out: 20.0
            -                1012 supriya:meters:2 (tracks[2]:output-levels)
            -                    in_: 18.0, out: 9.0
            -                1013 supriya:patch-cable:2x2 (tracks[2]:output)
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
                         1015 group (tracks[3]:group)
            +                1023 supriya:fb-patch-cable:2x2 (tracks[3]:feedback)
            +                    active: c12, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 20.0
                             1016 group (tracks[3]:tracks)
                             1019 supriya:meters:2 (tracks[3]:input-levels)
                                 in_: 20.0, out: 14.0
            @@ -25,6 +14,21 @@
                                 in_: 20.0, out: 16.0
                             1021 supriya:patch-cable:2x2 (tracks[3]:output)
                                 active: c12, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
            +            1007 group (tracks[2]:group)
            +                1008 group (tracks[2]:tracks)
            +                1011 supriya:meters:2 (tracks[2]:input-levels)
            +                    in_: 18.0, out: 7.0
            +                1009 group (tracks[2]:devices)
            +                1010 supriya:channel-strip:2 (tracks[2]:channel-strip)
            +                    active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
            +                1022 supriya:patch-cable:2x2 (sends[4]:synth)
            +                    active: c5, done_action: 2.0, gain: c11, gate: 1.0, in_: 18.0, out: 22.0
            +                1014 supriya:patch-cable:2x2
            +                    active: c5, done_action: 2.0, gain: c11, gate: 0.0, in_: 18.0, out: 20.0
            +                1012 supriya:meters:2 (tracks[2]:output-levels)
            +                    in_: 18.0, out: 9.0
            +                1013 supriya:patch-cable:2x2 (tracks[2]:output)
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
                     1004 supriya:meters:2 (mixers[1]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (mixers[1]:devices)
            """,
            """
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 3]
            - ['/s_new', 'supriya:patch-cable:2x2', 1022, 3, 1010, 'active', 'c5', 'gain', 'c11', 'in_', 18.0, 'out', 22.0]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1023, 0, 1015, 'active', 'c12', 'in_', 22.0, 'out', 20.0]
            - ['/n_after', 1007, 1015]
            - ['/g_head', 1001, 1015]
            - ['/n_set', 1014, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        # 9
        # move before older sibling, with send in self.
        (
            [
                (None, "add_mixer", {"name": "Mixer One"}),
                ("mixers[0]", "add_track", {"name": "Older Sibling"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0].tracks[1]", "add_send", {"target": "mixers[0].tracks[0]"}),
            ],
            "mixers[0].tracks[1]",
            "mixers[0]",
            0,
            does_not_raise,
            (0, 0),
            lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,6 +1,6 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1 'Mixer One'>
            -            <Track 2 'Older Sibling'>
                         <Track 3 'Self'>
                             <TrackSend 4 postfader target=<Track 2 'Older Sibling'>>
            +            <Track 2 'Older Sibling'>
            """,
            """
            --- initial
            +++ mutation
            @@ -1,9 +1,24 @@
             <session.contexts[0]>
                 NODE TREE 1000 group (mixers[1]:group)
                     1001 group (mixers[1]:tracks)
            +            1015 group (tracks[3]:group)
            +                1016 group (tracks[3]:tracks)
            +                1019 supriya:meters:2 (tracks[3]:input-levels)
            +                    in_: 22.0, out: 13.0
            +                1017 group (tracks[3]:devices)
            +                1018 supriya:channel-strip:2 (tracks[3]:channel-strip)
            +                    active: c11, done_action: 2.0, gain: c12, gate: 1.0, out: 22.0
            +                1023 supriya:patch-cable:2x2 (sends[4]:synth)
            +                    active: c11, done_action: 2.0, gain: c17, gate: 1.0, in_: 22.0, out: 20.0
            +                1022 supriya:patch-cable:2x2
            +                    active: c11, done_action: 2.0, gain: c17, gate: 0.0, in_: 22.0, out: 18.0
            +                1020 supriya:meters:2 (tracks[3]:output-levels)
            +                    in_: 22.0, out: 15.0
            +                1021 supriya:patch-cable:2x2 (tracks[3]:output)
            +                    active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 16.0
                         1007 group (tracks[2]:group)
            -                1014 supriya:fb-patch-cable:2x2 (tracks[2]:feedback)
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            +                1014 supriya:fb-patch-cable:2x2
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 20.0
                             1008 group (tracks[2]:tracks)
                             1011 supriya:meters:2 (tracks[2]:input-levels)
                                 in_: 20.0, out: 7.0
            @@ -14,19 +29,6 @@
                                 in_: 20.0, out: 9.0
                             1013 supriya:patch-cable:2x2 (tracks[2]:output)
                                 active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
            -            1015 group (tracks[3]:group)
            -                1016 group (tracks[3]:tracks)
            -                1019 supriya:meters:2 (tracks[3]:input-levels)
            -                    in_: 22.0, out: 13.0
            -                1017 group (tracks[3]:devices)
            -                1018 supriya:channel-strip:2 (tracks[3]:channel-strip)
            -                    active: c11, done_action: 2.0, gain: c12, gate: 1.0, out: 22.0
            -                1022 supriya:patch-cable:2x2 (sends[4]:synth)
            -                    active: c11, done_action: 2.0, gain: c17, gate: 1.0, in_: 22.0, out: 18.0
            -                1020 supriya:meters:2 (tracks[3]:output-levels)
            -                    in_: 22.0, out: 15.0
            -                1021 supriya:patch-cable:2x2 (tracks[3]:output)
            -                    active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 16.0
                     1004 supriya:meters:2 (mixers[1]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (mixers[1]:devices)
            """,
            """
            - ['/s_new', 'supriya:patch-cable:2x2', 1023, 3, 1018, 'active', 'c11', 'gain', 'c17', 'in_', 22.0, 'out', 20.0]
            - ['/g_head', 1001, 1015]
            - ['/n_after', 1007, 1015]
            - ['/n_set', 1022, 'done_action', 2.0, 'gate', 0.0]
            - ['/n_set', 1014, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        # 10
        # move after younger sibling, with sends in sibling.
        (
            [
                (None, "add_mixer", {"name": "Mixer One"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0]", "add_track", {"name": "Younger Sibling"}),
                ("mixers[0].tracks[1]", "add_send", {"target": "mixers[0].tracks[0]"}),
            ],
            "mixers[0].tracks[0]",
            "mixers[0]",
            1,
            does_not_raise,
            (0, 1),
            lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,6 +1,6 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1 'Mixer One'>
            -            <Track 2 'Self'>
                         <Track 3 'Younger Sibling'>
                             <TrackSend 4 postfader target=<Track 2 'Self'>>
            +            <Track 2 'Self'>
            """,
            """
            --- initial
            +++ mutation
            @@ -1,9 +1,24 @@
             <session.contexts[0]>
                 NODE TREE 1000 group (mixers[1]:group)
                     1001 group (mixers[1]:tracks)
            +            1015 group (tracks[3]:group)
            +                1016 group (tracks[3]:tracks)
            +                1019 supriya:meters:2 (tracks[3]:input-levels)
            +                    in_: 22.0, out: 13.0
            +                1017 group (tracks[3]:devices)
            +                1018 supriya:channel-strip:2 (tracks[3]:channel-strip)
            +                    active: c11, done_action: 2.0, gain: c12, gate: 1.0, out: 22.0
            +                1023 supriya:patch-cable:2x2 (sends[4]:synth)
            +                    active: c11, done_action: 2.0, gain: c17, gate: 1.0, in_: 22.0, out: 20.0
            +                1022 supriya:patch-cable:2x2
            +                    active: c11, done_action: 2.0, gain: c17, gate: 0.0, in_: 22.0, out: 18.0
            +                1020 supriya:meters:2 (tracks[3]:output-levels)
            +                    in_: 22.0, out: 15.0
            +                1021 supriya:patch-cable:2x2 (tracks[3]:output)
            +                    active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 16.0
                         1007 group (tracks[2]:group)
            -                1014 supriya:fb-patch-cable:2x2 (tracks[2]:feedback)
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            +                1014 supriya:fb-patch-cable:2x2
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 20.0
                             1008 group (tracks[2]:tracks)
                             1011 supriya:meters:2 (tracks[2]:input-levels)
                                 in_: 20.0, out: 7.0
            @@ -14,19 +29,6 @@
                                 in_: 20.0, out: 9.0
                             1013 supriya:patch-cable:2x2 (tracks[2]:output)
                                 active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
            -            1015 group (tracks[3]:group)
            -                1016 group (tracks[3]:tracks)
            -                1019 supriya:meters:2 (tracks[3]:input-levels)
            -                    in_: 22.0, out: 13.0
            -                1017 group (tracks[3]:devices)
            -                1018 supriya:channel-strip:2 (tracks[3]:channel-strip)
            -                    active: c11, done_action: 2.0, gain: c12, gate: 1.0, out: 22.0
            -                1022 supriya:patch-cable:2x2 (sends[4]:synth)
            -                    active: c11, done_action: 2.0, gain: c17, gate: 1.0, in_: 22.0, out: 18.0
            -                1020 supriya:meters:2 (tracks[3]:output-levels)
            -                    in_: 22.0, out: 15.0
            -                1021 supriya:patch-cable:2x2 (tracks[3]:output)
            -                    active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 16.0
                     1004 supriya:meters:2 (mixers[1]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (mixers[1]:devices)
            """,
            """
            - ['/s_new', 'supriya:patch-cable:2x2', 1023, 3, 1018, 'active', 'c11', 'gain', 'c17', 'in_', 22.0, 'out', 20.0]
            - ['/n_after', 1007, 1015]
            - ['/n_set', 1014, 'done_action', 2.0, 'gate', 0.0]
            - ['/n_set', 1022, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        # 11
        # move before older sibling, with send in sibling.
        (
            [
                (None, "add_mixer", {"name": "Mixer One"}),
                ("mixers[0]", "add_track", {"name": "Older Sibling"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0].tracks[0]", "add_send", {"target": "mixers[0].tracks[1]"}),
            ],
            "mixers[0].tracks[1]",
            "mixers[0]",
            0,
            does_not_raise,
            (0, 0),
            lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,6 +1,6 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1 'Mixer One'>
            +            <Track 3 'Self'>
                         <Track 2 'Older Sibling'>
                             <TrackSend 4 postfader target=<Track 3 'Self'>>
            -            <Track 3 'Self'>
            """,
            """
            --- initial
            +++ mutation
            @@ -1,20 +1,9 @@
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
            -                1014 supriya:patch-cable:2x2 (sends[4]:synth)
            -                    active: c5, done_action: 2.0, gain: c11, gate: 1.0, in_: 18.0, out: 20.0
            -                1012 supriya:meters:2 (tracks[2]:output-levels)
            -                    in_: 18.0, out: 9.0
            -                1013 supriya:patch-cable:2x2 (tracks[2]:output)
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
                         1015 group (tracks[3]:group)
            +                1022 supriya:fb-patch-cable:2x2 (tracks[3]:feedback)
            +                    active: c12, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 20.0
                             1016 group (tracks[3]:tracks)
                             1019 supriya:meters:2 (tracks[3]:input-levels)
                                 in_: 20.0, out: 14.0
            @@ -25,6 +14,21 @@
                                 in_: 20.0, out: 16.0
                             1021 supriya:patch-cable:2x2 (tracks[3]:output)
                                 active: c12, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
            +            1007 group (tracks[2]:group)
            +                1008 group (tracks[2]:tracks)
            +                1011 supriya:meters:2 (tracks[2]:input-levels)
            +                    in_: 18.0, out: 7.0
            +                1009 group (tracks[2]:devices)
            +                1010 supriya:channel-strip:2 (tracks[2]:channel-strip)
            +                    active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
            +                1023 supriya:patch-cable:2x2 (sends[4]:synth)
            +                    active: c5, done_action: 2.0, gain: c11, gate: 1.0, in_: 18.0, out: 22.0
            +                1014 supriya:patch-cable:2x2
            +                    active: c5, done_action: 2.0, gain: c11, gate: 0.0, in_: 18.0, out: 20.0
            +                1012 supriya:meters:2 (tracks[2]:output-levels)
            +                    in_: 18.0, out: 9.0
            +                1013 supriya:patch-cable:2x2 (tracks[2]:output)
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
                     1004 supriya:meters:2 (mixers[1]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (mixers[1]:devices)
            """,
            """
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 3]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1022, 0, 1015, 'active', 'c12', 'in_', 22.0, 'out', 20.0]
            - ['/s_new', 'supriya:patch-cable:2x2', 1023, 3, 1010, 'active', 'c5', 'gain', 'c11', 'in_', 18.0, 'out', 22.0]
            - ['/g_head', 1001, 1015]
            - ['/n_set', 1014, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_Track_move(
    commands: list[tuple[str | None, str, dict | None]],
    expected_components_diff: Callable[[Session], str] | str,
    expected_graph_order: list[int],
    expected_messages: str,
    expected_tree_diff: str,
    index: int,
    maybe_raises,
    parent: str,
    target: str,
    online: bool = True,
) -> None:
    async with run_test(
        annotation="numeric",
        commands=commands,
        expected_components_diff=expected_components_diff,
        expected_messages=expected_messages,
        expected_tree_diff=expected_tree_diff,
        online=online,
    ) as session:
        target_ = session[target]
        parent_ = session[parent]
        old_parent = target_.parent
        assert isinstance(old_parent, TrackContainer)
        assert isinstance(parent_, TrackContainer)
        assert isinstance(target_, Track)
        raised = True
        with maybe_raises:
            await target_.move(index=index, parent=parent_)
            raised = False
    assert target_.graph_order == expected_graph_order
    if not raised:
        assert target_.parent is parent_
        assert target_ in parent_.tracks
        if parent_ is not old_parent:
            assert target_ not in old_parent.tracks


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "commands, target, channel_count, maybe_raises, expected_tree_diff, expected_messages",
    [
        # 0
        # track: set channel count to 2
        # - no-op
        (
            [
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
            ],
            "mixers[0].tracks[0]",
            2,
            does_not_raise,
            "",
            "",
        ),
        # 1
        # track: set channel count to 4
        # - track changes to 4
        (
            [
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
            ],
            "mixers[0].tracks[0]",
            4,
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -3,15 +3,19 @@
                     1001 group (session.mixers[0]:tracks)
                         1007 group (session.mixers[0].tracks[0]:group)
                             1008 group (session.mixers[0].tracks[0]:tracks)
            -                1011 supriya:meters:2 (session.mixers[0].tracks[0]:input-levels)
            -                    in_: 18.0, out: 7.0
            +                1015 supriya:meters:4 (session.mixers[0].tracks[0]:input-levels)
            +                    in_: 20.0, out: 11.0
                             1009 group (session.mixers[0].tracks[0]:devices)
            -                1010 supriya:channel-strip:2 (session.mixers[0].tracks[0]:channel-strip)
            -                    active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
            -                1012 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
            -                    in_: 18.0, out: 9.0
            -                1013 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:output)
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            +                1010 supriya:channel-strip:2
            +                    active: c5, done_action: 2.0, gain: c6, gate: 0.0, out: 18.0
            +                1013 supriya:patch-cable:2x2
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 16.0
            +                1014 supriya:channel-strip:4 (session.mixers[0].tracks[0]:channel-strip)
            +                    active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 20.0
            +                1016 supriya:meters:4 (session.mixers[0].tracks[0]:output-levels)
            +                    in_: 20.0, out: 15.0
            +                1017 supriya:patch-cable:4x2 (session.mixers[0].tracks[0]:output)
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
                     1004 supriya:meters:2 (session.mixers[0]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (session.mixers[0]:devices)
            """,
            """
            - ['/d_recv', <SynthDef: supriya:channel-strip:4>]
            - ['/d_recv', <SynthDef: supriya:meters:4>]
            - ['/d_recv', <SynthDef: supriya:patch-cable:4x2>]
            - ['/sync', 3]
            - ['/c_fill', 11, 4, 0.0, 15, 4, 0.0]
            - [None,
               [['/s_new', 'supriya:channel-strip:4', 1014, 1, 1007, 'active', 'c5', 'gain', 'c6', 'out', 20.0],
                ['/s_new', 'supriya:meters:4', 1015, 3, 1008, 'in_', 20.0, 'out', 11.0],
                ['/s_new', 'supriya:meters:4', 1016, 3, 1014, 'in_', 20.0, 'out', 15.0],
                ['/s_new', 'supriya:patch-cable:4x2', 1017, 1, 1007, 'active', 'c5', 'in_', 20.0, 'out', 16.0]]]
            - [None,
               [['/n_set', 1010, 'done_action', 2.0, 'gate', 0.0],
                ['/n_free', 1011],
                ['/n_free', 1012],
                ['/n_set', 1013, 'done_action', 2.0, 'gate', 0.0]]]
            """,
        ),
        # 2
        # track: set channel count to 4
        # - track changes to 4
        # - child track changes to 4 also
        (
            [
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Child"}),
            ],
            "mixers[0].tracks[0]",
            4,
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -5,24 +5,32 @@
                             1008 group (session.mixers[0].tracks[0]:tracks)
                                 1014 group (session.mixers[0].tracks[0].tracks[0]:group)
                                     1015 group (session.mixers[0].tracks[0].tracks[0]:tracks)
            -                        1018 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:input-levels)
            -                            in_: 20.0, out: 13.0
            +                        1026 supriya:meters:4 (session.mixers[0].tracks[0].tracks[0]:input-levels)
            +                            in_: 26.0, out: 25.0
                                     1016 group (session.mixers[0].tracks[0].tracks[0]:devices)
            -                        1017 supriya:channel-strip:2 (session.mixers[0].tracks[0].tracks[0]:channel-strip)
            -                            active: c11, done_action: 2.0, gain: c12, gate: 1.0, out: 20.0
            -                        1019 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:output-levels)
            -                            in_: 20.0, out: 15.0
            -                        1020 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0]:output)
            -                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 18.0
            -                1011 supriya:meters:2 (session.mixers[0].tracks[0]:input-levels)
            -                    in_: 18.0, out: 7.0
            +                        1017 supriya:channel-strip:2
            +                            active: c11, done_action: 2.0, gain: c12, gate: 0.0, out: 20.0
            +                        1020 supriya:patch-cable:2x2
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 18.0
            +                        1025 supriya:channel-strip:4 (session.mixers[0].tracks[0].tracks[0]:channel-strip)
            +                            active: c11, done_action: 2.0, gain: c12, gate: 1.0, out: 26.0
            +                        1027 supriya:meters:4 (session.mixers[0].tracks[0].tracks[0]:output-levels)
            +                            in_: 26.0, out: 29.0
            +                        1028 supriya:patch-cable:4x4 (session.mixers[0].tracks[0].tracks[0]:output)
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 26.0, out: 22.0
            +                1022 supriya:meters:4 (session.mixers[0].tracks[0]:input-levels)
            +                    in_: 22.0, out: 17.0
                             1009 group (session.mixers[0].tracks[0]:devices)
            -                1010 supriya:channel-strip:2 (session.mixers[0].tracks[0]:channel-strip)
            -                    active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
            -                1012 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
            -                    in_: 18.0, out: 9.0
            -                1013 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:output)
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            +                1010 supriya:channel-strip:2
            +                    active: c5, done_action: 2.0, gain: c6, gate: 0.0, out: 18.0
            +                1013 supriya:patch-cable:2x2
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 16.0
            +                1021 supriya:channel-strip:4 (session.mixers[0].tracks[0]:channel-strip)
            +                    active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 22.0
            +                1023 supriya:meters:4 (session.mixers[0].tracks[0]:output-levels)
            +                    in_: 22.0, out: 21.0
            +                1024 supriya:patch-cable:4x2 (session.mixers[0].tracks[0]:output)
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 16.0
                     1004 supriya:meters:2 (session.mixers[0]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (session.mixers[0]:devices)
            """,
            """
            - ['/d_recv', <SynthDef: supriya:channel-strip:4>]
            - ['/d_recv', <SynthDef: supriya:meters:4>]
            - ['/d_recv', <SynthDef: supriya:patch-cable:4x2>]
            - ['/d_recv', <SynthDef: supriya:patch-cable:4x4>]
            - ['/sync', 3]
            - ['/c_fill', 17, 4, 0.0, 21, 4, 0.0]
            - ['/c_fill', 25, 4, 0.0, 29, 4, 0.0]
            - [None,
               [['/s_new', 'supriya:channel-strip:4', 1021, 1, 1007, 'active', 'c5', 'gain', 'c6', 'out', 22.0],
                ['/s_new', 'supriya:meters:4', 1022, 3, 1008, 'in_', 22.0, 'out', 17.0],
                ['/s_new', 'supriya:meters:4', 1023, 3, 1021, 'in_', 22.0, 'out', 21.0],
                ['/s_new', 'supriya:patch-cable:4x2', 1024, 1, 1007, 'active', 'c5', 'in_', 22.0, 'out', 16.0]]]
            - [None,
               [['/s_new', 'supriya:channel-strip:4', 1025, 1, 1014, 'active', 'c11', 'gain', 'c12', 'out', 26.0],
                ['/s_new', 'supriya:meters:4', 1026, 3, 1015, 'in_', 26.0, 'out', 25.0],
                ['/s_new', 'supriya:meters:4', 1027, 3, 1025, 'in_', 26.0, 'out', 29.0],
                ['/s_new', 'supriya:patch-cable:4x4', 1028, 1, 1014, 'active', 'c11', 'in_', 26.0, 'out', 22.0]]]
            - [None,
               [['/n_set', 1010, 'done_action', 2.0, 'gate', 0.0],
                ['/n_free', 1011],
                ['/n_free', 1012],
                ['/n_set', 1013, 'done_action', 2.0, 'gate', 0.0]]]
            - [None,
               [['/n_set', 1017, 'done_action', 2.0, 'gate', 0.0],
                ['/n_free', 1018],
                ['/n_free', 1019],
                ['/n_set', 1020, 'done_action', 2.0, 'gate', 0.0]]]
            """,
        ),
        # 3
        # (setup) child track: set channel count to 2
        # track: set channel count to 4
        # - track changes to 4
        # - child track changes back to 2
        (
            [
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Child"}),
                (
                    "mixers[0].tracks[0].tracks[0]",
                    "set_channel_count",
                    {"channel_count": 2},
                ),
            ],
            "mixers[0].tracks[0]",
            4,
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -12,17 +12,23 @@
                                         active: c11, done_action: 2.0, gain: c12, gate: 1.0, out: 20.0
                                     1019 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:output-levels)
                                         in_: 20.0, out: 15.0
            -                        1020 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0]:output)
            -                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 18.0
            -                1011 supriya:meters:2 (session.mixers[0].tracks[0]:input-levels)
            -                    in_: 18.0, out: 7.0
            +                        1020 supriya:patch-cable:2x2
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 18.0
            +                        1025 supriya:patch-cable:2x4 (session.mixers[0].tracks[0].tracks[0]:output)
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 22.0
            +                1022 supriya:meters:4 (session.mixers[0].tracks[0]:input-levels)
            +                    in_: 22.0, out: 17.0
                             1009 group (session.mixers[0].tracks[0]:devices)
            -                1010 supriya:channel-strip:2 (session.mixers[0].tracks[0]:channel-strip)
            -                    active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
            -                1012 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
            -                    in_: 18.0, out: 9.0
            -                1013 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:output)
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            +                1010 supriya:channel-strip:2
            +                    active: c5, done_action: 2.0, gain: c6, gate: 0.0, out: 18.0
            +                1013 supriya:patch-cable:2x2
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 16.0
            +                1021 supriya:channel-strip:4 (session.mixers[0].tracks[0]:channel-strip)
            +                    active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 22.0
            +                1023 supriya:meters:4 (session.mixers[0].tracks[0]:output-levels)
            +                    in_: 22.0, out: 21.0
            +                1024 supriya:patch-cable:4x2 (session.mixers[0].tracks[0]:output)
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 16.0
                     1004 supriya:meters:2 (session.mixers[0]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (session.mixers[0]:devices)
            """,
            """
            - ['/d_recv', <SynthDef: supriya:channel-strip:4>]
            - ['/d_recv', <SynthDef: supriya:meters:4>]
            - ['/d_recv', <SynthDef: supriya:patch-cable:2x4>]
            - ['/d_recv', <SynthDef: supriya:patch-cable:4x2>]
            - ['/sync', 3]
            - ['/c_fill', 17, 4, 0.0, 21, 4, 0.0]
            - [None,
               [['/s_new', 'supriya:channel-strip:4', 1021, 1, 1007, 'active', 'c5', 'gain', 'c6', 'out', 22.0],
                ['/s_new', 'supriya:meters:4', 1022, 3, 1008, 'in_', 22.0, 'out', 17.0],
                ['/s_new', 'supriya:meters:4', 1023, 3, 1021, 'in_', 22.0, 'out', 21.0],
                ['/s_new', 'supriya:patch-cable:4x2', 1024, 1, 1007, 'active', 'c5', 'in_', 22.0, 'out', 16.0]]]
            - ['/s_new', 'supriya:patch-cable:2x4', 1025, 1, 1014, 'active', 'c11', 'in_', 20.0, 'out', 22.0]
            - [None,
               [['/n_set', 1010, 'done_action', 2.0, 'gate', 0.0],
                ['/n_free', 1011],
                ['/n_free', 1012],
                ['/n_set', 1013, 'done_action', 2.0, 'gate', 0.0]]]
            - ['/n_set', 1020, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_Track_set_channel_count(
    channel_count: ChannelCount | Default,
    commands: list[tuple[str | None, str, dict | None]],
    expected_messages: str,
    expected_tree_diff: str,
    maybe_raises,
    online: bool,
    target: str,
) -> None:
    async with run_test(
        commands=commands,
        expected_messages=expected_messages,
        expected_tree_diff=expected_tree_diff,
        online=online,
    ) as session:
        target_ = session[target]
        assert isinstance(target_, Track)
        with maybe_raises:
            await target_.set_channel_count(channel_count=channel_count)
    assert target_.channel_count == channel_count


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "commands, input_to, input_from, maybe_raises, expected_components_diff, expected_tree_diff, expected_messages",
    [
        # 0
        # input from other mixer
        # - raises
        (
            [
                (None, "add_mixer", None),
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", None),
                ("mixers[1]", "add_track", None),
            ],
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
        # 1
        # input from self
        # - raises
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Self"}),
            ],
            "mixers[0].tracks[0]",
            "mixers[0].tracks[0]",
            pytest.raises(RuntimeError),
            """
            """,
            """
            """,
            """
            """,
        ),
        # 2
        # input is none
        # - no input
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Self"}),
            ],
            "mixers[0].tracks[0]",
            None,
            does_not_raise,
            """
            """,
            """
            """,
            """
            """,
        ),
        # 3
        # input from younger sibling
        # - self: expect feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0]", "add_track", {"name": "Younger Sibling"}),
            ],
            "mixers[0].tracks[0]",
            "mixers[0].tracks[1]",
            does_not_raise,
            lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,5 +1,5 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1>
            -            <Track 2 'Self'>
            +            <Track 2 'Self' input=<Track 3 'Younger Sibling'>>
                         <Track 3 'Younger Sibling'>
            """,
            """
            --- initial
            +++ mutation
            @@ -2,6 +2,8 @@
                 NODE TREE 1000 group (session.mixers[0]:group)
                     1001 group (session.mixers[0]:tracks)
                         1007 group (session.mixers[0].tracks[0]:group)
            +                1021 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0]:input)
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 18.0
                             1008 group (session.mixers[0].tracks[0]:tracks)
                             1011 supriya:meters:2 (session.mixers[0].tracks[0]:input-levels)
                                 in_: 18.0, out: 7.0
            """,
            """
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 3]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1021, 0, 1007, 'active', 'c5', 'in_', 20.0, 'out', 18.0]
            """,
        ),
        # 4
        # input from older sibling
        # - self: do not expect feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Older Sibling"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
            ],
            "mixers[0].tracks[1]",
            "mixers[0].tracks[0]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -2,4 +2,4 @@
                 <session.contexts[0]>
                     <Mixer 1>
                         <Track 2 'Older Sibling'>
            -            <Track 3 'Self'>
            +            <Track 3 'Self' input=<Track 2 'Older Sibling'>>
            """,
            """
            --- initial
            +++ mutation
            @@ -13,6 +13,8 @@
                             1013 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:output)
                                 active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
                         1014 group (session.mixers[0].tracks[1]:group)
            +                1021 supriya:patch-cable:2x2 (session.mixers[0].tracks[1]:input)
            +                    active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
                             1015 group (session.mixers[0].tracks[1]:tracks)
                             1018 supriya:meters:2 (session.mixers[0].tracks[1]:input-levels)
                                 in_: 20.0, out: 13.0
            """,
            """
            - ['/s_new', 'supriya:patch-cable:2x2', 1021, 0, 1014, 'active', 'c11', 'in_', 18.0, 'out', 20.0]
            """,
        ),
        # 5
        # input from child
        # - self: do not expect feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Child"}),
            ],
            "mixers[0].tracks[0]",
            "mixers[0].tracks[0].tracks[0]",
            does_not_raise,
            lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,5 +1,5 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1>
            -            <Track 2 'Self'>
            +            <Track 2 'Self' input=<Track 3 'Child'>>
                             <Track 3 'Child'>
            """,
            """
            --- initial
            +++ mutation
            @@ -2,6 +2,8 @@
                 NODE TREE 1000 group (session.mixers[0]:group)
                     1001 group (session.mixers[0]:tracks)
                         1007 group (session.mixers[0].tracks[0]:group)
            +                1021 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:input)
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 18.0
                             1008 group (session.mixers[0].tracks[0]:tracks)
                                 1014 group (session.mixers[0].tracks[0].tracks[0]:group)
                                     1015 group (session.mixers[0].tracks[0].tracks[0]:tracks)
            """,
            """
            - ['/s_new', 'supriya:patch-cable:2x2', 1021, 0, 1007, 'active', 'c5', 'in_', 20.0, 'out', 18.0]
            """,
        ),
        # 6
        # input from parent
        # - self: expect feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Parent"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Self"}),
            ],
            "mixers[0].tracks[0].tracks[0]",
            "mixers[0].tracks[0]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -2,4 +2,4 @@
                 <session.contexts[0]>
                     <Mixer 1>
                         <Track 2 'Parent'>
            -                <Track 3 'Self'>
            +                <Track 3 'Self' input=<Track 2 'Parent'>>
            """,
            """
            --- initial
            +++ mutation
            @@ -4,6 +4,8 @@
                         1007 group (session.mixers[0].tracks[0]:group)
                             1008 group (session.mixers[0].tracks[0]:tracks)
                                 1014 group (session.mixers[0].tracks[0].tracks[0]:group)
            +                        1021 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0]:input)
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
                                     1015 group (session.mixers[0].tracks[0].tracks[0]:tracks)
                                     1018 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:input-levels)
                                         in_: 20.0, out: 13.0
            """,
            """
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 3]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1021, 0, 1014, 'active', 'c11', 'in_', 18.0, 'out', 20.0]
            """,
        ),
        # 7
        # input from grandparent
        # - self: expect feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Grandparent"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Parent"}),
                ("mixers[0].tracks[0].tracks[0]", "add_track", {"name": "Self"}),
            ],
            "mixers[0].tracks[0].tracks[0].tracks[0]",
            "mixers[0].tracks[0]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -3,4 +3,4 @@
                     <Mixer 1>
                         <Track 2 'Grandparent'>
                             <Track 3 'Parent'>
            -                    <Track 4 'Self'>
            +                    <Track 4 'Self' input=<Track 2 'Grandparent'>>
            """,
            """
            --- initial
            +++ mutation
            @@ -6,6 +6,8 @@
                                 1014 group (session.mixers[0].tracks[0].tracks[0]:group)
                                     1015 group (session.mixers[0].tracks[0].tracks[0]:tracks)
                                         1021 group (session.mixers[0].tracks[0].tracks[0].tracks[0]:group)
            +                                1028 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].tracks[0]:input)
            +                                    active: c17, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 22.0
                                             1022 group (session.mixers[0].tracks[0].tracks[0].tracks[0]:tracks)
                                             1025 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0].tracks[0]:input-levels)
                                                 in_: 22.0, out: 19.0
            """,
            """
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 3]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1028, 0, 1021, 'active', 'c17', 'in_', 18.0, 'out', 22.0]
            """,
        ),
        # 8
        # input from grandchild
        # - self: do not expect feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Child"}),
                ("mixers[0].tracks[0].tracks[0]", "add_track", {"name": "Grandchild"}),
            ],
            "mixers[0].tracks[0]",
            "mixers[0].tracks[0].tracks[0].tracks[0]",
            does_not_raise,
            lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,6 +1,6 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1>
            -            <Track 2 'Self'>
            +            <Track 2 'Self' input=<Track 4 'Grandchild'>>
                             <Track 3 'Child'>
                                 <Track 4 'Grandchild'>
            """,
            """
            --- initial
            +++ mutation
            @@ -2,6 +2,8 @@
                 NODE TREE 1000 group (session.mixers[0]:group)
                     1001 group (session.mixers[0]:tracks)
                         1007 group (session.mixers[0].tracks[0]:group)
            +                1028 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:input)
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 18.0
                             1008 group (session.mixers[0].tracks[0]:tracks)
                                 1014 group (session.mixers[0].tracks[0].tracks[0]:group)
                                     1015 group (session.mixers[0].tracks[0].tracks[0]:tracks)
            """,
            """
            - ['/s_new', 'supriya:patch-cable:2x2', 1028, 0, 1007, 'active', 'c5', 'in_', 22.0, 'out', 18.0]
            """,
        ),
        # 9
        # input from older auntie
        # - self: do not expect feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Older Auntie"}),
                ("mixers[0]", "add_track", {"name": "Parent"}),
                ("mixers[0].tracks[1]", "add_track", {"name": "Self"}),
            ],
            "mixers[0].tracks[1].tracks[0]",
            "mixers[0].tracks[0]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -3,4 +3,4 @@
                     <Mixer 1>
                         <Track 2 'Older Auntie'>
                         <Track 3 'Parent'>
            -                <Track 4 'Self'>
            +                <Track 4 'Self' input=<Track 2 'Older Auntie'>>
            """,
            """
            --- initial
            +++ mutation
            @@ -15,6 +15,8 @@
                         1014 group (session.mixers[0].tracks[1]:group)
                             1015 group (session.mixers[0].tracks[1]:tracks)
                                 1021 group (session.mixers[0].tracks[1].tracks[0]:group)
            +                        1028 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].tracks[0]:input)
            +                            active: c17, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 22.0
                                     1022 group (session.mixers[0].tracks[1].tracks[0]:tracks)
                                     1025 supriya:meters:2 (session.mixers[0].tracks[1].tracks[0]:input-levels)
                                         in_: 22.0, out: 19.0
            """,
            """
            - ['/s_new', 'supriya:patch-cable:2x2', 1028, 0, 1021, 'active', 'c17', 'in_', 18.0, 'out', 22.0]
            """,
        ),
        # 10
        # input from younger auntie
        # - self: expect feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Parent"}),
                ("mixers[0]", "add_track", {"name": "Younger Auntie"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Self"}),
            ],
            "mixers[0].tracks[0].tracks[0]",
            "mixers[0].tracks[1]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -2,5 +2,5 @@
                 <session.contexts[0]>
                     <Mixer 1>
                         <Track 2 'Parent'>
            -                <Track 4 'Self'>
            +                <Track 4 'Self' input=<Track 3 'Younger Auntie'>>
                         <Track 3 'Younger Auntie'>
            """,
            """
            --- initial
            +++ mutation
            @@ -4,6 +4,8 @@
                         1007 group (session.mixers[0].tracks[0]:group)
                             1008 group (session.mixers[0].tracks[0]:tracks)
                                 1014 group (session.mixers[0].tracks[0].tracks[0]:group)
            +                        1028 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0]:input)
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 20.0
                                     1015 group (session.mixers[0].tracks[0].tracks[0]:tracks)
                                     1018 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:input-levels)
                                         in_: 20.0, out: 13.0
            """,
            """
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 3]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1028, 0, 1014, 'active', 'c11', 'in_', 22.0, 'out', 20.0]
            """,
        ),
        # 11
        # input from older cousin
        # - self: do not expect feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Older Auntie"}),
                ("mixers[0]", "add_track", {"name": "Parent"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Older Cousin"}),
                ("mixers[0].tracks[1]", "add_track", {"name": "Self"}),
            ],
            "mixers[0].tracks[1].tracks[0]",
            "mixers[0].tracks[0].tracks[0]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -4,4 +4,4 @@
                         <Track 2 'Older Auntie'>
                             <Track 4 'Older Cousin'>
                         <Track 3 'Parent'>
            -                <Track 5 'Self'>
            +                <Track 5 'Self' input=<Track 4 'Older Cousin'>>
            """,
            """
            --- initial
            +++ mutation
            @@ -26,6 +26,8 @@
                         1021 group (session.mixers[0].tracks[1]:group)
                             1022 group (session.mixers[0].tracks[1]:tracks)
                                 1028 group (session.mixers[0].tracks[1].tracks[0]:group)
            +                        1035 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].tracks[0]:input)
            +                            active: c23, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 24.0
                                     1029 group (session.mixers[0].tracks[1].tracks[0]:tracks)
                                     1032 supriya:meters:2 (session.mixers[0].tracks[1].tracks[0]:input-levels)
                                         in_: 24.0, out: 25.0
            """,
            """
            - ['/s_new', 'supriya:patch-cable:2x2', 1035, 0, 1028, 'active', 'c23', 'in_', 20.0, 'out', 24.0]
            """,
        ),
        # 12
        # input from younger cousin
        # - self: expect feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Parent"}),
                ("mixers[0]", "add_track", {"name": "Younger Auntie"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Self"}),
                ("mixers[0].tracks[1]", "add_track", {"name": "Younger Cousin"}),
            ],
            "mixers[0].tracks[0].tracks[0]",
            "mixers[0].tracks[1].tracks[0]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -2,6 +2,6 @@
                 <session.contexts[0]>
                     <Mixer 1>
                         <Track 2 'Parent'>
            -                <Track 4 'Self'>
            +                <Track 4 'Self' input=<Track 5 'Younger Cousin'>>
                         <Track 3 'Younger Auntie'>
                             <Track 5 'Younger Cousin'>
            """,
            """
            --- initial
            +++ mutation
            @@ -4,6 +4,8 @@
                         1007 group (session.mixers[0].tracks[0]:group)
                             1008 group (session.mixers[0].tracks[0]:tracks)
                                 1014 group (session.mixers[0].tracks[0].tracks[0]:group)
            +                        1035 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0]:input)
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 24.0, out: 20.0
                                     1015 group (session.mixers[0].tracks[0].tracks[0]:tracks)
                                     1018 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:input-levels)
                                         in_: 20.0, out: 13.0
            """,
            """
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 3]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1035, 0, 1014, 'active', 'c11', 'in_', 24.0, 'out', 20.0]
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_Track_set_input(
    commands: list[tuple[str | None, str, dict | None]],
    expected_components_diff: Callable[[Session], str] | str,
    expected_messages: str,
    expected_tree_diff: str,
    input_from: str | tuple[int, int] | None,
    input_to: str,
    maybe_raises,
    online: bool,
) -> None:
    async with run_test(
        commands=commands,
        expected_components_diff=expected_components_diff,
        expected_messages=expected_messages,
        expected_tree_diff=expected_tree_diff,
        online=online,
    ) as session:
        input_to_ = session[input_to]
        input_from_: BusGroup | Track | None = None
        assert isinstance(input_to_, Track)
        if isinstance(input_from, str):
            input_from_component = session[input_from]
            assert isinstance(input_from_component, Track)
            input_from_ = input_from_component
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
        with maybe_raises:
            await input_to_.set_input(input_from_)


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "commands",
    [
        [
            (None, "add_mixer", {"name": "Mixer"}),
            ("mixers[0]", "add_track", {"name": "A"}),
            ("mixers[0].tracks[0]", "add_track", {"name": "AA"}),
            ("mixers[0].tracks[0]", "add_track", {"name": "AB"}),
            ("mixers[0].tracks[0]", "add_track", {"name": "AC"}),
            ("mixers[0].tracks[0].tracks[0]", "add_track", {"name": "AAA"}),
            ("mixers[0]", "add_track", {"name": "B"}),
        ],
    ],
)
@pytest.mark.parametrize(
    "additional_commands, actions, expected_state, expected_messages",
    [
        # 0
        (
            [],
            [
                ("mixers[0].tracks[0]", "set_muted", {"muted": True}),
            ],
            [
                ("A", False, True, False),
                ("AA", True, False, False),
                ("AAA", True, False, False),
                ("AB", True, False, False),
                ("AC", True, False, False),
                ("B", True, False, False),
            ],
            """
            - ['/c_set', 5, 0.0]
            """,
        ),
        # 1
        (
            [],
            [
                ("mixers[0].tracks[0].tracks[0]", "set_muted", {"muted": True}),
            ],
            [
                ("A", True, False, False),
                ("AA", False, True, False),
                ("AAA", True, False, False),
                ("AB", True, False, False),
                ("AC", True, False, False),
                ("B", True, False, False),
            ],
            """
            - ['/c_set', 11, 0.0]
            """,
        ),
        # 2
        (
            [
                ("mixers[0].tracks[0]", "set_soloed", {"soloed": True}),
            ],
            [
                ("mixers[0].tracks[0]", "set_muted", {"muted": True}),
            ],
            [
                ("A", False, True, True),
                ("AA", True, False, False),
                ("AAA", True, False, False),
                ("AB", True, False, False),
                ("AC", True, False, False),
                ("B", False, False, False),
            ],
            """
            - ['/c_set', 5, 0.0]
            """,
        ),
        # 3
        (
            [
                ("mixers[0].tracks[1]", "set_soloed", {"soloed": True}),
            ],
            [
                ("mixers[0].tracks[1]", "set_muted", {"muted": True}),
            ],
            [
                ("A", False, False, False),
                ("AA", False, False, False),
                ("AAA", False, False, False),
                ("AB", False, False, False),
                ("AC", False, False, False),
                ("B", False, True, True),
            ],
            """
            - ['/c_set', 35, 0.0]
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_Track_set_muted(
    actions: list[tuple[str | None, str, dict | None]],
    additional_commands: list[tuple[str | None, str, dict | None]],
    commands: list[tuple[str | None, str, dict | None]],
    expected_messages: str,
    expected_state: list[tuple[str, bool, bool, bool]],
    online: bool,
) -> None:
    async with run_test(
        commands=commands + additional_commands,
        expected_messages=expected_messages,
        expected_components_diff=None,
        expected_tree_diff=None,
        online=online,
    ) as session:
        await apply_commands(session, actions)
    assert [
        (
            track.name,
            track.is_active,
            track.is_muted,
            track.is_soloed,
        )
        for track in session.walk(Track)
    ] == expected_state


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.asyncio
async def test_Track_set_name(online: bool) -> None:
    session = Session()
    mixer = await session.add_mixer()
    track = await mixer.add_track()
    if online:
        await session.boot()
    assert track.name is None
    for name in ("Foo", "Bar", "Baz"):
        track.set_name(name=name)
        assert track.name == name
    track.set_name(name=None)
    assert track.name is None


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "commands, output_from, output_to, maybe_raises, expected_components_diff, expected_tree_diff, expected_messages",
    [
        # 0
        # output to other mixer
        # - raises
        (
            [
                (None, "add_mixer", None),
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", None),
                ("mixers[1]", "add_track", None),
            ],
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
        # 1
        # output to self
        # - raises
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Self"}),
            ],
            "mixers[0].tracks[0]",
            "mixers[0].tracks[0]",
            pytest.raises(RuntimeError),
            """
            """,
            """
            """,
            """
            """,
        ),
        # 2
        # output is none
        # - no output
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Self"}),
            ],
            "mixers[0].tracks[0]",
            None,
            does_not_raise,
            lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,4 +1,4 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1>
            -            <Track 2 'Self'>
            +            <Track 2 'Self' output=None>
            """,
            """
            --- initial
            +++ mutation
            @@ -10,8 +10,8 @@
                                 active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
                             1012 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
                                 in_: 18.0, out: 9.0
            -                1013 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:output)
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            +                1013 supriya:patch-cable:2x2
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 16.0
                     1004 supriya:meters:2 (session.mixers[0]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (session.mixers[0]:devices)
            """,
            """
            - ['/n_set', 1013, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        # 3
        # output to younger sibling
        # - younger sibling: do not expect :feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0]", "add_track", {"name": "Younger Sibling"}),
            ],
            "mixers[0].tracks[0]",
            "mixers[0].tracks[1]",
            does_not_raise,
            lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,5 +1,5 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1>
            -            <Track 2 'Self'>
            +            <Track 2 'Self' output=<Track 3 'Younger Sibling'>>
                         <Track 3 'Younger Sibling'>
            """,
            """
            --- initial
            +++ mutation
            @@ -10,8 +10,10 @@
                                 active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
                             1012 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
                                 in_: 18.0, out: 9.0
            -                1013 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:output)
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            +                1013 supriya:patch-cable:2x2
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 16.0
            +                1021 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:output)
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
                         1014 group (session.mixers[0].tracks[1]:group)
                             1015 group (session.mixers[0].tracks[1]:tracks)
                             1018 supriya:meters:2 (session.mixers[0].tracks[1]:input-levels)
            """,
            """
            - ['/s_new', 'supriya:patch-cable:2x2', 1021, 1, 1007, 'active', 'c5', 'in_', 18.0, 'out', 20.0]
            - ['/n_set', 1013, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        # 4
        # output to older sibling
        # - older sibling: expect :feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Older Sibling"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
            ],
            "mixers[0].tracks[1]",
            "mixers[0].tracks[0]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -2,4 +2,4 @@
                 <session.contexts[0]>
                     <Mixer 1>
                         <Track 2 'Older Sibling'>
            -            <Track 3 'Self'>
            +            <Track 3 'Self' output=<Track 2 'Older Sibling'>>
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
            @@ -21,8 +23,10 @@
                                 active: c11, done_action: 2.0, gain: c12, gate: 1.0, out: 20.0
                             1019 supriya:meters:2 (session.mixers[0].tracks[1]:output-levels)
                                 in_: 20.0, out: 15.0
            -                1020 supriya:patch-cable:2x2 (session.mixers[0].tracks[1]:output)
            -                    active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
            +                1020 supriya:patch-cable:2x2
            +                    active: c11, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 16.0
            +                1021 supriya:patch-cable:2x2 (session.mixers[0].tracks[1]:output)
            +                    active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 22.0
                     1004 supriya:meters:2 (session.mixers[0]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (session.mixers[0]:devices)
            """,
            """
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 3]
            - ['/s_new', 'supriya:patch-cable:2x2', 1021, 1, 1014, 'active', 'c11', 'in_', 20.0, 'out', 22.0]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1022, 0, 1007, 'active', 'c5', 'in_', 22.0, 'out', 18.0]
            - ['/n_set', 1020, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        # 5
        # output to child
        # - child: expect :feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Child"}),
            ],
            "mixers[0].tracks[0]",
            "mixers[0].tracks[0].tracks[0]",
            does_not_raise,
            lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,5 +1,5 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1>
            -            <Track 2 'Self'>
            +            <Track 2 'Self' output=<Track 3 'Child'>>
                             <Track 3 'Child'>
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
            @@ -21,8 +23,10 @@
                                 active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
                             1012 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
                                 in_: 18.0, out: 9.0
            -                1013 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:output)
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            +                1013 supriya:patch-cable:2x2
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 16.0
            +                1021 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:output)
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 22.0
                     1004 supriya:meters:2 (session.mixers[0]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (session.mixers[0]:devices)
            """,
            """
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 3]
            - ['/s_new', 'supriya:patch-cable:2x2', 1021, 1, 1007, 'active', 'c5', 'in_', 18.0, 'out', 22.0]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1022, 0, 1014, 'active', 'c11', 'in_', 22.0, 'out', 20.0]
            - ['/n_set', 1013, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        # 6
        # output to mixer
        # - this is a no-op
        # - mixer: do not expect :feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Self"}),
            ],
            "mixers[0].tracks[0]",
            "mixers[0]",
            does_not_raise,
            lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,4 +1,4 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1>
            -            <Track 2 'Self'>
            +            <Track 2 'Self' output=<Mixer 1>>
            """,
            """
            """,
            """
            """,
        ),
        # 7
        # output to parent
        # - this is a no-op except for the Track repr
        # - parent: do not expect :feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Parent"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Self"}),
            ],
            "mixers[0].tracks[0].tracks[0]",
            "mixers[0].tracks[0]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -2,4 +2,4 @@
                 <session.contexts[0]>
                     <Mixer 1>
                         <Track 2 'Parent'>
            -                <Track 3 'Self'>
            +                <Track 3 'Self' output=<Track 2 'Parent'>>
            """,
            """
            """,
            """
            """,
        ),
        # 8
        # output is default
        # - this is a no-op
        # - outputs to parent
        # - parent: do not expect :feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Parent"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Self"}),
            ],
            "mixers[0].tracks[0].tracks[0]",
            DEFAULT,
            does_not_raise,
            """
            """,
            """
            """,
            """
            """,
        ),
        # 9
        # output to grandparent
        # - grandparent: do not expect :feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Grandparent"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Parent"}),
                ("mixers[0].tracks[0].tracks[0]", "add_track", {"name": "Self"}),
            ],
            "mixers[0].tracks[0].tracks[0].tracks[0]",
            "mixers[0].tracks[0]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -3,4 +3,4 @@
                     <Mixer 1>
                         <Track 2 'Grandparent'>
                             <Track 3 'Parent'>
            -                    <Track 4 'Self'>
            +                    <Track 4 'Self' output=<Track 2 'Grandparent'>>
            """,
            """
            --- initial
            +++ mutation
            @@ -14,8 +14,10 @@
                                                 active: c17, done_action: 2.0, gain: c18, gate: 1.0, out: 22.0
                                             1026 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0].tracks[0]:output-levels)
                                                 in_: 22.0, out: 21.0
            -                                1027 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].tracks[0]:output)
            -                                    active: c17, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 20.0
            +                                1027 supriya:patch-cable:2x2
            +                                    active: c17, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 22.0, out: 20.0
            +                                1028 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].tracks[0]:output)
            +                                    active: c17, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 18.0
                                     1018 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:input-levels)
                                         in_: 20.0, out: 13.0
                                     1016 group (session.mixers[0].tracks[0].tracks[0]:devices)
            """,
            """
            - ['/s_new', 'supriya:patch-cable:2x2', 1028, 1, 1021, 'active', 'c17', 'in_', 22.0, 'out', 18.0]
            - ['/n_set', 1027, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        # 10
        # output to grandchild
        # - grandchild: expect :feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Child"}),
                ("mixers[0].tracks[0].tracks[0]", "add_track", {"name": "Grandchild"}),
            ],
            "mixers[0].tracks[0]",
            "mixers[0].tracks[0].tracks[0].tracks[0]",
            does_not_raise,
            lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,6 +1,6 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1>
            -            <Track 2 'Self'>
            +            <Track 2 'Self' output=<Track 4 'Grandchild'>>
                             <Track 3 'Child'>
                                 <Track 4 'Grandchild'>
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
            @@ -32,8 +34,10 @@
                                 active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
                             1012 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
                                 in_: 18.0, out: 9.0
            -                1013 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:output)
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            +                1013 supriya:patch-cable:2x2
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 16.0
            +                1028 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:output)
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 24.0
                     1004 supriya:meters:2 (session.mixers[0]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (session.mixers[0]:devices)
            """,
            """
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 3]
            - ['/s_new', 'supriya:patch-cable:2x2', 1028, 1, 1007, 'active', 'c5', 'in_', 18.0, 'out', 24.0]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1029, 0, 1021, 'active', 'c17', 'in_', 24.0, 'out', 22.0]
            - ['/n_set', 1013, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        # 11
        # output to older auntie
        # - older auntie: expect :feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Older Auntie"}),
                ("mixers[0]", "add_track", {"name": "Parent"}),
                ("mixers[0].tracks[1]", "add_track", {"name": "Self"}),
            ],
            "mixers[0].tracks[1].tracks[0]",
            "mixers[0].tracks[0]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -3,4 +3,4 @@
                     <Mixer 1>
                         <Track 2 'Older Auntie'>
                         <Track 3 'Parent'>
            -                <Track 4 'Self'>
            +                <Track 4 'Self' output=<Track 2 'Older Auntie'>>
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
            @@ -23,8 +25,10 @@
                                         active: c17, done_action: 2.0, gain: c18, gate: 1.0, out: 22.0
                                     1026 supriya:meters:2 (session.mixers[0].tracks[1].tracks[0]:output-levels)
                                         in_: 22.0, out: 21.0
            -                        1027 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].tracks[0]:output)
            -                            active: c17, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 20.0
            +                        1027 supriya:patch-cable:2x2
            +                            active: c17, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 22.0, out: 20.0
            +                        1028 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].tracks[0]:output)
            +                            active: c17, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 24.0
                             1018 supriya:meters:2 (session.mixers[0].tracks[1]:input-levels)
                                 in_: 20.0, out: 13.0
                             1016 group (session.mixers[0].tracks[1]:devices)
            """,
            """
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 3]
            - ['/s_new', 'supriya:patch-cable:2x2', 1028, 1, 1021, 'active', 'c17', 'in_', 22.0, 'out', 24.0]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1029, 0, 1007, 'active', 'c5', 'in_', 24.0, 'out', 18.0]
            - ['/n_set', 1027, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        # 12
        # output to younger auntie
        # - younger auntie: do not expect :feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Parent"}),
                ("mixers[0]", "add_track", {"name": "Younger Auntie"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Self"}),
            ],
            "mixers[0].tracks[0].tracks[0]",
            "mixers[0].tracks[1]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -2,5 +2,5 @@
                 <session.contexts[0]>
                     <Mixer 1>
                         <Track 2 'Parent'>
            -                <Track 4 'Self'>
            +                <Track 4 'Self' output=<Track 3 'Younger Auntie'>>
                         <Track 3 'Younger Auntie'>
            """,
            """
            --- initial
            +++ mutation
            @@ -12,8 +12,10 @@
                                         active: c11, done_action: 2.0, gain: c12, gate: 1.0, out: 20.0
                                     1019 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:output-levels)
                                         in_: 20.0, out: 15.0
            -                        1020 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0]:output)
            -                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 18.0
            +                        1020 supriya:patch-cable:2x2
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 18.0
            +                        1028 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0]:output)
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 22.0
                             1011 supriya:meters:2 (session.mixers[0].tracks[0]:input-levels)
                                 in_: 18.0, out: 7.0
                             1009 group (session.mixers[0].tracks[0]:devices)
            """,
            """
            - ['/s_new', 'supriya:patch-cable:2x2', 1028, 1, 1014, 'active', 'c11', 'in_', 20.0, 'out', 22.0]
            - ['/n_set', 1020, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        # 13
        # output to older cousin
        # - older cousin: expect :feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Older Auntie"}),
                ("mixers[0]", "add_track", {"name": "Parent"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Older Cousin"}),
                ("mixers[0].tracks[1]", "add_track", {"name": "Self"}),
            ],
            "mixers[0].tracks[1].tracks[0]",
            "mixers[0].tracks[0].tracks[0]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -4,4 +4,4 @@
                         <Track 2 'Older Auntie'>
                             <Track 4 'Older Cousin'>
                         <Track 3 'Parent'>
            -                <Track 5 'Self'>
            +                <Track 5 'Self' output=<Track 4 'Older Cousin'>>
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
            @@ -34,8 +36,10 @@
                                         active: c23, done_action: 2.0, gain: c24, gate: 1.0, out: 24.0
                                     1033 supriya:meters:2 (session.mixers[0].tracks[1].tracks[0]:output-levels)
                                         in_: 24.0, out: 27.0
            -                        1034 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].tracks[0]:output)
            -                            active: c23, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 24.0, out: 22.0
            +                        1034 supriya:patch-cable:2x2
            +                            active: c23, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 24.0, out: 22.0
            +                        1035 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].tracks[0]:output)
            +                            active: c23, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 24.0, out: 26.0
                             1025 supriya:meters:2 (session.mixers[0].tracks[1]:input-levels)
                                 in_: 22.0, out: 19.0
                             1023 group (session.mixers[0].tracks[1]:devices)
            """,
            """
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 3]
            - ['/s_new', 'supriya:patch-cable:2x2', 1035, 1, 1028, 'active', 'c23', 'in_', 24.0, 'out', 26.0]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1036, 0, 1014, 'active', 'c11', 'in_', 26.0, 'out', 20.0]
            - ['/n_set', 1034, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        # 14
        # output to younger cousin
        # - younger cousin: do not expect :feedback
        (
            [
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Parent"}),
                ("mixers[0]", "add_track", {"name": "Younger Auntie"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Self"}),
                ("mixers[0].tracks[1]", "add_track", {"name": "Younger Cousin"}),
            ],
            "mixers[0].tracks[0].tracks[0]",
            "mixers[0].tracks[1].tracks[0]",
            does_not_raise,
            """
            --- initial
            +++ mutation
            @@ -2,6 +2,6 @@
                 <session.contexts[0]>
                     <Mixer 1>
                         <Track 2 'Parent'>
            -                <Track 4 'Self'>
            +                <Track 4 'Self' output=<Track 5 'Younger Cousin'>>
                         <Track 3 'Younger Auntie'>
                             <Track 5 'Younger Cousin'>
            """,
            """
            --- initial
            +++ mutation
            @@ -12,8 +12,10 @@
                                         active: c11, done_action: 2.0, gain: c12, gate: 1.0, out: 20.0
                                     1019 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:output-levels)
                                         in_: 20.0, out: 15.0
            -                        1020 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0]:output)
            -                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 18.0
            +                        1020 supriya:patch-cable:2x2
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 18.0
            +                        1035 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0]:output)
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 24.0
                             1011 supriya:meters:2 (session.mixers[0].tracks[0]:input-levels)
                                 in_: 18.0, out: 7.0
                             1009 group (session.mixers[0].tracks[0]:devices)
            """,
            """
            - ['/s_new', 'supriya:patch-cable:2x2', 1035, 1, 1014, 'active', 'c11', 'in_', 20.0, 'out', 24.0]
            - ['/n_set', 1020, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_Track_set_output(
    commands: list[tuple[str | None, str, dict | None]],
    expected_components_diff: Callable[[Session], str] | str,
    expected_messages: str,
    expected_tree_diff: str,
    maybe_raises,
    online: bool,
    output_from: str,
    output_to: Default | str | None,
) -> None:
    async with run_test(
        commands=commands,
        expected_components_diff=expected_components_diff,
        expected_messages=expected_messages,
        expected_tree_diff=expected_tree_diff,
        online=online,
    ) as session:
        output_from_ = session[output_from]
        output_to_: BusGroup | Default | TrackContainer | None = None
        assert isinstance(output_from_, Track)
        if isinstance(output_to, Default):
            output_to_ = DEFAULT
        elif isinstance(output_to, str):
            output_to_component = session[output_to]
            assert isinstance(output_to_component, TrackContainer)
            output_to_ = output_to_component
        # TODO: Because the context could be null, we need the "promise" of a bus group.
        # elif isinstance(target, tuple):
        #     index, count = target
        #     target_ = BusGroup(
        #         context=session["mixers[0]"].context,
        #         calculation_rate=CalculationRate.AUDIO,
        #         id_=index,
        #         count=count,
        #     )
        with maybe_raises:
            await output_from_.set_output(output_to_)


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "commands",
    [
        [
            (None, "add_mixer", {"name": "Mixer"}),
            ("mixers[0]", "add_track", {"name": "A"}),
            ("mixers[0].tracks[0]", "add_track", {"name": "AA"}),
            ("mixers[0].tracks[0]", "add_track", {"name": "AB"}),
            ("mixers[0].tracks[0]", "add_track", {"name": "AC"}),
            ("mixers[0].tracks[0].tracks[0]", "add_track", {"name": "AAA"}),
            ("mixers[0]", "add_track", {"name": "B"}),
        ],
    ],
)
@pytest.mark.parametrize(
    "actions, expected_state, expected_messages",
    [
        # 0
        # sololing mutes sibling tree
        (
            [("mixers[0].tracks[0]", "set_soloed", {"soloed": True})],
            [
                ("A", True, False, True),
                ("AA", True, False, False),
                ("AAA", True, False, False),
                ("AB", True, False, False),
                ("AC", True, False, False),
                ("B", False, False, False),
            ],
            """
            - ['/c_set', 35, 0.0]
            """,
        ),
        # 1
        # soloing mutes sibling tree
        (
            [("mixers[0].tracks[1]", "set_soloed", {"soloed": True})],
            [
                ("A", False, False, False),
                ("AA", False, False, False),
                ("AAA", False, False, False),
                ("AB", False, False, False),
                ("AC", False, False, False),
                ("B", True, False, True),
            ],
            """
            - ['/c_set', 5, 0.0, 11, 0.0, 17, 0.0, 23, 0.0, 29, 0.0]
            """,
        ),
        # 2
        # soloing includes parentage, 1
        (
            [("mixers[0].tracks[0].tracks[0]", "set_soloed", {"soloed": True})],
            [
                ("A", True, False, False),
                ("AA", True, False, True),
                ("AAA", True, False, False),
                ("AB", False, False, False),
                ("AC", False, False, False),
                ("B", False, False, False),
            ],
            """
            - ['/c_set', 23, 0.0, 29, 0.0, 35, 0.0]
            """,
        ),
        # 3
        # soloing includes parentage, 2
        (
            [
                (
                    "mixers[0].tracks[0].tracks[0].tracks[0]",
                    "set_soloed",
                    {"soloed": True},
                )
            ],
            [
                ("A", True, False, False),
                ("AA", True, False, False),
                ("AAA", True, False, True),
                ("AB", False, False, False),
                ("AC", False, False, False),
                ("B", False, False, False),
            ],
            """
            - ['/c_set', 23, 0.0, 29, 0.0, 35, 0.0]
            """,
        ),
        # 4
        # soloing is exclusive by default, and toggles off other solos
        (
            [
                ("mixers[0].tracks[0]", "set_soloed", {"soloed": True}),
                ("mixers[0].tracks[1]", "set_soloed", {"soloed": True}),
            ],
            [
                ("A", False, False, False),
                ("AA", False, False, False),
                ("AAA", False, False, False),
                ("AB", False, False, False),
                ("AC", False, False, False),
                ("B", True, False, True),
            ],
            """ 
            - ['/c_set', 35, 0.0]
            - ['/c_set', 5, 0.0, 11, 0.0, 17, 0.0, 23, 0.0, 29, 0.0, 35, 1.0]
            """,
        ),
        # 5
        # soloing can be non-exclusive
        (
            [
                ("mixers[0].tracks[0].tracks[0]", "set_soloed", {"soloed": True}),
                (
                    "mixers[0].tracks[0].tracks[1]",
                    "set_soloed",
                    {"exclusive": False, "soloed": True},
                ),
            ],
            [
                ("A", True, False, False),
                ("AA", True, False, True),
                ("AAA", True, False, False),
                ("AB", True, False, True),
                ("AC", False, False, False),
                ("B", False, False, False),
            ],
            """
            - ['/c_set', 23, 0.0, 29, 0.0, 35, 0.0]
            - ['/c_set', 23, 1.0]
            """,
        ),
        # 6
        # deleting a soloed track unmutes other tracks
        (
            [
                ("mixers[0].tracks[1]", "set_soloed", {"soloed": True}),
                ("mixers[0].tracks[1]", "delete", {}),
            ],
            [
                ("A", True, False, False),
                ("AA", True, False, False),
                ("AAA", True, False, False),
                ("AB", True, False, False),
                ("AC", True, False, False),
            ],
            """
            - ['/c_set', 5, 0.0, 11, 0.0, 17, 0.0, 23, 0.0, 29, 0.0]
            - [None, [['/n_set', 1042, 'gate', 0.0], ['/n_set', 1045, 'done_action', 14.0]]]
            - ['/c_set', 5, 1.0, 11, 1.0, 17, 1.0, 23, 1.0, 29, 1.0]
            """,
        ),
        # 7
        # moving a soloed track toggles parentage muting
        (
            [
                ("mixers[0].tracks[0].tracks[0]", "set_soloed", {"soloed": True}),
                (
                    "mixers[0].tracks[0].tracks[0]",
                    "move",
                    {"parent": "mixers[0].tracks[1]", "index": 0},
                ),
            ],
            [
                # This is wrong, A should be inactive, B should be active
                ("A", False, False, False),
                ("AB", False, False, False),
                ("AC", False, False, False),
                ("B", True, False, False),
                ("AA", True, False, True),
                ("AAA", True, False, False),
            ],
            """
            - ['/c_set', 23, 0.0, 29, 0.0, 35, 0.0]
            - ['/s_new', 'supriya:patch-cable:2x2', 1049, 1, 1014, 'active', 'c11', 'in_', 20.0, 'out', 28.0]
            - ['/g_head', 1043, 1014]
            - ['/n_set', 1020, 'done_action', 2.0, 'gate', 0.0]
            - ['/c_set', 5, 0.0, 35, 1.0]
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_Track_set_soloed(
    actions: list[tuple[str | None, str, dict | None]],
    commands: list[tuple[str | None, str, dict | None]],
    expected_messages: str,
    expected_state: list[tuple[str, bool, bool, bool]],
    online: bool,
) -> None:
    async with run_test(
        commands=commands,
        expected_messages=expected_messages,
        expected_components_diff=None,
        expected_tree_diff=None,
        online=online,
    ) as session:
        await apply_commands(session, actions)
    assert [
        (
            track.name,
            track.is_active,
            track.is_muted,
            track.is_soloed,
        )
        for track in session.walk(Track)
    ] == expected_state


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "commands, target, maybe_raises, expected_components_diff, expected_tree_diff, expected_messages",
    [
        # track without child tracks: raises
        (
            [
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
            ],
            "mixers[0].tracks[0]",
            pytest.raises(RuntimeError),
            "",
            "",
            "",
        ),
        # track with child tracks
        (
            [
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Older Child"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Younger Child"}),
            ],
            "mixers[0].tracks[0]",
            does_not_raise,
            lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,6 +1,5 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
            -            <Track 2 'Self'>
            -                <Track 3 'Older Child'>
            -                <Track 4 'Younger Child'>
            +            <Track 3 'Older Child'>
            +            <Track 4 'Younger Child'>
            """,
            """
            --- initial
            +++ mutation
            @@ -1,39 +1,43 @@
             <session.contexts[0]>
                 NODE TREE 1000 group (mixers[1]:group)
                     1001 group (mixers[1]:tracks)
            -            1007 group (tracks[2]:group)
            -                1008 group (tracks[2]:tracks)
            -                    1014 group (tracks[3]:group)
            -                        1015 group (tracks[3]:tracks)
            -                        1018 supriya:meters:2 (tracks[3]:input-levels)
            -                            in_: 20.0, out: 13.0
            -                        1016 group (tracks[3]:devices)
            -                        1017 supriya:channel-strip:2 (tracks[3]:channel-strip)
            -                            active: c11, done_action: 2.0, gain: c12, gate: 1.0, out: 20.0
            -                        1019 supriya:meters:2 (tracks[3]:output-levels)
            -                            in_: 20.0, out: 15.0
            -                        1020 supriya:patch-cable:2x2 (tracks[3]:output)
            -                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 18.0
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
            -                1011 supriya:meters:2 (tracks[2]:input-levels)
            +            1007 group
            +                1008 group
            +                1011 supriya:meters:2
                                 in_: 18.0, out: 7.0
            -                1009 group (tracks[2]:devices)
            -                1010 supriya:channel-strip:2 (tracks[2]:channel-strip)
            -                    active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
            -                1012 supriya:meters:2 (tracks[2]:output-levels)
            +                1009 group
            +                1010 supriya:channel-strip:2
            +                    active: c5, done_action: 14.0, gain: c6, gate: 0.0, out: 18.0
            +                1012 supriya:meters:2
                                 in_: 18.0, out: 9.0
            -                1013 supriya:patch-cable:2x2 (tracks[2]:output)
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            +                1013 supriya:patch-cable:2x2
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 16.0
            +            1014 group (tracks[3]:group)
            +                1015 group (tracks[3]:tracks)
            +                1018 supriya:meters:2 (tracks[3]:input-levels)
            +                    in_: 20.0, out: 13.0
            +                1016 group (tracks[3]:devices)
            +                1017 supriya:channel-strip:2 (tracks[3]:channel-strip)
            +                    active: c11, done_action: 2.0, gain: c12, gate: 1.0, out: 20.0
            +                1019 supriya:meters:2 (tracks[3]:output-levels)
            +                    in_: 20.0, out: 15.0
            +                1020 supriya:patch-cable:2x2
            +                    active: c11, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 18.0
            +                1028 supriya:patch-cable:2x2 (tracks[3]:output)
            +                    active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
            +            1021 group (tracks[4]:group)
            +                1022 group (tracks[4]:tracks)
            +                1025 supriya:meters:2 (tracks[4]:input-levels)
            +                    in_: 22.0, out: 19.0
            +                1023 group (tracks[4]:devices)
            +                1024 supriya:channel-strip:2 (tracks[4]:channel-strip)
            +                    active: c17, done_action: 2.0, gain: c18, gate: 1.0, out: 22.0
            +                1026 supriya:meters:2 (tracks[4]:output-levels)
            +                    in_: 22.0, out: 21.0
            +                1027 supriya:patch-cable:2x2
            +                    active: c17, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 22.0, out: 18.0
            +                1029 supriya:patch-cable:2x2 (tracks[4]:output)
            +                    active: c17, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 16.0
                     1004 supriya:meters:2 (mixers[1]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (mixers[1]:devices)
            """,
            """
            - ['/s_new', 'supriya:patch-cable:2x2', 1028, 1, 1014, 'active', 'c11', 'in_', 20.0, 'out', 16.0]
            - ['/s_new', 'supriya:patch-cable:2x2', 1029, 1, 1021, 'active', 'c17', 'in_', 22.0, 'out', 16.0]
            - ['/n_after', 1014, 1007]
            - ['/n_after', 1021, 1014]
            - [None, [['/n_set', 1007, 'gate', 0.0], ['/n_set', 1010, 'done_action', 14.0]]]
            - ['/n_set', 1020, 'done_action', 2.0, 'gate', 0.0]
            - ['/n_set', 1027, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_Track_ungroup(
    commands: list[tuple[str | None, str, dict | None]],
    expected_components_diff: Callable[[Session], str] | str,
    expected_tree_diff: str,
    expected_messages: str,
    maybe_raises,
    online: bool,
    target: str,
) -> None:
    async with run_test(
        annotation="numeric",
        commands=commands,
        expected_components_diff=expected_components_diff,
        expected_messages=expected_messages,
        expected_tree_diff=expected_tree_diff,
        online=online,
    ) as session:
        target_ = session[target]
        assert isinstance(target_, Track)
        with maybe_raises:
            await target_.ungroup()
