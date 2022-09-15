import pytest
from uqbar.strings import normalize

import supriya
import supriya.assets.synthdefs
import supriya.osc
import supriya.realtime
from supriya.osc import OscBundle, OscMessage


@pytest.fixture(autouse=True)
def shutdown_sync_servers(shutdown_scsynth):
    pass


@pytest.fixture
def server(persistent_server):
    persistent_server.reset()
    persistent_server.add_synthdef(supriya.assets.synthdefs.default)
    yield persistent_server


@pytest.mark.flaky(reruns=5)
def test__handle_response_01(server):

    group_a = supriya.realtime.Group().allocate(server)
    group_b = supriya.realtime.Group().allocate(server)

    synth_a = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_b = supriya.realtime.Synth(supriya.assets.synthdefs.test)

    group_a.append(synth_a)
    group_b.append(synth_b)

    remote_state = str(server.query())
    assert remote_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1001 group
                    1003 test
                        amplitude: 1.0, frequency: 440.0
                1000 group
                    1002 test
                        amplitude: 1.0, frequency: 440.0
        """
    )
    local_state = str(server.root_node)
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

    remote_state = str(server.query())
    assert remote_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1001 group
                1000 group
                    1002 test
                        amplitude: 1.0, frequency: 440.0
                    1003 test
                        amplitude: 1.0, frequency: 440.0
        """
    )
    local_state = str(server.root_node)
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

    remote_state = str(server.query())
    assert remote_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1001 group
                    1003 test
                        amplitude: 1.0, frequency: 440.0
                    1002 test
                        amplitude: 1.0, frequency: 440.0
                1000 group
        """
    )
    local_state = str(server.root_node)
    assert local_state == remote_state


def test_parentage_01(server):

    root_node = server.root_node
    default_group = server.default_group

    group_a = supriya.realtime.Group().allocate(server)
    group_b = supriya.realtime.Group().allocate(target_node=group_a)
    group_c = supriya.realtime.Group().allocate(target_node=group_b)
    group_d = supriya.realtime.Group().allocate(target_node=group_c)
    synth_a = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_b = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_d.extend([synth_a, synth_b])

    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 group
                        1002 group
                            1003 group
                                1004 test
                                1005 test
        """
    )

    assert group_a.parentage == (group_a, default_group, root_node)

    assert group_b.parentage == (group_b, group_a, default_group, root_node)

    assert group_c.parentage == (group_c, group_b, group_a, default_group, root_node)

    assert group_d.parentage == (
        group_d,
        group_c,
        group_b,
        group_a,
        default_group,
        root_node,
    )

    assert synth_a.parentage == (
        synth_a,
        group_d,
        group_c,
        group_b,
        group_a,
        default_group,
        root_node,
    )

    assert synth_b.parentage == (
        synth_b,
        group_d,
        group_c,
        group_b,
        group_a,
        default_group,
        root_node,
    )

    group_a.succeed_by(group_d)

    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 group
                        1002 group
                1003 group
                    1004 test
                    1005 test
        """
    )

    assert group_d.parentage == (group_d, default_group, root_node)

    assert synth_a.parentage == (synth_a, group_d, default_group, root_node)

    assert synth_b.parentage == (synth_b, group_d, default_group, root_node)


def test_synth_pause_unpause(server):
    synth = supriya.realtime.Synth().allocate(server)
    assert not synth.is_paused
    with server.osc_protocol.capture() as transcript:
        synth.pause()
    assert [
        (_.label, _.message) for _ in transcript if _.message.address != "/status.reply"
    ] == [("S", OscMessage("/n_run", 1000, 0))]
    assert synth.is_paused
    with server.osc_protocol.capture() as transcript:
        synth.pause()
    assert list(transcript) == []
    assert synth.is_paused
    with server.osc_protocol.capture() as transcript:
        synth.unpause()
    assert [
        (_.label, _.message) for _ in transcript if _.message.address != "/status.reply"
    ] == [("S", OscMessage("/n_run", 1000, 1))]
    assert not synth.is_paused
    with server.osc_protocol.capture() as transcript:
        synth.unpause()
    assert list(transcript) == []
    assert not synth.is_paused


def test_group_pause_unpause(server):
    group = supriya.realtime.Group().allocate(server)
    assert not group.is_paused
    with server.osc_protocol.capture() as transcript:
        group.pause()
    assert [
        (_.label, _.message) for _ in transcript if _.message.address != "/status.reply"
    ] == [("S", OscMessage("/n_run", 1000, 0))]
    assert group.is_paused
    with server.osc_protocol.capture() as transcript:
        group.pause()
    assert list(transcript) == []
    assert group.is_paused
    with server.osc_protocol.capture() as transcript:
        group.unpause()
    assert [(_.label, _.message) for _ in transcript] == [
        ("S", OscMessage("/n_run", 1000, 1))
    ]
    assert not group.is_paused
    with server.osc_protocol.capture() as transcript:
        group.unpause()
    assert list(transcript) == []
    assert not group.is_paused


def test_synth_allocate_free_paused(server):
    synth = supriya.realtime.Synth(synthdef=supriya.assets.synthdefs.test)
    synth.pause()
    assert synth.is_paused
    with server.osc_protocol.capture() as transcript:
        synth.allocate(server)
    bundle = OscBundle(
        contents=(
            OscMessage("/s_new", "test", 1000, 0, 1),
            OscMessage("/n_run", 1000, 0),
        )
    )
    assert [(_.label, _.message) for _ in transcript] == [
        ("S", OscMessage("/d_recv", supriya.assets.synthdefs.test.compile(), bundle)),
        ("R", OscMessage("/n_go", 1000, 1, -1, -1, 0)),
        ("R", OscMessage("/n_off", 1000, 1, -1, -1, 0)),
        ("R", OscMessage("/done", "/d_recv")),
    ]
    assert synth.is_paused
    with server.osc_protocol.capture() as transcript:
        synth.free()
    assert [(_.label, _.message) for _ in transcript] == [
        ("S", OscMessage("/n_free", 1000))
    ]
    assert synth.is_paused
    synth.unpause()
    assert not synth.is_paused


def test_group_allocate_paused(server):
    group = supriya.realtime.Group()
    group.pause()
    assert group.is_paused
    with server.osc_protocol.capture() as transcript:
        group.allocate(server)
    assert [(_.label, _.message) for _ in transcript] == [
        (
            "S",
            OscBundle(
                contents=(
                    OscMessage("/g_new", 1000, 0, 1),
                    OscMessage("/n_run", 1000, 0),
                    OscMessage("/sync", 0),
                )
            ),
        ),
        ("R", OscMessage("/n_go", 1000, 1, -1, -1, 1, -1, -1)),
        ("R", OscMessage("/n_off", 1000, 1, -1, -1, 1, -1, -1)),
        ("R", OscMessage("/synced", 0)),
    ]
    assert group.is_paused
    with server.osc_protocol.capture() as transcript:
        group.free()
    assert [(_.label, _.message) for _ in transcript] == [
        ("S", OscMessage("/n_free", 1000))
    ]
    assert group.is_paused
    group.unpause()
    assert not group.is_paused


def test_group_allocate_nested_paused(server):
    group = supriya.realtime.Group(
        [supriya.realtime.Synth(), supriya.realtime.Group([supriya.realtime.Synth()])]
    )
    group[0].pause()
    group[1][0].pause()
    assert not group.is_paused
    assert group[0].is_paused
    assert not group[1].is_paused
    assert group[1][0].is_paused
    with server.osc_protocol.capture() as transcript:
        group.allocate(server)
    assert [(_.label, _.message) for _ in transcript] == [
        (
            "S",
            OscBundle(
                contents=(
                    OscMessage("/g_new", 1000, 0, 1),
                    OscMessage("/s_new", "default", 1001, 0, 1000),
                    OscMessage("/g_new", 1002, 3, 1001),
                    OscMessage("/s_new", "default", 1003, 0, 1002),
                    OscMessage("/n_run", 1001, 0, 1003, 0),
                    OscMessage("/sync", 0),
                )
            ),
        ),
        ("R", OscMessage("/n_go", 1000, 1, -1, -1, 1, -1, -1)),
        ("R", OscMessage("/n_go", 1001, 1000, -1, -1, 0)),
        ("R", OscMessage("/n_go", 1002, 1000, 1001, -1, 1, -1, -1)),
        ("R", OscMessage("/n_go", 1003, 1002, -1, -1, 0)),
        ("R", OscMessage("/n_off", 1001, 1000, -1, 1002, 0)),
        ("R", OscMessage("/n_off", 1003, 1002, -1, -1, 0)),
        ("R", OscMessage("/synced", 0)),
    ]
    assert not group.is_paused
    assert group[0].is_paused
    assert not group[1].is_paused
    assert group[1][0].is_paused
    with server.osc_protocol.capture() as transcript:
        group.free()
    assert [(_.label, _.message) for _ in transcript] == [
        ("S", OscMessage("/n_free", 1000))
    ]
    assert not group.is_paused
    assert group[0].is_paused
    assert not group[1].is_paused
    assert group[1][0].is_paused


def test_precede_by(server):
    synth_a = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_b = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_c = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_d = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_e = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_a.allocate(server)
    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 test
        """
    )
    synth_a.precede_by(synth_b)
    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1001 test
                1000 test
        """
    )
    synth_a.precede_by([synth_c, synth_d])
    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1001 test
                1002 test
                1003 test
                1000 test
        """
    )
    synth_a.precede_by([synth_e, synth_b])
    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1002 test
                1003 test
                1004 test
                1001 test
                1000 test
        """
    )


def test_replace_with(server):
    synth_a = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_b = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_c = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_d = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_e = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_a.allocate(server)
    synth_b.allocate(server)
    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1001 test
                1000 test
        """
    )
    synth_a.replace_with(synth_c)
    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1001 test
                1002 test
        """
    )
    synth_b.replace_with([synth_d, synth_e])
    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1003 test
                1004 test
                1002 test
        """
    )
    synth_c.replace_with([synth_a, synth_e])
    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1003 test
                1005 test
                1004 test
        """
    )


def test_succeed_by(server):
    synth_a = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_b = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_c = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_d = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_e = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_a.allocate(server)
    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 test
        """
    )
    synth_a.succeed_by(synth_b)
    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 test
                1001 test
        """
    )
    synth_a.succeed_by([synth_c, synth_d])
    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 test
                1002 test
                1003 test
                1001 test
        """
    )
    synth_a.succeed_by([synth_e, synth_b])
    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 test
                1004 test
                1001 test
                1002 test
                1003 test
        """
    )
