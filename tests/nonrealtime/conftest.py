import os
import pathlib
import shutil
import types

import pytest

from supriya.nonrealtime import Session


@pytest.fixture
def nonrealtime_paths(tmpdir):
    test_directory_path = pathlib.Path(tmpdir)
    output_directory_path = test_directory_path / "output"
    render_directory_path = test_directory_path / "render"
    output_file_path = output_directory_path / "output.aiff"
    render_yml_file_path = output_directory_path / "render.yml"
    nonrealtime_paths = types.SimpleNamespace(
        test_directory_path=test_directory_path,
        output_directory_path=output_directory_path,
        render_directory_path=render_directory_path,
        output_file_path=output_file_path,
        render_yml_file_path=render_yml_file_path,
    )
    original_directory = pathlib.Path.cwd()
    for directory_path in [output_directory_path, render_directory_path]:
        directory_path.mkdir(parents=True, exist_ok=True)
    os.chdir(test_directory_path)
    yield nonrealtime_paths
    os.chdir(original_directory)
    for directory_path in [output_directory_path, render_directory_path]:
        if directory_path.exists():
            shutil.rmtree(directory_path)


@pytest.helpers.register
def make_test_session(
    input_=None,
    input_bus_channel_count=None,
    output_bus_channel_count=None,
    multiplier=1.0,
):
    session = Session(
        input_bus_channel_count=input_bus_channel_count,
        output_bus_channel_count=output_bus_channel_count,
        name="inner-session",
    )
    output_bus_channel_count = session.options.output_bus_channel_count
    synthdef = pytest.helpers.build_dc_synthdef(channel_count=output_bus_channel_count)
    with session.at(0):
        synth = session.add_synth(synthdef=synthdef, duration=10, source=0)
    with session.at(2):
        synth["source"] = 0.25 * multiplier
    with session.at(4):
        synth["source"] = 0.5 * multiplier
    with session.at(6):
        synth["source"] = 0.75 * multiplier
    with session.at(8):
        synth["source"] = 1.0 * multiplier
    assert synthdef.anonymous_name == "b47278d408f17357f6b260ec30ea213d"
    d_recv_commands = pytest.helpers.build_d_recv_commands([synthdef])
    assert session.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                ["/s_new", "b47278d408f17357f6b260ec30ea213d", 1000, 0, 0, "source", 0],
            ],
        ],
        [2.0, [["/n_set", 1000, "source", 0.25 * multiplier]]],
        [4.0, [["/n_set", 1000, "source", 0.5 * multiplier]]],
        [6.0, [["/n_set", 1000, "source", 0.75 * multiplier]]],
        [8.0, [["/n_set", 1000, "source", 1.0 * multiplier]]],
        [10.0, [["/n_free", 1000], [0]]],
    ]
    return session
