import pytest
from uqbar.strings import normalize

import supriya
import supriya.assets.synthdefs
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


def test___contains___01(server):
    group_a = supriya.realtime.Group()
    group_a.allocate(server)
    synth_a = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_a.append(synth_a)
    group_b = supriya.realtime.Group()
    group_a.append(group_b)
    synth_b = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_b.append(synth_b)
    synth_c = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_b.append(synth_c)
    group_c = supriya.realtime.Group()
    group_b.append(group_c)
    synth_d = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_a.append(synth_d)
    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 test
                    1002 group
                        1003 test
                        1004 test
                        1005 group
                    1006 test
        """
    )

    assert group_a not in group_a
    assert group_b in group_a
    assert group_c not in group_a
    assert synth_a in group_a
    assert synth_b not in group_a
    assert synth_c not in group_a
    assert synth_d in group_a

    assert group_a not in group_b
    assert group_b not in group_b
    assert group_c in group_b
    assert synth_a not in group_b
    assert synth_b in group_b
    assert synth_c in group_b
    assert synth_d not in group_b

    assert group_a not in group_c
    assert group_b not in group_c
    assert group_c not in group_c
    assert synth_a not in group_c
    assert synth_b not in group_c
    assert synth_c not in group_c
    assert synth_d not in group_c


def test___delitem___01(server):

    group_a = supriya.realtime.Group()
    group_a.allocate(server)
    synth_a = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_a.append(synth_a)
    group_b = supriya.realtime.Group()
    group_a.append(group_b)
    synth_b = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_b.append(synth_b)
    synth_c = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_b.append(synth_c)
    group_c = supriya.realtime.Group()
    group_b.append(group_c)
    synth_d = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_a.append(synth_d)

    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 test
                    1002 group
                        1003 test
                        1004 test
                        1005 group
                    1006 test
        """
    )

    del group_a[-1]

    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 test
                    1002 group
                        1003 test
                        1004 test
                        1005 group
        """
    )

    del group_b[1]

    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 test
                    1002 group
                        1003 test
                        1005 group
        """
    )

    del group_a[0]

    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1002 group
                        1003 test
                        1005 group
        """
    )

    del group_b[1]

    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1002 group
                        1003 test
        """
    )

    del group_a[0]

    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
        """
    )

    assert not group_b.is_allocated
    assert not group_c.is_allocated
    assert not synth_a.is_allocated
    assert not synth_b.is_allocated
    assert not synth_c.is_allocated
    assert not synth_d.is_allocated


def test___getitem___01(server):

    group_a = supriya.realtime.Group()
    group_a.allocate(server)
    synth_a = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_a.append(synth_a)
    group_b = supriya.realtime.Group()
    group_a.append(group_b)
    synth_b = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_b.append(synth_b)
    synth_c = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_b.append(synth_c)
    group_c = supriya.realtime.Group()
    group_b.append(group_c)
    synth_d = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_a.append(synth_d)

    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 test
                    1002 group
                        1003 test
                        1004 test
                        1005 group
                    1006 test
        """
    )

    assert group_a[0] is synth_a
    assert group_a[1] is group_b
    assert group_a[2] is synth_d

    assert group_b[0] is synth_b
    assert group_b[1] is synth_c
    assert group_b[2] is group_c

    assert group_a[-1] is synth_d
    assert group_a[-2] is group_b
    assert group_a[-3] is synth_a

    assert group_b[-1] is group_c
    assert group_b[-2] is synth_c
    assert group_b[-3] is synth_b

    assert group_a[:] == [synth_a, group_b, synth_d]
    assert group_a[1:] == [group_b, synth_d]
    assert group_a[1:-1] == [group_b]
    assert group_a[2:] == [synth_d]
    assert group_a[:-1] == [synth_a, group_b]
    assert group_a[:-2] == [synth_a]

    assert group_b[:] == [synth_b, synth_c, group_c]
    assert group_b[1:] == [synth_c, group_c]
    assert group_b[1:-1] == [synth_c]
    assert group_b[2:] == [group_c]
    assert group_b[:-1] == [synth_b, synth_c]
    assert group_b[:-2] == [synth_b]


