import dataclasses
from typing import Sequence

import pytest

from supriya.sessions import Chain, Rack, Session

from .conftest import Scenario


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "scenario",
    [
        Scenario(
            id="1/1 chains",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_rack", {"name": "Rack"}),
                ("mixers[0].devices[0].chains[0]", "set_name", {"name": "Self"}),
            ],
            subject="mixers[0].devices[0].chains[0]",
            expected_components_diff="""
            --- initial
            +++ mutation
            @@ -2,4 +2,3 @@
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
                         <Rack 2 'Rack'>
            -                <Chain 3 'Self'>
            """,
            expected_messages="""
            - ['/n_set', 1009, 'active', 0.0]
            - [None, [['/n_set', 1011, 'gate', 0.0], ['/n_set', 1015, 'done_action', 14.0]]]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -8,18 +8,18 @@
                             1008 group (devices[2]:chains)
                                 1011 group (chains[3]:group)
                                     1013 supriya:patch-cable:2x2:replace (chains[3]:input)
            -                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 18.0
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 16.0, out: 18.0
                                     1014 supriya:meters:2 (chains[3]:input-levels)
                                         in_: 18.0, out: 10.0
                                     1012 group (chains[3]:devices)
                                     1015 supriya:channel-strip:2 (chains[3]:channel-strip)
            -                            active: c8, done_action: 2.0, gain: c9, gate: 1.0, out: 18.0
            +                            active: c8, done_action: 14.0, gain: c9, gate: 0.0, out: 18.0
                                     1017 supriya:patch-cable:2x2 (chains[3]:output)
            -                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 20.0
                                     1016 supriya:meters:2 (chains[3]:output-levels)
                                         in_: 18.0, out: 12.0
                             1009 supriya:patch-cable:2x2 (devices[2]:output)
            -                    active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
            +                    active: 0.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
                             1010 supriya:meters:2 (devices[2]:output-levels)
                                 in_: 16.0, out: 6.0
                     1003 supriya:channel-strip:2 (mixers[1]:channel-strip)
            """,
        ),
        Scenario(
            id="1/2 chains",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_rack", {"name": "Rack"}),
                ("mixers[0].devices[0].chains[0]", "set_name", {"name": "Self"}),
                ("mixers[0].devices[0]", "add_chain", {"name": "Younger Sibling"}),
            ],
            subject="mixers[0].devices[0].chains[0]",
            expected_components_diff="""
            --- initial
            +++ mutation
            @@ -2,5 +2,4 @@
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
                         <Rack 2 'Rack'>
            -                <Chain 3 'Self'>
                             <Chain 4 'Younger Sibling'>
            """,
            expected_messages="""
            - [None, [['/n_set', 1011, 'gate', 0.0], ['/n_set', 1015, 'done_action', 14.0]]]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -8,14 +8,14 @@
                             1008 group (devices[2]:chains)
                                 1011 group (chains[3]:group)
                                     1013 supriya:patch-cable:2x2:replace (chains[3]:input)
            -                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 18.0
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 16.0, out: 18.0
                                     1014 supriya:meters:2 (chains[3]:input-levels)
                                         in_: 18.0, out: 10.0
                                     1012 group (chains[3]:devices)
                                     1015 supriya:channel-strip:2 (chains[3]:channel-strip)
            -                            active: c8, done_action: 2.0, gain: c9, gate: 1.0, out: 18.0
            +                            active: c8, done_action: 14.0, gain: c9, gate: 0.0, out: 18.0
                                     1017 supriya:patch-cable:2x2 (chains[3]:output)
            -                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 20.0
                                     1016 supriya:meters:2 (chains[3]:output-levels)
                                         in_: 18.0, out: 12.0
                                 1018 group (chains[4]:group)
            """,
        ),
        Scenario(
            id="2/2 chains",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_rack", {"name": "Rack"}),
                (
                    "mixers[0].devices[0].chains[0]",
                    "set_name",
                    {"name": "Older Sibling"},
                ),
                ("mixers[0].devices[0]", "add_chain", {"name": "Self"}),
            ],
            subject="mixers[0].devices[0].chains[1]",
            expected_components_diff="""
            --- initial
            +++ mutation
            @@ -3,4 +3,3 @@
                     <Mixer 1 'Mixer'>
                         <Rack 2 'Rack'>
                             <Chain 3 'Older Sibling'>
            -                <Chain 4 'Self'>
            """,
            expected_messages="""
            - [None, [['/n_set', 1018, 'gate', 0.0], ['/n_set', 1022, 'done_action', 14.0]]]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -20,14 +20,14 @@
                                         in_: 18.0, out: 12.0
                                 1018 group (chains[4]:group)
                                     1020 supriya:patch-cable:2x2:replace (chains[4]:input)
            -                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 18.0
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 16.0, out: 18.0
                                     1021 supriya:meters:2 (chains[4]:input-levels)
                                         in_: 18.0, out: 16.0
                                     1019 group (chains[4]:devices)
                                     1022 supriya:channel-strip:2 (chains[4]:channel-strip)
            -                            active: c14, done_action: 2.0, gain: c15, gate: 1.0, out: 18.0
            +                            active: c14, done_action: 14.0, gain: c15, gate: 0.0, out: 18.0
                                     1024 supriya:patch-cable:2x2 (chains[4]:output)
            -                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 20.0
                                     1023 supriya:meters:2 (chains[4]:output-levels)
                                         in_: 18.0, out: 18.0
                             1009 supriya:patch-cable:2x2 (devices[2]:output)
            """,
        ),
    ],
    ids=lambda scenario: scenario.id,
)
@pytest.mark.asyncio
async def test_Chain_delete(scenario: Scenario, online: bool) -> None:
    async with scenario.run(annotation_style="numeric", online=online) as session:
        target_ = session[scenario.subject]
        assert isinstance(target_, Chain)
        parent = target_.parent
        await target_.delete()
    assert parent
    assert target_ not in parent.chains
    assert target_.address == "chains[?]"
    assert target_.context is None
    assert target_.mixer is None
    assert target_.parent is None
    assert target_.session is None


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
            id="move to other mixer: raises",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                (None, "add_mixer", {"name": "Other Mixer"}),
                ("mixers[0]", "add_rack", {"name": "Rack"}),
                ("mixers[1]", "add_rack", {"name": "Other Rack"}),
                ("mixers[0].devices[0].chains[0]", "set_name", {"name": "Self"}),
            ],
            subject="mixers[0].devices[0].chains[0]",
            parent="mixers[1].devices[0]",
            index=0,
            expected_exception=RuntimeError,
            expected_components_diff=lambda session: "",
            expected_graph_order=(0, 0, 0),
            expected_messages="",
            expected_tree_diff="",
        ),
        MoveScenario(
            id="move to same parent, same index: no-op",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_rack", {"name": "Rack"}),
                ("mixers[0].devices[0].chains[0]", "set_name", {"name": "Self"}),
            ],
            subject="mixers[0].devices[0].chains[0]",
            parent="mixers[0].devices[0]",
            index=0,
            expected_components_diff=lambda session: "",
            expected_graph_order=(0, 0, 0),
            expected_messages="",
            expected_tree_diff="",
        ),
        MoveScenario(
            id="move to same parent, index too low",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_rack", {"name": "Rack"}),
                ("mixers[0].devices[0].chains[0]", "set_name", {"name": "Self"}),
            ],
            subject="mixers[0].devices[0].chains[0]",
            parent="mixers[0].devices[0]",
            index=-1,
            expected_exception=RuntimeError,
            expected_components_diff=lambda session: "",
            expected_graph_order=(0, 0, 0),
            expected_messages="",
            expected_tree_diff="",
        ),
        MoveScenario(
            id="move to same parent, index too high",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_rack", {"name": "Rack"}),
                ("mixers[0].devices[0].chains[0]", "set_name", {"name": "Self"}),
            ],
            subject="mixers[0].devices[0].chains[0]",
            parent="mixers[0].devices[0]",
            index=2,
            expected_exception=RuntimeError,
            expected_components_diff=lambda session: "",
            expected_graph_order=(0, 0, 0),
            expected_messages="",
            expected_tree_diff="",
        ),
        MoveScenario(
            id="move to other rack",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_rack", {"name": "Rack"}),
                ("mixers[0]", "add_rack", {"name": "Other Rack"}),
                ("mixers[0].devices[0].chains[0]", "set_name", {"name": "Self"}),
                ("mixers[0].devices[1].chains[0]", "set_name", {"name": "Cousin"}),
            ],
            subject="mixers[0].devices[0].chains[0]",
            parent="mixers[0].devices[1]",
            index=0,
            expected_components_diff=lambda session: """
            --- initial
            +++ mutation
            @@ -2,6 +2,6 @@
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
                         <Rack 2 'Rack'>
            +            <Rack 4 'Other Rack'>
                             <Chain 3 'Self'>
            -            <Rack 4 'Other Rack'>
                             <Chain 5 'Cousin'>
            """,
            expected_graph_order=(0, 1, 0),
            expected_messages="""
            - [None,
               [['/s_new', 'supriya:patch-cable:2x2:replace', 1029, 0, 1011, 'in_', 16.0, 'out', 22.0],
                ['/s_new', 'supriya:meters:2', 1030, 3, 1029, 'in_', 22.0, 'out', 10.0],
                ['/s_new', 'supriya:channel-strip:2', 1031, 3, 1012, 'active', 'c8', 'gain', 'c9', 'out', 22.0],
                ['/s_new', 'supriya:meters:2', 1032, 3, 1031, 'in_', 22.0, 'out', 12.0],
                ['/s_new', 'supriya:patch-cable:2x2', 1033, 3, 1031, 'in_', 22.0, 'out', 24.0]]]
            - ['/g_head', 1019, 1011]
            - ['/n_set', 1009, 'active', 0.0]
            - [None,
               [['/n_set', 1013, 'done_action', 2.0, 'gate', 0.0],
                ['/n_free', 1014],
                ['/n_set', 1015, 'done_action', 2.0, 'gate', 0.0],
                ['/n_free', 1016],
                ['/n_set', 1017, 'done_action', 2.0, 'gate', 0.0]]]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -6,24 +6,30 @@
                     1002 group (mixers[1]:devices)
                         1007 group (devices[2]:group)
                             1008 group (devices[2]:chains)
            -                    1011 group (chains[3]:group)
            -                        1013 supriya:patch-cable:2x2:replace (chains[3]:input)
            -                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 18.0
            -                        1014 supriya:meters:2 (chains[3]:input-levels)
            -                            in_: 18.0, out: 10.0
            -                        1012 group (chains[3]:devices)
            -                        1015 supriya:channel-strip:2 (chains[3]:channel-strip)
            -                            active: c8, done_action: 2.0, gain: c9, gate: 1.0, out: 18.0
            -                        1017 supriya:patch-cable:2x2 (chains[3]:output)
            -                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            -                        1016 supriya:meters:2 (chains[3]:output-levels)
            -                            in_: 18.0, out: 12.0
                             1009 supriya:patch-cable:2x2 (devices[2]:output)
            -                    active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
            +                    active: 0.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
                             1010 supriya:meters:2 (devices[2]:output-levels)
                                 in_: 16.0, out: 6.0
                         1018 group (devices[4]:group)
                             1019 group (devices[4]:chains)
            +                    1011 group (chains[3]:group)
            +                        1029 supriya:patch-cable:2x2:replace (chains[3]:input)
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 22.0
            +                        1030 supriya:meters:2 (chains[3]:input-levels)
            +                            in_: 22.0, out: 10.0
            +                        1013 supriya:patch-cable:2x2:replace (chains[3]:input)
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 16.0, out: 18.0
            +                        1012 group (chains[3]:devices)
            +                        1031 supriya:channel-strip:2 (chains[3]:channel-strip)
            +                            active: c8, done_action: 2.0, gain: c9, gate: 1.0, out: 22.0
            +                        1033 supriya:patch-cable:2x2 (chains[3]:output)
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 24.0
            +                        1032 supriya:meters:2 (chains[3]:output-levels)
            +                            in_: 22.0, out: 12.0
            +                        1015 supriya:channel-strip:2 (chains[3]:channel-strip)
            +                            active: c8, done_action: 2.0, gain: c9, gate: 0.0, out: 18.0
            +                        1017 supriya:patch-cable:2x2 (chains[3]:output)
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 20.0
                                 1022 group (chains[5]:group)
                                     1024 supriya:patch-cable:2x2:replace (chains[5]:input)
                                         active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 22.0
            """,
        ),
        MoveScenario(
            id="move to other rack, leaving sibling behind",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_rack", {"name": "Rack"}),
                ("mixers[0].devices[0].chains[0]", "set_name", {"name": "Self"}),
                ("mixers[0].devices[0]", "add_chain", {"name": "Sibling"}),
                ("mixers[0]", "add_rack", {"name": "Other Rack"}),
                ("mixers[0].devices[1].chains[0]", "set_name", {"name": "Cousin"}),
            ],
            subject="mixers[0].devices[0].chains[0]",
            parent="mixers[0].devices[1]",
            index=0,
            expected_components_diff=lambda session: """
            --- initial
            +++ mutation
            @@ -2,7 +2,7 @@
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
                         <Rack 2 'Rack'>
            -                <Chain 3 'Self'>
                             <Chain 4 'Sibling'>
                         <Rack 5 'Other Rack'>
            +                <Chain 3 'Self'>
                             <Chain 6 'Cousin'>
            """,
            expected_graph_order=(0, 1, 0),
            expected_messages="""
            - [None,
               [['/s_new', 'supriya:patch-cable:2x2:replace', 1036, 0, 1011, 'in_', 16.0, 'out', 22.0],
                ['/s_new', 'supriya:meters:2', 1037, 3, 1036, 'in_', 22.0, 'out', 10.0],
                ['/s_new', 'supriya:channel-strip:2', 1038, 3, 1012, 'active', 'c8', 'gain', 'c9', 'out', 22.0],
                ['/s_new', 'supriya:meters:2', 1039, 3, 1038, 'in_', 22.0, 'out', 12.0],
                ['/s_new', 'supriya:patch-cable:2x2', 1040, 3, 1038, 'in_', 22.0, 'out', 24.0]]]
            - ['/g_head', 1026, 1011]
            - [None,
               [['/n_set', 1013, 'done_action', 2.0, 'gate', 0.0],
                ['/n_free', 1014],
                ['/n_set', 1015, 'done_action', 2.0, 'gate', 0.0],
                ['/n_free', 1016],
                ['/n_set', 1017, 'done_action', 2.0, 'gate', 0.0]]]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -6,18 +6,6 @@
                     1002 group (mixers[1]:devices)
                         1007 group (devices[2]:group)
                             1008 group (devices[2]:chains)
            -                    1011 group (chains[3]:group)
            -                        1013 supriya:patch-cable:2x2:replace (chains[3]:input)
            -                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 18.0
            -                        1014 supriya:meters:2 (chains[3]:input-levels)
            -                            in_: 18.0, out: 10.0
            -                        1012 group (chains[3]:devices)
            -                        1015 supriya:channel-strip:2 (chains[3]:channel-strip)
            -                            active: c8, done_action: 2.0, gain: c9, gate: 1.0, out: 18.0
            -                        1017 supriya:patch-cable:2x2 (chains[3]:output)
            -                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            -                        1016 supriya:meters:2 (chains[3]:output-levels)
            -                            in_: 18.0, out: 12.0
                                 1018 group (chains[4]:group)
                                     1020 supriya:patch-cable:2x2:replace (chains[4]:input)
                                         active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 18.0
            @@ -36,6 +24,24 @@
                                 in_: 16.0, out: 6.0
                         1025 group (devices[5]:group)
                             1026 group (devices[5]:chains)
            +                    1011 group (chains[3]:group)
            +                        1036 supriya:patch-cable:2x2:replace (chains[3]:input)
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 22.0
            +                        1037 supriya:meters:2 (chains[3]:input-levels)
            +                            in_: 22.0, out: 10.0
            +                        1013 supriya:patch-cable:2x2:replace (chains[3]:input)
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 16.0, out: 18.0
            +                        1012 group (chains[3]:devices)
            +                        1038 supriya:channel-strip:2 (chains[3]:channel-strip)
            +                            active: c8, done_action: 2.0, gain: c9, gate: 1.0, out: 22.0
            +                        1040 supriya:patch-cable:2x2 (chains[3]:output)
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 24.0
            +                        1039 supriya:meters:2 (chains[3]:output-levels)
            +                            in_: 22.0, out: 12.0
            +                        1015 supriya:channel-strip:2 (chains[3]:channel-strip)
            +                            active: c8, done_action: 2.0, gain: c9, gate: 0.0, out: 18.0
            +                        1017 supriya:patch-cable:2x2 (chains[3]:output)
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 20.0
                                 1029 group (chains[6]:group)
                                     1031 supriya:patch-cable:2x2:replace (chains[6]:input)
                                         active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 22.0
            """,
        ),
        MoveScenario(
            id="move before sibling",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_rack", {"name": "Rack"}),
                ("mixers[0].devices[0].chains[0]", "set_name", {"name": "Sibling"}),
                ("mixers[0].devices[0]", "add_chain", {"name": "Self"}),
            ],
            subject="mixers[0].devices[0].chains[1]",
            parent="mixers[0].devices[0]",
            index=0,
            expected_components_diff=lambda session: """
            --- initial
            +++ mutation
            @@ -2,5 +2,5 @@
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
                         <Rack 2 'Rack'>
            +                <Chain 4 'Self'>
                             <Chain 3 'Sibling'>
            -                <Chain 4 'Self'>
            """,
            expected_graph_order=(0, 0, 0),
            expected_messages="""
            - ['/g_head', 1008, 1018]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -6,6 +6,18 @@
                     1002 group (mixers[1]:devices)
                         1007 group (devices[2]:group)
                             1008 group (devices[2]:chains)
            +                    1018 group (chains[4]:group)
            +                        1020 supriya:patch-cable:2x2:replace (chains[4]:input)
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 18.0
            +                        1021 supriya:meters:2 (chains[4]:input-levels)
            +                            in_: 18.0, out: 16.0
            +                        1019 group (chains[4]:devices)
            +                        1022 supriya:channel-strip:2 (chains[4]:channel-strip)
            +                            active: c14, done_action: 2.0, gain: c15, gate: 1.0, out: 18.0
            +                        1024 supriya:patch-cable:2x2 (chains[4]:output)
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            +                        1023 supriya:meters:2 (chains[4]:output-levels)
            +                            in_: 18.0, out: 18.0
                                 1011 group (chains[3]:group)
                                     1013 supriya:patch-cable:2x2:replace (chains[3]:input)
                                         active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 18.0
            @@ -18,18 +30,6 @@
                                         active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
                                     1016 supriya:meters:2 (chains[3]:output-levels)
                                         in_: 18.0, out: 12.0
            -                    1018 group (chains[4]:group)
            -                        1020 supriya:patch-cable:2x2:replace (chains[4]:input)
            -                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 18.0
            -                        1021 supriya:meters:2 (chains[4]:input-levels)
            -                            in_: 18.0, out: 16.0
            -                        1019 group (chains[4]:devices)
            -                        1022 supriya:channel-strip:2 (chains[4]:channel-strip)
            -                            active: c14, done_action: 2.0, gain: c15, gate: 1.0, out: 18.0
            -                        1024 supriya:patch-cable:2x2 (chains[4]:output)
            -                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            -                        1023 supriya:meters:2 (chains[4]:output-levels)
            -                            in_: 18.0, out: 18.0
                             1009 supriya:patch-cable:2x2 (devices[2]:output)
                                 active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
                             1010 supriya:meters:2 (devices[2]:output-levels)
            """,
        ),
        MoveScenario(
            id="move after sibling",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_rack", {"name": "Rack"}),
                ("mixers[0].devices[0].chains[0]", "set_name", {"name": "Self"}),
                ("mixers[0].devices[0]", "add_chain", {"name": "Sibling"}),
            ],
            subject="mixers[0].devices[0].chains[0]",
            parent="mixers[0].devices[0]",
            index=1,
            expected_components_diff=lambda session: """
            --- initial
            +++ mutation
            @@ -2,5 +2,5 @@
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
                         <Rack 2 'Rack'>
            +                <Chain 4 'Sibling'>
                             <Chain 3 'Self'>
            -                <Chain 4 'Sibling'>
            """,
            expected_graph_order=(0, 0, 1),
            expected_messages="""
            - ['/n_after', 1011, 1018]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -6,6 +6,18 @@
                     1002 group (mixers[1]:devices)
                         1007 group (devices[2]:group)
                             1008 group (devices[2]:chains)
            +                    1018 group (chains[4]:group)
            +                        1020 supriya:patch-cable:2x2:replace (chains[4]:input)
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 18.0
            +                        1021 supriya:meters:2 (chains[4]:input-levels)
            +                            in_: 18.0, out: 16.0
            +                        1019 group (chains[4]:devices)
            +                        1022 supriya:channel-strip:2 (chains[4]:channel-strip)
            +                            active: c14, done_action: 2.0, gain: c15, gate: 1.0, out: 18.0
            +                        1024 supriya:patch-cable:2x2 (chains[4]:output)
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            +                        1023 supriya:meters:2 (chains[4]:output-levels)
            +                            in_: 18.0, out: 18.0
                                 1011 group (chains[3]:group)
                                     1013 supriya:patch-cable:2x2:replace (chains[3]:input)
                                         active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 18.0
            @@ -18,18 +30,6 @@
                                         active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
                                     1016 supriya:meters:2 (chains[3]:output-levels)
                                         in_: 18.0, out: 12.0
            -                    1018 group (chains[4]:group)
            -                        1020 supriya:patch-cable:2x2:replace (chains[4]:input)
            -                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 18.0
            -                        1021 supriya:meters:2 (chains[4]:input-levels)
            -                            in_: 18.0, out: 16.0
            -                        1019 group (chains[4]:devices)
            -                        1022 supriya:channel-strip:2 (chains[4]:channel-strip)
            -                            active: c14, done_action: 2.0, gain: c15, gate: 1.0, out: 18.0
            -                        1024 supriya:patch-cable:2x2 (chains[4]:output)
            -                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            -                        1023 supriya:meters:2 (chains[4]:output-levels)
            -                            in_: 18.0, out: 18.0
                             1009 supriya:patch-cable:2x2 (devices[2]:output)
                                 active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
                             1010 supriya:meters:2 (devices[2]:output-levels)
            """,
        ),
    ],
    ids=lambda scenario: scenario.id,
)
@pytest.mark.asyncio
async def test_Chain_move(scenario: MoveScenario, online: bool) -> None:
    async with scenario.run(annotation_style="numeric", online=online) as session:
        subject = session[scenario.subject]
        parent = session[scenario.parent]
        old_parent = subject.parent
        assert isinstance(old_parent, Rack)
        assert isinstance(parent, Rack)
        assert isinstance(subject, Chain)
        await subject.move(index=scenario.index, parent=parent)
    assert subject.graph_order == scenario.expected_graph_order
    if scenario.expected_exception:
        return
    assert subject.parent is parent
    assert subject in parent.chains
    if parent is not old_parent:
        assert subject not in old_parent.chains


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.asyncio
async def test_Chain_set_name(online: bool) -> None:
    session = Session()
    mixer = await session.add_mixer()
    rack = await mixer.add_rack()
    chain = rack.chains[0]
    if online:
        await session.boot()
    assert chain.name == "Chain 1"
    for name in ("Foo", "Bar", "Baz"):
        chain.set_name(name=name)
        assert chain.name == name
    chain.set_name(name=None)
    assert chain.name is None
