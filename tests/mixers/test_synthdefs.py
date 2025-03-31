import asyncio
import difflib
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from uqbar.strings import normalize

from supriya import AsyncServer, DoneAction
from supriya.mixers.synthdefs import CHANNEL_STRIP_2, PATCH_CABLE_2_2


@pytest_asyncio.fixture
async def server() -> AsyncGenerator[AsyncServer, None]:
    server = await AsyncServer().boot()
    yield server
    await server.quit()


def calculate_diff(initial_tree: str, actual_tree: str) -> str:
    initial_tree = normalize(initial_tree) + "\n"
    actual_tree = normalize(actual_tree) + "\n"
    return "".join(
        difflib.unified_diff(
            normalize(initial_tree).splitlines(True),
            actual_tree.splitlines(True),
            tofile="mutation",
            fromfile="initial",
        )
    )


@pytest.mark.parametrize(
    "done_action, expected_diff",
    [
        (
            DoneAction.FREE_SYNTH,
            """
            --- initial
            +++ mutation
            @@ -1,5 +1,3 @@
             NODE TREE 0 group
                 1 group
                     1000 group
            -            1001 supriya:channel-strip:2
            -                active: 1.0, bus: 0.0, done_action: 2.0, gain: 0.0, gate: 1.0
            """,
        ),
        (
            DoneAction.FREE_SYNTH_AND_ENCLOSING_GROUP,
            """
            --- initial
            +++ mutation
            @@ -1,5 +1,2 @@
             NODE TREE 0 group
                 1 group
            -        1000 group
            -            1001 supriya:channel-strip:2
            -                active: 1.0, bus: 0.0, done_action: 2.0, gain: 0.0, gate: 1.0
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_free_channel_strip(
    done_action: DoneAction, expected_diff: str, server: AsyncServer
) -> None:
    """
    Done actions should be modulable.
    """
    with server.at():
        with server.add_synthdefs(CHANNEL_STRIP_2):
            group = server.add_group()
            synth = group.add_synth(synthdef=CHANNEL_STRIP_2)
    await server.sync()
    initial_tree = str(await server.query_tree())
    with server.at():
        synth.set(done_action=done_action)
        synth.free()
    assert initial_tree == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 supriya:channel-strip:2
                        active: 1.0, bus: 0.0, done_action: 2.0, gain: 0.0, gate: 1.0
        """,
    )
    await asyncio.sleep(0.1)
    actual_tree = str(await server.query_tree())
    actual_diff = calculate_diff(initial_tree, actual_tree)
    assert normalize(expected_diff) == normalize(actual_diff)


@pytest.mark.parametrize(
    "done_action, expected_diff",
    [
        (
            DoneAction.FREE_SYNTH,
            """
            --- initial
            +++ mutation
            @@ -1,5 +1,3 @@
             NODE TREE 0 group
                 1 group
                     1000 group
            -            1001 supriya:patch-cable:2x2
            -                active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 0.0, out: 0.0
            """,
        ),
        (
            DoneAction.FREE_SYNTH_AND_ENCLOSING_GROUP,
            """
            --- initial
            +++ mutation
            @@ -1,5 +1,2 @@
             NODE TREE 0 group
                 1 group
            -        1000 group
            -            1001 supriya:patch-cable:2x2
            -                active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 0.0, out: 0.0
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_free_patch_cable(
    done_action: DoneAction, expected_diff: str, server: AsyncServer
) -> None:
    """
    Done actions should be modulable.
    """
    with server.at():
        with server.add_synthdefs(PATCH_CABLE_2_2):
            group = server.add_group()
            synth = group.add_synth(synthdef=PATCH_CABLE_2_2)
    await server.sync()
    initial_tree = str(await server.query_tree())
    with server.at():
        synth.set(done_action=done_action)
        synth.free()
    assert initial_tree == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 supriya:patch-cable:2x2
                        active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 0.0, out: 0.0
        """,
    )
    await asyncio.sleep(0.1)
    actual_tree = str(await server.query_tree())
    actual_diff = calculate_diff(initial_tree, actual_tree)
    assert normalize(expected_diff) == normalize(actual_diff)
