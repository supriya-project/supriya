import dataclasses
from typing import Any, Sequence

import pytest

from supriya.sessions import Chain, Rack, Session

from .conftest import Scenario


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "scenario",
    [],
)
@pytest.mark.asyncio
async def test_Chain_delete(
    scenario: Scenario,
    online: bool,
) -> None:
    async with scenario.run(annotation=None, online=online) as session:
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
async def test_Chain_move(
    scenario: MoveScenario,
    online: bool,
) -> None:
    async with scenario.run(annotation="numeric", online=online) as session:
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
