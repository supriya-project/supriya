import pytest
from uqbar.strings import normalize

from supriya.mixers import Session
from supriya.mixers.mixers import Mixer

from .conftest import assert_diff, capture, format_messages


@pytest.mark.xfail
@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "expected_diff, expected_messages",
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
    complex_session: tuple[Session, str],
    expected_diff: str,
    expected_messages: str,
    mixer: Mixer,
    online: bool,
) -> None:
    # Pre-conditions
    session, initial_tree = complex_session
    print("Pre-conditions")
    if online:
        await session.boot()
    # Operation
    print("Operation")
    with capture(mixer.context) as messages:
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
    assert format_messages(messages) == normalize(expected_messages)