def test___graph___01(server):
    outer_group = supriya.Group()
    inner_group = supriya.Group()
    synth_a = supriya.Synth()
    synth_b = supriya.Synth()
    synth_c = supriya.Synth()
    outer_group.extend([synth_a, inner_group, synth_c])
    inner_group.append(synth_b)
    assert format(outer_group.__graph__(), "graphviz") == normalize(
        """
        digraph G {
            graph [bgcolor=transparent,
                color=lightslategrey,
                dpi=72,
                fontname=Arial,
                outputorder=edgesfirst,
                overlap=prism,
                penwidth=2,
                rankdir=TB,
                ranksep=0.5,
                splines=spline,
                style="dotted, rounded"];
            node [fontname=Arial,
                fontsize=12,
                penwidth=2,
                shape=Mrecord,
                style="filled, rounded"];
            edge [penwidth=2];
            group [fillcolor=lightsteelblue2,
                label="{ <f_0_0> Group | <f_0_1> id: 0 }"];
            "synth-0" [fillcolor=lightgoldenrod2,
                label="{ <f_0_0> Synth | <f_0_1> id: 0-0 }"];
            "group-1" [fillcolor=lightsteelblue2,
                label="{ <f_0_0> Group | <f_0_1> id: 0-1 }"];
            "synth-1-0" [fillcolor=lightgoldenrod2,
                label="{ <f_0_0> Synth | <f_0_1> id: 0-1-0 }"];
            "synth-2" [fillcolor=lightgoldenrod2,
                label="{ <f_0_0> Synth | <f_0_1> id: 0-2 }"];
            group -> "synth-0";
            group -> "group-1";
            group -> "synth-2";
            "group-1" -> "synth-1-0";
        }
        """
    )
    outer_group.allocate(server)
    assert format(outer_group.__graph__(), "graphviz") == normalize(
        """
        digraph G {
            graph [bgcolor=transparent,
                color=lightslategrey,
                dpi=72,
                fontname=Arial,
                outputorder=edgesfirst,
                overlap=prism,
                penwidth=2,
                rankdir=TB,
                ranksep=0.5,
                splines=spline,
                style="dotted, rounded"];
            node [fontname=Arial,
                fontsize=12,
                penwidth=2,
                shape=Mrecord,
                style="filled, rounded"];
            edge [penwidth=2];
            "group-1000" [fillcolor=lightsteelblue2,
                label="{ <f_0_0> Group | <f_0_1> id: 1000 }"];
            "synth-1001" [fillcolor=lightgoldenrod2,
                label="{ <f_0_0> Synth | <f_0_1> id: 1001 }"];
            "group-1002" [fillcolor=lightsteelblue2,
                label="{ <f_0_0> Group | <f_0_1> id: 1002 }"];
            "synth-1003" [fillcolor=lightgoldenrod2,
                label="{ <f_0_0> Synth | <f_0_1> id: 1003 }"];
            "synth-1004" [fillcolor=lightgoldenrod2,
                label="{ <f_0_0> Synth | <f_0_1> id: 1004 }"];
            "group-1000" -> "synth-1001";
            "group-1000" -> "group-1002";
            "group-1000" -> "synth-1004";
            "group-1002" -> "synth-1003";
        }
        """
    )
    outer_group.free()
    assert format(outer_group.__graph__(), "graphviz") == normalize(
        """
        digraph G {
            graph [bgcolor=transparent,
                color=lightslategrey,
                dpi=72,
                fontname=Arial,
                outputorder=edgesfirst,
                overlap=prism,
                penwidth=2,
                rankdir=TB,
                ranksep=0.5,
                splines=spline,
                style="dotted, rounded"];
            node [fontname=Arial,
                fontsize=12,
                penwidth=2,
                shape=Mrecord,
                style="filled, rounded"];
            edge [penwidth=2];
            group [fillcolor=lightsteelblue2,
                label="{ <f_0_0> Group | <f_0_1> id: 0 }"];
            "synth-0" [fillcolor=lightgoldenrod2,
                label="{ <f_0_0> Synth | <f_0_1> id: 0-0 }"];
            "group-1" [fillcolor=lightsteelblue2,
                label="{ <f_0_0> Group | <f_0_1> id: 0-1 }"];
            "synth-1-0" [fillcolor=lightgoldenrod2,
                label="{ <f_0_0> Synth | <f_0_1> id: 0-1-0 }"];
            "synth-2" [fillcolor=lightgoldenrod2,
                label="{ <f_0_0> Synth | <f_0_1> id: 0-2 }"];
            group -> "synth-0";
            group -> "group-1";
            group -> "synth-2";
            "group-1" -> "synth-1-0";
        }
        """
    )


