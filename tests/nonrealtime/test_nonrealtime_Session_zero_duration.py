import pytest

import supriya.assets.synthdefs
import supriya.nonrealtime
import supriya.synthdefs
import supriya.ugens


def test_manual_with_gate():
    session = supriya.nonrealtime.Session(0, 2)
    with session.at(0):
        group = session.add_group(duration=4)
    for i in range(4):
        with session.at(i):
            group.add_synth(duration=0)
    d_recv_commands = pytest.helpers.build_d_recv_commands(
        [supriya.assets.synthdefs.default]
    )
    assert session.to_lists(duration=5) == [
        [
            0.0,
            [
                *d_recv_commands,
                ["/g_new", 1000, 0, 0],
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1001, 0, 1000],
                ["/n_set", 1001, "gate", 0],
            ],
        ],
        [
            1.0,
            [
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1002, 0, 1000],
                ["/n_set", 1002, "gate", 0],
            ],
        ],
        [
            2.0,
            [
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1003, 0, 1000],
                ["/n_set", 1003, "gate", 0],
            ],
        ],
        [
            3.0,
            [
                ["/s_new", "da0982184cc8fa54cf9d288a0fe1f6ca", 1004, 0, 1000],
                ["/n_set", 1004, "gate", 0],
            ],
        ],
        [4.0, [["/n_free", 1000]]],
        [5.0, [[0]]],
    ]


def test_manual_without_gate():
    with supriya.synthdefs.SynthDefBuilder() as builder:
        source = supriya.ugens.DC.ar(source=1)
        supriya.ugens.Out.ar(bus=0, source=source)
    source_synthdef = builder.build()
    session = supriya.nonrealtime.Session(0, 1)
    with session.at(0):
        group = session.add_group(duration=4)
    for i in range(4):
        with session.at(i):
            group.add_synth(duration=0, synthdef=source_synthdef)
    assert session.to_lists(duration=10) == [
        [
            0.0,
            [
                ["/d_recv", bytearray(source_synthdef.compile())],
                ["/g_new", 1000, 0, 0],
                ["/s_new", "7839f99c38c2ac4326388a013cdd643c", 1001, 0, 1000],
            ],
        ],
        [1.0, [["/s_new", "7839f99c38c2ac4326388a013cdd643c", 1002, 0, 1000]]],
        [2.0, [["/s_new", "7839f99c38c2ac4326388a013cdd643c", 1003, 0, 1000]]],
        [3.0, [["/s_new", "7839f99c38c2ac4326388a013cdd643c", 1004, 0, 1000]]],
        [4.0, [["/n_free", 1000]]],
        [10.0, [[0]]],
    ]
