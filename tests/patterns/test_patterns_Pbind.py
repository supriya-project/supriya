import time

import pytest
import uqbar.strings

import supriya.assets.synthdefs
import supriya.nonrealtime
import supriya.patterns

pbind_01 = supriya.patterns.Pbind(
    amplitude=1.0,
    duration=supriya.patterns.Pseq([1.0, 2.0, 3.0], 1),
    frequency=supriya.patterns.Pseq([440, 660, 880], 1),
)


pbind_02 = supriya.patterns.Pbind(
    amplitude=1.0,
    duration=supriya.patterns.Pseq([1.0, 2.0, 3.0], 1),
    frequency=supriya.patterns.Pseq([[440, 550], [550, 660], [660, 770]]),
)


pbind_03 = supriya.patterns.Pbind(
    duration=1, delta=0.25, frequency=supriya.patterns.Pseq([220, 440, 330, 660], 2)
)


def test___iter___():
    events = list(pbind_01)
    assert pytest.helpers.get_objects_as_string(
        events, replace_uuids=True
    ) == uqbar.strings.normalize(
        """
        NoteEvent(
            amplitude=1.0,
            delta=1.0,
            duration=1.0,
            frequency=440,
            uuid=UUID('A'),
        )
        NoteEvent(
            amplitude=1.0,
            delta=2.0,
            duration=2.0,
            frequency=660,
            uuid=UUID('B'),
        )
        NoteEvent(
            amplitude=1.0,
            delta=3.0,
            duration=3.0,
            frequency=880,
            uuid=UUID('C'),
        )
        """
    )


def test_send():
    iterator = iter(pbind_01)
    next(iterator)
    with pytest.raises(StopIteration):
        iterator.send(True)


def test_manual_incommunicado_pbind_01():
    lists, deltas = pytest.helpers.manual_incommunicado(pbind_01)
    assert lists == [
        [10, [["/s_new", "default", 1000, 0, 1, "amplitude", 1.0, "frequency", 440]]],
        [
            11.0,
            [
                ["/n_set", 1000, "gate", 0],
                ["/s_new", "default", 1001, 0, 1, "amplitude", 1.0, "frequency", 660],
            ],
        ],
        [
            13.0,
            [
                ["/n_set", 1001, "gate", 0],
                ["/s_new", "default", 1002, 0, 1, "amplitude", 1.0, "frequency", 880],
            ],
        ],
        [16.0, [["/n_set", 1002, "gate", 0]]],
    ]
    assert deltas == [1.0, 2.0, 3.0, None]


def test_manual_communicado_pbind_01(server):
    player = supriya.patterns.EventPlayer(pbind_01, server=server)
    # Initial State
    server_state = str(server.query_remote_nodes(include_controls=True))
    assert server_state == uqbar.strings.normalize(
        r"""
        NODE TREE 0 group
            1 group
    """
    )
    # Step 1
    context = pytest.helpers.make_clock_context(0)
    player(context)
    server.sync()
    server_state = str(server.query_remote_nodes(include_controls=True))
    assert server_state == uqbar.strings.normalize(
        r"""
        NODE TREE 0 group
            1 group
                1000 default
                    out: 0.0, amplitude: 1.0, frequency: 440.0, gate: 1.0, pan: 0.5
    """
    )
    # Step 2
    context = pytest.helpers.make_clock_context(0)
    player(context)
    server.sync()
    server_state = str(server.query_remote_nodes(include_controls=True))
    assert server_state == uqbar.strings.normalize(
        r"""
        NODE TREE 0 group
            1 group
                1001 default
                    out: 0.0, amplitude: 1.0, frequency: 660.0, gate: 1.0, pan: 0.5
                1000 default
                    out: 0.0, amplitude: 1.0, frequency: 440.0, gate: 0.0, pan: 0.5
    """
    )
    # Wait for termination
    time.sleep(0.5)
    server_state = str(server.query_remote_nodes(include_controls=True))
    assert server_state == uqbar.strings.normalize(
        r"""
        NODE TREE 0 group
            1 group
                1001 default
                    out: 0.0, amplitude: 1.0, frequency: 660.0, gate: 1.0, pan: 0.5
    """
    )
    # Step 3
    context = pytest.helpers.make_clock_context(0)
    player(context)
    server.sync()
    server_state = str(server.query_remote_nodes(include_controls=True))
    assert server_state == uqbar.strings.normalize(
        r"""
        NODE TREE 0 group
            1 group
                1002 default
                    out: 0.0, amplitude: 1.0, frequency: 880.0, gate: 1.0, pan: 0.5
                1001 default
                    out: 0.0, amplitude: 1.0, frequency: 660.0, gate: 0.0, pan: 0.5
    """
    )
    # Wait for termination
    time.sleep(0.5)
    server_state = str(server.query_remote_nodes(include_controls=True))
    assert server_state == uqbar.strings.normalize(
        r"""
        NODE TREE 0 group
            1 group
                1002 default
                    out: 0.0, amplitude: 1.0, frequency: 880.0, gate: 1.0, pan: 0.5
    """
    )
    # Step 4
    player(context)
    server.sync()
    server_state = str(server.query_remote_nodes(include_controls=True))
    assert server_state == uqbar.strings.normalize(
        r"""
        NODE TREE 0 group
            1 group
                1002 default
                    out: 0.0, amplitude: 1.0, frequency: 880.0, gate: 0.0, pan: 0.5
    """
    )
    # Wait for termination
    time.sleep(0.5)
    server_state = str(server.query_remote_nodes(include_controls=True))
    assert server_state == uqbar.strings.normalize(
        r"""
        NODE TREE 0 group
            1 group
    """
    )


