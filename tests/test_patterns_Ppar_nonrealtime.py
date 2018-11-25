import pytest

import supriya.assets.synthdefs
import supriya.nonrealtime
import supriya.patterns

pattern_01 = supriya.patterns.Ppar(
    [
        supriya.patterns.Pbind(
            delta=8,
            duration=supriya.patterns.Pseq([10], 4),
            frequency=supriya.patterns.Pseq([1001, 1002, 1003, 1004]),
        ),
        supriya.patterns.Pbind(
            delta=10,
            duration=supriya.patterns.Pseq([10], 3),
            frequency=supriya.patterns.Pseq([2001, 2002, 2003]),
        ),
        supriya.patterns.Pbind(
            delta=12,
            duration=supriya.patterns.Pseq([10], 3),
            frequency=supriya.patterns.Pseq([3001, 3002, 3003]),
        ),
    ]
)


pattern_02 = pattern_01.with_bus()


pattern_03 = supriya.patterns.Ppar(
    [
        supriya.patterns.Pbind(
            delta=10,
            duration=supriya.patterns.Pseq([10], 3),
            frequency=supriya.patterns.Pseq([2001, 2002, 2003]),
        ).with_group(),
        supriya.patterns.Pbind(
            delta=12,
            duration=supriya.patterns.Pseq([10], 3),
            frequency=supriya.patterns.Pseq([3001, 3002, 3003]),
        ).with_group(),
    ]
)


pattern_04 = supriya.patterns.Ppar(
    [
        supriya.patterns.Pbind(
            delta=10,
            duration=supriya.patterns.Pseq([10], None),
            frequency=supriya.patterns.Pseq([1001, 1002, 1003, 1004, 1005]),
        ).with_group()
    ]
)


pattern_05 = supriya.patterns.Ppar(
    [
        supriya.patterns.Pgpar(
            [
                [
                    supriya.patterns.Pbind(
                        delta=10,
                        duration=supriya.patterns.Pseq([10], 3),
                        frequency=supriya.patterns.Pseq([1001, 1002, 1003]),
                    ),
                    supriya.patterns.Pbind(
                        delta=12,
                        duration=supriya.patterns.Pseq([10], 3),
                        frequency=supriya.patterns.Pseq([2001, 2002, 2003]),
                    ),
                ]
            ]
        ),
        supriya.patterns.Pgpar(
            [
                [
                    supriya.patterns.Pbind(
                        delta=10,
                        duration=supriya.patterns.Pseq([10], 3),
                        frequency=supriya.patterns.Pseq([3001, 3002, 3003]),
                    ),
                    supriya.patterns.Pbind(
                        delta=12,
                        duration=supriya.patterns.Pseq([10], 3),
                        frequency=supriya.patterns.Pseq([4001, 4002, 4003]),
                    ),
                ]
            ]
        ),
    ]
)


def test_nonrealtime_01a():
    session = supriya.nonrealtime.Session(0, 2)
    with session.at(0):
        final_offset = session.inscribe(pattern_01)
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
                    1001,
                ],
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1001,
                    0,
                    0,
                    "frequency",
                    2001,
                ],
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1002,
                    0,
                    0,
                    "frequency",
                    3001,
                ],
            ],
        ],
        [
            8.0,
            [
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1003,
                    0,
                    0,
                    "frequency",
                    1002,
                ]
            ],
        ],
        [
            10.0,
            [
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1004,
                    0,
                    0,
                    "frequency",
                    2002,
                ],
                ["/n_set", 1000, "gate", 0],
                ["/n_set", 1001, "gate", 0],
                ["/n_set", 1002, "gate", 0],
            ],
        ],
        [
            12.0,
            [
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1005,
                    0,
                    0,
                    "frequency",
                    3002,
                ]
            ],
        ],
        [
            16.0,
            [
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1006,
                    0,
                    0,
                    "frequency",
                    1003,
                ]
            ],
        ],
        [18.0, [["/n_set", 1003, "gate", 0]]],
        [
            20.0,
            [
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1007,
                    0,
                    0,
                    "frequency",
                    2003,
                ],
                ["/n_set", 1004, "gate", 0],
            ],
        ],
        [22.0, [["/n_set", 1005, "gate", 0]]],
        [
            24.0,
            [
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1008,
                    0,
                    0,
                    "frequency",
                    1004,
                ],
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1009,
                    0,
                    0,
                    "frequency",
                    3003,
                ],
            ],
        ],
        [26.0, [["/n_set", 1006, "gate", 0]]],
        [30.0, [["/n_set", 1007, "gate", 0]]],
        [34.0, [["/n_set", 1008, "gate", 0], ["/n_set", 1009, "gate", 0], [0]]],
    ]
    assert final_offset == 36.0


