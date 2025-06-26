import pytest
from uqbar.strings import normalize

from supriya.mixers import Session
from supriya.mixers.tracks import TrackSend

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
async def test_TrackSend_delete(
    commands: list[tuple[str | None, str, str | None]],
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
    assert isinstance(target_, TrackSend)
    parent = target_.parent
    # Operation
    print("Operation")
    with capture(target_.context) as messages:
        await target_.delete()
    # Post-conditions
    print("Post-conditions")
    assert parent
    assert target_ not in parent.sends
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
