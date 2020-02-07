import pytest
import uqbar.strings

import supriya.assets.synthdefs
import supriya.osc
import supriya.realtime


@pytest.mark.flaky(reruns=5)
def test_01(server):

    group_a = supriya.realtime.Group().allocate()
    group_b = supriya.realtime.Group().allocate()

    synth_a = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_b = supriya.realtime.Synth(supriya.assets.synthdefs.test)

    group_a.append(synth_a)
    group_b.append(synth_b)

    remote_state = str(server.query_remote_nodes())
    assert remote_state == uqbar.strings.normalize(
        """
        NODE TREE 0 group
            1 group
                1001 group
                    1003 test
                1000 group
                    1002 test
        """
    )
    local_state = str(server.query_local_nodes())
    assert local_state == remote_state

    with server.osc_protocol.capture() as transcript:
        osc_message = supriya.osc.OscMessage(
            "/n_after", synth_b.node_id, synth_a.node_id
        )
        server.send(osc_message)
        server.sync()

    assert [(_.label, _.message) for _ in transcript] == [
        ("S", supriya.osc.OscMessage("/n_after", 1003, 1002)),
        ("S", supriya.osc.OscMessage("/sync", 0)),
        ("R", supriya.osc.OscMessage("/n_move", 1003, 1000, 1002, -1, 0)),
        ("R", supriya.osc.OscMessage("/synced", 0)),
    ]

    remote_state = str(server.query_remote_nodes())
    assert remote_state == uqbar.strings.normalize(
        """
        NODE TREE 0 group
            1 group
                1001 group
                1000 group
                    1002 test
                    1003 test
        """
    )
    local_state = str(server.query_local_nodes())
    assert local_state == remote_state

    with server.osc_protocol.capture() as transcript:
        osc_message = supriya.osc.OscMessage(
            "/n_order", 0, group_b.node_id, synth_b.node_id, synth_a.node_id
        )
        server.send(osc_message)
        server.sync()

    assert [(_.label, _.message) for _ in transcript] == [
        ("S", supriya.osc.OscMessage("/n_order", 0, 1001, 1003, 1002)),
        ("S", supriya.osc.OscMessage("/sync", 1)),
        ("R", supriya.osc.OscMessage("/n_move", 1003, 1001, -1, -1, 0)),
        ("R", supriya.osc.OscMessage("/n_move", 1002, 1001, 1003, -1, 0)),
        ("R", supriya.osc.OscMessage("/synced", 1)),
    ]

    remote_state = str(server.query_remote_nodes())
    assert remote_state == uqbar.strings.normalize(
        """
        NODE TREE 0 group
            1 group
                1001 group
                    1003 test
                    1002 test
                1000 group
        """
    )
    local_state = str(server.query_local_nodes())
    assert local_state == remote_state