def test_automatic_communicado_pbind_01(server):
    pbind_01.play(server=server)
    time.sleep(6)


def test_manual_incommunicado_pbind_02():
    lists, deltas = pytest.helpers.manual_incommunicado(pbind_02)
    assert lists == [
        [
            10,
            [
                ["/s_new", "default", 1000, 0, 1, "amplitude", 1.0, "frequency", 440],
                ["/s_new", "default", 1001, 0, 1, "amplitude", 1.0, "frequency", 550],
            ],
        ],
        [
            11.0,
            [
                ["/n_set", 1000, "gate", 0],
                ["/n_set", 1001, "gate", 0],
                ["/s_new", "default", 1002, 0, 1, "amplitude", 1.0, "frequency", 550],
                ["/s_new", "default", 1003, 0, 1, "amplitude", 1.0, "frequency", 660],
            ],
        ],
        [
            13.0,
            [
                ["/n_set", 1002, "gate", 0],
                ["/n_set", 1003, "gate", 0],
                ["/s_new", "default", 1004, 0, 1, "amplitude", 1.0, "frequency", 660],
                ["/s_new", "default", 1005, 0, 1, "amplitude", 1.0, "frequency", 770],
            ],
        ],
        [16.0, [["/n_set", 1004, "gate", 0], ["/n_set", 1005, "gate", 0]]],
    ]
    assert deltas == [1.0, 2.0, 3.0, None]


