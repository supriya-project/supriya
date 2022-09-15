import pytest
from uqbar.strings import normalize

import supriya.assets.synthdefs
import supriya.nonrealtime


def test_basic():
    session = supriya.nonrealtime.Session()
    with session.at(0):
        node = session.add_group(duration=20)
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
        [20.0, [["/n_free", 1000], [0]]],
    ]
    node.set_duration(30)
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1000 group
        30.0:
            NODE TREE 0 group
        """
    )
    assert session.to_lists() == [
        [0.0, [["/g_new", 1000, 0, 0]]],
        [30.0, [["/n_free", 1000], [0]]],
    ]
    node.set_duration(10)
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1000 group
        10.0:
            NODE TREE 0 group
        """
    )
    assert session.to_lists() == [
        [0.0, [["/g_new", 1000, 0, 0]]],
        [10.0, [["/n_free", 1000], [0]]],
    ]


def test_contained():
    session = supriya.nonrealtime.Session()
    with session.at(0):
        group_one = session.add_group(duration=30)
        group_two = group_one.add_group(duration=20)
        group_three = group_two.add_group(duration=10)
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1000 group
                    1001 group
                        1002 group
        10.0:
            NODE TREE 0 group
                1000 group
                    1001 group
        20.0:
            NODE TREE 0 group
                1000 group
        30.0:
            NODE TREE 0 group
        """
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                ["/g_new", 1000, 0, 0],
                ["/g_new", 1001, 0, 1000],
                ["/g_new", 1002, 0, 1001],
            ],
        ],
        [10.0, [["/n_free", 1002]]],
        [20.0, [["/n_free", 1001]]],
        [30.0, [["/n_free", 1000], [0]]],
    ]

    group_three.set_duration(20)
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1000 group
                    1001 group
                        1002 group
        20.0:
            NODE TREE 0 group
                1000 group
        30.0:
            NODE TREE 0 group
        """
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                ["/g_new", 1000, 0, 0],
                ["/g_new", 1001, 0, 1000],
                ["/g_new", 1002, 0, 1001],
            ],
        ],
        [20.0, [["/n_free", 1001, 1002]]],
        [30.0, [["/n_free", 1000], [0]]],
    ]

    group_three.set_duration(25)
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1000 group
                    1001 group
                        1002 group
        20.0:
            NODE TREE 0 group
                1000 group
                    1002 group
        25.0:
            NODE TREE 0 group
                1000 group
        30.0:
            NODE TREE 0 group
        """
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                ["/g_new", 1000, 0, 0],
                ["/g_new", 1001, 0, 1000],
                ["/g_new", 1002, 0, 1001],
            ],
        ],
        [20.0, [["/n_before", 1002, 1001], ["/n_free", 1001]]],
        [25.0, [["/n_free", 1002]]],
        [30.0, [["/n_free", 1000], [0]]],
    ]

    group_three.set_duration(30)
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1000 group
                    1001 group
                        1002 group
        20.0:
            NODE TREE 0 group
                1000 group
                    1002 group
        30.0:
            NODE TREE 0 group
        """
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                ["/g_new", 1000, 0, 0],
                ["/g_new", 1001, 0, 1000],
                ["/g_new", 1002, 0, 1001],
            ],
        ],
        [20.0, [["/n_before", 1002, 1001], ["/n_free", 1001]]],
        [30.0, [["/n_free", 1000, 1002], [0]]],
    ]

    group_three.set_duration(35)
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1000 group
                    1001 group
                        1002 group
        20.0:
            NODE TREE 0 group
                1000 group
                    1002 group
        30.0:
            NODE TREE 0 group
                1002 group
        35.0:
            NODE TREE 0 group
        """
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                ["/g_new", 1000, 0, 0],
                ["/g_new", 1001, 0, 1000],
                ["/g_new", 1002, 0, 1001],
            ],
        ],
        [20.0, [["/n_before", 1002, 1001], ["/n_free", 1001]]],
        [30.0, [["/n_before", 1002, 1000], ["/n_free", 1000]]],
        [35.0, [["/n_free", 1002], [0]]],
    ]


def test_pbus():
    session = supriya.nonrealtime.Session()
    with session.at(0):
        group = session.add_group()
        synth = group.add_synth(add_action="ADD_AFTER")
        group.add_synth(duration=10)
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1000 group
                    1002 default
                1001 default
        10.0:
            NODE TREE 0 group
                1000 group
                1001 default
        inf:
            NODE TREE 0 group
        """
    )
    synth.set_duration(15)
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1000 group
                    1002 default
                1001 default
        10.0:
            NODE TREE 0 group
                1000 group
                1001 default
        15.0:
            NODE TREE 0 group
                1000 group
        inf:
            NODE TREE 0 group
        """
    )
    group.set_duration(15)
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1000 group
                    1002 default
                1001 default
        10.0:
            NODE TREE 0 group
                1000 group
                1001 default
        15.0:
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
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1001, 3, 1000],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1002, 0, 1000],
            ],
        ],
        [10.0, [["/n_set", 1002, "gate", 0]]],
        [15.0, [["/n_free", 1000], ["/n_set", 1001, "gate", 0], [0]]],
    ]


def test_clip_children():
    session = supriya.nonrealtime.Session()
    with session.at(0):
        outer_group = session.add_group(duration=20)
        inner_group = outer_group.add_group(duration=20)
        inner_group.add_synth(duration=20)
        outer_group.add_group(duration=20)
        session.add_group(duration=20)
    assert session.to_strings(include_timespans=True) == normalize(
        """
        0.0:
            NODE TREE 0 group (timespan: [-inf, inf])
                1004 group (timespan: [0.0, 20.0])
                1000 group (timespan: [0.0, 20.0])
                    1003 group (timespan: [0.0, 20.0])
                    1001 group (timespan: [0.0, 20.0])
                        1002 default (timespan: [0.0, 20.0])
        20.0:
            NODE TREE 0 group (timespan: [-inf, inf])
        """
    )
    outer_group.set_duration(10, clip_children=True)
    assert session.to_strings(include_timespans=True) == normalize(
        """
        0.0:
            NODE TREE 0 group (timespan: [-inf, inf])
                1004 group (timespan: [0.0, 20.0])
                1000 group (timespan: [0.0, 10.0])
                    1003 group (timespan: [0.0, 10.0])
                    1001 group (timespan: [0.0, 10.0])
                        1002 default (timespan: [0.0, 10.0])
        10.0:
            NODE TREE 0 group (timespan: [-inf, inf])
                1004 group (timespan: [0.0, 20.0])
        20.0:
            NODE TREE 0 group (timespan: [-inf, inf])
        """
    )
