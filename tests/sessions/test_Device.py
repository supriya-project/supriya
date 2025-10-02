from typing import Callable

import pytest

from supriya.sessions import Device, Session, Track

from .conftest import does_not_raise, run_test


@pytest.mark.xfail
@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    (
        "commands, device_target, sidechain_name, track_target, "
        "maybe_raises, expected_components_diff, expected_tree_diff, expected_messages"
    ),
    [
        (
            [],
            "",
            "",
            "",
            does_not_raise,
            "",
            "",
            "",
        ),
    ],
)
@pytest.mark.asyncio
async def test_Device_set_sidechain(
    commands: list[tuple[str | None, str, dict | None]],
    expected_components_diff: Callable[[Session], str] | str,
    expected_messages: str,
    expected_tree_diff: str,
    maybe_raises,
    online: bool,
    device_target: str,
    sidechain_name: str,
    track_target: str | None,
) -> None:
    async with run_test(
        commands=commands,
        expected_components_diff=expected_components_diff,
        expected_messages=expected_messages,
        expected_tree_diff=expected_tree_diff,
        online=online,
    ) as session:
        device = session[device_target]
        assert isinstance(device, Device)
        if track_target is not None:
            track = session[track_target]
            assert isinstance(track, Track)
        else:
            track = None
        raised = True
        with maybe_raises:
            await device.set_sidechain(sidechain_name, track)
            raised = False
    if not raised:
        assert device.sidechains[sidechain_name] is track