def test_nonrealtime_01b():
    d_recv_commands = pytest.helpers.build_d_recv_commands(
        [supriya.assets.synthdefs.default]
    )
    for duration in (10.0, 11.0, 12.0):
        session = supriya.nonrealtime.Session(0, 2)
        with session.at(0):
            final_offset = session.inscribe(pattern_01, duration=duration)
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
                        1001,
                    ],
                    [
                        "/s_new",
                        "da0982184cc8fa54cf9d288a0fe1f6ca",
                        1001,
                        0,
                        0,
                        "frequency",
                        2001,
                    ],
                    [
                        "/s_new",
                        "da0982184cc8fa54cf9d288a0fe1f6ca",
                        1002,
                        0,
                        0,
                        "frequency",
                        3001,
                    ],
                ],
            ],
            [
                10.0,
                [
                    ["/n_set", 1000, "gate", 0],
                    ["/n_set", 1001, "gate", 0],
                    ["/n_set", 1002, "gate", 0],
                    [0],
                ],
            ],
        ]
        assert final_offset == 10.0


def test_nonrealtime_02a():
    session = supriya.nonrealtime.Session(0, 2)
    with session.at(0):
        final_offset = session.inscribe(pattern_02)
    d_recv_commands = pytest.helpers.build_d_recv_commands(
        [supriya.assets.synthdefs.system_link_audio_2, supriya.assets.synthdefs.default]
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                ["/g_new", 1000, 0, 0],
                [
                    "/s_new",
                    "38a2c79fc9d58d06e361337163a4e80f",
                    1001,
                    3,
                    1000,
                    "fade_time",
                    0.25,
                    "in_",
                    2,
                ],
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1002,
                    0,
                    1000,
                    "frequency",
                    1001,
                    "out",
                    2,
                ],
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1003,
                    0,
                    1000,
                    "frequency",
                    2001,
                    "out",
                    2,
                ],
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1004,
                    0,
                    1000,
                    "frequency",
                    3001,
                    "out",
                    2,
                ],
            ],
        ],
        [
            8.0,
            [
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1005,
                    0,
                    1000,
                    "frequency",
                    1002,
                    "out",
                    2,
                ]
            ],
        ],
        [
            10.0,
            [
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1006,
                    0,
                    1000,
                    "frequency",
                    2002,
                    "out",
                    2,
                ],
                ["/n_set", 1002, "gate", 0],
                ["/n_set", 1003, "gate", 0],
                ["/n_set", 1004, "gate", 0],
            ],
        ],
        [
            12.0,
            [
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1007,
                    0,
                    1000,
                    "frequency",
                    3002,
                    "out",
                    2,
                ]
            ],
        ],
        [
            16.0,
            [
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1008,
                    0,
                    1000,
                    "frequency",
                    1003,
                    "out",
                    2,
                ]
            ],
        ],
        [18.0, [["/n_set", 1005, "gate", 0]]],
        [
            20.0,
            [
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1009,
                    0,
                    1000,
                    "frequency",
                    2003,
                    "out",
                    2,
                ],
                ["/n_set", 1006, "gate", 0],
            ],
        ],
        [22.0, [["/n_set", 1007, "gate", 0]]],
        [
            24.0,
            [
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1010,
                    0,
                    1000,
                    "frequency",
                    1004,
                    "out",
                    2,
                ],
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1011,
                    0,
                    1000,
                    "frequency",
                    3003,
                    "out",
                    2,
                ],
            ],
        ],
        [26.0, [["/n_set", 1008, "gate", 0]]],
        [30.0, [["/n_set", 1009, "gate", 0]]],
        [34.0, [["/n_set", 1010, "gate", 0], ["/n_set", 1011, "gate", 0]]],
        [36.0, [["/n_set", 1001, "gate", 0]]],
        [36.25, [["/n_free", 1000], [0]]],
    ]
    assert final_offset == 36.25


