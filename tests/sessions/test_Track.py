import dataclasses
from typing import Sequence

import pytest

from supriya import BusGroup
from supriya.sessions import (
    Session,
    SynthConfig,
    Track,
    TrackContainer,
    TrackSend,
)
from supriya.sessions.constants import ChannelCount
from supriya.typing import INHERIT, Inherit
from supriya.ugens import system  # lookup system.LAG_TIME to support monkeypatching

from .conftest import Scenario, apply_commands


@dataclasses.dataclass(frozen=True)
class AddSendScenario(Scenario):
    postfader: bool
    target: str


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "scenario",
    [
        AddSendScenario(
            id="send to other mixer",
            commands=[
                (None, "add_mixer", None),
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", None),
                ("mixers[1]", "add_track", None),
            ],
            postfader=True,
            subject="mixers[0].tracks[0]",
            target="mixers[1].tracks[0]",
            expected_exception=RuntimeError,
            expected_components_diff="",
            expected_tree_diff="",
            expected_messages="",
        ),
        AddSendScenario(
            id="send to self",
            commands=[
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Self"}),
            ],
            postfader=True,
            subject="mixers[0].tracks[0]",
            target="mixers[0].tracks[0]",
            expected_components_diff="""
            --- initial
            +++ mutation
            @@ -2,3 +2,4 @@
                 <session.contexts[0]>
                     <Mixer 1>
                         <Track 2 'Self'>
            +                <TrackSend 3 postfader target=<Track 2 'Self'>>
            """,
            expected_tree_diff="""
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
            expected_messages="""
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 3]
            - ['/c_set', 11, 0.0]
            - ['/s_new', 'supriya:patch-cable:2x2', 1014, 3, 1010, 'active', 'c5', 'gain', 'c11', 'in_', 18.0, 'out', 20.0]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1015, 0, 1007, 'active', 'c5', 'in_', 20.0, 'out', 18.0]
            """,
        ),
        AddSendScenario(
            id="send to older sibling",
            commands=[
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Older Sibling"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
            ],
            postfader=True,
            subject="mixers[0].tracks[1]",
            target="mixers[0].tracks[0]",
            expected_components_diff="""
            --- initial
            +++ mutation
            @@ -3,3 +3,4 @@
                     <Mixer 1>
                         <Track 2 'Older Sibling'>
                         <Track 3 'Self'>
            +                <TrackSend 4 postfader target=<Track 2 'Older Sibling'>>
            """,
            expected_tree_diff="""
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
            expected_messages="""
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 3]
            - ['/c_set', 17, 0.0]
            - ['/s_new', 'supriya:patch-cable:2x2', 1021, 3, 1017, 'active', 'c11', 'gain', 'c17', 'in_', 20.0, 'out', 22.0]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1022, 0, 1007, 'active', 'c5', 'in_', 22.0, 'out', 18.0]
            """,
        ),
        AddSendScenario(
            id="send to younger sibling",
            commands=[
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0]", "add_track", {"name": "Younger Sibling"}),
            ],
            postfader=True,
            subject="mixers[0].tracks[0]",
            target="mixers[0].tracks[1]",
            expected_components_diff="""
            --- initial
            +++ mutation
            @@ -2,4 +2,5 @@
                 <session.contexts[0]>
                     <Mixer 1>
                         <Track 2 'Self'>
            +                <TrackSend 4 postfader target=<Track 3 'Younger Sibling'>>
                         <Track 3 'Younger Sibling'>
            """,
            expected_tree_diff="""
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
            expected_messages="""
            - ['/c_set', 17, 0.0]
            - ['/s_new', 'supriya:patch-cable:2x2', 1021, 3, 1010, 'active', 'c5', 'gain', 'c17', 'in_', 18.0, 'out', 20.0]
            """,
        ),
        AddSendScenario(
            id="send to younger sibling, prefader",
            commands=[
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0]", "add_track", {"name": "Younger Sibling"}),
            ],
            postfader=False,
            subject="mixers[0].tracks[0]",
            target="mixers[0].tracks[1]",
            expected_components_diff="""
            --- initial
            +++ mutation
            @@ -2,4 +2,5 @@
                 <session.contexts[0]>
                     <Mixer 1>
                         <Track 2 'Self'>
            +                <TrackSend 4 prefader target=<Track 3 'Younger Sibling'>>
                         <Track 3 'Younger Sibling'>
            """,
            expected_tree_diff="""
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
            expected_messages="""
            - ['/c_set', 17, 0.0]
            - ['/s_new', 'supriya:patch-cable:2x2', 1021, 2, 1010, 'active', 'c5', 'gain', 'c17', 'in_', 18.0, 'out', 20.0]
            """,
        ),
        AddSendScenario(
            id="send to child",
            commands=[
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Child"}),
            ],
            postfader=True,
            subject="mixers[0].tracks[0]",
            target="mixers[0].tracks[0].tracks[0]",
            expected_components_diff="""
            --- initial
            +++ mutation
            @@ -3,3 +3,4 @@
                     <Mixer 1>
                         <Track 2 'Self'>
                             <Track 3 'Child'>
            +                <TrackSend 4 postfader target=<Track 3 'Child'>>
            """,
            expected_tree_diff="""
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
            expected_messages="""
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 3]
            - ['/c_set', 17, 0.0]
            - ['/s_new', 'supriya:patch-cable:2x2', 1021, 3, 1010, 'active', 'c5', 'gain', 'c17', 'in_', 18.0, 'out', 22.0]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1022, 0, 1014, 'active', 'c11', 'in_', 22.0, 'out', 20.0]
            """,
        ),
        AddSendScenario(
            id="sent to parent",
            commands=[
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Parent"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Self"}),
            ],
            postfader=True,
            subject="mixers[0].tracks[0].tracks[0]",
            target="mixers[0].tracks[0]",
            expected_components_diff="""
            --- initial
            +++ mutation
            @@ -3,3 +3,4 @@
                     <Mixer 1>
                         <Track 2 'Parent'>
                             <Track 3 'Self'>
            +                    <TrackSend 4 postfader target=<Track 2 'Parent'>>
            """,
            expected_tree_diff="""
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
            expected_messages="""
            - ['/c_set', 17, 0.0]
            - ['/s_new', 'supriya:patch-cable:2x2', 1021, 3, 1017, 'active', 'c11', 'gain', 'c17', 'in_', 20.0, 'out', 18.0]
            """,
        ),
        AddSendScenario(
            id="send to grandparent",
            commands=[
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Grandparent"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Parent"}),
                ("mixers[0].tracks[0].tracks[0]", "add_track", {"name": "Self"}),
            ],
            postfader=True,
            subject="mixers[0].tracks[0].tracks[0].tracks[0]",
            target="mixers[0].tracks[0]",
            expected_components_diff="""
            --- initial
            +++ mutation
            @@ -4,3 +4,4 @@
                         <Track 2 'Grandparent'>
                             <Track 3 'Parent'>
                                 <Track 4 'Self'>
            +                        <TrackSend 5 postfader target=<Track 2 'Grandparent'>>
            """,
            expected_tree_diff="""
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
            expected_messages="""
            - ['/c_set', 23, 0.0]
            - ['/s_new', 'supriya:patch-cable:2x2', 1028, 3, 1024, 'active', 'c17', 'gain', 'c23', 'in_', 22.0, 'out', 18.0]
            """,
        ),
        AddSendScenario(
            id="send to grandchild",
            commands=[
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Child"}),
                ("mixers[0].tracks[0].tracks[0]", "add_track", {"name": "Grandchild"}),
            ],
            postfader=True,
            subject="mixers[0].tracks[0]",
            target="mixers[0].tracks[0].tracks[0].tracks[0]",
            expected_components_diff="""
            --- initial
            +++ mutation
            @@ -4,3 +4,4 @@
                         <Track 2 'Self'>
                             <Track 3 'Child'>
                                 <Track 4 'Grandchild'>
            +                <TrackSend 5 postfader target=<Track 4 'Grandchild'>>
            """,
            expected_tree_diff="""
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
            expected_messages="""
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 3]
            - ['/c_set', 23, 0.0]
            - ['/s_new', 'supriya:patch-cable:2x2', 1028, 3, 1010, 'active', 'c5', 'gain', 'c23', 'in_', 18.0, 'out', 24.0]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1029, 0, 1021, 'active', 'c17', 'in_', 24.0, 'out', 22.0]
            """,
        ),
        AddSendScenario(
            id="send to older auntie",
            commands=[
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Older Auntie"}),
                ("mixers[0]", "add_track", {"name": "Parent"}),
                ("mixers[0].tracks[1]", "add_track", {"name": "Self"}),
            ],
            postfader=True,
            subject="mixers[0].tracks[1].tracks[0]",
            target="mixers[0].tracks[0]",
            expected_components_diff="""
            --- initial
            +++ mutation
            @@ -4,3 +4,4 @@
                         <Track 2 'Older Auntie'>
                         <Track 3 'Parent'>
                             <Track 4 'Self'>
            +                    <TrackSend 5 postfader target=<Track 2 'Older Auntie'>>
            """,
            expected_tree_diff="""
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
            expected_messages="""
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 3]
            - ['/c_set', 23, 0.0]
            - ['/s_new', 'supriya:patch-cable:2x2', 1028, 3, 1024, 'active', 'c17', 'gain', 'c23', 'in_', 22.0, 'out', 24.0]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1029, 0, 1007, 'active', 'c5', 'in_', 24.0, 'out', 18.0]
            """,
        ),
        AddSendScenario(
            id="send to younger auntie",
            commands=[
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Parent"}),
                ("mixers[0]", "add_track", {"name": "Younger Auntie"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Self"}),
            ],
            postfader=True,
            subject="mixers[0].tracks[0].tracks[0]",
            target="mixers[0].tracks[1]",
            expected_components_diff="""
            --- initial
            +++ mutation
            @@ -3,4 +3,5 @@
                     <Mixer 1>
                         <Track 2 'Parent'>
                             <Track 4 'Self'>
            +                    <TrackSend 5 postfader target=<Track 3 'Younger Auntie'>>
                         <Track 3 'Younger Auntie'>
            """,
            expected_tree_diff="""
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
            expected_messages="""
            - ['/c_set', 23, 0.0]
            - ['/s_new', 'supriya:patch-cable:2x2', 1028, 3, 1017, 'active', 'c11', 'gain', 'c23', 'in_', 20.0, 'out', 22.0]
            """,
        ),
        AddSendScenario(
            id="send to older cousin",
            commands=[
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Older Auntie"}),
                ("mixers[0]", "add_track", {"name": "Parent"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Older Cousin"}),
                ("mixers[0].tracks[1]", "add_track", {"name": "Self"}),
            ],
            postfader=True,
            subject="mixers[0].tracks[1].tracks[0]",
            target="mixers[0].tracks[0].tracks[0]",
            expected_components_diff="""
            --- initial
            +++ mutation
            @@ -5,3 +5,4 @@
                             <Track 4 'Older Cousin'>
                         <Track 3 'Parent'>
                             <Track 5 'Self'>
            +                    <TrackSend 6 postfader target=<Track 4 'Older Cousin'>>
            """,
            expected_tree_diff="""
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
            expected_messages="""
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 3]
            - ['/c_set', 29, 0.0]
            - ['/s_new', 'supriya:patch-cable:2x2', 1035, 3, 1031, 'active', 'c23', 'gain', 'c29', 'in_', 24.0, 'out', 26.0]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1036, 0, 1014, 'active', 'c11', 'in_', 26.0, 'out', 20.0]
            """,
        ),
        AddSendScenario(
            id="send to younger cousin",
            commands=[
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Parent"}),
                ("mixers[0]", "add_track", {"name": "Younger Auntie"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Self"}),
                ("mixers[0].tracks[1]", "add_track", {"name": "Younger Cousin"}),
            ],
            postfader=True,
            subject="mixers[0].tracks[0].tracks[0]",
            target="mixers[0].tracks[1].tracks[0]",
            expected_components_diff="""
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
            expected_tree_diff="""
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
            expected_messages="""
            - ['/c_set', 29, 0.0]
            - ['/s_new', 'supriya:patch-cable:2x2', 1035, 3, 1017, 'active', 'c11', 'gain', 'c29', 'in_', 20.0, 'out', 24.0]
            """,
        ),
    ],
    ids=lambda scenario: scenario.id,
)
@pytest.mark.asyncio
async def test_Track_add_send(
    scenario: AddSendScenario,
    online: bool,
) -> None:
    async with scenario.run(online=online) as session:
        subject = session[scenario.subject]
        target = session[scenario.target]
        assert isinstance(subject, Track)
        assert isinstance(target, TrackContainer)
        send = await subject.add_send(postfader=scenario.postfader, target=target)
    if scenario.expected_exception:
        return
    assert isinstance(send, TrackSend)
    assert send in subject.sends
    assert send.parent is subject
    assert send.postfader == scenario.postfader
    assert send.target is target
    assert subject.sends[-1] is send


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "scenario",
    [
        Scenario(
            id="just a track",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
            ],
            subject="mixers[0].tracks[0]",
            expected_components_diff=lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,4 +1,3 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
            -            <Track 2 'Self'>
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -7,11 +7,11 @@
                                 in_: 18.0, out: 7.0
                             1009 group (tracks[2]:devices)
                             1010 supriya:channel-strip:2 (tracks[2]:channel-strip)
            -                    active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
            +                    active: c5, done_action: 14.0, gain: c6, gate: 0.0, out: 18.0
                             1012 supriya:meters:2 (tracks[2]:output-levels)
                                 in_: 18.0, out: 9.0
                             1013 supriya:patch-cable:2x2 (tracks[2]:output)
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 16.0
                     1004 supriya:meters:2 (mixers[1]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (mixers[1]:devices)
            """,
            expected_messages="""
            - [None, [['/n_set', 1007, 'gate', 0.0], ['/n_set', 1010, 'done_action', 14.0]]]
            """,
        ),
        Scenario(
            id="parent track with child",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Child"}),
            ],
            subject="mixers[0].tracks[0]",
            expected_components_diff=lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,5 +1,3 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
            -            <Track 2 'Self'>
            -                <Track 3 'Child'>
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -9,20 +9,20 @@
                                         in_: 20.0, out: 13.0
                                     1016 group (tracks[3]:devices)
                                     1017 supriya:channel-strip:2 (tracks[3]:channel-strip)
            -                            active: c11, done_action: 2.0, gain: c12, gate: 1.0, out: 20.0
            +                            active: c11, done_action: 2.0, gain: c12, gate: 0.0, out: 20.0
                                     1019 supriya:meters:2 (tracks[3]:output-levels)
                                         in_: 20.0, out: 15.0
                                     1020 supriya:patch-cable:2x2 (tracks[3]:output)
            -                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 18.0
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 18.0
                             1011 supriya:meters:2 (tracks[2]:input-levels)
                                 in_: 18.0, out: 7.0
                             1009 group (tracks[2]:devices)
                             1010 supriya:channel-strip:2 (tracks[2]:channel-strip)
            -                    active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
            +                    active: c5, done_action: 14.0, gain: c6, gate: 0.0, out: 18.0
                             1012 supriya:meters:2 (tracks[2]:output-levels)
                                 in_: 18.0, out: 9.0
                             1013 supriya:patch-cable:2x2 (tracks[2]:output)
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 16.0
                     1004 supriya:meters:2 (mixers[1]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (mixers[1]:devices)
            """,
            expected_messages="""
            - [None, [['/n_set', 1007, 'gate', 0.0], ['/n_set', 1010, 'done_action', 14.0]]]
            """,
        ),
        Scenario(
            id="child track",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Parent"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Self"}),
            ],
            subject="mixers[0].tracks[0].tracks[0]",
            expected_components_diff="""
            --- initial
            +++ mutation
            @@ -2,4 +2,3 @@
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
                         <Track 2 'Parent'>
            -                <Track 3 'Self'>
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -9,11 +9,11 @@
                                         in_: 20.0, out: 13.0
                                     1016 group (tracks[3]:devices)
                                     1017 supriya:channel-strip:2 (tracks[3]:channel-strip)
            -                            active: c11, done_action: 2.0, gain: c12, gate: 1.0, out: 20.0
            +                            active: c11, done_action: 14.0, gain: c12, gate: 0.0, out: 20.0
                                     1019 supriya:meters:2 (tracks[3]:output-levels)
                                         in_: 20.0, out: 15.0
                                     1020 supriya:patch-cable:2x2 (tracks[3]:output)
            -                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 18.0
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 18.0
                             1011 supriya:meters:2 (tracks[2]:input-levels)
                                 in_: 18.0, out: 7.0
                             1009 group (tracks[2]:devices)
            """,
            expected_messages="""
            - [None, [['/n_set', 1014, 'gate', 0.0], ['/n_set', 1017, 'done_action', 14.0]]]
            """,
        ),
        Scenario(
            id="in-tree send to self",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0].tracks[0]", "add_send", {"target": "mixers[0].tracks[0]"}),
            ],
            subject="mixers[0].tracks[0]",
            expected_components_diff=lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,5 +1,3 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
            -            <Track 2 'Self'>
            -                <TrackSend 3 postfader target=<Track 2 'Self'>>
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -3,19 +3,19 @@
                     1001 group (mixers[1]:tracks)
                         1007 group (tracks[2]:group)
                             1014 supriya:fb-patch-cable:2x2 (tracks[2]:feedback)
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 20.0
                             1008 group (tracks[2]:tracks)
                             1011 supriya:meters:2 (tracks[2]:input-levels)
                                 in_: 20.0, out: 7.0
                             1009 group (tracks[2]:devices)
                             1010 supriya:channel-strip:2 (tracks[2]:channel-strip)
            -                    active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 20.0
            +                    active: c5, done_action: 14.0, gain: c6, gate: 0.0, out: 20.0
                             1015 supriya:patch-cable:2x2 (sends[3]:synth)
            -                    active: c5, done_action: 2.0, gain: c11, gate: 1.0, in_: 20.0, out: 18.0
            +                    active: c5, done_action: 2.0, gain: c11, gate: 0.0, in_: 20.0, out: 18.0
                             1012 supriya:meters:2 (tracks[2]:output-levels)
                                 in_: 20.0, out: 9.0
                             1013 supriya:patch-cable:2x2 (tracks[2]:output)
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 16.0
                     1004 supriya:meters:2 (mixers[1]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (mixers[1]:devices)
            """,
            expected_messages="""
            - [None, [['/n_set', 1007, 'gate', 0.0], ['/n_set', 1010, 'done_action', 14.0], ['/n_set', 1014, 'gate', 0.0]]]
            """,
        ),
        Scenario(
            id="in-tree send to out-of-tree track",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0]", "add_track", {"name": "Other"}),
                ("mixers[0].tracks[0]", "add_send", {"target": "mixers[0].tracks[1]"}),
            ],
            subject="mixers[0].tracks[0]",
            expected_components_diff=lambda session: f"""
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
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -7,13 +7,13 @@
                                 in_: 18.0, out: 7.0
                             1009 group (tracks[2]:devices)
                             1010 supriya:channel-strip:2 (tracks[2]:channel-strip)
            -                    active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
            +                    active: c5, done_action: 14.0, gain: c6, gate: 0.0, out: 18.0
                             1014 supriya:patch-cable:2x2 (sends[4]:synth)
            -                    active: c5, done_action: 2.0, gain: c11, gate: 1.0, in_: 18.0, out: 20.0
            +                    active: c5, done_action: 2.0, gain: c11, gate: 0.0, in_: 18.0, out: 20.0
                             1012 supriya:meters:2 (tracks[2]:output-levels)
                                 in_: 18.0, out: 9.0
                             1013 supriya:patch-cable:2x2 (tracks[2]:output)
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 16.0
                         1015 group (tracks[3]:group)
                             1016 group (tracks[3]:tracks)
                             1019 supriya:meters:2 (tracks[3]:input-levels)
            """,
            expected_messages="""
            - [None, [['/n_set', 1007, 'gate', 0.0], ['/n_set', 1010, 'done_action', 14.0]]]
            """,
        ),
        Scenario(
            id="out-of-tree send to in-tree track",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0]", "add_track", {"name": "Other"}),
                ("mixers[0].tracks[1]", "add_send", {"target": "mixers[0].tracks[0]"}),
            ],
            subject="mixers[0].tracks[0]",
            expected_components_diff=lambda session: f"""
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
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -3,17 +3,17 @@
                     1001 group (mixers[1]:tracks)
                         1007 group (tracks[2]:group)
                             1014 supriya:fb-patch-cable:2x2 (tracks[2]:feedback)
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 20.0
                             1008 group (tracks[2]:tracks)
                             1011 supriya:meters:2 (tracks[2]:input-levels)
                                 in_: 20.0, out: 7.0
                             1009 group (tracks[2]:devices)
                             1010 supriya:channel-strip:2 (tracks[2]:channel-strip)
            -                    active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 20.0
            +                    active: c5, done_action: 14.0, gain: c6, gate: 0.0, out: 20.0
                             1012 supriya:meters:2 (tracks[2]:output-levels)
                                 in_: 20.0, out: 9.0
                             1013 supriya:patch-cable:2x2 (tracks[2]:output)
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 16.0
                         1015 group (tracks[3]:group)
                             1016 group (tracks[3]:tracks)
                             1019 supriya:meters:2 (tracks[3]:input-levels)
            @@ -22,7 +22,7 @@
                             1018 supriya:channel-strip:2 (tracks[3]:channel-strip)
                                 active: c11, done_action: 2.0, gain: c12, gate: 1.0, out: 22.0
                             1022 supriya:patch-cable:2x2 (sends[4]:synth)
            -                    active: c11, done_action: 2.0, gain: c17, gate: 1.0, in_: 22.0, out: 18.0
            +                    active: c11, done_action: 2.0, gain: c17, gate: 0.0, in_: 22.0, out: 18.0
                             1020 supriya:meters:2 (tracks[3]:output-levels)
                                 in_: 22.0, out: 15.0
                             1021 supriya:patch-cable:2x2 (tracks[3]:output)
            """,
            expected_messages="""
            - [None, [['/n_set', 1007, 'gate', 0.0], ['/n_set', 1010, 'done_action', 14.0], ['/n_set', 1014, 'gate', 0.0]]]
            - ['/n_set', 1022, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        Scenario(
            id="out-of-tree send to in-tree child track",
            commands=[
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
            subject="mixers[0].tracks[0]",
            expected_components_diff=lambda session: f"""
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
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -5,26 +5,26 @@
                             1008 group (tracks[2]:tracks)
                                 1014 group (tracks[4]:group)
                                     1021 supriya:fb-patch-cable:2x2 (tracks[4]:feedback)
            -                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 22.0
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 22.0
                                     1015 group (tracks[4]:tracks)
                                     1018 supriya:meters:2 (tracks[4]:input-levels)
                                         in_: 22.0, out: 13.0
                                     1016 group (tracks[4]:devices)
                                     1017 supriya:channel-strip:2 (tracks[4]:channel-strip)
            -                            active: c11, done_action: 2.0, gain: c12, gate: 1.0, out: 22.0
            +                            active: c11, done_action: 2.0, gain: c12, gate: 0.0, out: 22.0
                                     1019 supriya:meters:2 (tracks[4]:output-levels)
                                         in_: 22.0, out: 15.0
                                     1020 supriya:patch-cable:2x2 (tracks[4]:output)
            -                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 18.0
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 22.0, out: 18.0
                             1011 supriya:meters:2 (tracks[2]:input-levels)
                                 in_: 18.0, out: 7.0
                             1009 group (tracks[2]:devices)
                             1010 supriya:channel-strip:2 (tracks[2]:channel-strip)
            -                    active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
            +                    active: c5, done_action: 14.0, gain: c6, gate: 0.0, out: 18.0
                             1012 supriya:meters:2 (tracks[2]:output-levels)
                                 in_: 18.0, out: 9.0
                             1013 supriya:patch-cable:2x2 (tracks[2]:output)
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 16.0
                         1022 group (tracks[3]:group)
                             1023 group (tracks[3]:tracks)
                             1026 supriya:meters:2 (tracks[3]:input-levels)
            @@ -33,7 +33,7 @@
                             1025 supriya:channel-strip:2 (tracks[3]:channel-strip)
                                 active: c17, done_action: 2.0, gain: c18, gate: 1.0, out: 24.0
                             1029 supriya:patch-cable:2x2 (sends[5]:synth)
            -                    active: c17, done_action: 2.0, gain: c23, gate: 1.0, in_: 24.0, out: 20.0
            +                    active: c17, done_action: 2.0, gain: c23, gate: 0.0, in_: 24.0, out: 20.0
                             1027 supriya:meters:2 (tracks[3]:output-levels)
                                 in_: 24.0, out: 21.0
                             1028 supriya:patch-cable:2x2 (tracks[3]:output)
            """,
            expected_messages="""
            - [None, [['/n_set', 1007, 'gate', 0.0], ['/n_set', 1010, 'done_action', 14.0]]]
            - ['/n_set', 1029, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        Scenario(
            id="out-of-tree track output",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0]", "add_track", {"name": "Other"}),
                (
                    "mixers[0].tracks[1]",
                    "set_output",
                    {"output": "mixers[0].tracks[0]"},
                ),
            ],
            subject="mixers[0].tracks[0]",
            expected_components_diff=lambda session: f"""
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
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -3,17 +3,17 @@
                     1001 group (mixers[1]:tracks)
                         1007 group (tracks[2]:group)
                             1014 supriya:fb-patch-cable:2x2 (tracks[2]:feedback)
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 20.0
                             1008 group (tracks[2]:tracks)
                             1011 supriya:meters:2 (tracks[2]:input-levels)
                                 in_: 20.0, out: 7.0
                             1009 group (tracks[2]:devices)
                             1010 supriya:channel-strip:2 (tracks[2]:channel-strip)
            -                    active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 20.0
            +                    active: c5, done_action: 14.0, gain: c6, gate: 0.0, out: 20.0
                             1012 supriya:meters:2 (tracks[2]:output-levels)
                                 in_: 20.0, out: 9.0
                             1013 supriya:patch-cable:2x2 (tracks[2]:output)
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 16.0
                         1015 group (tracks[3]:group)
                             1016 group (tracks[3]:tracks)
                             1019 supriya:meters:2 (tracks[3]:input-levels)
            @@ -24,7 +24,7 @@
                             1020 supriya:meters:2 (tracks[3]:output-levels)
                                 in_: 22.0, out: 15.0
                             1021 supriya:patch-cable:2x2 (tracks[3]:output)
            -                    active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 18.0
            +                    active: c11, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 22.0, out: 18.0
                     1004 supriya:meters:2 (mixers[1]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (mixers[1]:devices)
            """,
            expected_messages="""
            - [None, [['/n_set', 1007, 'gate', 0.0], ['/n_set', 1010, 'done_action', 14.0], ['/n_set', 1014, 'gate', 0.0]]]
            - ['/n_set', 1021, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        Scenario(
            id="out-of-tree track input",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0]", "add_track", {"name": "Other"}),
                ("mixers[0].tracks[1]", "set_input", {"input_": "mixers[0].tracks[0]"}),
            ],
            subject="mixers[0].tracks[0]",
            expected_components_diff=lambda session: f"""
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
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -7,14 +7,14 @@
                                 in_: 18.0, out: 7.0
                             1009 group (tracks[2]:devices)
                             1010 supriya:channel-strip:2 (tracks[2]:channel-strip)
            -                    active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
            +                    active: c5, done_action: 14.0, gain: c6, gate: 0.0, out: 18.0
                             1012 supriya:meters:2 (tracks[2]:output-levels)
                                 in_: 18.0, out: 9.0
                             1013 supriya:patch-cable:2x2 (tracks[2]:output)
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 16.0
                         1014 group (tracks[3]:group)
                             1020 supriya:patch-cable:2x2 (tracks[3]:input)
            -                    active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            +                    active: c11, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 20.0
                             1015 group (tracks[3]:tracks)
                             1018 supriya:meters:2 (tracks[3]:input-levels)
                                 in_: 20.0, out: 13.0
            """,
            expected_messages="""
            - [None, [['/n_set', 1007, 'gate', 0.0], ['/n_set', 1010, 'done_action', 14.0]]]
            - ['/n_set', 1020, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
    ],
    ids=lambda scenario: scenario.id,
)
@pytest.mark.asyncio
async def test_Track_delete(
    scenario: Scenario,
    online: bool,
) -> None:
    async with scenario.run(annotation_style="numeric", online=online) as session:
        subject = session[scenario.subject]
        assert isinstance(subject, Track)
        parent = subject.parent
        await subject.delete()
    assert parent
    assert subject not in parent.tracks
    assert subject.address == "tracks[?]"
    assert subject.context is None
    assert subject.parent is None
    assert subject.mixer is None
    assert subject.session is None


