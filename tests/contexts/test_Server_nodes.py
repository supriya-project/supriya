import asyncio
import logging
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from uqbar.strings import normalize

from supriya import AsyncServer, OscBundle, OscMessage, Server, SynthDef, default
from supriya.contexts.responses import NodeInfo
from supriya.enums import NodeAction


async def get(x):
    if asyncio.iscoroutine(x):
        return await x
    return x


@pytest.fixture(autouse=True)
def use_caplog(caplog):
    caplog.set_level(logging.INFO)


@pytest_asyncio.fixture(autouse=True, params=[AsyncServer, Server])
async def context(request) -> AsyncGenerator[AsyncServer | Server, None]:
    context = request.param()
    await get(context.boot())
    context.add_synthdefs(default)
    await get(context.sync())
    yield context


@pytest.mark.asyncio
async def test_Group_children(context: AsyncServer | Server) -> None:
    # root node's child(ren) is the default grop
    assert context.root_node.children == [context.default_group]
    # the default group initializes without children
    assert context.default_group.children == []
    # groups initially have no children
    group = context.add_group()
    assert context.default_group.children == []  # waiting for the /n_go response
    assert group.children == []  # waiting for the /n_go response
    await get(context.sync())
    assert context.default_group.children == [group]
    assert group.children == []
    # groups can have children
    synth_a = group.add_synth(default)
    assert group.children == []  # waiting for the /n_go response
    await get(context.sync())
    assert group.children == [synth_a]
    # modifying the group's children on the context modifies in the client
    synth_b = group.add_synth(default, add_action="ADD_TO_TAIL")
    synth_c = group.add_synth(default, add_action="ADD_TO_HEAD")
    synth_d = synth_b.add_synth(default, add_action="ADD_BEFORE")
    assert group.children == [synth_a]  # waiting for the /n_go response
    await get(context.sync())
    assert group.children == [synth_c, synth_a, synth_d, synth_b]
    # freed groups have no children
    group.free()
    assert group.children == [synth_c, synth_a, synth_d, synth_b]  # waiting for /n_end
    await get(context.sync())
    assert group.children == []
    # no children on an unbooted context
    await get(context.quit())
    assert context.root_node.children == []


@pytest.mark.asyncio
async def test_Node_active(context: AsyncServer | Server) -> None:
    # nodes are active by default
    group = context.add_group()
    assert group.active  # waiting for the /n_go response
    await get(context.sync())
    assert group.active
    # paused nodes are inactive
    group.pause()
    assert group.active  # waiting for the /n_run response
    await get(context.sync())
    assert not group.active
    # unpaused nodes are active
    group.unpause()
    assert not group.active  # waiting for the /n_run response
    await get(context.sync())
    assert group.active


@pytest.mark.asyncio
async def test_Node_allocated(context: AsyncServer | Server) -> None:
    # groups can be allocated
    group = context.add_group()
    assert not group.allocated  # waiting for the /n_go response
    await get(context.sync())
    assert group.allocated
    # freed nodes are unallocated
    group.free()
    assert group.allocated  # waiting for the /n_end response
    await get(context.sync())
    assert not group.allocated
    # synths can be allocated
    synth = context.add_synth(default)
    assert not synth.allocated  # waiting for the /n_go response
    await get(context.sync())
    assert synth.allocated
    # nothing is allocated on an unbooted context
    await get(context.quit())
    assert not synth.allocated
    # allocation state is stored in the context, not the node
    await get(context.boot())
    assert not synth.allocated


@pytest.mark.asyncio
async def test_Node_parent(context: AsyncServer | Server) -> None:
    group = context.add_group()
    assert group.parent is None  # waiting for the /n_go response
    await asyncio.sleep(0.1)
    assert group.parent is not None
    assert group.parent == context.default_group
    assert group.parent.parent == context.root_node


@pytest.mark.asyncio
async def test_add_group(context: AsyncServer | Server) -> None:
    with context.osc_protocol.capture() as transcript:
        # /g_new
        group = context.add_group()
        # /p_new
        context.add_group(parallel=True)
        with context.at(1.23):
            context.add_group(parallel=True, target_node=group)
            context.add_group(parallel=True, target_node=group)
            context.add_group(target_node=group)
            context.add_group(target_node=group)
    assert transcript.filtered(received=False, status=False) == [
        OscMessage("/g_new", 1000, 0, 1),
        OscMessage("/p_new", 1001, 0, 1),
        OscBundle(
            contents=(
                OscMessage("/p_new", 1002, 0, 1000, 1003, 0, 1000),
                OscMessage("/g_new", 1004, 0, 1000, 1005, 0, 1000),
            ),
            timestamp=1.23 + context.latency,
        ),
    ]
    # guard against invalid add-actions
    synth = context.add_synth(default)
    with pytest.raises(ValueError):
        synth.add_group(add_action="ADD_TO_HEAD")
    with pytest.raises(ValueError):
        synth.add_group(add_action="ADD_TO_TAIL")


