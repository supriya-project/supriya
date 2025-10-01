from typing import Callable

import pytest

from supriya.sessions import Chain, Rack, Session

from .conftest import run_test


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "commands, target, expected_components_diff, expected_tree_diff, expected_messages",
    [],
)
@pytest.mark.asyncio
async def test_Chain_delete(
    commands: list[tuple[str | None, str, dict | None]],
    expected_components_diff: Callable[[Session], str] | str,
    expected_messages: str,
    expected_tree_diff: str,
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


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    (
        "commands, target, parent, index, maybe_raises, "
        "expected_graph_order, expected_components_diff, expected_tree_diff, expected_messages"
    ),
    [],
)
@pytest.mark.asyncio
async def test_Chain_move(
    commands: list[tuple[str | None, str, dict | None]],
    expected_components_diff: Callable[[Session], str] | str,
    expected_graph_order: list[int],
    expected_messages: str,
    expected_tree_diff: str,
    index: int,
    maybe_raises,
    online: bool,
    parent: str,
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
        parent_ = session[parent]
        old_parent = target_.parent
        assert isinstance(old_parent, Rack)
        assert isinstance(parent_, Rack)
        assert isinstance(target_, Chain)
        raised = True
        with maybe_raises:
            await target_.move(index=index, parent=parent_)
            raised = False
    assert target_.graph_order == expected_graph_order
    if not raised:
        assert target_.parent is parent_
        assert target_ in parent_.chains
        if parent_ is not old_parent:
            assert target_ not in old_parent.chains


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
