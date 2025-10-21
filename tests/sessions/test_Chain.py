import dataclasses
from typing import Any, Sequence

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
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -8,18 +8,18 @@
                             1008 group (devices[2]:chains)
                                 1010 group (chains[3]:group)
                                     1012 supriya:patch-cable:2x2:replace (chains[3]:input)
            -                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 18.0
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 16.0, out: 18.0
                                     1013 supriya:meters:2 (chains[3]:input-levels)
                                         in_: 18.0, out: 8.0
                                     1011 group (chains[3]:devices)
                                     1014 supriya:channel-strip:2 (chains[3]:channel-strip)
            -                            active: c6, done_action: 2.0, gain: c7, gate: 1.0, out: 18.0
            +                            active: c6, done_action: 14.0, gain: c7, gate: 0.0, out: 18.0
                                     1016 supriya:patch-cable:2x2 (chains[3]:output)
            -                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 20.0
                                     1015 supriya:meters:2 (chains[3]:output-levels)
                                         in_: 18.0, out: 10.0
                             1009 supriya:patch-cable:2x2 (devices[2]:output)
            -                    active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
            +                    active: 0.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
                     1003 supriya:channel-strip:2 (mixers[1]:channel-strip)
                         active: 1.0, done_action: 2.0, gain: c0, gate: 1.0, out: 16.0
                     1005 supriya:meters:2 (mixers[1]:output-levels)
            """,
            expected_messages="""
            - ['/n_set', 1009, 'active', 0.0]
            - [None, [['/n_set', 1010, 'gate', 0.0], ['/n_set', 1014, 'done_action', 14.0]]]
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
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -8,14 +8,14 @@
                             1008 group (devices[2]:chains)
                                 1010 group (chains[3]:group)
                                     1012 supriya:patch-cable:2x2:replace (chains[3]:input)
            -                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 18.0
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 16.0, out: 18.0
                                     1013 supriya:meters:2 (chains[3]:input-levels)
                                         in_: 18.0, out: 8.0
                                     1011 group (chains[3]:devices)
                                     1014 supriya:channel-strip:2 (chains[3]:channel-strip)
            -                            active: c6, done_action: 2.0, gain: c7, gate: 1.0, out: 18.0
            +                            active: c6, done_action: 14.0, gain: c7, gate: 0.0, out: 18.0
                                     1016 supriya:patch-cable:2x2 (chains[3]:output)
            -                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 20.0
                                     1015 supriya:meters:2 (chains[3]:output-levels)
                                         in_: 18.0, out: 10.0
                                 1017 group (chains[4]:group)
            """,
            expected_messages="""
            - [None, [['/n_set', 1010, 'gate', 0.0], ['/n_set', 1014, 'done_action', 14.0]]]
            """,
        ),
        Scenario(
            id="1/2 chains",
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
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -20,14 +20,14 @@
                                         in_: 18.0, out: 10.0
                                 1017 group (chains[4]:group)
                                     1019 supriya:patch-cable:2x2:replace (chains[4]:input)
            -                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 18.0
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 16.0, out: 18.0
                                     1020 supriya:meters:2 (chains[4]:input-levels)
                                         in_: 18.0, out: 14.0
                                     1018 group (chains[4]:devices)
                                     1021 supriya:channel-strip:2 (chains[4]:channel-strip)
            -                            active: c12, done_action: 2.0, gain: c13, gate: 1.0, out: 18.0
            +                            active: c12, done_action: 14.0, gain: c13, gate: 0.0, out: 18.0
                                     1023 supriya:patch-cable:2x2 (chains[4]:output)
            -                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 20.0
                                     1022 supriya:meters:2 (chains[4]:output-levels)
                                         in_: 18.0, out: 16.0
                             1009 supriya:patch-cable:2x2 (devices[2]:output)
            """,
            expected_messages="""
            - [None, [['/n_set', 1017, 'gate', 0.0], ['/n_set', 1021, 'done_action', 14.0]]]
            """,
        ),
    ],
    ids=lambda value: value.id,
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
    maybe_raises: Any
    parent: str


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "scenario",
    [],
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
        raised = True
        with scenario.maybe_raises:
            await subject.move(index=scenario.index, parent=parent)
            raised = False
    assert subject.graph_order == scenario.expected_graph_order
    if not raised:
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
    assert chain.name is None
    for name in ("Foo", "Bar", "Baz"):
        chain.set_name(name=name)
        assert chain.name == name
    chain.set_name(name=None)
    assert chain.name is None