@pytest.mark.asyncio
async def test_add_synth(
    context: AsyncServer | Server, two_voice_synthdef: SynthDef
) -> None:
    context.add_synthdefs(default, two_voice_synthdef)
    await get(context.sync())
    with context.osc_protocol.capture() as transcript:
        bus_a = context.add_bus("AUDIO")
        bus_c = context.add_bus("CONTROL")
        synth = context.add_synth(default)
        context.add_synth(default, frequency=bus_a, amplitude="c0", pan=0.25, out=0)
        context.add_synth(two_voice_synthdef, frequencies=(123, 456))
        with context.at(1.23):
            context.add_synth(default, add_action="ADD_AFTER", target_node=synth)
            context.add_synth(
                default, frequency=bus_c.map_symbol(), amplitude="a16", pan=0.25, out=0
            )
    assert transcript.filtered(received=False, status=False) == [
        OscMessage("/s_new", "supriya:default", 1000, 0, 1),
        OscMessage(
            "/s_new",
            "supriya:default",
            1001,
            0,
            1,
            "amplitude",
            "c0",
            "frequency",
            16.0,  # cast to an int
            "pan",
            0.25,
        ),
        OscMessage(
            "/s_new",
            "test:two-voice",
            1002,
            0,
            1,
            "frequencies",
            (123.0, 456.0),
        ),
        OscBundle(
            contents=(
                OscMessage("/s_new", "supriya:default", 1003, 3, 1000),
                OscMessage(
                    "/s_new",
                    "supriya:default",
                    1004,
                    0,
                    1,
                    "amplitude",
                    "a16",
                    "frequency",
                    "c0",
                    "pan",
                    0.25,
                ),
            ),
            timestamp=1.23 + context.latency,
        ),
    ]
    # guard against invalid add-actions
    synth = context.add_synth(default)
    with pytest.raises(ValueError):
        synth.add_synth(default, add_action="ADD_TO_HEAD")
    with pytest.raises(ValueError):
        synth.add_synth(default, add_action="ADD_TO_TAIL")


@pytest.mark.asyncio
async def test_free_group_children(context: AsyncServer | Server) -> None:
    grandparent = context.add_group()
    # setup
    parent = grandparent.add_group()
    grandparent.add_synth(default)
    parent.add_synth(default)
    assert str(await get(context.query_tree())) == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1002 supriya:default
                        out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5
                    1001 group
                        1003 supriya:default
                            out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5
        """
    )
    # /g_freeAll
    with context.osc_protocol.capture() as transcript:
        grandparent.free_children()
    assert transcript.filtered(received=False, status=False) == [
        OscMessage("/g_freeAll", 1000)
    ]
    assert str(await get(context.query_tree())) == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
        """
    )
    # setup
    parent = grandparent.add_group()
    grandparent.add_synth(default)
    parent.add_synth(default)
    assert str(await get(context.query_tree())) == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1005 supriya:default
                        out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5
                    1004 group
                        1006 supriya:default
                            out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5
        """
    )
    # /g_deepFree
    with context.osc_protocol.capture() as transcript:
        grandparent.free_children(synths_only=True)
    assert transcript.filtered(received=False, status=False) == [
        OscMessage("/g_deepFree", 1000)
    ]
    assert str(await get(context.query_tree())) == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1004 group
        """
    )


@pytest.mark.asyncio
async def test_free_node(context: AsyncServer | Server) -> None:
    group = context.add_group()
    synth = context.add_synth(default)
    with context.osc_protocol.capture() as transcript:
        group.free()
        synth.free()
    assert transcript.filtered(received=False, status=False) == [
        OscMessage("/n_free", 1000),
        OscMessage("/n_set", 1001, "gate", 0),
    ]


@pytest.mark.asyncio
async def test_get_synth_controls(context: AsyncServer | Server) -> None:
    with context.at():
        with context.add_synthdefs(default):
            synth = context.add_synth(
                default, frequency=432.0, amplitude=0.333, panning=0.1
            )
    assert await get(context.sync())
    controls = await get(synth.get("frequency", "amplitude"))
    assert {key: round(value, 3) for key, value in controls.items()} == {
        "frequency": 432.0,
        "amplitude": 0.333,
    }
    # unsynced
    with context.osc_protocol.capture() as transcript:
        with context.at():
            assert await get(synth.get("frequency", sync=False)) is None
    assert transcript.filtered(received=False, status=False) == [
        OscMessage("/s_get", 1000, "frequency")
    ]