def test_manual_communicado_pbind_02(server):
    player = supriya.patterns.EventPlayer(pbind_02, server=server)  # Initial State
    server_state = str(server.query_remote_nodes(include_controls=True))
    assert server_state == uqbar.strings.normalize(
        r"""
        NODE TREE 0 group
            1 group
    """
    )
    # Step 1
    context = pytest.helpers.make_clock_context(0)
    player(context)
    server.sync()
    server_state = str(server.query_remote_nodes(include_controls=True))
    assert server_state == uqbar.strings.normalize(
        r"""
        NODE TREE 0 group
            1 group
                1001 default
                    out: 0.0, amplitude: 1.0, frequency: 550.0, gate: 1.0, pan: 0.5
                1000 default
                    out: 0.0, amplitude: 1.0, frequency: 440.0, gate: 1.0, pan: 0.5
    """
    )
    # Step 2
    context = pytest.helpers.make_clock_context(0)
    player(context)
    server.sync()
    server_state = str(server.query_remote_nodes(include_controls=True))
    assert server_state == uqbar.strings.normalize(
        r"""
        NODE TREE 0 group
            1 group
                1003 default
                    out: 0.0, amplitude: 1.0, frequency: 660.0, gate: 1.0, pan: 0.5
                1002 default
                    out: 0.0, amplitude: 1.0, frequency: 550.0, gate: 1.0, pan: 0.5
                1001 default
                    out: 0.0, amplitude: 1.0, frequency: 550.0, gate: 0.0, pan: 0.5
                1000 default
                    out: 0.0, amplitude: 1.0, frequency: 440.0, gate: 0.0, pan: 0.5
    """
    )
    # Wait for termination
    time.sleep(0.5)
    server_state = str(server.query_remote_nodes(include_controls=True))
    assert server_state == uqbar.strings.normalize(
        r"""
        NODE TREE 0 group
            1 group
                1003 default
                    out: 0.0, amplitude: 1.0, frequency: 660.0, gate: 1.0, pan: 0.5
                1002 default
                    out: 0.0, amplitude: 1.0, frequency: 550.0, gate: 1.0, pan: 0.5
    """
    )
    # Step 3
    context = pytest.helpers.make_clock_context(0)
    player(context)
    server.sync()
    server_state = str(server.query_remote_nodes(include_controls=True))
    assert server_state == uqbar.strings.normalize(
        r"""
        NODE TREE 0 group
            1 group
                1005 default
                    out: 0.0, amplitude: 1.0, frequency: 770.0, gate: 1.0, pan: 0.5
                1004 default
                    out: 0.0, amplitude: 1.0, frequency: 660.0, gate: 1.0, pan: 0.5
                1003 default
                    out: 0.0, amplitude: 1.0, frequency: 660.0, gate: 0.0, pan: 0.5
                1002 default
                    out: 0.0, amplitude: 1.0, frequency: 550.0, gate: 0.0, pan: 0.5
    """
    )
    # Wait for termination
    time.sleep(0.5)
    server_state = str(server.query_remote_nodes(include_controls=True))
    assert server_state == uqbar.strings.normalize(
        r"""
        NODE TREE 0 group
            1 group
                1005 default
                    out: 0.0, amplitude: 1.0, frequency: 770.0, gate: 1.0, pan: 0.5
                1004 default
                    out: 0.0, amplitude: 1.0, frequency: 660.0, gate: 1.0, pan: 0.5
    """
    )
    # Step 4
    context = pytest.helpers.make_clock_context(0)
    player(context)
    server.sync()
    server_state = str(server.query_remote_nodes(include_controls=True))
    assert server_state == uqbar.strings.normalize(
        r"""
        NODE TREE 0 group
            1 group
                1005 default
                    out: 0.0, amplitude: 1.0, frequency: 770.0, gate: 0.0, pan: 0.5
                1004 default
                    out: 0.0, amplitude: 1.0, frequency: 660.0, gate: 0.0, pan: 0.5
    """
    )
    # Wait for termination
    time.sleep(0.5)
    server_state = str(server.query_remote_nodes(include_controls=True))
    assert server_state == uqbar.strings.normalize(
        r"""
        NODE TREE 0 group
            1 group
    """
    )


def test_automatic_communicado_pbind_02(server):
    pbind_02.play(server=server)
    time.sleep(6)


def test_manual_incommunicado_pbind_03():
    lists, deltas = pytest.helpers.manual_incommunicado(pbind_03)
    assert deltas == [
        0.25,
        0.25,
        0.25,
        0.25,
        0.25,
        0.25,
        0.25,
        0.25,
        0.25,
        0.25,
        0.25,
        None,
    ]
    assert lists == [
        [10, [["/s_new", "default", 1000, 0, 1, "frequency", 220]]],
        [10.25, [["/s_new", "default", 1001, 0, 1, "frequency", 440]]],
        [10.5, [["/s_new", "default", 1002, 0, 1, "frequency", 330]]],
        [10.75, [["/s_new", "default", 1003, 0, 1, "frequency", 660]]],
        [
            11.0,
            [
                ["/n_set", 1000, "gate", 0],
                ["/s_new", "default", 1004, 0, 1, "frequency", 220],
            ],
        ],
        [
            11.25,
            [
                ["/n_set", 1001, "gate", 0],
                ["/s_new", "default", 1005, 0, 1, "frequency", 440],
            ],
        ],
        [
            11.5,
            [
                ["/n_set", 1002, "gate", 0],
                ["/s_new", "default", 1006, 0, 1, "frequency", 330],
            ],
        ],
        [
            11.75,
            [
                ["/n_set", 1003, "gate", 0],
                ["/s_new", "default", 1007, 0, 1, "frequency", 660],
            ],
        ],
        [12.0, [["/n_set", 1004, "gate", 0]]],
        [12.25, [["/n_set", 1005, "gate", 0]]],
        [12.5, [["/n_set", 1006, "gate", 0]]],
        [12.75, [["/n_set", 1007, "gate", 0]]],
    ]


