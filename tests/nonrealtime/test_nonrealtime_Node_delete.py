import pytest
from uqbar.strings import normalize

import supriya.assets.synthdefs
import supriya.nonrealtime


def test_01():
    session = supriya.nonrealtime.Session()
    with session.at(0):
        session.add_group(duration=20)
        group = session.add_group(duration=20)
        group.add_synth(duration=20)
        session.add_group(duration=20)
    d_recv_commands = pytest.helpers.build_d_recv_commands(
        [supriya.assets.synthdefs.default]
    )
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1003 group
                1001 group
                    1002 default
                1000 group
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
                ["/g_new", 1001, 0, 0],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1002, 0, 1001],
                ["/g_new", 1003, 0, 0],
            ],
        ],
        [20.0, [["/n_free", 1000, 1001, 1003], ["/n_set", 1002, "gate", 0], [0]]],
    ]
    group.delete()
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1003 group
                1002 default
                1000 group
        20.0:
            NODE TREE 0 group
        """
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                ["/g_new", 1003, 0, 0],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1002, 3, 1003],
                ["/g_new", 1000, 3, 1002],
            ],
        ],
        [20.0, [["/n_free", 1000, 1003], ["/n_set", 1002, "gate", 0], [0]]],
    ]


def test_02():
    session = supriya.nonrealtime.Session()
    with session.at(0):
        group = session.add_group(duration=20)
        synth_a = group.add_synth(duration=20)
        synth_b = session.add_synth(duration=20)
    with session.at(5):
        group.move_node(synth_b, "ADD_TO_TAIL")
    with session.at(15):
        session.move_node(synth_a, "ADD_TO_TAIL")
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1002 default
                1000 group
                    1001 default
        5.0:
            NODE TREE 0 group
                1000 group
                    1001 default
                    1002 default
        15.0:
            NODE TREE 0 group
                1000 group
                    1002 default
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
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1002, 0, 0],
            ],
        ],
        [5.0, [["/g_tail", 1000, 1002]]],
        [15.0, [["/g_tail", 0, 1001]]],
        [
            20.0,
            [
                ["/n_free", 1000],
                ["/n_set", 1001, "gate", 0],
                ["/n_set", 1002, "gate", 0],
                [0],
            ],
        ],
    ]
    group.delete()
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1002 default
                1001 default
        5.0:
            NODE TREE 0 group
                1001 default
                1002 default
        15.0:
            NODE TREE 0 group
                1002 default
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
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1002, 0, 0],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1001, 3, 1002],
            ],
        ],
        [5.0, [["/n_before", 1001, 1002]]],
        [15.0, [["/n_before", 1002, 1001]]],
        [20.0, [["/n_set", 1001, "gate", 0], ["/n_set", 1002, "gate", 0], [0]]],
    ]


def test_03():
    session = supriya.nonrealtime.Session()
    with session.at(0):
        group = session.add_group(duration=20)
        synth_a = session.add_synth(duration=20, frequency=444)
        subgroup = group.add_group(duration=20)
        synth_b = session.add_synth(duration=20, frequency=555)
    with session.at(5):
        subgroup.move_node(synth_b, "ADD_TO_TAIL")
    with session.at(15):
        group.move_node(synth_a, "ADD_TO_TAIL")
    assert session.to_strings(True) == normalize(
        """
        0.0:
            NODE TREE 0 group
                1003 default
                    amplitude: 0.1, frequency: 555.0, gate: 1.0, out: 0.0, pan: 0.5
                1001 default
                    amplitude: 0.1, frequency: 444.0, gate: 1.0, out: 0.0, pan: 0.5
                1000 group
                    1002 group
        5.0:
            NODE TREE 0 group
                1001 default
                    amplitude: 0.1, frequency: 444.0, gate: 1.0, out: 0.0, pan: 0.5
                1000 group
                    1002 group
                        1003 default
                            amplitude: 0.1, frequency: 555.0, gate: 1.0, out: 0.0, pan: 0.5
        15.0:
            NODE TREE 0 group
                1000 group
                    1002 group
                        1003 default
                            amplitude: 0.1, frequency: 555.0, gate: 1.0, out: 0.0, pan: 0.5
                    1001 default
                        amplitude: 0.1, frequency: 444.0, gate: 1.0, out: 0.0, pan: 0.5
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
                    0,
                    0,
                    "frequency",
                    444,
                ],
                ["/g_new", 1002, 0, 1000],
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1003,
                    0,
                    0,
                    "frequency",
                    555,
                ],
            ],
        ],
        [5.0, [["/g_tail", 1002, 1003]]],
        [15.0, [["/g_tail", 1000, 1001]]],
        [
            20.0,
            [
                ["/n_free", 1000, 1002],
                ["/n_set", 1001, "gate", 0],
                ["/n_set", 1003, "gate", 0],
                [0],
            ],
        ],
    ]
    group.delete()
    assert session.to_strings(True) == normalize(
        """
        0.0:
            NODE TREE 0 group
                1003 default
                    amplitude: 0.1, frequency: 555.0, gate: 1.0, out: 0.0, pan: 0.5
                1001 default
                    amplitude: 0.1, frequency: 444.0, gate: 1.0, out: 0.0, pan: 0.5
                1002 group
        5.0:
            NODE TREE 0 group
                1001 default
                    amplitude: 0.1, frequency: 444.0, gate: 1.0, out: 0.0, pan: 0.5
                1002 group
                    1003 default
                        amplitude: 0.1, frequency: 555.0, gate: 1.0, out: 0.0, pan: 0.5
        15.0:
            NODE TREE 0 group
                1002 group
                    1003 default
                        amplitude: 0.1, frequency: 555.0, gate: 1.0, out: 0.0, pan: 0.5
                1001 default
                    amplitude: 0.1, frequency: 444.0, gate: 1.0, out: 0.0, pan: 0.5
        20.0:
            NODE TREE 0 group
        """
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1003,
                    0,
                    0,
                    "frequency",
                    555,
                ],
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1001,
                    3,
                    1003,
                    "frequency",
                    444,
                ],
                ["/g_new", 1002, 3, 1001],
            ],
        ],
        [
            5.0,
            [
                ["/n_before", 1001, 1003],
                ["/n_before", 1002, 1003],
                ["/g_head", 1002, 1003],
            ],
        ],
        [15.0, [["/n_before", 1002, 1001]]],
        [
            20.0,
            [
                ["/n_free", 1002],
                ["/n_set", 1001, "gate", 0],
                ["/n_set", 1003, "gate", 0],
                [0],
            ],
        ],
    ]


