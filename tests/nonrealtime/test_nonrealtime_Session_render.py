import asyncio
import logging
import platform
import pprint
from pathlib import Path

import pytest

import supriya
import supriya.nonrealtime
import supriya.scsynth
import supriya.soundfiles


def test_00a(nonrealtime_paths):
    """
    No input, no output file path specified, no render path specified.
    """
    session = pytest.helpers.make_test_session()
    exit_code, output_file_path = session.render()
    pytest.helpers.assert_soundfile_ok(output_file_path, exit_code, 10.0, 44100, 8)
    assert Path(supriya.output_path) in output_file_path.parents
    assert pytest.helpers.sample_soundfile(output_file_path) == {
        0.0: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        0.21: [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        0.41: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
        0.61: [0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75],
        0.81: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        0.99: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
    }


def test_00b(nonrealtime_paths):
    """
    No input, no output file path specified, render path specified.
    """
    session = pytest.helpers.make_test_session()
    exit_code, output_file_path = session.render(
        render_directory_path=nonrealtime_paths.render_directory_path
    )
    pytest.helpers.assert_soundfile_ok(output_file_path, exit_code, 10.0, 44100, 8)
    assert Path(nonrealtime_paths.render_directory_path) in output_file_path.parents
    assert pytest.helpers.sample_soundfile(output_file_path) == {
        0.0: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        0.21: [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        0.41: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
        0.61: [0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75],
        0.81: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        0.99: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
    }


def test_00c(caplog, nonrealtime_paths):
    """
    No input, no output file path specified, no render path specified,
    output already exists.
    """
    session = pytest.helpers.make_test_session()
    osc_path = Path().joinpath(
        supriya.output_path, "session-7b3f85710f19667f73f745b8ac8080a0.osc"
    )
    aiff_path = Path().joinpath(
        supriya.output_path, "session-7b3f85710f19667f73f745b8ac8080a0.aiff"
    )
    if osc_path.exists():
        osc_path.unlink()
    if aiff_path.exists():
        aiff_path.unlink()

    with caplog.at_level(logging.INFO, logger="supriya.nonrealtime"):
        exit_code, output_file_path = session.render()
    pytest.helpers.assert_soundfile_ok(output_file_path, exit_code, 10.0, 44100, 8)
    assert pytest.helpers.sample_soundfile(output_file_path) == {
        0.0: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        0.21: [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        0.41: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
        0.61: [0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75],
        0.81: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        0.99: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
    }
    assert output_file_path == aiff_path
    assert osc_path.exists()
    assert aiff_path.exists()

    caplog.clear()
    with caplog.at_level(logging.INFO, logger="supriya.nonrealtime"):
        exit_code, output_file_path = session.render()
    pytest.helpers.assert_soundfile_ok(output_file_path, exit_code, 10.0, 44100, 8)
    assert pytest.helpers.sample_soundfile(output_file_path) == {
        0.0: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        0.21: [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        0.41: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
        0.61: [0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75],
        0.81: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        0.99: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
    }
    assert output_file_path == aiff_path
    assert osc_path.exists()
    assert aiff_path.exists()

    osc_path.unlink()

    caplog.clear()
    with caplog.at_level(logging.INFO, logger="supriya.nonrealtime"):
        exit_code, output_file_path = session.render()
    pytest.helpers.assert_soundfile_ok(output_file_path, exit_code, 10.0, 44100, 8)
    assert pytest.helpers.sample_soundfile(output_file_path) == {
        0.0: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        0.21: [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        0.41: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
        0.61: [0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75],
        0.81: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        0.99: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
    }
    assert output_file_path == aiff_path
    assert not osc_path.exists()  # OSC file not recreated if output exists
    assert aiff_path.exists()

    aiff_path.unlink()

    caplog.clear()
    with caplog.at_level(logging.INFO, logger="supriya.nonrealtime"):
        exit_code, output_file_path = session.render()
    pytest.helpers.assert_soundfile_ok(output_file_path, exit_code, 10.0, 44100, 8)
    assert pytest.helpers.sample_soundfile(output_file_path) == {
        0.0: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        0.21: [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        0.41: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
        0.61: [0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75],
        0.81: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        0.99: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
    }
    assert output_file_path == aiff_path
    assert osc_path.exists()
    assert aiff_path.exists()


def test_01(nonrealtime_paths):
    """
    No input.
    """
    session = pytest.helpers.make_test_session()
    synthdef = pytest.helpers.build_dc_synthdef(8)
    assert synthdef.anonymous_name == "b47278d408f17357f6b260ec30ea213d"
    assert session.to_lists() == [
        [
            0.0,
            [
                ["/d_recv", synthdef.compile()],
                ["/s_new", "b47278d408f17357f6b260ec30ea213d", 1000, 0, 0, "source", 0],
            ],
        ],
        [2.0, [["/n_set", 1000, "source", 0.25]]],
        [4.0, [["/n_set", 1000, "source", 0.5]]],
        [6.0, [["/n_set", 1000, "source", 0.75]]],
        [8.0, [["/n_set", 1000, "source", 1.0]]],
        [10.0, [["/n_free", 1000], [0]]],
    ]
    exit_code, _ = session.render(
        nonrealtime_paths.output_file_path,
        render_directory_path=nonrealtime_paths.render_directory_path,
    )
    pytest.helpers.assert_soundfile_ok(
        nonrealtime_paths.output_file_path, exit_code, 10.0, 44100, 8
    )
    assert pytest.helpers.sample_soundfile(nonrealtime_paths.output_file_path) == {
        0.0: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        0.21: [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        0.41: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
        0.61: [0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75],
        0.81: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        0.99: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
    }


def test_02(nonrealtime_paths):
    """
    Soundfile NRT input, matched channels.
    """
    path_one = nonrealtime_paths.output_directory_path / "output-one.aiff"
    path_two = nonrealtime_paths.output_directory_path / "output-two.aiff"
    session_one = pytest.helpers.make_test_session()
    exit_code, _ = session_one.render(
        path_one, render_directory_path=nonrealtime_paths.render_directory_path
    )
    pytest.helpers.assert_soundfile_ok(path_one, exit_code, 10.0, 44100, 8)
    session_two = supriya.nonrealtime.Session(input_=path_one)
    synthdef = pytest.helpers.build_multiplier_synthdef(8)
    with session_two.at(0):
        session_two.add_synth(
            synthdef=synthdef,
            duration=10,
            in_bus=session_two.audio_input_bus_group,
            out_bus=session_two.audio_output_bus_group,
            multiplier=-0.5,
        )
    exit_code, _ = session_two.render(
        path_two, render_directory_path=nonrealtime_paths.render_directory_path
    )
    pytest.helpers.assert_soundfile_ok(path_two, exit_code, 10.0, 44100, 8)
    assert pytest.helpers.sample_soundfile(path_two) == {
        0.0: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        0.21: [-0.125, -0.125, -0.125, -0.125, -0.125, -0.125, -0.125, -0.125],
        0.41: [-0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25],
        0.61: [-0.375, -0.375, -0.375, -0.375, -0.375, -0.375, -0.375, -0.375],
        0.81: [-0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5],
        0.99: [-0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5],
    }


def test_03(nonrealtime_paths):
    """
    Soundfile NRT input, mismatched channels.
    """
    path_one = nonrealtime_paths.output_directory_path / "output-one.aiff"
    path_two = nonrealtime_paths.output_directory_path / "output-two.aiff"
    session_one = pytest.helpers.make_test_session()
    exit_code, _ = session_one.render(
        path_one, render_directory_path=nonrealtime_paths.render_directory_path
    )
    pytest.helpers.assert_soundfile_ok(path_one, exit_code, 10.0, 44100, 8)
    session_two = supriya.nonrealtime.Session(
        input_=path_one, input_bus_channel_count=2, output_bus_channel_count=4
    )
    synthdef = pytest.helpers.build_multiplier_synthdef(4)
    with session_two.at(0):
        session_two.add_synth(
            synthdef=synthdef,
            duration=10,
            in_bus=session_two.audio_input_bus_group,
            out_bus=session_two.audio_output_bus_group,
            multiplier=-0.5,
        )
    assert session_two.to_lists() == [
        [
            0.0,
            [
                ["/d_recv", bytearray(synthdef.compile())],
                [
                    "/s_new",
                    "1d83a887914f0ac8ac3de461f4cc637c",
                    1000,
                    0,
                    0,
                    "in_bus",
                    4,
                    "multiplier",
                    -0.5,
                    "out_bus",
                    0,
                ],
            ],
        ],
        [10.0, [["/n_free", 1000], [0]]],
    ]
    exit_code, _ = session_two.render(
        path_two, render_directory_path=nonrealtime_paths.render_directory_path
    )
    pytest.helpers.assert_soundfile_ok(path_two, exit_code, 10.0, 44100, 4)
    assert pytest.helpers.sample_soundfile(path_two) == {
        0.0: [0.0, 0.0, 0.0, 0.0],
        0.21: [-0.125, -0.125, -0.125, -0.125],
        0.41: [-0.25, -0.25, -0.25, -0.25],
        0.61: [-0.375, -0.375, -0.375, -0.375],
        0.81: [-0.5, -0.5, -0.5, -0.5],
        0.99: [-0.5, -0.5, -0.5, -0.5],
    }


def test_04(nonrealtime_paths):
    """
    Session NRT input, matched channels.
    """
    session_one = pytest.helpers.make_test_session()
    session_two = supriya.nonrealtime.Session(input_=session_one)
    synthdef = pytest.helpers.build_multiplier_synthdef(8)
    with session_two.at(0):
        session_two.add_synth(
            synthdef=synthdef,
            duration=10,
            in_bus=session_two.audio_input_bus_group,
            out_bus=session_two.audio_output_bus_group,
            multiplier=-0.5,
        )
    assert session_two.to_lists() == [
        [
            0.0,
            [
                ["/d_recv", bytearray(synthdef.compile())],
                [
                    "/s_new",
                    "76abe8508565e1ca3dd243fe960a6945",
                    1000,
                    0,
                    0,
                    "in_bus",
                    8,
                    "multiplier",
                    -0.5,
                    "out_bus",
                    0,
                ],
            ],
        ],
        [10.0, [["/n_free", 1000], [0]]],
    ]
    exit_code, _ = session_two.render(
        nonrealtime_paths.output_file_path,
        render_directory_path=nonrealtime_paths.render_directory_path,
    )
    pytest.helpers.assert_soundfile_ok(
        nonrealtime_paths.output_file_path, exit_code, 10.0, 44100, 8
    )
    assert pytest.helpers.sample_soundfile(nonrealtime_paths.output_file_path) == {
        0.0: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        0.21: [-0.125, -0.125, -0.125, -0.125, -0.125, -0.125, -0.125, -0.125],
        0.41: [-0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25],
        0.61: [-0.375, -0.375, -0.375, -0.375, -0.375, -0.375, -0.375, -0.375],
        0.81: [-0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5],
        0.99: [-0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5],
    }


def test_05(nonrealtime_paths):
    """
    Soundfile DiskIn input.
    """
    path_one = nonrealtime_paths.output_directory_path / "output-one.aiff"
    path_two = nonrealtime_paths.output_directory_path / "output-two.aiff"
    session_one = pytest.helpers.make_test_session()
    exit_code, _ = session_one.render(
        path_one, render_directory_path=nonrealtime_paths.render_directory_path
    )
    pytest.helpers.assert_soundfile_ok(path_one, exit_code, 10.0, 44100, 8)
    session_two = supriya.nonrealtime.Session()
    synthdef = pytest.helpers.build_diskin_synthdef(channel_count=8)
    with session_two.at(0):
        buffer_ = session_two.cue_soundfile(path_one, duration=10)
        session_two.add_synth(synthdef=synthdef, buffer_id=buffer_, duration=10)
    print(path_one)
    pprint.pprint(session_one.to_lists())
    print(path_two)
    pprint.pprint(session_two.to_lists())
    assert session_two.to_lists() == [
        [
            0.0,
            [
                ["/d_recv", bytearray(synthdef.compile())],
                ["/b_alloc", 0, 32768, 8],
                ["/b_read", 0, str(path_one), 0, -1, 0, 1],
                [
                    "/s_new",
                    "42367b5102dfa250b301ec698b3bd6c4",
                    1000,
                    0,
                    0,
                    "buffer_id",
                    0,
                ],
            ],
        ],
        [10.0, [["/n_free", 1000], ["/b_close", 0], ["/b_free", 0], [0]]],
    ]
    exit_code, _ = session_two.render(
        path_two, render_directory_path=nonrealtime_paths.render_directory_path
    )
    pytest.helpers.assert_soundfile_ok(path_two, exit_code, 10.0, 44100, 8)
    assert pytest.helpers.sample_soundfile(path_two) == {
        0.0: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        0.21: [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        0.41: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
        0.61: [0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75],
        0.81: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        0.99: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
    }


def test_06(nonrealtime_paths):
    """
    Session DiskIn input.
    """
    session_one = pytest.helpers.make_test_session()
    session_two = supriya.nonrealtime.Session()
    synthdef = pytest.helpers.build_diskin_synthdef(channel_count=8)
    with session_two.at(0):
        buffer_ = session_two.cue_soundfile(session_one, duration=10)
        session_two.add_synth(synthdef=synthdef, buffer_id=buffer_, duration=10)
    assert session_two.to_lists() == [
        [
            0.0,
            [
                ["/d_recv", bytearray(synthdef.compile())],
                ["/b_alloc", 0, 32768, 8],
                [
                    "/b_read",
                    0,
                    "session-7b3f85710f19667f73f745b8ac8080a0.aiff",
                    0,
                    -1,
                    0,
                    1,
                ],
                [
                    "/s_new",
                    "42367b5102dfa250b301ec698b3bd6c4",
                    1000,
                    0,
                    0,
                    "buffer_id",
                    0,
                ],
            ],
        ],
        [10.0, [["/n_free", 1000], ["/b_close", 0], ["/b_free", 0], [0]]],
    ]
    exit_code, _ = session_two.render(
        nonrealtime_paths.output_file_path,
        render_directory_path=nonrealtime_paths.render_directory_path,
    )
    pytest.helpers.assert_soundfile_ok(
        nonrealtime_paths.output_file_path, exit_code, 10.0, 44100, 8
    )
    assert pytest.helpers.sample_soundfile(nonrealtime_paths.output_file_path) == {
        0.0: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        0.21: [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        0.41: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
        0.61: [0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75],
        0.81: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        0.99: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
    }


def test_07(nonrealtime_paths):
    """
    Chained Session DiskIn input.
    """
    session_one = pytest.helpers.make_test_session()
    session_two = supriya.nonrealtime.Session()
    session_three = supriya.nonrealtime.Session()
    diskin_synthdef = pytest.helpers.build_diskin_synthdef(channel_count=8)
    multiplier_synthdef = pytest.helpers.build_multiplier_synthdef(channel_count=8)
    with session_two.at(0):
        buffer_ = session_two.cue_soundfile(session_one, duration=10)
        synth = session_two.add_synth(
            synthdef=diskin_synthdef, buffer_id=buffer_, duration=10
        )
        synth.add_synth(
            add_action="ADD_AFTER",
            duration=10,
            synthdef=multiplier_synthdef,
            multiplier=-1.0,
        )
    with session_three.at(0):
        buffer_ = session_three.cue_soundfile(session_two, duration=10)
        synth = session_three.add_synth(
            synthdef=diskin_synthdef, buffer_id=buffer_, duration=10
        )
        synth.add_synth(
            add_action="ADD_AFTER",
            duration=10,
            synthdef=multiplier_synthdef,
            multiplier=-0.5,
        )
    d_recv_commands = pytest.helpers.build_d_recv_commands(
        [diskin_synthdef, multiplier_synthdef]
    )
    buffer_one_name = "session-7b3f85710f19667f73f745b8ac8080a0.aiff"
    assert session_two.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                ["/b_alloc", 0, 32768, 8],
                ["/b_read", 0, buffer_one_name, 0, -1, 0, 1],
                [
                    "/s_new",
                    "42367b5102dfa250b301ec698b3bd6c4",
                    1000,
                    0,
                    0,
                    "buffer_id",
                    0,
                ],
                [
                    "/s_new",
                    "76abe8508565e1ca3dd243fe960a6945",
                    1001,
                    3,
                    1000,
                    "multiplier",
                    -1.0,
                ],
            ],
        ],
        [10.0, [["/n_free", 1000, 1001], ["/b_close", 0], ["/b_free", 0], [0]]],
    ]

    buffer_two_name = "session-a9bccd241b0e5b56d123924992fbdc05.aiff"
    assert session_three.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                ["/b_alloc", 0, 32768, 8],
                ["/b_read", 0, buffer_two_name, 0, -1, 0, 1],
                [
                    "/s_new",
                    "42367b5102dfa250b301ec698b3bd6c4",
                    1000,
                    0,
                    0,
                    "buffer_id",
                    0,
                ],
                [
                    "/s_new",
                    "76abe8508565e1ca3dd243fe960a6945",
                    1001,
                    3,
                    1000,
                    "multiplier",
                    -0.5,
                ],
            ],
        ],
        [10.0, [["/n_free", 1000, 1001], ["/b_close", 0], ["/b_free", 0], [0]]],
    ]

    buffer_one_path = nonrealtime_paths.render_directory_path / buffer_one_name
    buffer_two_path = nonrealtime_paths.render_directory_path / buffer_two_name

    assert not buffer_one_path.exists()
    assert not buffer_two_path.exists()
    exit_code, _ = session_three.render(
        nonrealtime_paths.output_file_path,
        render_directory_path=nonrealtime_paths.render_directory_path,
    )
    pytest.helpers.assert_soundfile_ok(buffer_one_path, exit_code, 10.0, 44100, 8)
    assert pytest.helpers.sample_soundfile(buffer_one_path) == {
        0.0: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        0.21: [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        0.41: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
        0.61: [0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75],
        0.81: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        0.99: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
    }
    pytest.helpers.assert_soundfile_ok(buffer_two_path, exit_code, 10.0, 44100, 8)
    assert pytest.helpers.sample_soundfile(buffer_two_path) == {
        0.0: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        0.21: [-0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25],
        0.41: [-0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5],
        0.61: [-0.75, -0.75, -0.75, -0.75, -0.75, -0.75, -0.75, -0.75],
        0.81: [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
        0.99: [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
    }
    pytest.helpers.assert_soundfile_ok(
        nonrealtime_paths.output_file_path, exit_code, 10.0, 44100, 8
    )
    assert pytest.helpers.sample_soundfile(nonrealtime_paths.output_file_path) == {
        0.0: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        0.21: [0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125],
        0.41: [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        0.61: [0.375, 0.375, 0.375, 0.375, 0.375, 0.375, 0.375, 0.375],
        0.81: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
        0.99: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
    }


def test_08(caplog, nonrealtime_paths):
    """
    Fanned Session DiskIn input and NRT input.
    """
    session_one = pytest.helpers.make_test_session(multiplier=0.25)
    session_two = supriya.nonrealtime.Session()
    session_three = supriya.nonrealtime.Session()
    diskin_synthdef = pytest.helpers.build_diskin_synthdef(channel_count=8)
    with session_two.at(0):
        buffer_one = session_two.cue_soundfile(session_one, duration=10)
        buffer_two = session_two.cue_soundfile(session_one, duration=10)
        session_two.add_synth(
            synthdef=diskin_synthdef, buffer_id=buffer_one, duration=10
        )
        session_two.add_synth(
            synthdef=diskin_synthdef, buffer_id=buffer_two, duration=10
        )
    with session_three.at(0):
        buffer_one = session_three.cue_soundfile(session_one, duration=10)
        buffer_two = session_three.cue_soundfile(session_two, duration=10)
        session_three.add_synth(
            synthdef=diskin_synthdef, buffer_id=buffer_one, duration=10
        )
        session_three.add_synth(
            synthdef=diskin_synthdef, buffer_id=buffer_two, duration=10
        )
    assert session_one.to_lists() == [
        [
            0.0,
            [
                ["/d_recv", bytearray(pytest.helpers.build_dc_synthdef(8).compile())],
                ["/s_new", "b47278d408f17357f6b260ec30ea213d", 1000, 0, 0, "source", 0],
            ],
        ],
        [2.0, [["/n_set", 1000, "source", 0.0625]]],
        [4.0, [["/n_set", 1000, "source", 0.125]]],
        [6.0, [["/n_set", 1000, "source", 0.1875]]],
        [8.0, [["/n_set", 1000, "source", 0.25]]],
        [10.0, [["/n_free", 1000], [0]]],
    ]
    assert session_two.to_lists() == [
        [
            0.0,
            [
                ["/d_recv", bytearray(diskin_synthdef.compile())],
                ["/b_alloc", 0, 32768, 8],
                ["/b_alloc", 1, 32768, 8],
                [
                    "/b_read",
                    0,
                    "session-c6d86f3d482a8bac1f7cc6650017da8e.aiff",
                    0,
                    -1,
                    0,
                    1,
                ],
                [
                    "/b_read",
                    1,
                    "session-c6d86f3d482a8bac1f7cc6650017da8e.aiff",
                    0,
                    -1,
                    0,
                    1,
                ],
                [
                    "/s_new",
                    "42367b5102dfa250b301ec698b3bd6c4",
                    1000,
                    0,
                    0,
                    "buffer_id",
                    0,
                ],
                [
                    "/s_new",
                    "42367b5102dfa250b301ec698b3bd6c4",
                    1001,
                    0,
                    0,
                    "buffer_id",
                    1,
                ],
            ],
        ],
        [
            10.0,
            [
                ["/n_free", 1000, 1001],
                ["/b_close", 0],
                ["/b_free", 0],
                ["/b_close", 1],
                ["/b_free", 1],
                [0],
            ],
        ],
    ]
    assert session_three.to_lists() == [
        [
            0.0,
            [
                ["/d_recv", bytearray(diskin_synthdef.compile())],
                ["/b_alloc", 0, 32768, 8],
                ["/b_alloc", 1, 32768, 8],
                [
                    "/b_read",
                    0,
                    "session-c6d86f3d482a8bac1f7cc6650017da8e.aiff",
                    0,
                    -1,
                    0,
                    1,
                ],
                [
                    "/b_read",
                    1,
                    "session-81d02f16aff7797ca3ac041facb61b95.aiff",
                    0,
                    -1,
                    0,
                    1,
                ],
                [
                    "/s_new",
                    "42367b5102dfa250b301ec698b3bd6c4",
                    1000,
                    0,
                    0,
                    "buffer_id",
                    0,
                ],
                [
                    "/s_new",
                    "42367b5102dfa250b301ec698b3bd6c4",
                    1001,
                    0,
                    0,
                    "buffer_id",
                    1,
                ],
            ],
        ],
        [
            10.0,
            [
                ["/n_free", 1000, 1001],
                ["/b_close", 0],
                ["/b_free", 0],
                ["/b_close", 1],
                ["/b_free", 1],
                [0],
            ],
        ],
    ]
    session_one_path = nonrealtime_paths.render_directory_path.joinpath(
        "session-c6d86f3d482a8bac1f7cc6650017da8e.aiff"
    )
    session_two_path = nonrealtime_paths.render_directory_path.joinpath(
        "session-81d02f16aff7797ca3ac041facb61b95.aiff"
    )
    with caplog.at_level(logging.INFO, logger="supriya.nonrealtime"):
        exit_code, _ = session_three.render(
            nonrealtime_paths.output_file_path,
            render_directory_path=nonrealtime_paths.render_directory_path,
        )
    pytest.helpers.assert_soundfile_ok(session_one_path, exit_code, 10.0, 44100, 8)
    assert pytest.helpers.sample_soundfile(session_one_path) == {
        0.0: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        0.21: [0.0625, 0.0625, 0.0625, 0.0625, 0.0625, 0.0625, 0.0625, 0.0625],
        0.41: [0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125],
        0.61: [0.1875, 0.1875, 0.1875, 0.1875, 0.1875, 0.1875, 0.1875, 0.1875],
        0.81: [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        0.99: [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
    }
    pytest.helpers.assert_soundfile_ok(session_two_path, exit_code, 10.0, 44100, 8)
    assert pytest.helpers.sample_soundfile(session_two_path) == {
        0.0: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        0.21: [0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125],
        0.41: [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        0.61: [0.375, 0.375, 0.375, 0.375, 0.375, 0.375, 0.375, 0.375],
        0.81: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
        0.99: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
    }
    pytest.helpers.assert_soundfile_ok(
        nonrealtime_paths.output_file_path, exit_code, 10.0, 44100, 8
    )
    assert pytest.helpers.sample_soundfile(nonrealtime_paths.output_file_path) == {
        0.0: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        0.21: [0.1875, 0.1875, 0.1875, 0.1875, 0.1875, 0.1875, 0.1875, 0.1875],
        0.41: [0.375, 0.375, 0.375, 0.375, 0.375, 0.375, 0.375, 0.375],
        0.61: [0.5625, 0.5625, 0.5625, 0.5625, 0.5625, 0.5625, 0.5625, 0.5625],
        0.81: [0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75],
        0.99: [0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75],
    }


@pytest.mark.skipif(platform.system() == "Windows", reason="requires say/espeak")
def test_09(nonrealtime_paths):
    """
    Non-session renderable NRT input.
    """
    say = supriya.soundfiles.Say("Some text.")
    session = supriya.nonrealtime.Session(1, 1, input_=say)
    synthdef = pytest.helpers.build_multiplier_synthdef(1)
    with session.at(0):
        session.add_synth(
            synthdef=synthdef,
            duration=2,
            in_bus=session.audio_input_bus_group,
            out_bus=session.audio_output_bus_group,
            multiplier=0.5,
        )
    assert session.to_lists() == [
        [
            0.0,
            [
                ["/d_recv", bytearray(synthdef.compile())],
                [
                    "/s_new",
                    "85c1d1b6f6c9b59c042b53d39019b8f5",
                    1000,
                    0,
                    0,
                    "in_bus",
                    1,
                    "multiplier",
                    0.5,
                    "out_bus",
                    0,
                ],
            ],
        ],
        [2.0, [["/n_free", 1000], [0]]],
    ]
    exit_code, _ = session.render(
        nonrealtime_paths.output_file_path,
        render_directory_path=nonrealtime_paths.render_directory_path,
    )


@pytest.mark.skipif(platform.system() == "Windows", reason="requires say/espeak")
def test_10(nonrealtime_paths):
    """
    Non-session renderable DiskIn input.
    """
    say = supriya.soundfiles.Say("Some text.")
    session = supriya.nonrealtime.Session(0, 1)
    synthdef = pytest.helpers.build_diskin_synthdef(channel_count=1)
    with session.at(0):
        buffer_ = session.cue_soundfile(say, duration=2)
        session.add_synth(synthdef=synthdef, buffer_id=buffer_, duration=2)
    assert session.to_lists() == [
        [
            0.0,
            [
                ["/d_recv", bytearray(synthdef.compile())],
                ["/b_alloc", 0, 32768, 1],
                [
                    "/b_read",
                    0,
                    "say-5f2b51ca2fdc5baa31ec02e002f69aec.aiff",
                    0,
                    -1,
                    0,
                    1,
                ],
                [
                    "/s_new",
                    "9c69c44ff72c62dfa4c2f0a0e99f05ce",
                    1000,
                    0,
                    0,
                    "buffer_id",
                    0,
                ],
            ],
        ],
        [2.0, [["/n_free", 1000], ["/b_close", 0], ["/b_free", 0], [0]]],
    ]
    exit_code, _ = session.render(
        nonrealtime_paths.output_file_path,
        render_directory_path=nonrealtime_paths.render_directory_path,
    )


@pytest.mark.skipif(platform.system() == "Windows", reason="requires say/espeak")
def test_11(nonrealtime_paths):
    """
    Chained session and non-session inputs.
    """
    multiplier_synthdef = pytest.helpers.build_multiplier_synthdef(1)
    diskin_synthdef = pytest.helpers.build_diskin_synthdef(channel_count=1)
    say = supriya.soundfiles.Say("Some text.")
    session_one = supriya.nonrealtime.Session(1, 1, input_=say)
    with session_one.at(0):
        session_one.add_synth(
            synthdef=multiplier_synthdef,
            duration=2,
            in_bus=session_one.audio_input_bus_group,
            out_bus=session_one.audio_output_bus_group,
            multiplier=0.5,
        )
    session_two = supriya.nonrealtime.Session(1, 1, input_=session_one)
    with session_two.at(0):
        session_two.add_synth(
            synthdef=multiplier_synthdef,
            duration=2,
            in_bus=session_two.audio_input_bus_group,
            out_bus=session_two.audio_output_bus_group,
            multiplier=-0.5,
        )
        buffer_ = session_two.cue_soundfile(say, duration=2)
        session_two.add_synth(synthdef=diskin_synthdef, buffer_id=buffer_, duration=2)
    assert session_two.to_lists() == [
        [
            0.0,
            [
                ["/d_recv", bytearray(multiplier_synthdef.compile())],
                ["/d_recv", bytearray(diskin_synthdef.compile())],
                ["/b_alloc", 0, 32768, 1],
                [
                    "/b_read",
                    0,
                    "say-5f2b51ca2fdc5baa31ec02e002f69aec.aiff",
                    0,
                    -1,
                    0,
                    1,
                ],
                [
                    "/s_new",
                    "85c1d1b6f6c9b59c042b53d39019b8f5",
                    1000,
                    0,
                    0,
                    "in_bus",
                    1,
                    "multiplier",
                    -0.5,
                    "out_bus",
                    0,
                ],
                [
                    "/s_new",
                    "9c69c44ff72c62dfa4c2f0a0e99f05ce",
                    1001,
                    0,
                    0,
                    "buffer_id",
                    0,
                ],
            ],
        ],
        [2.0, [["/n_free", 1000, 1001], ["/b_close", 0], ["/b_free", 0], [0]]],
    ]
    exit_code, _ = session_two.render(
        nonrealtime_paths.output_file_path,
        render_directory_path=nonrealtime_paths.render_directory_path,
    )


def test_12(nonrealtime_paths):
    """
    No input, no output file path specified, render path specified, output suppressed
    """
    session = pytest.helpers.make_test_session()
    exit_code, output_file_path = session.render(
        render_directory_path=nonrealtime_paths.render_directory_path,
        suppress_output=True,
    )
    if platform.system() == "Windows":
        assert exit_code == 3221226505
        assert output_file_path == Path("NUL")
    else:
        assert exit_code == 0
        assert output_file_path == Path("/dev/null")
    assert list(nonrealtime_paths.render_directory_path.iterdir()) == [
        nonrealtime_paths.render_directory_path
        / "session-7b3f85710f19667f73f745b8ac8080a0.osc"
    ]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "durations",
    (
        [10],
        [10, 10],  # both repeat
        [10, 11],  # no repeats
        [10, 11, 12],  # no repeats
        [10, 10, 13],  # first two repeats
        [10, 13, 13],  # last two repeats
        [11, 14, 11],  # interleaved repeats
    ),
)
async def test_render_async(caplog, nonrealtime_paths, durations):
    session = pytest.helpers.make_test_session()
    with caplog.at_level(logging.DEBUG, logger="supriya.nonrealtime"):
        tasks = [
            session.render_async(
                duration=duration,
                render_directory_path=nonrealtime_paths.render_directory_path,
            )
            for duration in durations
        ]
        results = await asyncio.gather(*tasks)
    for (exit_code, output_file_path), duration in zip(results, durations):
        pytest.helpers.assert_soundfile_ok(
            output_file_path, exit_code, duration, 44100, 8
        )