def test_nonrealtime_01a():
    session = supriya.nonrealtime.Session()
    with session.at(0):
        final_offset = session.inscribe(pbind_01)
    d_recv_commands = pytest.helpers.build_d_recv_commands(
        [supriya.assets.synthdefs.default]
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1000,
                    0,
                    0,
                    "amplitude",
                    1.0,
                    "frequency",
                    440,
                ],
            ],
        ],
        [
            1.0,
            [
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1001,
                    0,
                    0,
                    "amplitude",
                    1.0,
                    "frequency",
                    660,
                ],
                ["/n_set", 1000, "gate", 0],
            ],
        ],
        [
            3.0,
            [
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1002,
                    0,
                    0,
                    "amplitude",
                    1.0,
                    "frequency",
                    880,
                ],
                ["/n_set", 1001, "gate", 0],
            ],
        ],
        [6.0, [["/n_set", 1002, "gate", 0], [0]]],
    ]
    assert final_offset == 6.0


def test_nonrealtime_01b():
    session = supriya.nonrealtime.Session()
    with session.at(0):
        final_offset = session.inscribe(pbind_01, duration=3)
    d_recv_commands = pytest.helpers.build_d_recv_commands(
        [supriya.assets.synthdefs.default]
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1000,
                    0,
                    0,
                    "amplitude",
                    1.0,
                    "frequency",
                    440,
                ],
            ],
        ],
        [
            1.0,
            [
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1001,
                    0,
                    0,
                    "amplitude",
                    1.0,
                    "frequency",
                    660,
                ],
                ["/n_set", 1000, "gate", 0],
            ],
        ],
        [3.0, [["/n_set", 1001, "gate", 0], [0]]],
    ]
    assert final_offset == 3.0


def test_nonrealtime_01c():
    session = supriya.nonrealtime.Session()
    with session.at(0):
        final_offset = session.inscribe(pbind_01, duration=2)
    d_recv_commands = pytest.helpers.build_d_recv_commands(
        [supriya.assets.synthdefs.default]
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1000,
                    0,
                    0,
                    "amplitude",
                    1.0,
                    "frequency",
                    440,
                ],
            ],
        ],
        [1.0, [["/n_set", 1000, "gate", 0], [0]]],
    ]
    assert final_offset == 1.0


def test_nonrealtime_02a():
    session = supriya.nonrealtime.Session()
    with session.at(10):
        final_offset = session.inscribe(pbind_02)
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
                    1.0,
                    "frequency",
                    440,
                ],
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1001,
                    0,
                    0,
                    "amplitude",
                    1.0,
                    "frequency",
                    550,
                ],
            ],
        ],
        [
            11.0,
            [
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1002,
                    0,
                    0,
                    "amplitude",
                    1.0,
                    "frequency",
                    550,
                ],
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1003,
                    0,
                    0,
                    "amplitude",
                    1.0,
                    "frequency",
                    660,
                ],
                ["/n_set", 1000, "gate", 0],
                ["/n_set", 1001, "gate", 0],
            ],
        ],
        [
            13.0,
            [
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1004,
                    0,
                    0,
                    "amplitude",
                    1.0,
                    "frequency",
                    660,
                ],
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1005,
                    0,
                    0,
                    "amplitude",
                    1.0,
                    "frequency",
                    770,
                ],
                ["/n_set", 1002, "gate", 0],
                ["/n_set", 1003, "gate", 0],
            ],
        ],
        [16.0, [["/n_set", 1004, "gate", 0], ["/n_set", 1005, "gate", 0], [0]]],
    ]
    assert final_offset == 16.0