def test___iter___01(server):

    group_a = supriya.realtime.Group()
    group_a.allocate(server)
    synth_a = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_a.append(synth_a)
    group_b = supriya.realtime.Group()
    group_a.append(group_b)
    synth_b = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_b.append(synth_b)
    synth_c = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_b.append(synth_c)
    group_c = supriya.realtime.Group()
    group_b.append(group_c)
    synth_d = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_a.append(synth_d)

    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 test
                    1002 group
                        1003 test
                        1004 test
                        1005 group
                    1006 test
        """
    )

    assert [x for x in group_a] == [synth_a, group_b, synth_d]

    assert [x for x in group_b] == [synth_b, synth_c, group_c]

    assert [x for x in group_c] == []


def test___len___01(server):

    group_a = supriya.realtime.Group()
    group_a.allocate(server)

    assert len(group_a) == 0

    synth_a = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_a.append(synth_a)

    assert len(group_a) == 1

    group_b = supriya.realtime.Group()
    group_a.append(group_b)

    assert len(group_a) == 2
    assert len(group_b) == 0

    synth_b = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_b.append(synth_b)

    assert len(group_a) == 2
    assert len(group_b) == 1

    synth_c = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_b.append(synth_c)

    assert len(group_a) == 2
    assert len(group_b) == 2

    synth_d = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_a.append(synth_d)

    assert len(group_a) == 3
    assert len(group_b) == 2

    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 test
                    1002 group
                        1003 test
                        1004 test
                    1005 test
        """
    )

    assert len(group_a) == 3
    assert len(group_b) == 2

    group_a.pop()

    assert len(group_a) == 2

    group_b.pop()

    assert len(group_b) == 1

    group_a.pop()

    assert len(group_a) == 1
    assert len(group_b) == 1
    assert not group_b[0].is_allocated

    group_a.pop()

    assert len(group_a) == 0

    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
        """
    )


def test___setitem___01(server):

    group = supriya.realtime.Group().allocate(server)
    assert len(group) == 0
    remote_state = str(server.query())
    assert remote_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
        """
    )

    synth = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    assert synth.parent is None
    assert not synth.is_allocated

    group[:] = [synth]
    assert len(group) == 1
    assert synth.parent is group
    assert synth in group
    assert synth.is_allocated
    remote_state = str(server.query())
    assert remote_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 test
                        amplitude: 1.0, frequency: 440.0
        """
    )

    group[:] = []
    assert len(group) == 0
    assert synth.parent is None
    assert synth not in group
    assert not synth.is_allocated
    remote_state = str(server.query())
    assert remote_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
        """
    )