@dataclasses.dataclass(frozen=True)
class GainScenario(Scenario):
    gain: float


@pytest.mark.parametrize(
    "scenario",
    [
        GainScenario(
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
                (
                    "mixers[0].tracks[0]",
                    "add_device",
                    {
                        "name": "Device",
                        "synth_configs": [
                            SynthConfig(synthdef=system.build_dc_synthdef)
                        ],
                    },
                ),
            ],
            subject="mixers[0].tracks[0]",
            gain=-6,
            expected_levels=[
                ("Mixer", [0.5, 0.5], [0.5, 0.5]),
                ("Self", [0.0, 0.0], [0.5, 0.5]),
                ("Device", [0.0, 0.0], [1.0, 1.0]),
            ],
        ),
        GainScenario(
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Child Track"}),
                (
                    "mixers[0].tracks[0].tracks[0]",
                    "add_device",
                    {
                        "name": "Device",
                        "synth_configs": [
                            SynthConfig(synthdef=system.build_dc_synthdef)
                        ],
                    },
                ),
            ],
            subject="mixers[0].tracks[0]",
            gain=-6,
            expected_levels=[
                ("Mixer", [0.5, 0.5], [0.5, 0.5]),
                ("Self", [1.0, 1.0], [0.5, 0.5]),
                ("Child Track", [0.0, 0.0], [1.0, 1.0]),
                ("Device", [0.0, 0.0], [1.0, 1.0]),
            ],
        ),
        GainScenario(
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Child Track"}),
                (
                    "mixers[0].tracks[0].tracks[0]",
                    "add_device",
                    {
                        "name": "Device",
                        "synth_configs": [
                            SynthConfig(synthdef=system.build_dc_synthdef)
                        ],
                    },
                ),
                ("mixers[0].tracks[0]", "set_parameter", {"name": "gain", "value": -6}),
            ],
            subject="mixers[0].tracks[0].tracks[0]",
            gain=-6,
            expected_levels=[
                ("Mixer", [0.25, 0.25], [0.25, 0.25]),
                ("Self", [0.5, 0.5], [0.25, 0.25]),
                ("Child Track", [0.0, 0.0], [0.5, 0.5]),
                ("Device", [0.0, 0.0], [1.0, 1.0]),
            ],
        ),
    ],
)
@pytest.mark.asyncio
async def test_Track_gain(
    scenario: GainScenario,
) -> None:
    async with scenario.run(online=True) as session:
        subject = session[scenario.subject]
        assert isinstance(subject, Track)
        subject.parameters["gain"].set(scenario.gain)


