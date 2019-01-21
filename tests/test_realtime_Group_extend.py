import uqbar.strings

import supriya.assets.synthdefs
import supriya.realtime


def test_noop(server):
    group = supriya.realtime.Group().allocate()
    server_state = str(server.query_remote_nodes(True))
    assert server_state == uqbar.strings.normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
        """
    )
    assert str(server.query_local_nodes(include_controls=True)) == server_state
    with server.osc_io.capture() as transcript:
        group.extend([])
    assert [(_.label, _.message) for _ in transcript] == []
    server_state = str(server.query_remote_nodes(True))
    assert server_state == uqbar.strings.normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
        """
    )
    assert str(server.query_local_nodes(include_controls=True)) == server_state


def test_allocate_nested(server):
    group = supriya.realtime.Group()
    synth_a = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_b = supriya.realtime.Synth(supriya.assets.synthdefs.test, amplitude=0.0)
    group.extend([synth_a, synth_b])
    with server.osc_io.capture() as transcript:
        group.allocate()
    server_state = str(server.query_remote_nodes(True))
    assert server_state == uqbar.strings.normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 test
                        amplitude: 1.0, frequency: 440.0
                    1002 test
                        amplitude: 0.0, frequency: 440.0
        """
    )
    assert str(server.query_local_nodes(include_controls=True)) == server_state
    bundle = supriya.osc.OscBundle(
        contents=(
            supriya.osc.OscMessage(21, 1000, 0, 1),
            supriya.osc.OscMessage(9, "test", 1001, 0, 1000),
            supriya.osc.OscMessage(9, "test", 1002, 3, 1001, "amplitude", 0.0),
        )
    )
    assert [(_.label, _.message) for _ in transcript] == [
        (
            "S",
            supriya.osc.OscMessage(
                5, bytearray(supriya.assets.synthdefs.test.compile()), bundle
            ),
        ),
        ("R", supriya.osc.OscMessage("/n_go", 1000, 1, -1, -1, 1, -1, -1)),
        ("R", supriya.osc.OscMessage("/n_go", 1001, 1000, -1, -1, 0)),
        ("R", supriya.osc.OscMessage("/n_go", 1002, 1000, 1001, -1, 0)),
        ("R", supriya.osc.OscMessage("/done", "/d_recv")),
    ]


def test_extend_unallocated(server):
    group = supriya.realtime.Group()
    group.allocate()
    synth_a = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_b = supriya.realtime.Synth(supriya.assets.synthdefs.test, amplitude=0.0)
    with server.osc_io.capture() as transcript:
        group.extend([synth_a, synth_b])
    server_state = str(server.query_remote_nodes(True))
    assert server_state == uqbar.strings.normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 test
                        amplitude: 1.0, frequency: 440.0
                    1002 test
                        amplitude: 0.0, frequency: 440.0
        """
    )
    assert str(server.query_local_nodes(include_controls=True)) == server_state
    bundle = supriya.osc.OscBundle(
        contents=(
            supriya.osc.OscMessage(9, "test", 1001, 0, 1000),
            supriya.osc.OscMessage(9, "test", 1002, 3, 1001, "amplitude", 0.0),
        )
    )
    assert [(_.label, _.message) for _ in transcript] == [
        (
            "S",
            supriya.osc.OscMessage(5, supriya.assets.synthdefs.test.compile(), bundle),
        ),
        ("R", supriya.osc.OscMessage("/n_go", 1001, 1000, -1, -1, 0)),
        ("R", supriya.osc.OscMessage("/n_go", 1002, 1000, 1001, -1, 0)),
        ("R", supriya.osc.OscMessage("/done", "/d_recv")),
    ]