def test___setitem___02(server):

    group = supriya.realtime.Group().allocate(server)
    synth_a = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_b = supriya.realtime.Synth(supriya.assets.synthdefs.test)

    group[:] = [synth_a, synth_b]
    assert len(group) == 2
    assert synth_a.parent is group
    assert synth_b.parent is group
    assert synth_a in group
    assert synth_b in group
    assert synth_a.is_allocated
    assert synth_b.is_allocated
    assert synth_a is group[0]
    assert synth_b is group[1]
    remote_state = str(server.query())
    assert remote_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 test
                        amplitude: 1.0, frequency: 440.0
                    1002 test
                        amplitude: 1.0, frequency: 440.0
        """
    )

    group[:] = [synth_b, synth_a]
    assert len(group) == 2
    assert synth_a.parent is group
    assert synth_b.parent is group
    assert synth_a in group
    assert synth_b in group
    assert synth_a.is_allocated
    assert synth_b.is_allocated
    assert synth_a is group[1]
    assert synth_b is group[0]
    remote_state = str(server.query())
    assert remote_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1002 test
                        amplitude: 1.0, frequency: 440.0
                    1001 test
                        amplitude: 1.0, frequency: 440.0
        """
    )

    group[:] = []
    assert len(group) == 0
    assert synth_a.parent is None
    assert synth_b.parent is None
    assert synth_a not in group
    assert synth_b not in group
    assert not synth_a.is_allocated
    assert not synth_b.is_allocated
    remote_state = str(server.query())
    assert remote_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
        """
    )


def test___setitem___03(server):

    group_a = supriya.realtime.Group()
    group_a.allocate(server)

    synth_a = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_a.append(synth_a)

    group_b = supriya.realtime.Group()
    group_a.append(group_b)

    synth_b = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_b.append(synth_b)

    synth_c = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_b.append(synth_c)

    group_c = supriya.realtime.Group()
    group_b.append(group_c)

    synth_d = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_a.append(synth_d)

    remote_state = str(server.query())
    assert remote_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 test
                        amplitude: 1.0, frequency: 440.0
                    1002 group
                        1003 test
                            amplitude: 1.0, frequency: 440.0
                        1004 test
                            amplitude: 1.0, frequency: 440.0
                        1005 group
                    1006 test
                        amplitude: 1.0, frequency: 440.0
        """
    )

    assert len(group_a) == 3
    assert len(group_b) == 3
    assert len(group_c) == 0

    assert synth_a.parent is group_a
    assert synth_b.parent is group_b
    assert synth_c.parent is group_b
    assert synth_d.parent is group_a
    assert group_b.parent is group_a
    assert group_c.parent is group_b

    assert synth_a is group_a[0]
    assert synth_b is group_b[0]
    assert synth_c is group_b[1]
    assert synth_d is group_a[2]
    assert group_b is group_a[1]
    assert group_c is group_b[2]

    del group_a[-1]

    remote_state = str(server.query())
    assert remote_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 test
                        amplitude: 1.0, frequency: 440.0
                    1002 group
                        1003 test
                            amplitude: 1.0, frequency: 440.0
                        1004 test
                            amplitude: 1.0, frequency: 440.0
                        1005 group
        """
    )

    assert len(group_a) == 2
    assert len(group_b) == 3
    assert len(group_c) == 0

    assert synth_a.parent is group_a
    assert synth_b.parent is group_b
    assert synth_c.parent is group_b
    assert synth_d.parent is None
    assert group_b.parent is group_a
    assert group_c.parent is group_b

    assert synth_a is group_a[0]
    assert synth_b is group_b[0]
    assert synth_c is group_b[1]
    assert synth_d not in group_a
    assert group_b is group_a[1]
    assert group_c is group_b[2]

    del group_b[1]

    remote_state = str(server.query())
    assert remote_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 test
                        amplitude: 1.0, frequency: 440.0
                    1002 group
                        1003 test
                            amplitude: 1.0, frequency: 440.0
                        1005 group
        """
    )

    assert len(group_a) == 2
    assert len(group_b) == 2
    assert len(group_c) == 0

    assert synth_a.parent is group_a
    assert synth_b.parent is group_b
    assert synth_c.parent is None
    assert synth_d.parent is None
    assert group_b.parent is group_a
    assert group_c.parent is group_b

    assert synth_a is group_a[0]
    assert synth_b is group_b[0]
    assert synth_c not in group_b
    assert synth_d not in group_a
    assert group_b is group_a[1]
    assert group_c is group_b[1]

    del group_a[0]

    remote_state = str(server.query())
    assert remote_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1002 group
                        1003 test
                            amplitude: 1.0, frequency: 440.0
                        1005 group
        """
    )

    assert len(group_a) == 1
    assert len(group_b) == 2
    assert len(group_c) == 0

    assert synth_a.parent is None
    assert synth_b.parent is group_b
    assert synth_c.parent is None
    assert synth_d.parent is None
    assert group_b.parent is group_a
    assert group_c.parent is group_b

    assert synth_a not in group_a
    assert synth_b is group_b[0]
    assert synth_c not in group_b
    assert synth_d not in group_a
    assert group_b is group_a[0]
    assert group_c is group_b[1]

    del group_b[1]

    remote_state = str(server.query())
    assert remote_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1002 group
                        1003 test
                            amplitude: 1.0, frequency: 440.0
        """
    )

    assert len(group_a) == 1
    assert len(group_b) == 1
    assert len(group_c) == 0

    assert synth_a.parent is None
    assert synth_b.parent is group_b
    assert synth_c.parent is None
    assert synth_d.parent is None
    assert group_b.parent is group_a
    assert group_c.parent is None

    assert synth_a not in group_a
    assert synth_b is group_b[0]
    assert synth_c not in group_b
    assert synth_d not in group_a
    assert group_b is group_a[0]
    assert group_c not in group_b

    del group_a[0]

    remote_state = str(server.query())
    assert remote_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
        """
    )

    assert len(group_a) == 0
    assert len(group_b) == 1
    assert len(group_c) == 0

    assert synth_a.parent is None
    assert synth_b.parent is group_b
    assert synth_c.parent is None
    assert synth_d.parent is None
    assert group_b.parent is None
    assert group_c.parent is None

    assert synth_a not in group_a
    assert synth_b is group_b[0]
    assert synth_c not in group_b
    assert synth_d not in group_a
    assert group_b not in group_a
    assert group_c not in group_b

    assert not synth_b.is_allocated


def test___setitem___04(server):

    group_a = supriya.realtime.Group().allocate(server)
    group_b = supriya.realtime.Group().allocate(server)

    synth_a = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_b = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_c = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_d = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_e = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_f = supriya.realtime.Synth(supriya.assets.synthdefs.test)

    local_state = str(server.root_node)
    remote_state = str(server.query())
    assert remote_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1001 group
                1000 group
        """
    )
    assert local_state == remote_state
    assert len(group_a) == 0
    assert len(group_b) == 0

    group_a[:] = [synth_a, synth_b]

    local_state = str(server.root_node)
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
    assert local_state == remote_state
    assert len(group_a) == 2
    assert len(group_b) == 0

    group_a[:] = [synth_b, synth_a]

    local_state = str(server.root_node)
    remote_state = str(server.query())
    assert remote_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1001 group
                1000 group
                    1003 test
                        amplitude: 1.0, frequency: 440.0
                    1002 test
                        amplitude: 1.0, frequency: 440.0
        """
    )
    assert local_state == remote_state
    assert len(group_a) == 2
    assert len(group_b) == 0

    group_a[:] = [synth_c, synth_d, synth_b, synth_a]

    local_state = str(server.root_node)
    remote_state = str(server.query())
    assert remote_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1001 group
                1000 group
                    1004 test
                        amplitude: 1.0, frequency: 440.0
                    1005 test
                        amplitude: 1.0, frequency: 440.0
                    1003 test
                        amplitude: 1.0, frequency: 440.0
                    1002 test
                        amplitude: 1.0, frequency: 440.0
        """
    )
    assert local_state == remote_state
    assert len(group_a) == 4
    assert len(group_b) == 0

    group_b[1:-1] = [synth_c, synth_b]

    local_state = str(server.root_node)
    remote_state = str(server.query())
    assert remote_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1001 group
                    1004 test
                        amplitude: 1.0, frequency: 440.0
                    1003 test
                        amplitude: 1.0, frequency: 440.0
                1000 group
                    1005 test
                        amplitude: 1.0, frequency: 440.0
                    1002 test
                        amplitude: 1.0, frequency: 440.0
        """
    )
    assert local_state == remote_state
    assert len(group_a) == 2
    assert len(group_b) == 2

    group_b[1:-1] = [synth_b, synth_c, synth_e]

    local_state = str(server.root_node)
    remote_state = str(server.query())
    assert remote_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1001 group
                    1003 test
                        amplitude: 1.0, frequency: 440.0
                    1004 test
                        amplitude: 1.0, frequency: 440.0
                    1006 test
                        amplitude: 1.0, frequency: 440.0
                1000 group
                    1005 test
                        amplitude: 1.0, frequency: 440.0
                    1002 test
                        amplitude: 1.0, frequency: 440.0
        """
    )
    assert local_state == remote_state
    assert len(group_a) == 2
    assert len(group_b) == 3

    group_a[:] = [synth_c, synth_f]

    local_state = str(server.root_node)
    remote_state = str(server.query())
    assert remote_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1001 group
                    1003 test
                        amplitude: 1.0, frequency: 440.0
                    1006 test
                        amplitude: 1.0, frequency: 440.0
                1000 group
                    1004 test
                        amplitude: 1.0, frequency: 440.0
                    1007 test
                        amplitude: 1.0, frequency: 440.0
        """
    )
    assert local_state == remote_state
    assert len(group_a) == 2
    assert len(group_b) == 2

    group_a[:-1] = [synth_f]

    local_state = str(server.root_node)
    remote_state = str(server.query())
    assert remote_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1001 group
                    1003 test
                        amplitude: 1.0, frequency: 440.0
                    1006 test
                        amplitude: 1.0, frequency: 440.0
                1000 group
                    1007 test
                        amplitude: 1.0, frequency: 440.0
        """
    )
    assert local_state == remote_state
    assert len(group_a) == 1
    assert len(group_b) == 2

    group_b[len(group_b) :] = [group_a]

    local_state = str(server.root_node)
    remote_state = str(server.query())
    assert remote_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1001 group
                    1003 test
                        amplitude: 1.0, frequency: 440.0
                    1006 test
                        amplitude: 1.0, frequency: 440.0
                    1000 group
                        1007 test
                            amplitude: 1.0, frequency: 440.0
        """
    )
    assert local_state == remote_state
    assert len(group_a) == 1
    assert len(group_b) == 3


def test___setitem___05(server):

    group_a = supriya.realtime.Group(name="Group A")
    synth_a = supriya.realtime.Synth(supriya.assets.synthdefs.test, name="Synth A")
    group_a.append(synth_a)

    group_b = supriya.realtime.Group(name="Group B")
    group_a.append(group_b)

    synth_b = supriya.realtime.Synth(supriya.assets.synthdefs.test, name="Synth B")
    group_b.append(synth_b)

    synth_c = supriya.realtime.Synth(supriya.assets.synthdefs.test, name="Synth C")
    group_b.append(synth_c)

    group_c = supriya.realtime.Group(name="Group C")
    group_b.append(group_c)

    synth_d = supriya.realtime.Synth(supriya.assets.synthdefs.test, name="Synth D")
    group_a.append(synth_d)

    synth_e = supriya.realtime.Synth(supriya.assets.synthdefs.test, name="Synth E")

    group_a.allocate(server)

    remote_state = str(server.query())
    assert remote_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 test
                        amplitude: 1.0, frequency: 440.0
                    1002 group
                        1003 test
                            amplitude: 1.0, frequency: 440.0
                        1004 test
                            amplitude: 1.0, frequency: 440.0
                        1005 group
                    1006 test
                        amplitude: 1.0, frequency: 440.0
        """
    )

    group_a_state = str(group_a)
    assert group_a_state == normalize(
        """
        1000 group (Group A)
            1001 test (Synth A)
                amplitude: 1.0, frequency: 440.0
            1002 group (Group B)
                1003 test (Synth B)
                    amplitude: 1.0, frequency: 440.0
                1004 test (Synth C)
                    amplitude: 1.0, frequency: 440.0
                1005 group (Group C)
            1006 test (Synth D)
                amplitude: 1.0, frequency: 440.0
        """
    )

    assert group_a.node_id == 1000
    assert synth_a.node_id == 1001
    assert group_b.node_id == 1002
    assert synth_b.node_id == 1003
    assert synth_c.node_id == 1004
    assert group_c.node_id == 1005
    assert synth_d.node_id == 1006
    assert synth_e.node_id is None

    synth_e.allocate(add_action=supriya.AddAction.REPLACE, target_node=group_a)

    remote_state = str(server.query())
    assert remote_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1007 test
                    amplitude: 1.0, frequency: 440.0
        """
    )

    assert group_a.node_id is None
    assert synth_a.node_id is None
    assert group_b.node_id is None
    assert synth_b.node_id is None
    assert synth_c.node_id is None
    assert group_c.node_id is None
    assert synth_d.node_id is None
    assert synth_e.node_id == 1007

    group_a_state = str(group_a)
    assert group_a_state == normalize(
        """
        ??? group (Group A)
            ??? test (Synth A)
                amplitude: 1.0, frequency: 440.0
            ??? group (Group B)
                ??? test (Synth B)
                    amplitude: 1.0, frequency: 440.0
                ??? test (Synth C)
                    amplitude: 1.0, frequency: 440.0
                ??? group (Group C)
            ??? test (Synth D)
                amplitude: 1.0, frequency: 440.0
        """
    )


def test___setitem___06(server):

    group = supriya.realtime.Group()

    synth_a = supriya.realtime.Synth(
        name="Synth A", synthdef=supriya.assets.synthdefs.test
    )

    synth_b = supriya.realtime.Synth(
        name="Synth B", synthdef=supriya.assets.synthdefs.test
    )
    synth_b["amplitude"] = 0.5
    synth_b["frequency"] = 443

    audio_bus = supriya.realtime.Bus(0, "audio").allocate(server)
    control_bus = supriya.realtime.Bus(1, "control").allocate(server)

    synth_c = supriya.realtime.Synth(
        name="Synth C", synthdef=supriya.assets.synthdefs.test
    )
    synth_c["amplitude"] = audio_bus
    synth_c["frequency"] = control_bus

    group[:] = [synth_a, synth_b, synth_c]

    group_state = str(group)
    assert group_state == normalize(
        """
        ??? group
            ??? test (Synth A)
                amplitude: 1.0, frequency: 440.0
            ??? test (Synth B)
                amplitude: 0.5, frequency: 443.0
            ??? test (Synth C)
                amplitude: a0, frequency: c1
        """
    )

    group.allocate(server)

    group_state = str(group)
    assert group_state == normalize(
        """
        1000 group
            1001 test (Synth A)
                amplitude: 1.0, frequency: 440.0
            1002 test (Synth B)
                amplitude: 0.5, frequency: 443.0
            1003 test (Synth C)
                amplitude: a0, frequency: c1
        """
    )

    remote_state = str(server.query())
    assert remote_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 test
                        amplitude: 1.0, frequency: 440.0
                    1002 test
                        amplitude: 0.5, frequency: 443.0
                    1003 test
                        amplitude: a0, frequency: c1
        """
    )

    synth_b["amplitude", "frequency"] = 0.75, 880
    synth_c["amplitude", "frequency"] = control_bus, audio_bus

    remote_state = str(server.query())
    assert remote_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 test
                        amplitude: 1.0, frequency: 440.0
                    1002 test
                        amplitude: 0.75, frequency: 880.0
                    1003 test
                        amplitude: c1, frequency: a0
        """
    )

    group[:] = [synth_c, synth_b, synth_a]

    remote_state = str(server.query())
    assert remote_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1003 test
                        amplitude: c1, frequency: a0
                    1002 test
                        amplitude: 0.75, frequency: 880.0
                    1001 test
                        amplitude: 1.0, frequency: 440.0
        """
    )

    group.free()

    group_state = str(group)
    assert group_state == normalize(
        """
        ??? group
            ??? test (Synth C)
                amplitude: c1, frequency: a0
            ??? test (Synth B)
                amplitude: 0.75, frequency: 880.0
            ??? test (Synth A)
                amplitude: 1.0, frequency: 440.0
        """
    )


