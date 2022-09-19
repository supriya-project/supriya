import pytest
from uqbar.strings import normalize

import supriya.assets.synthdefs
import supriya.nonrealtime


def test_basic():
    session = supriya.nonrealtime.Session()
    with session.at(0):
        group = session.add_group(duration=20)
        synth = session.add_synth(duration=20)
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1001 default
                1000 group
        20.0:
            NODE TREE 0 group
        """
    )
    d_recv_commands = pytest.helpers.build_d_recv_commands(
        [supriya.assets.synthdefs.default]
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                ["/g_new", 1000, 0, 0],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1001, 0, 0],
            ],
        ],
        [20.0, [["/n_free", 1000], ["/n_set", 1001, "gate", 0], [0]]],
    ]

    with session.at(10):
        old_group, new_group = group.split()
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1001 default
                1000 group
        10.0:
            NODE TREE 0 group
                1001 default
                1002 group
        20.0:
            NODE TREE 0 group
        """
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                ["/g_new", 1000, 0, 0],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1001, 0, 0],
            ],
        ],
        [10.0, [["/g_new", 1002, 2, 1000], ["/n_free", 1000]]],
        [20.0, [["/n_free", 1002], ["/n_set", 1001, "gate", 0], [0]]],
    ]

    with session.at(10):
        old_synth, new_synth = synth.split()
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1001 default
                1000 group
        10.0:
            NODE TREE 0 group
                1003 default
                1002 group
        20.0:
            NODE TREE 0 group
        """
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                ["/g_new", 1000, 0, 0],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1001, 0, 0],
            ],
        ],
        [
            10.0,
            [
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1003, 2, 1001],
                ["/g_new", 1002, 2, 1000],
                ["/n_free", 1000],
                ["/n_set", 1001, "gate", 0],
            ],
        ],
        [20.0, [["/n_free", 1002], ["/n_set", 1003, "gate", 0], [0]]],
    ]


def test_basic_group_settings():
    session = supriya.nonrealtime.Session()
    with session.at(0):
        group = session.add_group(duration=20)
    with session.at(5):
        group["foo"] = 111
    with session.at(10):
        group["foo"] = 222
    with session.at(15):
        group["foo"] = 333
    assert group._events == {"foo": [(5, 111), (10, 222), (15, 333)]}
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1000 group
        20.0:
            NODE TREE 0 group
        """
    )
    assert session.to_lists() == [
        [0.0, [["/g_new", 1000, 0, 0]]],
        [5.0, [["/n_set", 1000, "foo", 111]]],
        [10.0, [["/n_set", 1000, "foo", 222]]],
        [15.0, [["/n_set", 1000, "foo", 333]]],
        [20.0, [["/n_free", 1000], [0]]],
    ]

    with session.at(10):
        old_group, new_group = group.split()
    assert old_group._events == {"foo": [(5, 111)]}
    assert new_group._events == {"foo": [(10, 222), (15, 333)]}
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1000 group
        10.0:
            NODE TREE 0 group
                1001 group
        20.0:
            NODE TREE 0 group
        """
    )
    assert session.to_lists() == [
        [0.0, [["/g_new", 1000, 0, 0]]],
        [5.0, [["/n_set", 1000, "foo", 111]]],
        [
            10.0,
            [
                ["/g_new", 1001, 2, 1000],
                ["/n_set", 1001, "foo", 222],
                ["/n_free", 1000],
            ],
        ],
        [15.0, [["/n_set", 1001, "foo", 333]]],
        [20.0, [["/n_free", 1001], [0]]],
    ]


def test_basic_synth_settings():
    session = supriya.nonrealtime.Session()
    with session.at(10):
        synth = session.add_synth(
            synthdef=supriya.assets.synthdefs.default, duration=20, amplitude=0.5
        )
    with session.at(15):
        synth["amplitude"] = 0.25
    with session.at(20):
        synth["frequency"] = 666
    with session.at(25):
        synth["amplitude"] = 0.75
    assert synth._events == {
        "amplitude": [(15, 0.25), (25, 0.75)],
        "frequency": [(20, 666)],
    }
    assert session.to_strings(True) == normalize(
        """
        0.0:
            NODE TREE 0 group
        10.0:
            NODE TREE 0 group
                1000 default
                    amplitude: 0.5, frequency: 440.0, gate: 1.0, out: 0.0, pan: 0.5
        15.0:
            NODE TREE 0 group
                1000 default
                    amplitude: 0.25, frequency: 440.0, gate: 1.0, out: 0.0, pan: 0.5
        20.0:
            NODE TREE 0 group
                1000 default
                    amplitude: 0.25, frequency: 666.0, gate: 1.0, out: 0.0, pan: 0.5
        25.0:
            NODE TREE 0 group
                1000 default
                    amplitude: 0.75, frequency: 666.0, gate: 1.0, out: 0.0, pan: 0.5
        30.0:
            NODE TREE 0 group
        """
    )
    d_recv_commands = pytest.helpers.build_d_recv_commands(
        [supriya.assets.synthdefs.default]
    )
    assert session.to_lists() == [
        [
            10.0,
            [
                *d_recv_commands,
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1000,
                    0,
                    0,
                    "amplitude",
                    0.5,
                ],
            ],
        ],
        [15.0, [["/n_set", 1000, "amplitude", 0.25]]],
        [20.0, [["/n_set", 1000, "frequency", 666]]],
        [25.0, [["/n_set", 1000, "amplitude", 0.75]]],
        [30.0, [["/n_set", 1000, "gate", 0], [0]]],
    ]

    with session.at(20):
        old_synth, new_synth = synth.split()
    assert old_synth._events == {"amplitude": [(15, 0.25)]}
    assert new_synth._events == {
        "amplitude": [(20, 0.25), (25, 0.75)],
        "frequency": [(20, 666)],
    }
    assert session.to_strings(True) == normalize(
        """
        0.0:
            NODE TREE 0 group
        10.0:
            NODE TREE 0 group
                1000 default
                    amplitude: 0.5, frequency: 440.0, gate: 1.0, out: 0.0, pan: 0.5
        15.0:
            NODE TREE 0 group
                1000 default
                    amplitude: 0.25, frequency: 440.0, gate: 1.0, out: 0.0, pan: 0.5
        20.0:
            NODE TREE 0 group
                1001 default
                    amplitude: 0.25, frequency: 666.0, gate: 1.0, out: 0.0, pan: 0.5
        25.0:
            NODE TREE 0 group
                1001 default
                    amplitude: 0.75, frequency: 666.0, gate: 1.0, out: 0.0, pan: 0.5
        30.0:
            NODE TREE 0 group
        """
    )
    assert session.to_lists() == [
        [
            10.0,
            [
                *d_recv_commands,
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1000,
                    0,
                    0,
                    "amplitude",
                    0.5,
                ],
            ],
        ],
        [15.0, [["/n_set", 1000, "amplitude", 0.25]]],
        [
            20.0,
            [
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1001,
                    2,
                    1000,
                    "amplitude",
                    0.25,
                    "frequency",
                    666,
                ],
                ["/n_set", 1000, "gate", 0],
            ],
        ],
        [25.0, [["/n_set", 1001, "amplitude", 0.75]]],
        [30.0, [["/n_set", 1001, "gate", 0], [0]]],
    ]


def test_basic_node_order():
    session = supriya.nonrealtime.Session()
    with session.at(0) as moment:
        group = session.add_group(duration=20)
        group.add_synth(duration=20, frequency=1111, add_action="ADD_TO_TAIL")
        group.add_synth(add_action="ADD_TO_TAIL", duration=20, frequency=2222)
        group.add_synth(add_action="ADD_TO_TAIL", duration=20, frequency=3333)
        children = moment.state.nodes_to_children[group]
        assert [_["frequency"] for _ in children] == [1111, 2222, 3333]
    assert session.to_strings(True) == normalize(
        """
        0.0:
            NODE TREE 0 group
                1000 group
                    1001 default
                        amplitude: 0.1, frequency: 1111.0, gate: 1.0, out: 0.0, pan: 0.5
                    1002 default
                        amplitude: 0.1, frequency: 2222.0, gate: 1.0, out: 0.0, pan: 0.5
                    1003 default
                        amplitude: 0.1, frequency: 3333.0, gate: 1.0, out: 0.0, pan: 0.5
        20.0:
            NODE TREE 0 group
        """
    )
    d_recv_commands = pytest.helpers.build_d_recv_commands(
        [supriya.assets.synthdefs.default]
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                ["/g_new", 1000, 0, 0],
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1001,
                    1,
                    1000,
                    "frequency",
                    1111,
                ],
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1002,
                    1,
                    1000,
                    "frequency",
                    2222,
                ],
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1003,
                    1,
                    1000,
                    "frequency",
                    3333,
                ],
            ],
        ],
        [
            20.0,
            [
                ["/n_free", 1000],
                ["/n_set", 1001, "gate", 0],
                ["/n_set", 1002, "gate", 0],
                ["/n_set", 1003, "gate", 0],
                [0],
            ],
        ],
    ]
    with session.at(10) as moment:
        _, new_group = group.split()
        children = moment.state.nodes_to_children[new_group]
        assert [_["frequency"] for _ in children] == [1111, 2222, 3333]
    assert session.to_strings(True) == normalize(
        """
        0.0:
            NODE TREE 0 group
                1000 group
                    1001 default
                        amplitude: 0.1, frequency: 1111.0, gate: 1.0, out: 0.0, pan: 0.5
                    1002 default
                        amplitude: 0.1, frequency: 2222.0, gate: 1.0, out: 0.0, pan: 0.5
                    1003 default
                        amplitude: 0.1, frequency: 3333.0, gate: 1.0, out: 0.0, pan: 0.5
        10.0:
            NODE TREE 0 group
                1004 group
                    1005 default
                        amplitude: 0.1, frequency: 1111.0, gate: 1.0, out: 0.0, pan: 0.5
                    1006 default
                        amplitude: 0.1, frequency: 2222.0, gate: 1.0, out: 0.0, pan: 0.5
                    1007 default
                        amplitude: 0.1, frequency: 3333.0, gate: 1.0, out: 0.0, pan: 0.5
        20.0:
            NODE TREE 0 group
        """
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                ["/g_new", 1000, 0, 0],
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1001,
                    1,
                    1000,
                    "frequency",
                    1111,
                ],
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1002,
                    1,
                    1000,
                    "frequency",
                    2222,
                ],
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1003,
                    1,
                    1000,
                    "frequency",
                    3333,
                ],
            ],
        ],
        [
            10.0,
            [
                ["/g_new", 1004, 2, 1000],
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1005,
                    1,
                    1004,
                    "frequency",
                    1111,
                ],
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1006,
                    1,
                    1004,
                    "frequency",
                    2222,
                ],
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1007,
                    1,
                    1004,
                    "frequency",
                    3333,
                ],
                ["/n_free", 1000],
                ["/n_set", 1001, "gate", 0],
                ["/n_set", 1002, "gate", 0],
                ["/n_set", 1003, "gate", 0],
            ],
        ],
        [
            20.0,
            [
                ["/n_free", 1004],
                ["/n_set", 1005, "gate", 0],
                ["/n_set", 1006, "gate", 0],
                ["/n_set", 1007, "gate", 0],
                [0],
            ],
        ],
    ]


def test_entering():
    def make_session():
        session = supriya.nonrealtime.Session()
        with session.at(0):
            group = session.add_group(duration=20)
            synth = session.add_synth(duration=20)
        with session.at(10):
            group.move_node(synth)
        assert session.to_strings() == normalize(
            """
            0.0:
                NODE TREE 0 group
                    1001 default
                    1000 group
            10.0:
                NODE TREE 0 group
                    1000 group
                        1001 default
            20.0:
                NODE TREE 0 group
            """
        )
        d_recv_commands = pytest.helpers.build_d_recv_commands(
            [supriya.assets.synthdefs.default]
        )
        assert session.to_lists() == [
            [
                0.0,
                [
                    *d_recv_commands,
                    ["/g_new", 1000, 0, 0],
                    ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1001, 0, 0],
                ],
            ],
            [10.0, [["/g_head", 1000, 1001]]],
            [20.0, [["/n_free", 1000], ["/n_set", 1001, "gate", 0], [0]]],
        ]
        return session, group

    session, group = make_session()
    with session.at(10):
        group.split(split_occupiers=True, split_traversers=True)
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1001 default
                1000 group
        10.0:
            NODE TREE 0 group
                1002 group
                    1003 default
        20.0:
            NODE TREE 0 group
        """
    )
    d_recv_commands = pytest.helpers.build_d_recv_commands(
        [supriya.assets.synthdefs.default]
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                ["/g_new", 1000, 0, 0],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1001, 0, 0],
            ],
        ],
        [
            10.0,
            [
                ["/g_new", 1002, 2, 1000],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1003, 1, 1002],
                ["/n_free", 1000],
                ["/n_set", 1001, "gate", 0],
            ],
        ],
        [20.0, [["/n_free", 1002], ["/n_set", 1003, "gate", 0], [0]]],
    ]

    session, group = make_session()
    with session.at(10):
        group.split(split_occupiers=False, split_traversers=True)
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1001 default
                1000 group
        10.0:
            NODE TREE 0 group
                1002 group
                    1003 default
        20.0:
            NODE TREE 0 group
        """
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                ["/g_new", 1000, 0, 0],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1001, 0, 0],
            ],
        ],
        [
            10.0,
            [
                ["/g_new", 1002, 2, 1000],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1003, 1, 1002],
                ["/n_free", 1000],
                ["/n_set", 1001, "gate", 0],
            ],
        ],
        [20.0, [["/n_free", 1002], ["/n_set", 1003, "gate", 0], [0]]],
    ]

    session, group = make_session()
    with session.at(10):
        group.split(split_occupiers=True, split_traversers=False)
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1001 default
                1000 group
        10.0:
            NODE TREE 0 group
                1002 group
                    1001 default
        20.0:
            NODE TREE 0 group
        """
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                ["/g_new", 1000, 0, 0],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1001, 0, 0],
            ],
        ],
        [10.0, [["/g_new", 1002, 2, 1000], ["/g_tail", 1002, 1001], ["/n_free", 1000]]],
        [20.0, [["/n_free", 1002], ["/n_set", 1001, "gate", 0], [0]]],
    ]

    session, group = make_session()
    with session.at(10):
        group.split(split_occupiers=False, split_traversers=False)
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1001 default
                1000 group
        10.0:
            NODE TREE 0 group
                1002 group
                    1001 default
        20.0:
            NODE TREE 0 group
        """
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                ["/g_new", 1000, 0, 0],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1001, 0, 0],
            ],
        ],
        [10.0, [["/g_new", 1002, 2, 1000], ["/g_tail", 1002, 1001], ["/n_free", 1000]]],
        [20.0, [["/n_free", 1002], ["/n_set", 1001, "gate", 0], [0]]],
    ]


def test_exiting():
    def make_session():
        session = supriya.nonrealtime.Session()
        with session.at(0):
            group = session.add_group(duration=20)
            synth = group.add_synth(duration=20)
        with session.at(10):
            session.move_node(synth)
        assert session.to_strings() == normalize(
            """
            0.0:
                NODE TREE 0 group
                    1000 group
                        1001 default
            10.0:
                NODE TREE 0 group
                    1001 default
                    1000 group
            20.0:
                NODE TREE 0 group
            """
        )
        d_recv_commands = pytest.helpers.build_d_recv_commands(
            [supriya.assets.synthdefs.default]
        )
        assert session.to_lists() == [
            [
                0.0,
                [
                    *d_recv_commands,
                    ["/g_new", 1000, 0, 0],
                    ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1001, 0, 1000],
                ],
            ],
            [10.0, [["/g_head", 0, 1001]]],
            [20.0, [["/n_free", 1000], ["/n_set", 1001, "gate", 0], [0]]],
        ]
        return session, group

    session, group = make_session()
    with session.at(10):
        group.split(split_occupiers=True, split_traversers=True)
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1000 group
                    1001 default
        10.0:
            NODE TREE 0 group
                1003 default
                1002 group
        20.0:
            NODE TREE 0 group
        """
    )
    d_recv_commands = pytest.helpers.build_d_recv_commands(
        [supriya.assets.synthdefs.default]
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                ["/g_new", 1000, 0, 0],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1001, 0, 1000],
            ],
        ],
        [
            10.0,
            [
                ["/g_new", 1002, 2, 1000],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1003, 0, 0],
                ["/n_free", 1000],
                ["/n_set", 1001, "gate", 0],
            ],
        ],
        [20.0, [["/n_free", 1002], ["/n_set", 1003, "gate", 0], [0]]],
    ]

    session, group = make_session()
    with session.at(10):
        group.split(split_occupiers=False, split_traversers=True)
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1000 group
                    1001 default
        10.0:
            NODE TREE 0 group
                1003 default
                1002 group
        20.0:
            NODE TREE 0 group
        """
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                ["/g_new", 1000, 0, 0],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1001, 0, 1000],
            ],
        ],
        [
            10.0,
            [
                ["/g_new", 1002, 2, 1000],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1003, 0, 0],
                ["/n_free", 1000],
                ["/n_set", 1001, "gate", 0],
            ],
        ],
        [20.0, [["/n_free", 1002], ["/n_set", 1003, "gate", 0], [0]]],
    ]

    session, group = make_session()
    with session.at(10):
        group.split(split_occupiers=True, split_traversers=False)
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1000 group
                    1001 default
        10.0:
            NODE TREE 0 group
                1001 default
                1002 group
        20.0:
            NODE TREE 0 group
        """
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                ["/g_new", 1000, 0, 0],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1001, 0, 1000],
            ],
        ],
        [10.0, [["/g_new", 1002, 2, 1000], ["/g_head", 0, 1001], ["/n_free", 1000]]],
        [20.0, [["/n_free", 1002], ["/n_set", 1001, "gate", 0], [0]]],
    ]

    session, group = make_session()
    with session.at(10):
        group.split(split_occupiers=False, split_traversers=False)
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1000 group
                    1001 default
        10.0:
            NODE TREE 0 group
                1001 default
                1002 group
        20.0:
            NODE TREE 0 group
        """
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                ["/g_new", 1000, 0, 0],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1001, 0, 1000],
            ],
        ],
        [10.0, [["/g_new", 1002, 2, 1000], ["/g_head", 0, 1001], ["/n_free", 1000]]],
        [20.0, [["/n_free", 1002], ["/n_set", 1001, "gate", 0], [0]]],
    ]


def test_occupying():
    def make_session():
        session = supriya.nonrealtime.Session()
        with session.at(0):
            group = session.add_group(duration=20)
            group.add_synth(duration=20)
        assert session.to_strings() == normalize(
            """
            0.0:
                NODE TREE 0 group
                    1000 group
                        1001 default
            20.0:
                NODE TREE 0 group
            """
        )
        d_recv_commands = pytest.helpers.build_d_recv_commands(
            [supriya.assets.synthdefs.default]
        )
        assert session.to_lists() == [
            [
                0.0,
                [
                    *d_recv_commands,
                    ["/g_new", 1000, 0, 0],
                    ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1001, 0, 1000],
                ],
            ],
            [20.0, [["/n_free", 1000], ["/n_set", 1001, "gate", 0], [0]]],
        ]
        return session, group

    session, group = make_session()
    with session.at(10):
        group.split()
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1000 group
                    1001 default
        10.0:
            NODE TREE 0 group
                1002 group
                    1003 default
        20.0:
            NODE TREE 0 group
        """
    )
    d_recv_commands = pytest.helpers.build_d_recv_commands(
        [supriya.assets.synthdefs.default]
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                ["/g_new", 1000, 0, 0],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1001, 0, 1000],
            ],
        ],
        [
            10.0,
            [
                ["/g_new", 1002, 2, 1000],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1003, 1, 1002],
                ["/n_free", 1000],
                ["/n_set", 1001, "gate", 0],
            ],
        ],
        [20.0, [["/n_free", 1002], ["/n_set", 1003, "gate", 0], [0]]],
    ]

    session, group = make_session()
    with session.at(10):
        group.split(split_occupiers=False)
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1000 group
                    1001 default
        10.0:
            NODE TREE 0 group
                1002 group
                    1001 default
        20.0:
            NODE TREE 0 group
        """
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                ["/g_new", 1000, 0, 0],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1001, 0, 1000],
            ],
        ],
        [10.0, [["/g_new", 1002, 2, 1000], ["/g_tail", 1002, 1001], ["/n_free", 1000]]],
        [20.0, [["/n_free", 1002], ["/n_set", 1001, "gate", 0], [0]]],
    ]

    session, group = make_session()
    with session.at(10):
        group.split(split_traversers=False)
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1000 group
                    1001 default
        10.0:
            NODE TREE 0 group
                1002 group
                    1003 default
        20.0:
            NODE TREE 0 group
        """
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                ["/g_new", 1000, 0, 0],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1001, 0, 1000],
            ],
        ],
        [
            10.0,
            [
                ["/g_new", 1002, 2, 1000],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1003, 1, 1002],
                ["/n_free", 1000],
                ["/n_set", 1001, "gate", 0],
            ],
        ],
        [20.0, [["/n_free", 1002], ["/n_set", 1003, "gate", 0], [0]]],
    ]

    session, group = make_session()
    with session.at(10):
        group.split(split_occupiers=False, split_traversers=False)
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1000 group
                    1001 default
        10.0:
            NODE TREE 0 group
                1002 group
                    1001 default
        20.0:
            NODE TREE 0 group
        """
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                ["/g_new", 1000, 0, 0],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1001, 0, 1000],
            ],
        ],
        [10.0, [["/g_new", 1002, 2, 1000], ["/g_tail", 1002, 1001], ["/n_free", 1000]]],
        [20.0, [["/n_free", 1002], ["/n_set", 1001, "gate", 0], [0]]],
    ]


def test_starting():
    def make_session():
        session = supriya.nonrealtime.Session()
        with session.at(0):
            group = session.add_group(duration=20)
        with session.at(10):
            group.add_synth(duration=10)
        assert session.to_strings() == normalize(
            """
            0.0:
                NODE TREE 0 group
                    1000 group
            10.0:
                NODE TREE 0 group
                    1000 group
                        1001 default
            20.0:
                NODE TREE 0 group
            """
        )
        d_recv_commands = pytest.helpers.build_d_recv_commands(
            [supriya.assets.synthdefs.default]
        )
        assert session.to_lists() == [
            [0.0, [["/g_new", 1000, 0, 0]]],
            [
                10.0,
                [
                    *d_recv_commands,
                    ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1001, 0, 1000],
                ],
            ],
            [20.0, [["/n_free", 1000], ["/n_set", 1001, "gate", 0], [0]]],
        ]
        return session, group

    session, group = make_session()
    with session.at(10):
        group.split(split_occupiers=True, split_traversers=True)
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1000 group
        10.0:
            NODE TREE 0 group
                1002 group
                    1001 default
        20.0:
            NODE TREE 0 group
        """
    )
    d_recv_commands = pytest.helpers.build_d_recv_commands(
        [supriya.assets.synthdefs.default]
    )
    assert session.to_lists() == [
        [0.0, [["/g_new", 1000, 0, 0]]],
        [
            10.0,
            [
                *d_recv_commands,
                ["/g_new", 1002, 2, 1000],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1001, 1, 1002],
                ["/n_free", 1000],
            ],
        ],
        [20.0, [["/n_free", 1002], ["/n_set", 1001, "gate", 0], [0]]],
    ]

    session, group = make_session()
    with session.at(10):
        group.split(split_occupiers=False, split_traversers=True)
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1000 group
        10.0:
            NODE TREE 0 group
                1002 group
                    1001 default
        20.0:
            NODE TREE 0 group
        """
    )
    assert session.to_lists() == [
        [0.0, [["/g_new", 1000, 0, 0]]],
        [
            10.0,
            [
                *d_recv_commands,
                ["/g_new", 1002, 2, 1000],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1001, 1, 1002],
                ["/n_free", 1000],
            ],
        ],
        [20.0, [["/n_free", 1002], ["/n_set", 1001, "gate", 0], [0]]],
    ]

    session, group = make_session()
    with session.at(10):
        group.split(split_occupiers=True, split_traversers=False)
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1000 group
        10.0:
            NODE TREE 0 group
                1002 group
                    1001 default
        20.0:
            NODE TREE 0 group
        """
    )
    assert session.to_lists() == [
        [0.0, [["/g_new", 1000, 0, 0]]],
        [
            10.0,
            [
                *d_recv_commands,
                ["/g_new", 1002, 2, 1000],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1001, 1, 1002],
                ["/n_free", 1000],
            ],
        ],
        [20.0, [["/n_free", 1002], ["/n_set", 1001, "gate", 0], [0]]],
    ]

    session, group = make_session()
    with session.at(10):
        group.split(split_occupiers=False, split_traversers=False)
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1000 group
        10.0:
            NODE TREE 0 group
                1002 group
                    1001 default
        20.0:
            NODE TREE 0 group
        """
    )
    assert session.to_lists() == [
        [0.0, [["/g_new", 1000, 0, 0]]],
        [
            10.0,
            [
                *d_recv_commands,
                ["/g_new", 1002, 2, 1000],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1001, 1, 1002],
                ["/n_free", 1000],
            ],
        ],
        [20.0, [["/n_free", 1002], ["/n_set", 1001, "gate", 0], [0]]],
    ]


def test_stopping():
    def make_session():
        session = supriya.nonrealtime.Session()
        with session.at(0):
            group = session.add_group(duration=20)
            group.add_synth(duration=10)
        assert session.to_strings() == normalize(
            """
            0.0:
                NODE TREE 0 group
                    1000 group
                        1001 default
            10.0:
                NODE TREE 0 group
                    1000 group
            20.0:
                NODE TREE 0 group
            """
        )
        d_recv_commands = pytest.helpers.build_d_recv_commands(
            [supriya.assets.synthdefs.default]
        )
        assert session.to_lists() == [
            [
                0.0,
                [
                    *d_recv_commands,
                    ["/g_new", 1000, 0, 0],
                    ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1001, 0, 1000],
                ],
            ],
            [10.0, [["/n_set", 1001, "gate", 0]]],
            [20.0, [["/n_free", 1000], [0]]],
        ]
        return session, group

    session, group = make_session()
    with session.at(10):
        group.split(split_occupiers=True, split_traversers=True)
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1000 group
                    1001 default
        10.0:
            NODE TREE 0 group
                1002 group
        20.0:
            NODE TREE 0 group
        """
    )
    d_recv_commands = pytest.helpers.build_d_recv_commands(
        [supriya.assets.synthdefs.default]
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                ["/g_new", 1000, 0, 0],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1001, 0, 1000],
            ],
        ],
        [
            10.0,
            [["/g_new", 1002, 2, 1000], ["/n_free", 1000], ["/n_set", 1001, "gate", 0]],
        ],
        [20.0, [["/n_free", 1002], [0]]],
    ]

    session, group = make_session()
    with session.at(10):
        group.split(split_occupiers=False, split_traversers=True)
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1000 group
                    1001 default
        10.0:
            NODE TREE 0 group
                1002 group
        20.0:
            NODE TREE 0 group
        """
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                ["/g_new", 1000, 0, 0],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1001, 0, 1000],
            ],
        ],
        [
            10.0,
            [["/g_new", 1002, 2, 1000], ["/n_free", 1000], ["/n_set", 1001, "gate", 0]],
        ],
        [20.0, [["/n_free", 1002], [0]]],
    ]

    session, group = make_session()
    with session.at(10):
        group.split(split_occupiers=True, split_traversers=False)
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1000 group
                    1001 default
        10.0:
            NODE TREE 0 group
                1002 group
        20.0:
            NODE TREE 0 group
        """
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                ["/g_new", 1000, 0, 0],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1001, 0, 1000],
            ],
        ],
        [
            10.0,
            [["/g_new", 1002, 2, 1000], ["/n_free", 1000], ["/n_set", 1001, "gate", 0]],
        ],
        [20.0, [["/n_free", 1002], [0]]],
    ]

    session, group = make_session()
    with session.at(10):
        group.split(split_occupiers=False, split_traversers=False)
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1000 group
                    1001 default
        10.0:
            NODE TREE 0 group
                1002 group
        20.0:
            NODE TREE 0 group
        """
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                ["/g_new", 1000, 0, 0],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1001, 0, 1000],
            ],
        ],
        [
            10.0,
            [["/g_new", 1002, 2, 1000], ["/n_free", 1000], ["/n_set", 1001, "gate", 0]],
        ],
        [20.0, [["/n_free", 1002], [0]]],
    ]


def test_nested_entering():
    def make_session():
        session = supriya.nonrealtime.Session()
        with session.at(0):
            group = session.add_group(duration=20)
            subgroup = group.add_group(duration=20)
            synth = session.add_synth(duration=20)
        with session.at(10):
            subgroup.move_node(synth)
        assert session.to_strings() == normalize(
            """
            0.0:
                NODE TREE 0 group
                    1002 default
                    1000 group
                        1001 group
            10.0:
                NODE TREE 0 group
                    1000 group
                        1001 group
                            1002 default
            20.0:
                NODE TREE 0 group
            """
        )
        d_recv_commands = pytest.helpers.build_d_recv_commands(
            [supriya.assets.synthdefs.default]
        )
        assert session.to_lists() == [
            [
                0.0,
                [
                    *d_recv_commands,
                    ["/g_new", 1000, 0, 0],
                    ["/g_new", 1001, 0, 1000],
                    ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1002, 0, 0],
                ],
            ],
            [10.0, [["/g_head", 1001, 1002]]],
            [20.0, [["/n_free", 1000, 1001], ["/n_set", 1002, "gate", 0], [0]]],
        ]
        return session, group

    session, group = make_session()
    with session.at(10):
        group.split(split_occupiers=True, split_traversers=True)
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1002 default
                1000 group
                    1001 group
        10.0:
            NODE TREE 0 group
                1003 group
                    1004 group
                        1005 default
        20.0:
            NODE TREE 0 group
        """
    )
    d_recv_commands = pytest.helpers.build_d_recv_commands(
        [supriya.assets.synthdefs.default]
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                ["/g_new", 1000, 0, 0],
                ["/g_new", 1001, 0, 1000],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1002, 0, 0],
            ],
        ],
        [
            10.0,
            [
                ["/g_new", 1003, 2, 1000],
                ["/g_new", 1004, 1, 1003],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1005, 1, 1004],
                ["/n_free", 1000, 1001],
                ["/n_set", 1002, "gate", 0],
            ],
        ],
        [20.0, [["/n_free", 1003, 1004], ["/n_set", 1005, "gate", 0], [0]]],
    ]

    session, group = make_session()
    with session.at(10):
        group.split(split_occupiers=False, split_traversers=True)
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1002 default
                1000 group
                    1001 group
        10.0:
            NODE TREE 0 group
                1003 group
                    1001 group
                        1002 default
        20.0:
            NODE TREE 0 group
        """
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                ["/g_new", 1000, 0, 0],
                ["/g_new", 1001, 0, 1000],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1002, 0, 0],
            ],
        ],
        [
            10.0,
            [
                ["/g_new", 1003, 2, 1000],
                ["/g_tail", 1003, 1001],
                ["/g_head", 1001, 1002],
                ["/n_free", 1000],
            ],
        ],
        [20.0, [["/n_free", 1001, 1003], ["/n_set", 1002, "gate", 0], [0]]],
    ]

    session, group = make_session()
    with session.at(10):
        group.split(split_occupiers=True, split_traversers=False)
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1002 default
                1000 group
                    1001 group
        10.0:
            NODE TREE 0 group
                1003 group
                    1004 group
                        1002 default
        20.0:
            NODE TREE 0 group
        """
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                ["/g_new", 1000, 0, 0],
                ["/g_new", 1001, 0, 1000],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1002, 0, 0],
            ],
        ],
        [
            10.0,
            [
                ["/g_new", 1003, 2, 1000],
                ["/g_new", 1004, 1, 1003],
                ["/g_tail", 1004, 1002],
                ["/n_free", 1000, 1001],
            ],
        ],
        [20.0, [["/n_free", 1003, 1004], ["/n_set", 1002, "gate", 0], [0]]],
    ]

    session, group = make_session()
    with session.at(10):
        group.split(split_occupiers=False, split_traversers=False)
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1002 default
                1000 group
                    1001 group
        10.0:
            NODE TREE 0 group
                1003 group
                    1001 group
                        1002 default
        20.0:
            NODE TREE 0 group
        """
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                ["/g_new", 1000, 0, 0],
                ["/g_new", 1001, 0, 1000],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1002, 0, 0],
            ],
        ],
        [
            10.0,
            [
                ["/g_new", 1003, 2, 1000],
                ["/g_tail", 1003, 1001],
                ["/g_head", 1001, 1002],
                ["/n_free", 1000],
            ],
        ],
        [20.0, [["/n_free", 1001, 1003], ["/n_set", 1002, "gate", 0], [0]]],
    ]


def test_nested_exiting():
    def make_session():
        session = supriya.nonrealtime.Session()
        with session.at(0):
            group = session.add_group(duration=20)
            subgroup = group.add_group(duration=20)
            synth = subgroup.add_synth(duration=20)
        with session.at(10):
            session.move_node(synth)
        assert session.to_strings() == normalize(
            """
            0.0:
                NODE TREE 0 group
                    1000 group
                        1001 group
                            1002 default
            10.0:
                NODE TREE 0 group
                    1002 default
                    1000 group
                        1001 group
            20.0:
                NODE TREE 0 group
            """
        )
        d_recv_commands = pytest.helpers.build_d_recv_commands(
            [supriya.assets.synthdefs.default]
        )
        assert session.to_lists() == [
            [
                0.0,
                [
                    *d_recv_commands,
                    ["/g_new", 1000, 0, 0],
                    ["/g_new", 1001, 0, 1000],
                    ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1002, 0, 1001],
                ],
            ],
            [10.0, [["/g_head", 0, 1002]]],
            [20.0, [["/n_free", 1000, 1001], ["/n_set", 1002, "gate", 0], [0]]],
        ]
        return session, group

    session, group = make_session()
    with session.at(10):
        group.split(split_occupiers=True, split_traversers=True)
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1000 group
                    1001 group
                        1002 default
        10.0:
            NODE TREE 0 group
                1005 default
                1003 group
                    1004 group
        20.0:
            NODE TREE 0 group
        """
    )
    d_recv_commands = pytest.helpers.build_d_recv_commands(
        [supriya.assets.synthdefs.default]
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                ["/g_new", 1000, 0, 0],
                ["/g_new", 1001, 0, 1000],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1002, 0, 1001],
            ],
        ],
        [
            10.0,
            [
                ["/g_new", 1003, 2, 1000],
                ["/g_new", 1004, 1, 1003],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1005, 0, 0],
                ["/n_free", 1000, 1001],
                ["/n_set", 1002, "gate", 0],
            ],
        ],
        [20.0, [["/n_free", 1003, 1004], ["/n_set", 1005, "gate", 0], [0]]],
    ]

    session, group = make_session()
    with session.at(10):
        group.split(split_occupiers=False, split_traversers=True)
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1000 group
                    1001 group
                        1002 default
        10.0:
            NODE TREE 0 group
                1002 default
                1003 group
                    1001 group
        20.0:
            NODE TREE 0 group
        """
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                ["/g_new", 1000, 0, 0],
                ["/g_new", 1001, 0, 1000],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1002, 0, 1001],
            ],
        ],
        [
            10.0,
            [
                ["/g_new", 1003, 2, 1000],
                ["/g_tail", 1003, 1001],
                ["/g_head", 0, 1002],
                ["/n_free", 1000],
            ],
        ],
        [20.0, [["/n_free", 1001, 1003], ["/n_set", 1002, "gate", 0], [0]]],
    ]

    session, group = make_session()
    with session.at(10):
        group.split(split_occupiers=True, split_traversers=False)
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1000 group
                    1001 group
                        1002 default
        10.0:
            NODE TREE 0 group
                1002 default
                1003 group
                    1004 group
        20.0:
            NODE TREE 0 group
        """
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                ["/g_new", 1000, 0, 0],
                ["/g_new", 1001, 0, 1000],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1002, 0, 1001],
            ],
        ],
        [
            10.0,
            [
                ["/g_new", 1003, 2, 1000],
                ["/g_new", 1004, 1, 1003],
                ["/g_head", 0, 1002],
                ["/n_free", 1000, 1001],
            ],
        ],
        [20.0, [["/n_free", 1003, 1004], ["/n_set", 1002, "gate", 0], [0]]],
    ]

    session, group = make_session()
    with session.at(10):
        group.split(split_occupiers=False, split_traversers=False)
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1000 group
                    1001 group
                        1002 default
        10.0:
            NODE TREE 0 group
                1002 default
                1003 group
                    1001 group
        20.0:
            NODE TREE 0 group
        """
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                ["/g_new", 1000, 0, 0],
                ["/g_new", 1001, 0, 1000],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1002, 0, 1001],
            ],
        ],
        [
            10.0,
            [
                ["/g_new", 1003, 2, 1000],
                ["/g_tail", 1003, 1001],
                ["/g_head", 0, 1002],
                ["/n_free", 1000],
            ],
        ],
        [20.0, [["/n_free", 1001, 1003], ["/n_set", 1002, "gate", 0], [0]]],
    ]