@dataclasses.dataclass(frozen=True)
class MoveScenario(Scenario):
    expected_graph_order: Sequence[int]
    index: int
    parent: str


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "scenario",
    [
        MoveScenario(
            id="move to other mixer",
            commands=[
                (None, "add_mixer", {"name": "Mixer One"}),
                (None, "add_mixer", {"name": "Mixer Two"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
            ],
            subject="mixers[0].tracks[0]",
            parent="mixers[1]",
            index=0,
            expected_exception=RuntimeError,
            expected_graph_order=(0, 0),
            expected_components_diff="",
            expected_tree_diff="",
            expected_messages="",
        ),
        MoveScenario(
            id="move under child",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Child"}),
            ],
            subject="mixers[0].tracks[0]",
            parent="mixers[0].tracks[0].tracks[0]",
            index=0,
            expected_exception=RuntimeError,
            expected_graph_order=(0, 0),
            expected_components_diff="",
            expected_tree_diff="",
            expected_messages="",
        ),
        MoveScenario(
            id="move to same parent, index too low",
            commands=[
                (None, "add_mixer", {"name": "Mixer One"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
            ],
            subject="mixers[0].tracks[0]",
            parent="mixers[0]",
            index=-1,
            expected_exception=RuntimeError,
            expected_graph_order=(0, 0),
            expected_components_diff="",
            expected_tree_diff="",
            expected_messages="",
        ),
        MoveScenario(
            id="move to same parent, index too high",
            commands=[
                (None, "add_mixer", {"name": "Mixer One"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
            ],
            subject="mixers[0].tracks[0]",
            parent="mixers[0]",
            index=2,
            expected_exception=RuntimeError,
            expected_graph_order=(0, 0),
            expected_components_diff="",
            expected_tree_diff="",
            expected_messages="",
        ),
        MoveScenario(
            id="move to same parent, same index",
            commands=[
                (None, "add_mixer", {"name": "Mixer One"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
            ],
            subject="mixers[0].tracks[0]",
            parent="mixers[0]",
            index=0,
            expected_graph_order=(0, 0),
            expected_components_diff="",
            expected_tree_diff="",
            expected_messages="",
        ),
        MoveScenario(
            id="move after younger sibling",
            commands=[
                (None, "add_mixer", {"name": "Mixer One"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0]", "add_track", {"name": "Younger Sibling"}),
            ],
            subject="mixers[0].tracks[0]",
            parent="mixers[0]",
            index=1,
            expected_graph_order=(0, 1),
            expected_components_diff=lambda session: f"""
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
            expected_tree_diff="""
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
            expected_messages="""
            - ['/n_after', 1007, 1014]
            """,
        ),
        MoveScenario(
            id="move before older sibling",
            commands=[
                (None, "add_mixer", {"name": "Mixer One"}),
                ("mixers[0]", "add_track", {"name": "Eldest Sibling"}),
                ("mixers[0]", "add_track", {"name": "Older Sibling"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
            ],
            subject="mixers[0].tracks[2]",
            parent="mixers[0]",
            index=0,
            expected_graph_order=(0, 0),
            expected_components_diff=lambda session: f"""
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
            expected_tree_diff="""
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
            expected_messages="""
            - ['/g_head', 1001, 1021]
            """,
        ),
        MoveScenario(
            id="move under sibling",
            commands=[
                (None, "add_mixer", {"name": "Mixer One"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0]", "add_track", {"name": "Younger Sibling"}),
            ],
            subject="mixers[0].tracks[0]",
            parent="mixers[0].tracks[1]",
            index=0,
            expected_graph_order=(0, 0, 0),
            expected_components_diff=lambda session: f"""
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
            expected_tree_diff="""
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
            +                        1013 supriya:patch-cable:2x2 (tracks[2]:output)
            +                            active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 16.0
            +                        1021 supriya:patch-cable:2x2 (tracks[2]:output)
            +                            active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
                             1018 supriya:meters:2 (tracks[3]:input-levels)
                                 in_: 20.0, out: 13.0
                             1016 group (tracks[3]:devices)
            """,
            expected_messages="""
            - ['/s_new', 'supriya:patch-cable:2x2', 1021, 1, 1007, 'active', 'c5', 'in_', 18.0, 'out', 20.0]
            - ['/g_head', 1015, 1007]
            - ['/g_head', 1001, 1014]
            - ['/n_set', 1013, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        MoveScenario(
            id="move after younger sibling, with send in self",
            commands=[
                (None, "add_mixer", {"name": "Mixer One"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0]", "add_track", {"name": "Younger Sibling"}),
                ("mixers[0].tracks[0]", "add_send", {"target": "mixers[0].tracks[1]"}),
            ],
            subject="mixers[0].tracks[0]",
            parent="mixers[0]",
            index=1,
            expected_graph_order=(0, 1),
            expected_components_diff=lambda session: f"""
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
            expected_tree_diff="""
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
            +                1014 supriya:patch-cable:2x2 (sends[4]:synth)
            +                    active: c5, done_action: 2.0, gain: c11, gate: 0.0, in_: 18.0, out: 20.0
            +                1012 supriya:meters:2 (tracks[2]:output-levels)
            +                    in_: 18.0, out: 9.0
            +                1013 supriya:patch-cable:2x2 (tracks[2]:output)
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
                     1004 supriya:meters:2 (mixers[1]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (mixers[1]:devices)
            """,
            expected_messages="""
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 3]
            - ['/s_new', 'supriya:patch-cable:2x2', 1022, 3, 1010, 'active', 'c5', 'gain', 'c11', 'in_', 18.0, 'out', 22.0]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1023, 0, 1015, 'active', 'c12', 'in_', 22.0, 'out', 20.0]
            - ['/n_after', 1007, 1015]
            - ['/g_head', 1001, 1015]
            - ['/n_set', 1014, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        MoveScenario(
            id="move before older sibling, with send in self",
            commands=[
                (None, "add_mixer", {"name": "Mixer One"}),
                ("mixers[0]", "add_track", {"name": "Older Sibling"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0].tracks[1]", "add_send", {"target": "mixers[0].tracks[0]"}),
            ],
            subject="mixers[0].tracks[1]",
            parent="mixers[0]",
            index=0,
            expected_graph_order=(0, 0),
            expected_components_diff=lambda session: f"""
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
            expected_tree_diff="""
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
            +                1022 supriya:patch-cable:2x2 (sends[4]:synth)
            +                    active: c11, done_action: 2.0, gain: c17, gate: 0.0, in_: 22.0, out: 18.0
            +                1020 supriya:meters:2 (tracks[3]:output-levels)
            +                    in_: 22.0, out: 15.0
            +                1021 supriya:patch-cable:2x2 (tracks[3]:output)
            +                    active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 16.0
                         1007 group (tracks[2]:group)
                             1014 supriya:fb-patch-cable:2x2 (tracks[2]:feedback)
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
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
            expected_messages="""
            - ['/s_new', 'supriya:patch-cable:2x2', 1023, 3, 1018, 'active', 'c11', 'gain', 'c17', 'in_', 22.0, 'out', 20.0]
            - ['/g_head', 1001, 1015]
            - ['/n_after', 1007, 1015]
            - ['/n_set', 1022, 'done_action', 2.0, 'gate', 0.0]
            - ['/n_set', 1014, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        MoveScenario(
            id="move after younger sibling, with send in sibling",
            commands=[
                (None, "add_mixer", {"name": "Mixer One"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0]", "add_track", {"name": "Younger Sibling"}),
                ("mixers[0].tracks[1]", "add_send", {"target": "mixers[0].tracks[0]"}),
            ],
            subject="mixers[0].tracks[0]",
            parent="mixers[0]",
            index=1,
            expected_graph_order=(0, 1),
            expected_components_diff=lambda session: f"""
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
            expected_tree_diff="""
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
            +                1022 supriya:patch-cable:2x2 (sends[4]:synth)
            +                    active: c11, done_action: 2.0, gain: c17, gate: 0.0, in_: 22.0, out: 18.0
            +                1020 supriya:meters:2 (tracks[3]:output-levels)
            +                    in_: 22.0, out: 15.0
            +                1021 supriya:patch-cable:2x2 (tracks[3]:output)
            +                    active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 16.0
                         1007 group (tracks[2]:group)
                             1014 supriya:fb-patch-cable:2x2 (tracks[2]:feedback)
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
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
            expected_messages="""
            - ['/s_new', 'supriya:patch-cable:2x2', 1023, 3, 1018, 'active', 'c11', 'gain', 'c17', 'in_', 22.0, 'out', 20.0]
            - ['/n_after', 1007, 1015]
            - ['/n_set', 1014, 'done_action', 2.0, 'gate', 0.0]
            - ['/n_set', 1022, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        MoveScenario(
            id="move before older sibling, with send in sibling",
            commands=[
                (None, "add_mixer", {"name": "Mixer One"}),
                ("mixers[0]", "add_track", {"name": "Older Sibling"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0].tracks[0]", "add_send", {"target": "mixers[0].tracks[1]"}),
            ],
            subject="mixers[0].tracks[1]",
            parent="mixers[0]",
            index=0,
            expected_graph_order=(0, 0),
            expected_components_diff=lambda session: f"""
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
            expected_tree_diff="""
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
            +                1014 supriya:patch-cable:2x2 (sends[4]:synth)
            +                    active: c5, done_action: 2.0, gain: c11, gate: 0.0, in_: 18.0, out: 20.0
            +                1012 supriya:meters:2 (tracks[2]:output-levels)
            +                    in_: 18.0, out: 9.0
            +                1013 supriya:patch-cable:2x2 (tracks[2]:output)
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
                     1004 supriya:meters:2 (mixers[1]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (mixers[1]:devices)
            """,
            expected_messages="""
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 3]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1022, 0, 1015, 'active', 'c12', 'in_', 22.0, 'out', 20.0]
            - ['/s_new', 'supriya:patch-cable:2x2', 1023, 3, 1010, 'active', 'c5', 'gain', 'c11', 'in_', 18.0, 'out', 22.0]
            - ['/g_head', 1001, 1015]
            - ['/n_set', 1014, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
    ],
    ids=lambda scenario: scenario.id,
)
@pytest.mark.asyncio
async def test_Track_move(
    scenario: MoveScenario,
    online: bool,
) -> None:
    async with scenario.run(annotation_style="numeric", online=online) as session:
        subject = session[scenario.subject]
        parent = session[scenario.parent]
        old_parent = subject.parent
        assert isinstance(old_parent, TrackContainer)
        assert isinstance(parent, TrackContainer)
        assert isinstance(subject, Track)
        await subject.move(index=scenario.index, parent=parent)
    assert subject.graph_order == scenario.expected_graph_order
    if scenario.expected_exception:
        return
    assert subject.parent is parent
    assert subject in parent.tracks
    if parent is not old_parent:
        assert subject not in old_parent.tracks


@dataclasses.dataclass(frozen=True)
class SetChannelCountScenario(Scenario):
    channel_count: ChannelCount | Inherit


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "scenario",
    [
        SetChannelCountScenario(
            id="track -> 2",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
            ],
            subject="mixers[0].tracks[0]",
            channel_count=2,
            expected_tree_diff="",
            expected_messages="",
        ),
        SetChannelCountScenario(
            id="track -> 4",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
            ],
            subject="mixers[0].tracks[0]",
            channel_count=4,
            expected_tree_diff="""
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
                             1010 supriya:channel-strip:2 (session.mixers[0].tracks[0]:channel-strip)
            -                    active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
            -                1012 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
            -                    in_: 18.0, out: 9.0
            +                    active: c5, done_action: 2.0, gain: c6, gate: 0.0, out: 18.0
                             1013 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:output)
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
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
            expected_messages="""
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
        SetChannelCountScenario(
            id="track -> 4, child -> 4",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Child"}),
            ],
            subject="mixers[0].tracks[0]",
            channel_count=4,
            expected_tree_diff="""
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
                                     1017 supriya:channel-strip:2 (session.mixers[0].tracks[0].tracks[0]:channel-strip)
            -                            active: c11, done_action: 2.0, gain: c12, gate: 1.0, out: 20.0
            -                        1019 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:output-levels)
            -                            in_: 20.0, out: 15.0
            +                            active: c11, done_action: 2.0, gain: c12, gate: 0.0, out: 20.0
                                     1020 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0]:output)
            -                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 18.0
            -                1011 supriya:meters:2 (session.mixers[0].tracks[0]:input-levels)
            -                    in_: 18.0, out: 7.0
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
                             1010 supriya:channel-strip:2 (session.mixers[0].tracks[0]:channel-strip)
            -                    active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
            -                1012 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
            -                    in_: 18.0, out: 9.0
            +                    active: c5, done_action: 2.0, gain: c6, gate: 0.0, out: 18.0
                             1013 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:output)
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
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
            expected_messages="""
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
        SetChannelCountScenario(
            id="track:2, child:2, track -> 4, child -> 2",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Child"}),
                (
                    "mixers[0].tracks[0].tracks[0]",
                    "set_channel_count",
                    {"channel_count": 2},
                ),
            ],
            subject="mixers[0].tracks[0]",
            channel_count=4,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -13,16 +13,22 @@
                                     1019 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:output-levels)
                                         in_: 20.0, out: 15.0
                                     1020 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0]:output)
            -                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 18.0
            -                1011 supriya:meters:2 (session.mixers[0].tracks[0]:input-levels)
            -                    in_: 18.0, out: 7.0
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 18.0
            +                        1025 supriya:patch-cable:2x4 (session.mixers[0].tracks[0].tracks[0]:output)
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 22.0
            +                1022 supriya:meters:4 (session.mixers[0].tracks[0]:input-levels)
            +                    in_: 22.0, out: 17.0
                             1009 group (session.mixers[0].tracks[0]:devices)
                             1010 supriya:channel-strip:2 (session.mixers[0].tracks[0]:channel-strip)
            -                    active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
            -                1012 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
            -                    in_: 18.0, out: 9.0
            +                    active: c5, done_action: 2.0, gain: c6, gate: 0.0, out: 18.0
                             1013 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:output)
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
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
            expected_messages="""
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
    ids=lambda scenario: scenario.id,
)
@pytest.mark.asyncio
async def test_Track_set_channel_count(
    scenario: SetChannelCountScenario,
    online: bool,
) -> None:
    async with scenario.run(online=online) as session:
        subject = session[scenario.subject]
        assert isinstance(subject, Track)
        await subject.set_channel_count(channel_count=scenario.channel_count)
    assert subject.channel_count == scenario.channel_count


@dataclasses.dataclass(frozen=True)
class SetInputScenario(Scenario):
    source: str | None


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "scenario",
    [
        SetInputScenario(
            id="input from other mixer",
            commands=[
                (None, "add_mixer", None),
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", None),
                ("mixers[1]", "add_track", None),
            ],
            subject="mixers[0].tracks[0]",
            source="mixers[1].tracks[0]",
            expected_exception=RuntimeError,
            expected_components_diff="",
            expected_tree_diff="",
            expected_messages="",
        ),
        SetInputScenario(
            id="input from self",
            commands=[
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Self"}),
            ],
            subject="mixers[0].tracks[0]",
            source="mixers[0].tracks[0]",
            expected_exception=RuntimeError,
            expected_components_diff="",
            expected_tree_diff="",
            expected_messages="",
        ),
        SetInputScenario(
            id="input is none",
            commands=[
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Self"}),
            ],
            subject="mixers[0].tracks[0]",
            source=None,
            expected_components_diff="",
            expected_tree_diff="",
            expected_messages="",
        ),
        SetInputScenario(
            id="input from younger sibling",
            commands=[
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0]", "add_track", {"name": "Younger Sibling"}),
            ],
            subject="mixers[0].tracks[0]",
            source="mixers[0].tracks[1]",
            expected_components_diff=lambda session: f"""
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
            expected_tree_diff="""
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
            expected_messages="""
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 3]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1021, 0, 1007, 'active', 'c5', 'in_', 20.0, 'out', 18.0]
            """,
        ),
        SetInputScenario(
            id="input from older sibing",
            commands=[
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Older Sibling"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
            ],
            subject="mixers[0].tracks[1]",
            source="mixers[0].tracks[0]",
            expected_components_diff="""
            --- initial
            +++ mutation
            @@ -2,4 +2,4 @@
                 <session.contexts[0]>
                     <Mixer 1>
                         <Track 2 'Older Sibling'>
            -            <Track 3 'Self'>
            +            <Track 3 'Self' input=<Track 2 'Older Sibling'>>
            """,
            expected_tree_diff="""
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
            expected_messages="""
            - ['/s_new', 'supriya:patch-cable:2x2', 1021, 0, 1014, 'active', 'c11', 'in_', 18.0, 'out', 20.0]
            """,
        ),
        SetInputScenario(
            id="input from child",
            commands=[
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Child"}),
            ],
            subject="mixers[0].tracks[0]",
            source="mixers[0].tracks[0].tracks[0]",
            expected_components_diff=lambda session: f"""
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
            expected_tree_diff="""
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
            expected_messages="""
            - ['/s_new', 'supriya:patch-cable:2x2', 1021, 0, 1007, 'active', 'c5', 'in_', 20.0, 'out', 18.0]
            """,
        ),
        SetInputScenario(
            id="input from parent",
            commands=[
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Parent"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Self"}),
            ],
            subject="mixers[0].tracks[0].tracks[0]",
            source="mixers[0].tracks[0]",
            expected_components_diff="""
            --- initial
            +++ mutation
            @@ -2,4 +2,4 @@
                 <session.contexts[0]>
                     <Mixer 1>
                         <Track 2 'Parent'>
            -                <Track 3 'Self'>
            +                <Track 3 'Self' input=<Track 2 'Parent'>>
            """,
            expected_tree_diff="""
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
            expected_messages="""
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 3]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1021, 0, 1014, 'active', 'c11', 'in_', 18.0, 'out', 20.0]
            """,
        ),
        SetInputScenario(
            id="input from grandparent",
            commands=[
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Grandparent"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Parent"}),
                ("mixers[0].tracks[0].tracks[0]", "add_track", {"name": "Self"}),
            ],
            subject="mixers[0].tracks[0].tracks[0].tracks[0]",
            source="mixers[0].tracks[0]",
            expected_components_diff="""
            --- initial
            +++ mutation
            @@ -3,4 +3,4 @@
                     <Mixer 1>
                         <Track 2 'Grandparent'>
                             <Track 3 'Parent'>
            -                    <Track 4 'Self'>
            +                    <Track 4 'Self' input=<Track 2 'Grandparent'>>
            """,
            expected_tree_diff="""
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
            expected_messages="""
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 3]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1028, 0, 1021, 'active', 'c17', 'in_', 18.0, 'out', 22.0]
            """,
        ),
        SetInputScenario(
            id="input from grandchild",
            commands=[
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Child"}),
                ("mixers[0].tracks[0].tracks[0]", "add_track", {"name": "Grandchild"}),
            ],
            subject="mixers[0].tracks[0]",
            source="mixers[0].tracks[0].tracks[0].tracks[0]",
            expected_components_diff=lambda session: f"""
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
            expected_tree_diff="""
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
            expected_messages="""
            - ['/s_new', 'supriya:patch-cable:2x2', 1028, 0, 1007, 'active', 'c5', 'in_', 22.0, 'out', 18.0]
            """,
        ),
        SetInputScenario(
            id="input from older auntie",
            commands=[
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Older Auntie"}),
                ("mixers[0]", "add_track", {"name": "Parent"}),
                ("mixers[0].tracks[1]", "add_track", {"name": "Self"}),
            ],
            subject="mixers[0].tracks[1].tracks[0]",
            source="mixers[0].tracks[0]",
            expected_components_diff="""
            --- initial
            +++ mutation
            @@ -3,4 +3,4 @@
                     <Mixer 1>
                         <Track 2 'Older Auntie'>
                         <Track 3 'Parent'>
            -                <Track 4 'Self'>
            +                <Track 4 'Self' input=<Track 2 'Older Auntie'>>
            """,
            expected_tree_diff="""
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
            expected_messages="""
            - ['/s_new', 'supriya:patch-cable:2x2', 1028, 0, 1021, 'active', 'c17', 'in_', 18.0, 'out', 22.0]
            """,
        ),
        SetInputScenario(
            id="input from younger auntie",
            commands=[
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Parent"}),
                ("mixers[0]", "add_track", {"name": "Younger Auntie"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Self"}),
            ],
            subject="mixers[0].tracks[0].tracks[0]",
            source="mixers[0].tracks[1]",
            expected_components_diff="""
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
            expected_tree_diff="""
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
            expected_messages="""
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 3]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1028, 0, 1014, 'active', 'c11', 'in_', 22.0, 'out', 20.0]
            """,
        ),
        SetInputScenario(
            id="input from older cousin",
            commands=[
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Older Auntie"}),
                ("mixers[0]", "add_track", {"name": "Parent"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Older Cousin"}),
                ("mixers[0].tracks[1]", "add_track", {"name": "Self"}),
            ],
            subject="mixers[0].tracks[1].tracks[0]",
            source="mixers[0].tracks[0].tracks[0]",
            expected_components_diff="""
            --- initial
            +++ mutation
            @@ -4,4 +4,4 @@
                         <Track 2 'Older Auntie'>
                             <Track 4 'Older Cousin'>
                         <Track 3 'Parent'>
            -                <Track 5 'Self'>
            +                <Track 5 'Self' input=<Track 4 'Older Cousin'>>
            """,
            expected_tree_diff="""
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
            expected_messages="""
            - ['/s_new', 'supriya:patch-cable:2x2', 1035, 0, 1028, 'active', 'c23', 'in_', 20.0, 'out', 24.0]
            """,
        ),
        SetInputScenario(
            id="input from younger cousin",
            commands=[
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Parent"}),
                ("mixers[0]", "add_track", {"name": "Younger Auntie"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Self"}),
                ("mixers[0].tracks[1]", "add_track", {"name": "Younger Cousin"}),
            ],
            subject="mixers[0].tracks[0].tracks[0]",
            source="mixers[0].tracks[1].tracks[0]",
            expected_components_diff="""
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
            expected_tree_diff="""
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
            expected_messages="""
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 3]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1035, 0, 1014, 'active', 'c11', 'in_', 24.0, 'out', 20.0]
            """,
        ),
    ],
    ids=lambda scenario: scenario.id,
)
@pytest.mark.asyncio
async def test_Track_set_input(
    scenario: SetInputScenario,
    online: bool,
) -> None:
    async with scenario.run(online=online) as session:
        subject = session[scenario.subject]
        source: BusGroup | Track | None = None
        assert isinstance(subject, Track)
        if isinstance(scenario.source, str):
            source_component = session[scenario.source]
            assert isinstance(source_component, Track)
            source = source_component
        await subject.set_input(source)


SET_MUTED_COMMANDS: list[tuple[str | None, str, dict | None]] = [
    (None, "add_mixer", {"name": "Mixer"}),
    ("mixers[0]", "add_track", {"name": "A"}),
    ("mixers[0].tracks[0]", "add_track", {"name": "AA"}),
    ("mixers[0].tracks[0]", "add_track", {"name": "AB"}),
    ("mixers[0].tracks[0]", "add_track", {"name": "AC"}),
    ("mixers[0].tracks[0].tracks[0]", "add_track", {"name": "AAA"}),
    ("mixers[0]", "add_track", {"name": "B"}),
]


@dataclasses.dataclass(frozen=True)
class SetMutedScenario(Scenario):
    actions: list[tuple[str | None, str, dict | None]]
    expected_state: list[tuple[str, bool, bool, bool]]


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "scenario",
    [
        SetMutedScenario(
            commands=SET_MUTED_COMMANDS,
            actions=[("mixers[0].tracks[0]", "set_muted", {"muted": True})],
            expected_state=[
                ("A", False, True, False),
                ("AA", True, False, False),
                ("AAA", True, False, False),
                ("AB", True, False, False),
                ("AC", True, False, False),
                ("B", True, False, False),
            ],
            expected_messages="""
            - ['/c_set', 5, 0.0]
            """,
        ),
        SetMutedScenario(
            commands=SET_MUTED_COMMANDS,
            actions=[("mixers[0].tracks[0].tracks[0]", "set_muted", {"muted": True})],
            expected_state=[
                ("A", True, False, False),
                ("AA", False, True, False),
                ("AAA", True, False, False),
                ("AB", True, False, False),
                ("AC", True, False, False),
                ("B", True, False, False),
            ],
            expected_messages="""
            - ['/c_set', 11, 0.0]
            """,
        ),
        SetMutedScenario(
            commands=SET_MUTED_COMMANDS
            + [
                ("mixers[0].tracks[0]", "set_soloed", {"soloed": True}),
            ],
            actions=[
                ("mixers[0].tracks[0]", "set_muted", {"muted": True}),
            ],
            expected_state=[
                ("A", False, True, True),
                ("AA", True, False, False),
                ("AAA", True, False, False),
                ("AB", True, False, False),
                ("AC", True, False, False),
                ("B", False, False, False),
            ],
            expected_messages="""
            - ['/c_set', 5, 0.0]
            """,
        ),
        SetMutedScenario(
            commands=SET_MUTED_COMMANDS
            + [
                ("mixers[0].tracks[1]", "set_soloed", {"soloed": True}),
            ],
            actions=[
                ("mixers[0].tracks[1]", "set_muted", {"muted": True}),
            ],
            expected_state=[
                ("A", False, False, False),
                ("AA", False, False, False),
                ("AAA", False, False, False),
                ("AB", False, False, False),
                ("AC", False, False, False),
                ("B", False, True, True),
            ],
            expected_messages="""
            - ['/c_set', 35, 0.0]
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_Track_set_muted(
    scenario: SetMutedScenario,
    online: bool,
) -> None:
    async with scenario.run(online=online) as session:
        await apply_commands(session, scenario.actions)
    assert [
        (
            track.name,
            track.is_active,
            track.is_muted,
            track.is_soloed,
        )
        for track in session.walk(Track)
    ] == scenario.expected_state


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


@dataclasses.dataclass(frozen=True)
class SetOutputScenario(Scenario):
    target: Inherit | str | None


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "scenario",
    [
        SetOutputScenario(
            id="output to the mixer",
            commands=[
                (None, "add_mixer", None),
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", None),
                ("mixers[1]", "add_track", None),
            ],
            subject="mixers[0].tracks[0]",
            target="mixers[1].tracks[0]",
            expected_exception=RuntimeError,
            expected_components_diff="",
            expected_tree_diff="",
            expected_messages="",
        ),
        SetOutputScenario(
            id="output to self",
            commands=[
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Self"}),
            ],
            subject="mixers[0].tracks[0]",
            target="mixers[0].tracks[0]",
            expected_exception=RuntimeError,
            expected_components_diff="",
            expected_tree_diff="",
            expected_messages="",
        ),
        SetOutputScenario(
            id="output is none",
            commands=[
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Self"}),
            ],
            subject="mixers[0].tracks[0]",
            target=None,
            expected_components_diff=lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,4 +1,4 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1>
            -            <Track 2 'Self'>
            +            <Track 2 'Self' output=None>
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -11,7 +11,7 @@
                             1012 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
                                 in_: 18.0, out: 9.0
                             1013 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:output)
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 16.0
                     1004 supriya:meters:2 (session.mixers[0]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (session.mixers[0]:devices)
            """,
            expected_messages="""
            - ['/n_set', 1013, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        SetOutputScenario(
            id="output to younger sibling",
            commands=[
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0]", "add_track", {"name": "Younger Sibling"}),
            ],
            subject="mixers[0].tracks[0]",
            target="mixers[0].tracks[1]",
            expected_components_diff=lambda session: f"""
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
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -11,7 +11,9 @@
                             1012 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
                                 in_: 18.0, out: 9.0
                             1013 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:output)
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 16.0
            +                1021 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:output)
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
                         1014 group (session.mixers[0].tracks[1]:group)
                             1015 group (session.mixers[0].tracks[1]:tracks)
                             1018 supriya:meters:2 (session.mixers[0].tracks[1]:input-levels)
            """,
            expected_messages="""
            - ['/s_new', 'supriya:patch-cable:2x2', 1021, 1, 1007, 'active', 'c5', 'in_', 18.0, 'out', 20.0]
            - ['/n_set', 1013, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        SetOutputScenario(
            id="output to older sibling",
            commands=[
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Older Sibling"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
            ],
            subject="mixers[0].tracks[1]",
            target="mixers[0].tracks[0]",
            expected_components_diff="""
            --- initial
            +++ mutation
            @@ -2,4 +2,4 @@
                 <session.contexts[0]>
                     <Mixer 1>
                         <Track 2 'Older Sibling'>
            -            <Track 3 'Self'>
            +            <Track 3 'Self' output=<Track 2 'Older Sibling'>>
            """,
            expected_tree_diff="""
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
            @@ -22,7 +24,9 @@
                             1019 supriya:meters:2 (session.mixers[0].tracks[1]:output-levels)
                                 in_: 20.0, out: 15.0
                             1020 supriya:patch-cable:2x2 (session.mixers[0].tracks[1]:output)
            -                    active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
            +                    active: c11, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 16.0
            +                1021 supriya:patch-cable:2x2 (session.mixers[0].tracks[1]:output)
            +                    active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 22.0
                     1004 supriya:meters:2 (session.mixers[0]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (session.mixers[0]:devices)
            """,
            expected_messages="""
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 3]
            - ['/s_new', 'supriya:patch-cable:2x2', 1021, 1, 1014, 'active', 'c11', 'in_', 20.0, 'out', 22.0]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1022, 0, 1007, 'active', 'c5', 'in_', 22.0, 'out', 18.0]
            - ['/n_set', 1020, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        SetOutputScenario(
            id="output to child",
            commands=[
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Child"}),
            ],
            subject="mixers[0].tracks[0]",
            target="mixers[0].tracks[0].tracks[0]",
            expected_components_diff=lambda session: f"""
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
            expected_tree_diff="""
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
            @@ -22,7 +24,9 @@
                             1012 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
                                 in_: 18.0, out: 9.0
                             1013 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:output)
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 16.0
            +                1021 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:output)
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 22.0
                     1004 supriya:meters:2 (session.mixers[0]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (session.mixers[0]:devices)
            """,
            expected_messages="""
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 3]
            - ['/s_new', 'supriya:patch-cable:2x2', 1021, 1, 1007, 'active', 'c5', 'in_', 18.0, 'out', 22.0]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1022, 0, 1014, 'active', 'c11', 'in_', 22.0, 'out', 20.0]
            - ['/n_set', 1013, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        SetOutputScenario(
            id="output to mixer",
            commands=[
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Self"}),
            ],
            subject="mixers[0].tracks[0]",
            target="mixers[0]",
            expected_components_diff=lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,4 +1,4 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1>
            -            <Track 2 'Self'>
            +            <Track 2 'Self' output=<Mixer 1>>
            """,
            expected_tree_diff="",
            expected_messages="",
        ),
        SetOutputScenario(
            id="output to parent",
            commands=[
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Parent"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Self"}),
            ],
            subject="mixers[0].tracks[0].tracks[0]",
            target="mixers[0].tracks[0]",
            expected_components_diff="""
            --- initial
            +++ mutation
            @@ -2,4 +2,4 @@
                 <session.contexts[0]>
                     <Mixer 1>
                         <Track 2 'Parent'>
            -                <Track 3 'Self'>
            +                <Track 3 'Self' output=<Track 2 'Parent'>>
            """,
            expected_tree_diff="",
            expected_messages="",
        ),
        SetOutputScenario(
            id="output is default",
            commands=[
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Parent"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Self"}),
            ],
            subject="mixers[0].tracks[0].tracks[0]",
            target=INHERIT,
            expected_components_diff="",
            expected_tree_diff="",
            expected_messages="",
        ),
        SetOutputScenario(
            id="output to grandparent",
            commands=[
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Grandparent"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Parent"}),
                ("mixers[0].tracks[0].tracks[0]", "add_track", {"name": "Self"}),
            ],
            subject="mixers[0].tracks[0].tracks[0].tracks[0]",
            target="mixers[0].tracks[0]",
            expected_components_diff="""
            --- initial
            +++ mutation
            @@ -3,4 +3,4 @@
                     <Mixer 1>
                         <Track 2 'Grandparent'>
                             <Track 3 'Parent'>
            -                    <Track 4 'Self'>
            +                    <Track 4 'Self' output=<Track 2 'Grandparent'>>
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -15,7 +15,9 @@
                                             1026 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0].tracks[0]:output-levels)
                                                 in_: 22.0, out: 21.0
                                             1027 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].tracks[0]:output)
            -                                    active: c17, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 20.0
            +                                    active: c17, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 22.0, out: 20.0
            +                                1028 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].tracks[0]:output)
            +                                    active: c17, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 18.0
                                     1018 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:input-levels)
                                         in_: 20.0, out: 13.0
                                     1016 group (session.mixers[0].tracks[0].tracks[0]:devices)
            """,
            expected_messages="""
            - ['/s_new', 'supriya:patch-cable:2x2', 1028, 1, 1021, 'active', 'c17', 'in_', 22.0, 'out', 18.0]
            - ['/n_set', 1027, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        SetOutputScenario(
            id="output to grandchild",
            commands=[
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Child"}),
                ("mixers[0].tracks[0].tracks[0]", "add_track", {"name": "Grandchild"}),
            ],
            subject="mixers[0].tracks[0]",
            target="mixers[0].tracks[0].tracks[0].tracks[0]",
            expected_components_diff=lambda session: f"""
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
            expected_tree_diff="""
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
            @@ -33,7 +35,9 @@
                             1012 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
                                 in_: 18.0, out: 9.0
                             1013 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:output)
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 16.0
            +                1028 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:output)
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 24.0
                     1004 supriya:meters:2 (session.mixers[0]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (session.mixers[0]:devices)
            """,
            expected_messages="""
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 3]
            - ['/s_new', 'supriya:patch-cable:2x2', 1028, 1, 1007, 'active', 'c5', 'in_', 18.0, 'out', 24.0]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1029, 0, 1021, 'active', 'c17', 'in_', 24.0, 'out', 22.0]
            - ['/n_set', 1013, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        SetOutputScenario(
            id="output to older auntie",
            commands=[
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Older Auntie"}),
                ("mixers[0]", "add_track", {"name": "Parent"}),
                ("mixers[0].tracks[1]", "add_track", {"name": "Self"}),
            ],
            subject="mixers[0].tracks[1].tracks[0]",
            target="mixers[0].tracks[0]",
            expected_components_diff="""
            --- initial
            +++ mutation
            @@ -3,4 +3,4 @@
                     <Mixer 1>
                         <Track 2 'Older Auntie'>
                         <Track 3 'Parent'>
            -                <Track 4 'Self'>
            +                <Track 4 'Self' output=<Track 2 'Older Auntie'>>
            """,
            expected_tree_diff="""
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
            @@ -24,7 +26,9 @@
                                     1026 supriya:meters:2 (session.mixers[0].tracks[1].tracks[0]:output-levels)
                                         in_: 22.0, out: 21.0
                                     1027 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].tracks[0]:output)
            -                            active: c17, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 20.0
            +                            active: c17, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 22.0, out: 20.0
            +                        1028 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].tracks[0]:output)
            +                            active: c17, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 24.0
                             1018 supriya:meters:2 (session.mixers[0].tracks[1]:input-levels)
                                 in_: 20.0, out: 13.0
                             1016 group (session.mixers[0].tracks[1]:devices)
            """,
            expected_messages="""
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 3]
            - ['/s_new', 'supriya:patch-cable:2x2', 1028, 1, 1021, 'active', 'c17', 'in_', 22.0, 'out', 24.0]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1029, 0, 1007, 'active', 'c5', 'in_', 24.0, 'out', 18.0]
            - ['/n_set', 1027, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        SetOutputScenario(
            id="output to younger auntie",
            commands=[
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Parent"}),
                ("mixers[0]", "add_track", {"name": "Younger Auntie"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Self"}),
            ],
            subject="mixers[0].tracks[0].tracks[0]",
            target="mixers[0].tracks[1]",
            expected_components_diff="""
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
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -13,7 +13,9 @@
                                     1019 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:output-levels)
                                         in_: 20.0, out: 15.0
                                     1020 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0]:output)
            -                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 18.0
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 18.0
            +                        1028 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0]:output)
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 22.0
                             1011 supriya:meters:2 (session.mixers[0].tracks[0]:input-levels)
                                 in_: 18.0, out: 7.0
                             1009 group (session.mixers[0].tracks[0]:devices)
            """,
            expected_messages="""
            - ['/s_new', 'supriya:patch-cable:2x2', 1028, 1, 1014, 'active', 'c11', 'in_', 20.0, 'out', 22.0]
            - ['/n_set', 1020, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        SetOutputScenario(
            id="output to older cousin",
            commands=[
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Older Auntie"}),
                ("mixers[0]", "add_track", {"name": "Parent"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Older Cousin"}),
                ("mixers[0].tracks[1]", "add_track", {"name": "Self"}),
            ],
            subject="mixers[0].tracks[1].tracks[0]",
            target="mixers[0].tracks[0].tracks[0]",
            expected_components_diff="""
            --- initial
            +++ mutation
            @@ -4,4 +4,4 @@
                         <Track 2 'Older Auntie'>
                             <Track 4 'Older Cousin'>
                         <Track 3 'Parent'>
            -                <Track 5 'Self'>
            +                <Track 5 'Self' output=<Track 4 'Older Cousin'>>
            """,
            expected_tree_diff="""
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
            @@ -35,7 +37,9 @@
                                     1033 supriya:meters:2 (session.mixers[0].tracks[1].tracks[0]:output-levels)
                                         in_: 24.0, out: 27.0
                                     1034 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].tracks[0]:output)
            -                            active: c23, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 24.0, out: 22.0
            +                            active: c23, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 24.0, out: 22.0
            +                        1035 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].tracks[0]:output)
            +                            active: c23, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 24.0, out: 26.0
                             1025 supriya:meters:2 (session.mixers[0].tracks[1]:input-levels)
                                 in_: 22.0, out: 19.0
                             1023 group (session.mixers[0].tracks[1]:devices)
            """,
            expected_messages="""
            - ['/d_recv', <SynthDef: supriya:fb-patch-cable:2x2>]
            - ['/sync', 3]
            - ['/s_new', 'supriya:patch-cable:2x2', 1035, 1, 1028, 'active', 'c23', 'in_', 24.0, 'out', 26.0]
            - ['/s_new', 'supriya:fb-patch-cable:2x2', 1036, 0, 1014, 'active', 'c11', 'in_', 26.0, 'out', 20.0]
            - ['/n_set', 1034, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        SetOutputScenario(
            id="output to younger cousin",
            commands=[
                (None, "add_mixer", None),
                ("mixers[0]", "add_track", {"name": "Parent"}),
                ("mixers[0]", "add_track", {"name": "Younger Auntie"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Self"}),
                ("mixers[0].tracks[1]", "add_track", {"name": "Younger Cousin"}),
            ],
            subject="mixers[0].tracks[0].tracks[0]",
            target="mixers[0].tracks[1].tracks[0]",
            expected_components_diff="""
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
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -13,7 +13,9 @@
                                     1019 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:output-levels)
                                         in_: 20.0, out: 15.0
                                     1020 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0]:output)
            -                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 18.0
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 18.0
            +                        1035 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0]:output)
            +                            active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 24.0
                             1011 supriya:meters:2 (session.mixers[0].tracks[0]:input-levels)
                                 in_: 18.0, out: 7.0
                             1009 group (session.mixers[0].tracks[0]:devices)
            """,
            expected_messages="""
            - ['/s_new', 'supriya:patch-cable:2x2', 1035, 1, 1014, 'active', 'c11', 'in_', 20.0, 'out', 24.0]
            - ['/n_set', 1020, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
    ],
    ids=lambda scenario: scenario.id,
)
@pytest.mark.asyncio
async def test_Track_set_output(
    scenario: SetOutputScenario,
    online: bool,
) -> None:
    async with scenario.run(online=online) as session:
        output_from_ = session[scenario.subject]
        target: BusGroup | Inherit | TrackContainer | None = None
        assert isinstance(output_from_, Track)
        if isinstance(scenario.target, Inherit):
            target = INHERIT
        elif isinstance(scenario.target, str):
            targetcomponent = session[scenario.target]
            assert isinstance(targetcomponent, TrackContainer)
            target = targetcomponent
        await output_from_.set_output(target)


SET_SOLOED_COMMANDS: list[tuple[str | None, str, dict | None]] = [
    (None, "add_mixer", {"name": "Mixer"}),
    ("mixers[0]", "add_track", {"name": "A"}),
    ("mixers[0].tracks[0]", "add_track", {"name": "AA"}),
    ("mixers[0].tracks[0]", "add_track", {"name": "AB"}),
    ("mixers[0].tracks[0]", "add_track", {"name": "AC"}),
    ("mixers[0].tracks[0].tracks[0]", "add_track", {"name": "AAA"}),
    ("mixers[0]", "add_track", {"name": "B"}),
]


@dataclasses.dataclass(frozen=True)
class SetSoloedScenario(Scenario):
    actions: list[tuple[str | None, str, dict | None]]
    expected_state: list[tuple[str, bool, bool, bool]]


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "scenario",
    [
        SetSoloedScenario(
            commands=SET_SOLOED_COMMANDS,
            actions=[("mixers[0].tracks[0]", "set_soloed", {"soloed": True})],
            expected_state=[
                ("A", True, False, True),
                ("AA", True, False, False),
                ("AAA", True, False, False),
                ("AB", True, False, False),
                ("AC", True, False, False),
                ("B", False, False, False),
            ],
            expected_messages="""
            - ['/c_set', 35, 0.0]
            """,
        ),
        SetSoloedScenario(
            commands=SET_SOLOED_COMMANDS,
            actions=[("mixers[0].tracks[1]", "set_soloed", {"soloed": True})],
            expected_state=[
                ("A", False, False, False),
                ("AA", False, False, False),
                ("AAA", False, False, False),
                ("AB", False, False, False),
                ("AC", False, False, False),
                ("B", True, False, True),
            ],
            expected_messages="""
            - ['/c_set', 5, 0.0, 11, 0.0, 17, 0.0, 23, 0.0, 29, 0.0]
            """,
        ),
        SetSoloedScenario(
            commands=SET_SOLOED_COMMANDS,
            actions=[("mixers[0].tracks[0].tracks[0]", "set_soloed", {"soloed": True})],
            expected_state=[
                ("A", True, False, False),
                ("AA", True, False, True),
                ("AAA", True, False, False),
                ("AB", False, False, False),
                ("AC", False, False, False),
                ("B", False, False, False),
            ],
            expected_messages="""
            - ['/c_set', 23, 0.0, 29, 0.0, 35, 0.0]
            """,
        ),
        SetSoloedScenario(
            commands=SET_SOLOED_COMMANDS,
            actions=[
                (
                    "mixers[0].tracks[0].tracks[0].tracks[0]",
                    "set_soloed",
                    {"soloed": True},
                )
            ],
            expected_state=[
                ("A", True, False, False),
                ("AA", True, False, False),
                ("AAA", True, False, True),
                ("AB", False, False, False),
                ("AC", False, False, False),
                ("B", False, False, False),
            ],
            expected_messages="""
            - ['/c_set', 23, 0.0, 29, 0.0, 35, 0.0]
            """,
        ),
        SetSoloedScenario(
            commands=SET_SOLOED_COMMANDS,
            actions=[
                ("mixers[0].tracks[0]", "set_soloed", {"soloed": True}),
                ("mixers[0].tracks[1]", "set_soloed", {"soloed": True}),
            ],
            expected_state=[
                ("A", False, False, False),
                ("AA", False, False, False),
                ("AAA", False, False, False),
                ("AB", False, False, False),
                ("AC", False, False, False),
                ("B", True, False, True),
            ],
            expected_messages=""" 
            - ['/c_set', 35, 0.0]
            - ['/c_set', 5, 0.0, 11, 0.0, 17, 0.0, 23, 0.0, 29, 0.0, 35, 1.0]
            """,
        ),
        SetSoloedScenario(
            commands=SET_SOLOED_COMMANDS,
            actions=[
                ("mixers[0].tracks[0].tracks[0]", "set_soloed", {"soloed": True}),
                (
                    "mixers[0].tracks[0].tracks[1]",
                    "set_soloed",
                    {"exclusive": False, "soloed": True},
                ),
            ],
            expected_state=[
                ("A", True, False, False),
                ("AA", True, False, True),
                ("AAA", True, False, False),
                ("AB", True, False, True),
                ("AC", False, False, False),
                ("B", False, False, False),
            ],
            expected_messages="""
            - ['/c_set', 23, 0.0, 29, 0.0, 35, 0.0]
            - ['/c_set', 23, 1.0]
            """,
        ),
        SetSoloedScenario(
            commands=SET_SOLOED_COMMANDS,
            actions=[
                ("mixers[0].tracks[1]", "set_soloed", {"soloed": True}),
                ("mixers[0].tracks[1]", "delete", {}),
            ],
            expected_state=[
                ("A", True, False, False),
                ("AA", True, False, False),
                ("AAA", True, False, False),
                ("AB", True, False, False),
                ("AC", True, False, False),
            ],
            expected_messages="""
            - ['/c_set', 5, 0.0, 11, 0.0, 17, 0.0, 23, 0.0, 29, 0.0]
            - [None, [['/n_set', 1042, 'gate', 0.0], ['/n_set', 1045, 'done_action', 14.0]]]
            - ['/c_set', 5, 1.0, 11, 1.0, 17, 1.0, 23, 1.0, 29, 1.0]
            """,
        ),
        SetSoloedScenario(
            commands=SET_SOLOED_COMMANDS,
            actions=[
                ("mixers[0].tracks[0].tracks[0]", "set_soloed", {"soloed": True}),
                (
                    "mixers[0].tracks[0].tracks[0]",
                    "move",
                    {"parent": "mixers[0].tracks[1]", "index": 0},
                ),
            ],
            expected_state=[
                ("A", False, False, False),
                ("AB", False, False, False),
                ("AC", False, False, False),
                ("B", True, False, False),
                ("AA", True, False, True),
                ("AAA", True, False, False),
            ],
            expected_messages="""
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
    scenario: SetSoloedScenario,
    online: bool,
) -> None:
    async with scenario.run(online=online) as session:
        await apply_commands(session, scenario.actions)
    assert [
        (
            track.name,
            track.is_active,
            track.is_muted,
            track.is_soloed,
        )
        for track in session.walk(Track)
    ] == scenario.expected_state


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "scenario",
    [
        Scenario(
            id="track without child tracks",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
            ],
            subject="mixers[0].tracks[0]",
            expected_exception=RuntimeError,
            expected_components_diff="",
            expected_tree_diff="",
            expected_messages="",
        ),
        Scenario(
            id="track with child tracks",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Self"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Older Child"}),
                ("mixers[0].tracks[0]", "add_track", {"name": "Younger Child"}),
            ],
            subject="mixers[0].tracks[0]",
            expected_components_diff=lambda session: f"""
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
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -3,37 +3,41 @@
                     1001 group (mixers[1]:tracks)
                         1007 group (tracks[2]:group)
                             1008 group (tracks[2]:tracks)
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
                             1011 supriya:meters:2 (tracks[2]:input-levels)
                                 in_: 18.0, out: 7.0
                             1009 group (tracks[2]:devices)
                             1010 supriya:channel-strip:2 (tracks[2]:channel-strip)
            -                    active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
            +                    active: c5, done_action: 14.0, gain: c6, gate: 0.0, out: 18.0
                             1012 supriya:meters:2 (tracks[2]:output-levels)
                                 in_: 18.0, out: 9.0
                             1013 supriya:patch-cable:2x2 (tracks[2]:output)
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
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
            +                1020 supriya:patch-cable:2x2 (tracks[3]:output)
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
            +                1027 supriya:patch-cable:2x2 (tracks[4]:output)
            +                    active: c17, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 22.0, out: 18.0
            +                1029 supriya:patch-cable:2x2 (tracks[4]:output)
            +                    active: c17, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 16.0
                     1004 supriya:meters:2 (mixers[1]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (mixers[1]:devices)
            """,
            expected_messages="""
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
    scenario: Scenario,
    online: bool,
) -> None:
    async with scenario.run(annotation_style="numeric", online=online) as session:
        subject = session[scenario.subject]
        assert isinstance(subject, Track)
        await subject.ungroup()
