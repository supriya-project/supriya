import uqbar.strings

import supriya.assets.synthdefs
import supriya.realtime


def test_01(server):

    group = supriya.realtime.Group().allocate()
    assert len(group) == 0
    remote_state = str(server.query())
    assert remote_state == uqbar.strings.normalize(
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
    assert remote_state == uqbar.strings.normalize(
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
    assert remote_state == uqbar.strings.normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
        """
    )


def test_02(server):

    group = supriya.realtime.Group().allocate()
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
    assert remote_state == uqbar.strings.normalize(
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
    assert remote_state == uqbar.strings.normalize(
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
    assert remote_state == uqbar.strings.normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
        """
    )


def test_03(server):

    group_a = supriya.realtime.Group()
    group_a.allocate()

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
    assert remote_state == uqbar.strings.normalize(
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
    assert remote_state == uqbar.strings.normalize(
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
    assert remote_state == uqbar.strings.normalize(
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
    assert remote_state == uqbar.strings.normalize(
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
    assert remote_state == uqbar.strings.normalize(
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
    assert remote_state == uqbar.strings.normalize(
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


def test_04(server):

    group_a = supriya.realtime.Group().allocate()
    group_b = supriya.realtime.Group().allocate()

    synth_a = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_b = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_c = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_d = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_e = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_f = supriya.realtime.Synth(supriya.assets.synthdefs.test)

    local_state = str(server.root_node)
    remote_state = str(server.query())
    assert remote_state == uqbar.strings.normalize(
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
    assert remote_state == uqbar.strings.normalize(
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
    assert remote_state == uqbar.strings.normalize(
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
    assert remote_state == uqbar.strings.normalize(
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
    assert remote_state == uqbar.strings.normalize(
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
    assert remote_state == uqbar.strings.normalize(
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
    assert remote_state == uqbar.strings.normalize(
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
    assert remote_state == uqbar.strings.normalize(
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
    assert remote_state == uqbar.strings.normalize(
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


def test_05(server):

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

    group_a.allocate()

    remote_state = str(server.query())
    assert remote_state == uqbar.strings.normalize(
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
    assert group_a_state == uqbar.strings.normalize(
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
    assert remote_state == uqbar.strings.normalize(
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
    assert group_a_state == uqbar.strings.normalize(
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


def test_06(server):

    group = supriya.realtime.Group()

    synth_a = supriya.realtime.Synth(
        name="Synth A", synthdef=supriya.assets.synthdefs.test
    )

    synth_b = supriya.realtime.Synth(
        name="Synth B", synthdef=supriya.assets.synthdefs.test
    )
    synth_b["amplitude"] = 0.5
    synth_b["frequency"] = 443

    audio_bus = supriya.realtime.Bus(0, "audio").allocate()
    control_bus = supriya.realtime.Bus(1, "control").allocate()

    synth_c = supriya.realtime.Synth(
        name="Synth C", synthdef=supriya.assets.synthdefs.test
    )
    synth_c["amplitude"] = audio_bus
    synth_c["frequency"] = control_bus

    group[:] = [synth_a, synth_b, synth_c]

    group_state = str(group)
    assert group_state == uqbar.strings.normalize(
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

    group.allocate()

    group_state = str(group)
    assert group_state == uqbar.strings.normalize(
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
    assert remote_state == uqbar.strings.normalize(
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
    assert remote_state == uqbar.strings.normalize(
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
    assert remote_state == uqbar.strings.normalize(
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
    assert group_state == uqbar.strings.normalize(
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