def test_nonrealtime_02b():
    d_recv_commands = pytest.helpers.build_d_recv_commands(
        [supriya.assets.synthdefs.default, supriya.assets.synthdefs.system_link_audio_2]
    )
    for duration in (10.0, 11.0, 12.0):
        session = supriya.nonrealtime.Session(0, 2)
        with session.at(0):
            final_offset = session.inscribe(pattern_02, duration=duration)
        assert session.to_lists() == [
            [
                0.0,
                [
                    *d_recv_commands,
                    ["/g_new", 1000, 0, 0],
                    [
                        "/s_new",
                        "38a2c79fc9d58d06e361337163a4e80f",
                        1001,
                        3,
                        1000,
                        "fade_time",
                        0.25,
                        "in_",
                        2,
                    ],
                    [
                        "/s_new",
                        "da0982184cc8fa54cf9d288a0fe1f6ca",
                        1002,
                        0,
                        1000,
                        "frequency",
                        1001,
                        "out",
                        2,
                    ],
                    [
                        "/s_new",
                        "da0982184cc8fa54cf9d288a0fe1f6ca",
                        1003,
                        0,
                        1000,
                        "frequency",
                        2001,
                        "out",
                        2,
                    ],
                    [
                        "/s_new",
                        "da0982184cc8fa54cf9d288a0fe1f6ca",
                        1004,
                        0,
                        1000,
                        "frequency",
                        3001,
                        "out",
                        2,
                    ],
                ],
            ],
            [
                10.0,
                [
                    ["/n_set", 1001, "gate", 0],
                    ["/n_set", 1002, "gate", 0],
                    ["/n_set", 1003, "gate", 0],
                    ["/n_set", 1004, "gate", 0],
                ],
            ],
            [10.25, [["/n_free", 1000], [0]]],
        ]
        assert final_offset == 10.25


def test_nonrealtime_03a():
    session = supriya.nonrealtime.Session(0, 2)
    with session.at(0):
        final_offset = session.inscribe(pattern_03)
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
                    1000,
                    "frequency",
                    2001,
                ],
                ["/g_new", 1002, 0, 0],
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1003,
                    0,
                    1002,
                    "frequency",
                    3001,
                ],
            ],
        ],
        [
            10.0,
            [
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1004,
                    0,
                    1000,
                    "frequency",
                    2002,
                ],
                ["/n_set", 1001, "gate", 0],
                ["/n_set", 1003, "gate", 0],
            ],
        ],
        [
            12.0,
            [
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1005,
                    0,
                    1002,
                    "frequency",
                    3002,
                ]
            ],
        ],
        [
            20.0,
            [
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1006,
                    0,
                    1000,
                    "frequency",
                    2003,
                ],
                ["/n_set", 1004, "gate", 0],
            ],
        ],
        [22.0, [["/n_set", 1005, "gate", 0]]],
        [
            24.0,
            [
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1007,
                    0,
                    1002,
                    "frequency",
                    3003,
                ]
            ],
        ],
        [30.0, [["/n_set", 1006, "gate", 0]]],
        [30.25, [["/n_free", 1000]]],
        [34.0, [["/n_set", 1007, "gate", 0]]],
        [36.25, [["/n_free", 1002], [0]]],
    ]
    assert final_offset == 36.25


def test_nonrealtime_04b():
    session = supriya.nonrealtime.Session(0, 2)
    with session.at(0):
        final_offset = session.inscribe(pattern_04, duration=29.0)
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
                    1000,
                    "frequency",
                    1001,
                ],
            ],
        ],
        [
            10.0,
            [
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1002,
                    0,
                    1000,
                    "frequency",
                    1002,
                ],
                ["/n_set", 1001, "gate", 0],
            ],
        ],
        [20.0, [["/n_set", 1002, "gate", 0]]],
        [20.25, [["/n_free", 1000], [0]]],
    ]
    assert final_offset == 20.25


