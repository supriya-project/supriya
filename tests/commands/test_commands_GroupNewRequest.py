import pytest
from uqbar.strings import normalize

import supriya
from supriya.exceptions import NodeNotAllocated


def test_1():
    group_a = supriya.realtime.Group()
    group_b = supriya.realtime.Group()
    group_c = supriya.realtime.Group()
    assert group_a.node_id is None
    assert group_b.node_id is None
    assert group_c.node_id is None
    request = supriya.commands.GroupNewRequest(
        items=[
            supriya.commands.GroupNewRequest.Item(
                node_id=group_b, target_node_id=group_a
            ),
            supriya.commands.GroupNewRequest.Item(
                node_id=group_c, target_node_id=group_b
            ),
        ]
    )
    assert request.items[0].node_id is group_b
    assert request.items[0].target_node_id is group_a
    assert request.items[1].node_id is group_c
    assert request.items[1].target_node_id is group_b
    with pytest.raises(NodeNotAllocated):
        request.to_osc()


def test_2(server):
    """
    Local application allocates the groups' IDs before we generate the OSC
    message.
    """
    group_a = supriya.realtime.Group().allocate(server)
    group_b = supriya.realtime.Group()
    group_c = supriya.realtime.Group()
    assert group_a.node_id == 1000
    assert group_b.node_id is None
    assert group_c.node_id is None
    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
        """
    )
    request = supriya.commands.GroupNewRequest(
        items=[
            supriya.commands.GroupNewRequest.Item(
                add_action="add_to_head", node_id=group_b, target_node_id=group_a
            ),
            supriya.commands.GroupNewRequest.Item(
                add_action="add_to_head", node_id=group_c, target_node_id=group_b
            ),
        ]
    )
    with server.osc_protocol.capture() as transcript:
        request.communicate(server)
        server.sync()
    assert [(_.label, _.message) for _ in transcript] == [
        ("S", supriya.osc.OscMessage("/g_new", 1001, 0, 1000, 1002, 0, 1001)),
        ("R", supriya.osc.OscMessage("/n_go", 1001, 1000, -1, -1, 1, -1, -1)),
        ("R", supriya.osc.OscMessage("/n_go", 1002, 1001, -1, -1, 1, -1, -1)),
        ("S", supriya.osc.OscMessage("/sync", 0)),
        ("R", supriya.osc.OscMessage("/synced", 0)),
    ]
    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 group
                        1002 group
        """
    )
    assert group_b.node_id == 1001
    assert group_b.parent is group_a
    assert group_b.is_allocated
    assert group_c.node_id == 1002
    assert group_c.parent is group_b
    assert group_c.is_allocated


def test_3(server):
    """
    Communicating without a pre-existing group creates that group during local
    application.
    """
    group_a = supriya.realtime.Group().allocate(server)
    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
        """
    )
    request = supriya.commands.GroupNewRequest(
        items=[
            supriya.commands.GroupNewRequest.Item(
                add_action="add_to_head", node_id=1001, target_node_id=group_a
            ),
            supriya.commands.GroupNewRequest.Item(
                add_action="add_to_head", node_id=1002, target_node_id=1001
            ),
        ]
    )
    with server.osc_protocol.capture() as transcript:
        request.communicate(server)
        server.sync()
    assert [(_.label, _.message) for _ in transcript] == [
        ("S", supriya.osc.OscMessage("/g_new", 1001, 0, 1000, 1002, 0, 1001)),
        ("R", supriya.osc.OscMessage("/n_go", 1001, 1000, -1, -1, 1, -1, -1)),
        ("R", supriya.osc.OscMessage("/n_go", 1002, 1001, -1, -1, 1, -1, -1)),
        ("S", supriya.osc.OscMessage("/sync", 0)),
        ("R", supriya.osc.OscMessage("/synced", 0)),
    ]
    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 group
                        1002 group
        """
    )
    group_b = server[1001]
    group_c = server[1002]
    assert group_b.parent is group_a
    assert group_c.parent is group_b