def test_nonrealtime_03a():
    session = supriya.nonrealtime.Session()
    with session.at(0):
        final_offset = session.inscribe(pbind_03)
    d_recv_commands = pytest.helpers.build_d_recv_commands(
        [supriya.assets.synthdefs.default]
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1000,
                    0,
                    0,
                    "frequency",
                    220,
                ],
            ],
        ],
        [
            0.25,
            [
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1001,
                    0,
                    0,
                    "frequency",
                    440,
                ]
            ],
        ],
        [
            0.5,
            [
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1002,
                    0,
                    0,
                    "frequency",
                    330,
                ]
            ],
        ],
        [
            0.75,
            [
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1003,
                    0,
                    0,
                    "frequency",
                    660,
                ]
            ],
        ],
        [
            1.0,
            [
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1004,
                    0,
                    0,
                    "frequency",
                    220,
                ],
                ["/n_set", 1000, "gate", 0],
            ],
        ],
        [
            1.25,
            [
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1005,
                    0,
                    0,
                    "frequency",
                    440,
                ],
                ["/n_set", 1001, "gate", 0],
            ],
        ],
        [
            1.5,
            [
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1006,
                    0,
                    0,
                    "frequency",
                    330,
                ],
                ["/n_set", 1002, "gate", 0],
            ],
        ],
        [
            1.75,
            [
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1007,
                    0,
                    0,
                    "frequency",
                    660,
                ],
                ["/n_set", 1003, "gate", 0],
            ],
        ],
        [2.0, [["/n_set", 1004, "gate", 0]]],
        [2.25, [["/n_set", 1005, "gate", 0]]],
        [2.5, [["/n_set", 1006, "gate", 0]]],
        [2.75, [["/n_set", 1007, "gate", 0], [0]]],
    ]
    assert final_offset == 2.75


def test_manual_stop_pbind_01(server):
    # Initial State
    server_state = str(server.query_remote_nodes(include_controls=True))
    assert server_state == uqbar.strings.normalize(
        r"""
        NODE TREE 0 group
            1 group
    """
    )
    player = pbind_01.play(server=server)
    time.sleep(2.5)
    server_state = str(server.query_remote_nodes(include_controls=True))
    assert server_state == uqbar.strings.normalize(
        r"""
        NODE TREE 0 group
            1 group
                1001 default
                    out: 0.0, amplitude: 1.0, frequency: 660.0, gate: 1.0, pan: 0.5
    """
    )
    player.stop()
    server_state = str(server.query_remote_nodes(include_controls=True))
    assert server_state == uqbar.strings.normalize(
        r"""
        NODE TREE 0 group
            1 group
    """
    )
    #        assert server_state == uqbar.strings.normalize(r'''
    #            NODE TREE 0 group
    #                1 group
    #                    1001 default
    #                        out: 0.0, amplitude: 1.0, frequency: 660.0, gate: 0.0, pan: 0.5
    #        ''')
    # Wait for termination
    time.sleep(0.5)
    server_state = str(server.query_remote_nodes(include_controls=True))
    assert server_state == uqbar.strings.normalize(
        r"""
        NODE TREE 0 group
            1 group
    """
    )


def test_manual_stop_pbind_02(server):
    # Initial State
    server_state = str(server.query_remote_nodes(include_controls=True))
    assert server_state == uqbar.strings.normalize(
        r"""
        NODE TREE 0 group
            1 group
    """
    )
    player = pbind_02.play(server=server)
    time.sleep(2)
    server.sync()
    server_state = str(server.query_remote_nodes(include_controls=True))
    assert server_state == uqbar.strings.normalize(
        r"""
        NODE TREE 0 group
            1 group
                1003 default
                    out: 0.0, amplitude: 1.0, frequency: 660.0, gate: 1.0, pan: 0.5
                1002 default
                    out: 0.0, amplitude: 1.0, frequency: 550.0, gate: 1.0, pan: 0.5
                1001 default
                    out: 0.0, amplitude: 1.0, frequency: 550.0, gate: 0.0, pan: 0.5
                1000 default
                    out: 0.0, amplitude: 1.0, frequency: 440.0, gate: 0.0, pan: 0.5
    """
    )
    player.stop()
    server.sync()
    server_state = str(server.query_remote_nodes(include_controls=True))
    assert server_state == uqbar.strings.normalize(
        r"""
        NODE TREE 0 group
            1 group
                1001 default
                    out: 0.0, amplitude: 1.0, frequency: 550.0, gate: 0.0, pan: 0.5
                1000 default
                    out: 0.0, amplitude: 1.0, frequency: 440.0, gate: 0.0, pan: 0.5
    """
    )
    # Wait for termination
    time.sleep(0.5)
    server_state = str(server.query_remote_nodes(include_controls=True))
    assert server_state == uqbar.strings.normalize(
        r"""
        NODE TREE 0 group
            1 group
    """
    )