def test_nonrealtime_05a():
    session = supriya.nonrealtime.Session(0, 2)
    with session.at(0):
        final_offset = session.inscribe(pattern_05)
    d_recv_commands = pytest.helpers.build_d_recv_commands(
        [supriya.assets.synthdefs.default]
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                ["/g_new", 1000, 1, 0],
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1001,
                    0,
                    1000,
                    "frequency",
                    1001,
                ],
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1002,
                    0,
                    1000,
                    "frequency",
                    2001,
                ],
                ["/g_new", 1003, 1, 0],
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1004,
                    0,
                    1003,
                    "frequency",
                    3001,
                ],
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1005,
                    0,
                    1003,
                    "frequency",
                    4001,
                ],
            ],
        ],
        [
            10.0,
            [
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1006,
                    0,
                    1000,
                    "frequency",
                    1002,
                ],
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1007,
                    0,
                    1003,
                    "frequency",
                    3002,
                ],
                ["/n_set", 1001, "gate", 0],
                ["/n_set", 1002, "gate", 0],
                ["/n_set", 1004, "gate", 0],
                ["/n_set", 1005, "gate", 0],
            ],
        ],
        [
            12.0,
            [
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1008,
                    0,
                    1000,
                    "frequency",
                    2002,
                ],
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1009,
                    0,
                    1003,
                    "frequency",
                    4002,
                ],
            ],
        ],
        [
            20.0,
            [
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1010,
                    0,
                    1000,
                    "frequency",
                    1003,
                ],
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1011,
                    0,
                    1003,
                    "frequency",
                    3003,
                ],
                ["/n_set", 1006, "gate", 0],
                ["/n_set", 1007, "gate", 0],
            ],
        ],
        [22.0, [["/n_set", 1008, "gate", 0], ["/n_set", 1009, "gate", 0]]],
        [
            24.0,
            [
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1012,
                    0,
                    1000,
                    "frequency",
                    2003,
                ],
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1013,
                    0,
                    1003,
                    "frequency",
                    4003,
                ],
            ],
        ],
        [30.0, [["/n_set", 1010, "gate", 0], ["/n_set", 1011, "gate", 0]]],
        [34.0, [["/n_set", 1012, "gate", 0], ["/n_set", 1013, "gate", 0]]],
        [36.25, [["/n_free", 1000, 1003], [0]]],
    ]
    assert final_offset == 36.25


def test_nonrealtime_05b():
    session = supriya.nonrealtime.Session(0, 2)
    with session.at(0):
        final_offset = session.inscribe(pattern_05, duration=25.0)
    d_recv_commands = pytest.helpers.build_d_recv_commands(
        [supriya.assets.synthdefs.default]
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                ["/g_new", 1000, 1, 0],
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1001,
                    0,
                    1000,
                    "frequency",
                    1001,
                ],
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1002,
                    0,
                    1000,
                    "frequency",
                    2001,
                ],
                ["/g_new", 1003, 1, 0],
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1004,
                    0,
                    1003,
                    "frequency",
                    3001,
                ],
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1005,
                    0,
                    1003,
                    "frequency",
                    4001,
                ],
            ],
        ],
        [
            10.0,
            [
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1006,
                    0,
                    1000,
                    "frequency",
                    1002,
                ],
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1007,
                    0,
                    1003,
                    "frequency",
                    3002,
                ],
                ["/n_set", 1001, "gate", 0],
                ["/n_set", 1002, "gate", 0],
                ["/n_set", 1004, "gate", 0],
                ["/n_set", 1005, "gate", 0],
            ],
        ],
        [
            12.0,
            [
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1008,
                    0,
                    1000,
                    "frequency",
                    2002,
                ],
                [
                    "/s_new",
                    "da0982184cc8fa54cf9d288a0fe1f6ca",
                    1009,
                    0,
                    1003,
                    "frequency",
                    4002,
                ],
            ],
        ],
        [20.0, [["/n_set", 1006, "gate", 0], ["/n_set", 1007, "gate", 0]]],
        [22.0, [["/n_set", 1008, "gate", 0], ["/n_set", 1009, "gate", 0]]],
        [22.25, [["/n_free", 1000, 1003], [0]]],
    ]
    assert final_offset == 22.25