def test_04():
    session = supriya.nonrealtime.Session()
    with session.at(0):
        synth_a = session.add_synth(duration=10)
    with session.at(5):
        synth_b = synth_a.add_synth(duration=10)
        synth_b.add_synth(duration=5)
    d_recv_commands = pytest.helpers.build_d_recv_commands(
        [supriya.assets.synthdefs.default]
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1000, 0, 0],
            ],
        ],
        [
            5.0,
            [
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1001, 2, 1000],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1002, 2, 1001],
            ],
        ],
        [10.0, [["/n_set", 1000, "gate", 0], ["/n_set", 1002, "gate", 0]]],
        [15.0, [["/n_set", 1001, "gate", 0], [0]]],
    ]
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1000 default
        5.0:
            NODE TREE 0 group
                1002 default
                1001 default
                1000 default
        10.0:
            NODE TREE 0 group
                1001 default
        15.0:
            NODE TREE 0 group
        """
    )
    synth_a.delete()
    assert session.to_lists() == [
        [
            5.0,
            [
                *d_recv_commands,
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1002, 0, 0],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1001, 3, 1002],
            ],
        ],
        [10.0, [["/n_set", 1002, "gate", 0]]],
        [15.0, [["/n_set", 1001, "gate", 0], [0]]],
    ]
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
        5.0:
            NODE TREE 0 group
                1002 default
                1001 default
        10.0:
            NODE TREE 0 group
                1001 default
        15.0:
            NODE TREE 0 group
        """
    )