@pytest.mark.asyncio
async def test_get_synth_control_range(context: AsyncServer | Server) -> None:
    # TBH, not sure what the semantics of this command are supposed to be.
    with context.at():
        with context.add_synthdefs(default):
            synth = context.add_synth(
                default, frequency=432.0, amplitude=0.25, panning=0.1
            )
    assert await get(context.sync())
    assert await get(synth.get_range("amplitude", 5)) == (0.25, 0.0, 0.0, 0.0, 0.0)
    # unsynced
    with context.osc_protocol.capture() as transcript:
        with context.at():
            assert await get(synth.get_range("frequency", 3, sync=False)) is None
    assert transcript.filtered(received=False, status=False) == [
        OscMessage("/s_getn", 1000, "frequency", 3)
    ]


@pytest.mark.asyncio
async def test_map_node(context: AsyncServer | Server) -> None:
    bus_a = context.add_bus("AUDIO")
    bus_c = context.add_bus("CONTROL")
    synth = context.add_synth(default)
    with context.osc_protocol.capture() as transcript:
        synth.map(frequency=bus_a, amplitude=bus_c, pan=None)
    assert transcript.filtered(received=False, status=False) == [
        OscBundle(
            contents=(
                OscMessage("/n_map", 1000, "amplitude", 0, "pan", -1),
                OscMessage("/n_mapa", 1000, "frequency", 16),
            )
        )
    ]


@pytest.mark.asyncio
async def test_move_node(context: AsyncServer | Server) -> None:
    group = context.add_group()
    synth = context.add_synth(default)
    with context.osc_protocol.capture() as transcript:
        group.move(target_node=synth, add_action="ADD_AFTER")
        synth.move(target_node=group, add_action="ADD_BEFORE")
        synth.move(target_node=group, add_action="ADD_TO_TAIL")
        synth.move(target_node=group, add_action="ADD_TO_HEAD")
    assert transcript.filtered(received=False, status=False) == [
        OscMessage("/n_after", 1000, 1001),
        OscMessage("/n_before", 1001, 1000),
        OscMessage("/g_tail", 1000, 1001),
        OscMessage("/g_head", 1000, 1001),
    ]


@pytest.mark.asyncio
async def test_order_nodes(context: AsyncServer | Server) -> None:
    group_a = context.add_group()
    group_b = context.add_group()
    group_c = context.add_group()
    with context.osc_protocol.capture() as transcript:
        group_a.order(group_b, group_c, add_action="ADD_TO_TAIL")
    assert transcript.filtered(received=False, status=False) == [
        OscMessage("/n_order", 1, 1000, 1001, 1002)
    ]


@pytest.mark.asyncio
async def test_pause_node(context: AsyncServer | Server) -> None:
    group = context.add_group()
    with context.osc_protocol.capture() as transcript:
        group.pause()
    assert transcript.filtered(received=False, status=False) == [
        OscMessage("/n_run", 1000, 0)
    ]


@pytest.mark.asyncio
async def test_query_node(context: AsyncServer | Server) -> None:
    group = context.add_group()
    await asyncio.sleep(0.1)
    assert await get(group.query()) == NodeInfo(
        action=NodeAction.NODE_QUERIED,
        head_id=-1,
        is_group=True,
        next_id=-1,
        node_id=1000,
        parent_id=1,
        previous_id=-1,
        tail_id=-1,
    )
    # unsynced
    with context.osc_protocol.capture() as transcript:
        with context.at():
            assert await get(group.query(sync=False)) is None
    assert transcript.filtered(received=False, status=False) == [
        OscMessage("/n_query", 1000)
    ]


@pytest.mark.asyncio
async def test_set_node(context: AsyncServer | Server) -> None:
    group = context.add_group()
    with context.osc_protocol.capture() as transcript:
        group.set((1, 2.3), (2, [3.4, 4.5]), foo=3.145, bar=4.5, baz=[1.23, 4.56])
    assert transcript.filtered(received=False, status=False) == [
        OscMessage(
            "/n_set",
            1000,
            1,
            2.3,
            2,
            [3.4, 4.5],
            "bar",
            4.5,
            "baz",
            [1.23, 4.56],
            "foo",
            3.145,
        )
    ]


@pytest.mark.asyncio
async def test_set_node_range(context: AsyncServer | Server) -> None:
    group = context.add_group()
    with context.osc_protocol.capture() as transcript:
        group.set_range((2, [3.4, 4.5]), baz=[1.23, 4.56])
    assert transcript.filtered(received=False, status=False) == [
        OscMessage("/n_setn", 1000, 2, 2, 3.4, 4.5, "baz", 2, 1.23, 4.56)
    ]


@pytest.mark.asyncio
async def test_unpause_node(context: AsyncServer | Server) -> None:
    group_a = context.add_group()
    group_b = context.add_group()
    group_c = context.add_group()
    with context.osc_protocol.capture() as transcript:
        group_a.unpause()
        with context.at(1.23):
            group_b.unpause()
            group_c.unpause()
    assert transcript.filtered(received=False, status=False) == [
        OscMessage("/n_run", 1000, 1),
        OscBundle(
            contents=(OscMessage("/n_run", 1001, 1, 1002, 1),),
            timestamp=1.23 + context.latency,
        ),
    ]
