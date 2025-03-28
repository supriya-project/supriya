import pytest
from uqbar.strings import normalize

from supriya.mixers import Session
from supriya.mixers.mixers import Mixer

from .conftest import assert_diff, capture, format_messages


@pytest.mark.xfail
@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "expected_diff, expected_commands",
    [
        (
            "",
            """
            - ['/n_set', 1000, 'gate', 0.0]
            - ['/n_set', 1004, 'gate', 0.0]
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_Mixer_delete(
    expected_commands: str,
    expected_diff: str,
    mixer: Mixer,
    online: bool,
    complex_session: tuple[Session, str],
) -> None:
    # Pre-conditions
    session, initial_tree = complex_session
    print("Pre-conditions")
    if online:
        await session.boot()
    # Operation
    print("Operation")
    with capture(mixer.context) as commands:
        await mixer.delete()
    # Post-conditions
    print("Post-conditions")
    if not online:
        raise Exception
    await assert_diff(
        session,
        expected_diff,
        expected_initial_tree="""
        <session.contexts[0]>
        """,
    )
    assert format_messages(commands) == normalize(expected_commands)