def test_append_01(server):

    group_a = supriya.realtime.Group()
    group_a.allocate(target_node=server)

    group_b = supriya.realtime.Group()
    group_b.allocate(target_node=server)

    synthdef = supriya.assets.synthdefs.test
    assert synthdef not in server

    synth_a = supriya.realtime.Synth(synthdef)
    assert synthdef not in server
    assert not synth_a.is_allocated

    group_a.append(synth_a)
    assert synthdef in server
    assert synth_a.is_allocated
    assert synth_a.parent is group_a
    assert synth_a in group_a
    assert synth_a not in group_b

    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1001 group
                1000 group
                    1002 test
        """
    )

    group_b.append(synth_a)
    assert synthdef in server
    assert synth_a.is_allocated
    assert synth_a.parent is group_b
    assert synth_a in group_b
    assert synth_a not in group_a

    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1001 group
                    1002 test
                1000 group
        """
    )

    synth_b = supriya.realtime.Synth(synthdef)
    assert not synth_b.is_allocated
    assert synth_b.parent is None

    group_b.append(synth_b)
    assert synth_b.is_allocated
    assert synth_b.parent is group_b

    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1001 group
                    1002 test
                    1003 test
                1000 group
        """
    )


def test_extend_noop(server):
    group = supriya.realtime.Group().allocate(server)
    server_state = str(server.query())
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
        """
    )
    assert str(server.root_node) == server_state
    with server.osc_protocol.capture() as transcript:
        group.extend([])
    assert [(_.label, _.message) for _ in transcript] == []
    server_state = str(server.query())
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
        """
    )
    assert str(server.root_node) == server_state


def test_extend_allocate_nested(server):
    group = supriya.realtime.Group()
    synth_a = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_b = supriya.realtime.Synth(supriya.assets.synthdefs.test, amplitude=0.0)
    group.extend([synth_a, synth_b])
    with server.osc_protocol.capture() as transcript:
        group.allocate(server)
    server_state = str(server.query())
    assert server_state == normalize(
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
    assert str(server.root_node) == server_state
    bundle = OscBundle(
        contents=(
            OscMessage("/g_new", 1000, 0, 1),
            OscMessage("/s_new", "test", 1001, 0, 1000),
            OscMessage("/s_new", "test", 1002, 3, 1001, "amplitude", 0.0),
        )
    )
    assert [(_.label, _.message) for _ in transcript] == [
        (
            "S",
            OscMessage(
                "/d_recv", bytearray(supriya.assets.synthdefs.test.compile()), bundle
            ),
        ),
        ("R", OscMessage("/n_go", 1000, 1, -1, -1, 1, -1, -1)),
        ("R", OscMessage("/n_go", 1001, 1000, -1, -1, 0)),
        ("R", OscMessage("/n_go", 1002, 1000, 1001, -1, 0)),
        ("R", OscMessage("/done", "/d_recv")),
    ]


def test_extend_extend_unallocated(server):
    group = supriya.realtime.Group()
    group.allocate(server)
    synth_a = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_b = supriya.realtime.Synth(supriya.assets.synthdefs.test, amplitude=0.0)
    with server.osc_protocol.capture() as transcript:
        group.extend([synth_a, synth_b])
    server_state = str(server.query())
    assert server_state == normalize(
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
    assert str(server.root_node) == server_state
    bundle = OscBundle(
        contents=(
            OscMessage("/s_new", "test", 1001, 0, 1000),
            OscMessage("/s_new", "test", 1002, 3, 1001, "amplitude", 0.0),
        )
    )
    assert [
        (_.label, _.message)
        for _ in transcript
        if _.message.address not in ("/status", "/status.reply")
    ] == [
        ("S", OscMessage("/d_recv", supriya.assets.synthdefs.test.compile(), bundle)),
        ("R", OscMessage("/n_go", 1001, 1000, -1, -1, 0)),
        ("R", OscMessage("/n_go", 1002, 1000, 1001, -1, 0)),
        ("R", OscMessage("/done", "/d_recv")),
    ]


def test_extend_extend_allocate_nested_and_move(server):
    synth = supriya.realtime.Synth().allocate(server)
    synthdef = supriya.assets.synthdefs.test
    group_a = supriya.realtime.Group().allocate(server)
    group_b = supriya.realtime.Group(
        [
            supriya.realtime.Synth(synthdef=synthdef),
            supriya.realtime.Group([supriya.realtime.Synth(synthdef=synthdef)]),
        ]
    )
    server_state = str(server.query())
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1001 group
                1000 default
                    out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5
        """
    )
    assert str(server.root_node) == server_state
    with server.osc_protocol.capture() as transcript:
        group_a.extend([group_b, synth])
    bundle = OscBundle(
        contents=(
            OscMessage("/g_new", 1002, 0, 1001),
            OscMessage("/s_new", "test", 1003, 0, 1002),
            OscMessage("/g_new", 1004, 3, 1003),
            OscMessage("/s_new", "test", 1005, 0, 1004),
            OscMessage("/n_after", 1000, 1002),
        )
    )
    assert [
        (_.label, _.message)
        for _ in transcript
        if _.message.address not in ("/status", "/status.reply")
    ] == [
        ("S", OscMessage("/d_recv", supriya.assets.synthdefs.test.compile(), bundle)),
        ("R", OscMessage("/n_go", 1002, 1001, -1, -1, 1, -1, -1)),
        ("R", OscMessage("/n_go", 1003, 1002, -1, -1, 0)),
        ("R", OscMessage("/n_go", 1004, 1002, 1003, -1, 1, -1, -1)),
        ("R", OscMessage("/n_go", 1005, 1004, -1, -1, 0)),
        ("R", OscMessage("/n_move", 1000, 1001, 1002, -1, 0)),
        ("R", OscMessage("/done", "/d_recv")),
    ]
    server_state = str(server.query())
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1001 group
                    1002 group
                        1003 test
                            amplitude: 1.0, frequency: 440.0
                        1004 group
                            1005 test
                                amplitude: 1.0, frequency: 440.0
                    1000 default
                        out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5
        """
    )
    assert str(server.root_node) == server_state


def test_extend_x(server):
    group_a = supriya.realtime.Group()
    group_a.allocate(target_node=server)
    group_b = supriya.realtime.Group()
    group_b.allocate(target_node=server)
    server_state = str(server.query())
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1001 group
                1000 group
        """
    )
    synthdef = supriya.assets.synthdefs.test
    assert synthdef not in server
    synth_a = supriya.realtime.Synth(synthdef)
    synth_b = supriya.realtime.Synth(synthdef)
    synth_c = supriya.realtime.Synth(synthdef)
    synth_d = supriya.realtime.Synth(synthdef)
    assert not synth_a.is_allocated
    assert not synth_b.is_allocated
    assert not synth_c.is_allocated
    assert not synth_d.is_allocated
    synth_a.allocate(server)
    server_state = str(server.query())
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1002 test
                    amplitude: 1.0, frequency: 440.0
                1001 group
                1000 group
        """
    )
    group_a.extend([synth_a, synth_b])
    server_state = str(server.query())
    assert server_state == normalize(
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
    group_b.extend([synth_c])
    server_state = str(server.query())
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1001 group
                    1004 test
                        amplitude: 1.0, frequency: 440.0
                1000 group
                    1002 test
                        amplitude: 1.0, frequency: 440.0
                    1003 test
                        amplitude: 1.0, frequency: 440.0
        """
    )
    group_b.extend([synth_d, synth_b, synth_a])
    server_state = str(server.query())
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1001 group
                    1004 test
                        amplitude: 1.0, frequency: 440.0
                    1005 test
                        amplitude: 1.0, frequency: 440.0
                    1003 test
                        amplitude: 1.0, frequency: 440.0
                    1002 test
                        amplitude: 1.0, frequency: 440.0
                1000 group
        """
    )


def test_index_01(server):

    group_a = supriya.realtime.Group()
    group_a.allocate(server)

    synth_a = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_a.append(synth_a)

    group_b = supriya.realtime.Group()
    group_a.append(group_b)

    synth_b = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_b.append(synth_b)

    synth_c = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_b.append(synth_c)

    synth_d = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_a.append(synth_d)

    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 test
                    1002 group
                        1003 test
                        1004 test
                    1005 test
        """
    )

    assert group_a.index(synth_a) == 0
    assert group_a.index(group_b) == 1
    assert group_a.index(synth_d) == 2
    assert group_b.index(synth_b) == 0
    assert group_b.index(synth_c) == 1


