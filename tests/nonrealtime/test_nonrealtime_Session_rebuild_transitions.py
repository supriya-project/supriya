import pytest
from uqbar.strings import normalize

import supriya.assets.synthdefs
import supriya.nonrealtime


def test_01():
    session = supriya.nonrealtime.Session()
    with session.at(0):
        session.add_group(duration=20)
        group_b = session.add_group(duration=20)
        group_b.add_synth(duration=20)
    assert session.to_strings(True) == normalize(
        """
        0.0:
            NODE TREE 0 group
                1001 group
                    1002 default
                        amplitude: 0.1, frequency: 440.0, gate: 1.0, out: 0.0, pan: 0.5
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
                ["/g_new", 1001, 0, 0],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1002, 0, 1001],
            ],
        ],
        [20.0, [["/n_free", 1000, 1001], ["/n_set", 1002, "gate", 0], [0]]],
    ]
    session.rebuild_transitions()
    assert session.to_strings(True) == normalize(
        """
        0.0:
            NODE TREE 0 group
                1001 group
                    1002 default
                        amplitude: 0.1, frequency: 440.0, gate: 1.0, out: 0.0, pan: 0.5
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
                ["/g_new", 1001, 0, 0],
                ["/g_new", 1000, 3, 1001],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1002, 0, 1001],
            ],
        ],
        [20.0, [["/n_free", 1000, 1001], ["/n_set", 1002, "gate", 0], [0]]],
    ]
