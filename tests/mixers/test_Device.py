import pytest
from uqbar.strings import normalize

from supriya.mixers import Session
from supriya.mixers.devices import Device, DeviceContainer

from .conftest import (
    apply_commands,
    assert_components_diff,
    assert_tree_diff,
    capture,
    debug_components,
    debug_tree,
    format_messages,
)


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "commands, target, expected_components_diff, expected_tree_diff, expected_messages",
    [],
)
@pytest.mark.asyncio
async def test_Device_delete(
    commands: list[tuple[str | None, str, dict | None]],
    expected_components_diff: str,
    expected_messages: str,
    expected_tree_diff: str,
    online: bool,
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
    target_ = session[target]
    assert isinstance(target_, Device)
    parent = target_.parent
    # Operation
    print("Operation")
    with capture(target_.context) as messages:
        await target_.delete()
    # Post-conditions
    print("Post-conditions")
    assert parent
    assert target_ not in parent.devices
    assert target_.parent is None
    assert_components_diff(session, expected_components_diff, initial_components)
    if not online:
        return
    await assert_tree_diff(
        session,
        expected_tree_diff,
        expected_initial_tree=initial_tree,
    )
    assert format_messages(messages) == normalize(expected_messages)


@pytest.mark.parametrize(
    "commands, target, parent, index, maybe_raises, expected_graph_order, expected_components_diff, expected_tree_diff, expected_messages",
    [],
)
@pytest.mark.asyncio
async def test_Device_move(
    commands: list[tuple[str | None, str, dict | None]],
    expected_components_diff: str,
    expected_graph_order: list[int],
    expected_messages: str,
    expected_tree_diff: str,
    index: int,
    maybe_raises,
    parent: str,
    target: str,
    online: bool = True,
) -> None:
    # Pre-conditions
    print("Pre-conditions")
    session = Session()
    await apply_commands(session, commands)
    initial_components = debug_components(session)
    if online:
        await session.boot()
        await session.sync()
        initial_tree = await debug_tree(session, annotation="numeric")
    target_ = session[target]
    parent_ = session[parent]
    old_parent = target_.parent
    assert isinstance(old_parent, DeviceContainer)
    assert isinstance(parent_, DeviceContainer)
    assert isinstance(target_, Device)
    # Operation
    print("Operation")
    raised = True
    with maybe_raises, capture(session["mixers[0]"].context) as messages:
        await target_.move(index=index, parent=parent_)
        raised = False
    # Post-conditions
    print("Post-conditions")
    assert target_.graph_order == expected_graph_order
    if not raised:
        assert target_.parent is parent_
        assert target_ in parent_.devices
        if parent_ is not old_parent:
            assert target_ not in old_parent.devices
    assert_components_diff(session, expected_components_diff, initial_components)
    if not online:
        return
    await assert_tree_diff(
        session,
        expected_tree_diff,
        expected_initial_tree=initial_tree,
        annotation="numeric",
    )
    assert format_messages(messages) == normalize(expected_messages)