def test_extend_allocate_nested_and_move(server):
    synth = supriya.realtime.Synth().allocate()
    synthdef = supriya.assets.synthdefs.test
    group_a = supriya.realtime.Group().allocate()
    group_b = supriya.realtime.Group(
        [
            supriya.realtime.Synth(synthdef=synthdef),
            supriya.realtime.Group([supriya.realtime.Synth(synthdef=synthdef)]),
        ]
    )
    server_state = str(server.query_remote_nodes())
    assert server_state == uqbar.strings.normalize(
        """
        NODE TREE 0 group
            1 group
                1001 group
                1000 default
        """
    )
    assert str(server.query_local_nodes()) == server_state
    with server.osc_io.capture() as transcript:
        group_a.extend([group_b, synth])
    bundle = supriya.osc.OscBundle(
        contents=(
            supriya.osc.OscMessage(21, 1002, 0, 1001),
            supriya.osc.OscMessage(9, "test", 1003, 0, 1002),
            supriya.osc.OscMessage(21, 1004, 3, 1003),
            supriya.osc.OscMessage(9, "test", 1005, 0, 1004),
            supriya.osc.OscMessage(19, 1000, 1002),
        )
    )
    assert [(_.label, _.message) for _ in transcript] == [
        (
            "S",
            supriya.osc.OscMessage(5, supriya.assets.synthdefs.test.compile(), bundle),
        ),
        ("R", supriya.osc.OscMessage("/n_go", 1002, 1001, -1, -1, 1, -1, -1)),
        ("R", supriya.osc.OscMessage("/n_go", 1003, 1002, -1, -1, 0)),
        ("R", supriya.osc.OscMessage("/n_go", 1004, 1002, 1003, -1, 1, -1, -1)),
        ("R", supriya.osc.OscMessage("/n_go", 1005, 1004, -1, -1, 0)),
        ("R", supriya.osc.OscMessage("/n_move", 1000, 1001, 1002, -1, 0)),
        ("R", supriya.osc.OscMessage("/done", "/d_recv")),
    ]
    server_state = str(server.query_remote_nodes())
    assert server_state == uqbar.strings.normalize(
        """
        NODE TREE 0 group
            1 group
                1001 group
                    1002 group
                        1003 test
                        1004 group
                            1005 test
                    1000 default
        """
    )
    assert str(server.query_local_nodes()) == server_state


def test_x(server):
    group_a = supriya.realtime.Group()
    group_a.allocate(target_node=server)
    group_b = supriya.realtime.Group()
    group_b.allocate(target_node=server)
    server_state = str(server.query_remote_nodes())
    assert server_state == uqbar.strings.normalize(
        """
        NODE TREE 0 group
            1 group
                1001 group
                1000 group
        """
    )
    synthdef = supriya.assets.synthdefs.test
    assert not synthdef.is_allocated
    synth_a = supriya.realtime.Synth(synthdef)
    synth_b = supriya.realtime.Synth(synthdef)
    synth_c = supriya.realtime.Synth(synthdef)
    synth_d = supriya.realtime.Synth(synthdef)
    assert not synth_a.is_allocated
    assert not synth_b.is_allocated
    assert not synth_c.is_allocated
    assert not synth_d.is_allocated
    synth_a.allocate()
    server_state = str(server.query_remote_nodes())
    assert server_state == uqbar.strings.normalize(
        """
        NODE TREE 0 group
            1 group
                1002 test
                1001 group
                1000 group
        """
    )
    group_a.extend([synth_a, synth_b])
    server_state = str(server.query_remote_nodes())
    assert server_state == uqbar.strings.normalize(
        """
        NODE TREE 0 group
            1 group
                1001 group
                1000 group
                    1002 test
                    1003 test
        """
    )
    group_b.extend([synth_c])
    server_state = str(server.query_remote_nodes())
    assert server_state == uqbar.strings.normalize(
        """
        NODE TREE 0 group
            1 group
                1001 group
                    1004 test
                1000 group
                    1002 test
                    1003 test
        """
    )
    group_b.extend([synth_d, synth_b, synth_a])
    server_state = str(server.query_remote_nodes())
    assert server_state == uqbar.strings.normalize(
        """
        NODE TREE 0 group
            1 group
                1001 group
                    1004 test
                    1005 test
                    1003 test
                    1002 test
                1000 group
        """
    )