def test_insert_01(server):
    group = supriya.realtime.Group().allocate(server)
    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
        """
    )
    synth_a = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group.insert(0, synth_a)
    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 test
        """
    )
    synth_b = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group.insert(0, synth_b)
    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1002 test
                    1001 test
        """
    )
    synth_c = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group.insert(1, synth_c)
    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1002 test
                    1003 test
                    1001 test
        """
    )
    synth_d = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group.insert(3, synth_d)
    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1002 test
                    1003 test
                    1001 test
                    1004 test
        """
    )


def test_pop_01(server):

    group_a = supriya.realtime.Group()
    group_a.allocate(server)
    synth_a = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_a.append(synth_a)
    group_b = supriya.realtime.Group()
    group_a.append(group_b)
    synth_b = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_b.append(synth_b)
    synth_c = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_b.append(synth_c)
    group_c = supriya.realtime.Group()
    group_b.append(group_c)
    synth_d = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_a.append(synth_d)

    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 test
                    1002 group
                        1003 test
                        1004 test
                        1005 group
                    1006 test
        """
    )

    group_a.pop()

    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 test
                    1002 group
                        1003 test
                        1004 test
                        1005 group
        """
    )

    group_b.pop(1)

    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 test
                    1002 group
                        1003 test
                        1005 group
        """
    )

    group_a.pop(0)

    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1002 group
                        1003 test
                        1005 group
        """
    )

    group_b.pop()

    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1002 group
                        1003 test
        """
    )

    group_a.pop()

    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
        """
    )

    assert not group_b.is_allocated
    assert not group_c.is_allocated
    assert not synth_a.is_allocated
    assert not synth_b.is_allocated
    assert not synth_c.is_allocated
    assert not synth_d.is_allocated


def test_remove_01(server):

    group_a = supriya.realtime.Group()
    group_a.allocate(server)
    synth_a = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_a.append(synth_a)
    group_b = supriya.realtime.Group()
    group_a.append(group_b)
    synth_b = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_b.append(synth_b)
    synth_c = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_b.append(synth_c)
    group_c = supriya.realtime.Group()
    group_b.append(group_c)
    synth_d = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_a.append(synth_d)

    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 test
                    1002 group
                        1003 test
                        1004 test
                        1005 group
                    1006 test
        """
    )

    group_a.remove(synth_d)

    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 test
                    1002 group
                        1003 test
                        1004 test
                        1005 group
        """
    )

    group_b.remove(synth_c)

    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 test
                    1002 group
                        1003 test
                        1005 group
        """
    )

    group_a.remove(synth_a)

    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1002 group
                        1003 test
                        1005 group
        """
    )

    group_b.remove(group_c)

    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1002 group
                        1003 test
        """
    )

    group_a.remove(group_b)

    server_state = str(server.query(False))
    assert server_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
        """
    )

    assert not group_b.is_allocated
    assert not group_c.is_allocated
    assert not synth_a.is_allocated
    assert not synth_b.is_allocated
    assert not synth_c.is_allocated
    assert not synth_d.is_allocated
