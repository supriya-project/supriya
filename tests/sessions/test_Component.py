import pytest
from uqbar.strings import normalize

from supriya.sessions import Session

from .conftest import (
    capture,
    debug_tree,
    format_messages,
)


@pytest.mark.asyncio
async def test_Component_connections_01():
    # Pre-conditions
    session = Session()
    mixer = await session.add_mixer()
    track_one = await mixer.add_track()
    track_two = await mixer.add_track()
    send = await track_one.add_send(target=track_two)
    await session.boot()
    # Operation
    with capture(session.contexts[0]) as messages:
        await send.delete()
    # Post-conditions
    assert format_messages(messages) == normalize(
        """
        - ['/n_set', 1014, 'done_action', 2.0, 'gate', 0.0]
        """,
    )
    assert track_one._connections == {}
    assert track_two._connections == {}


@pytest.mark.asyncio
async def test_Component_connections_02():
    # Pre-conditions
    session = Session()
    mixer = await session.add_mixer()
    track_one = await mixer.add_track()
    track_two = await mixer.add_track()
    await track_one.add_send(target=track_two)
    await session.boot()
    initial_tree = await debug_tree(session, annotation=None)
    # Operation
    with capture(session.contexts[0]) as messages:
        await track_one.delete()
    # Post-conditions
    print(initial_tree)
    assert format_messages(messages) == normalize(
        """
        - [None, [['/n_set', 1007, 'gate', 0.0], ['/n_set', 1010, 'done_action', 14.0]]]
        """,
    )
    assert track_two._connections == {}


@pytest.mark.asyncio
async def test_Component_connections_03():
    # Pre-conditions
    session = Session()
    mixer = await session.add_mixer()
    track_one = await mixer.add_track()
    track_two = await mixer.add_track()
    await track_one.add_send(target=track_two)
    await session.boot()
    initial_tree = await debug_tree(session, annotation=None)
    # Operation
    with capture(session.contexts[0]) as messages:
        await track_two.delete()
    # Post-conditions
    print(initial_tree)
    assert format_messages(messages) == normalize(
        """
        - [None, [['/n_set', 1015, 'gate', 0.0], ['/n_set', 1018, 'done_action', 14.0]]]
        - ['/n_set', 1014, 'done_action', 2.0, 'gate', 0.0]
        """,
    )
    assert track_one._connections == {}
