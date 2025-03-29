import os
import pathlib
import stat
from tempfile import NamedTemporaryFile, TemporaryDirectory

import pytest

from supriya import scsynth


@pytest.fixture
def mock_env_scsynth_path(monkeypatch):
    monkeypatch.delenv(scsynth.ENVAR_SERVER_EXECUTABLE, raising=False)
    monkeypatch.setenv("PATH", "")


def test_find_argument(mock_env_scsynth_path):
    with NamedTemporaryFile() as tmp:
        expected = pathlib.Path(tmp.name).absolute()
        expected.chmod(expected.stat().st_mode | stat.S_IEXEC)
        got = scsynth.find(expected)
        assert got == expected


def test_find_env_var(mock_env_scsynth_path, monkeypatch):
    with NamedTemporaryFile() as tmp:
        expected = pathlib.Path(tmp.name).absolute()
        expected.chmod(expected.stat().st_mode | stat.S_IEXEC)
        monkeypatch.setenv(scsynth.ENVAR_SERVER_EXECUTABLE, str(expected))
        got = scsynth.find()
        assert got == expected


def test_find_on_path(mock_env_scsynth_path, monkeypatch):
    with TemporaryDirectory() as tmp_dir:
        scsynth_path = pathlib.Path(tmp_dir) / "scsynth"
        with open(scsynth_path, "w"):
            scsynth_path.chmod(scsynth_path.stat().st_mode | stat.S_IEXEC)
            monkeypatch.setenv("PATH", os.pathsep + tmp_dir)
            got = scsynth.find()
            expected = scsynth_path.resolve().absolute()
            assert got == expected


@pytest.mark.parametrize(
    "kwargs, expected",
    [
        # nothing specified
        (
            {},
            [
                "/path/to/executable",
                "-R",
                "0",
                "-l",
                "1",
                "-u",
                "57110",
            ],
        ),
        # only input device defined
        (
            {"input_device": "Device X"},
            [
                "/path/to/executable",
                "-H",
                "Device X",
                "",
                "-R",
                "0",
                "-l",
                "1",
                "-u",
                "57110",
            ],
        ),
        # only output device defined
        (
            {"output_device": "Device Y"},
            [
                "/path/to/executable",
                "-H",
                "",
                "Device Y",
                "-R",
                "0",
                "-l",
                "1",
                "-u",
                "57110",
            ],
        ),
        # input and output devices defined, but different
        (
            {"input_device": "Device P", "output_device": "Device Q"},
            [
                "/path/to/executable",
                "-H",
                "Device P",
                "Device Q",
                "-R",
                "0",
                "-l",
                "1",
                "-u",
                "57110",
            ],
        ),
        # input and output devices defined, and identical
        (
            {"input_device": "Device Z", "output_device": "Device Z"},
            [
                "/path/to/executable",
                "-H",
                "Device Z",
                "-R",
                "0",
                "-l",
                "1",
                "-u",
                "57110",
            ],
        ),
        # many flags specified
        (
            {
                "audio_bus_channel_count": 1024 * 2,
                "block_size": 64 * 2,
                "buffer_count": 1024 * 2,
                "control_bus_channel_count": 16384 * 2,
                "executable": "supernova",
                "hardware_buffer_size": 512,
                "initial_node_id": 100,
                "input_bus_channel_count": 16,
                "input_device": "Hypothetical Input Device",
                "input_stream_mask": "01101010",
                "ip_address": "0.0.0.0",
                "load_synthdefs": False,
                "maximum_logins": 23,
                "maximum_node_count": 1024 * 2,
                "maximum_synthdef_count": 1024 * 2,
                "memory_locking": True,
                "memory_size": 8192 * 2,
                "output_bus_channel_count": 8 * 2,
                "output_device": "Hypothetical Output Device",
                "output_stream_mask": "10010101",
                "password": "changeme",
                "protocol": "tcp",
                "random_number_generator_count": 64 * 2,
                "restricted_path": "/restricted/path",
                "safety_clip": "inf",
                "sample_rate": 44100,
                "threads": 8,
                "ugen_plugins_path": "/path/to/ugens",
                "verbosity": 1,
                "wire_buffer_count": 64 * 22,
                "zero_configuration": True,
            },
            [
                "/path/to/executable",
                "-B",
                "0.0.0.0",
                "-D",
                "0",
                "-H",
                "Hypothetical Input Device",
                "Hypothetical Output Device",
                "-I",
                "01101010",
                "-L",
                "-O",
                "10010101",
                "-P",
                "/restricted/path",
                "-S",
                "44100",
                "-T",
                "8",
                "-U",
                "/path/to/ugens",
                "-Z",
                "512",
                "-a",
                "2048",
                "-b",
                "2048",
                "-c",
                "32768",
                "-d",
                "2048",
                "-i",
                "16",
                "-l",
                "23",
                "-m",
                "16384",
                "-n",
                "2048",
                "-o",
                "16",
                "-p",
                "changeme",
                "-r",
                "128",
                "-s",
                "inf",
                "-t",
                "57110",
                "-v",
                "1",
                "-w",
                "1408",
                "-z",
                "128",
            ],
        ),
    ],
)
def test_Options(kwargs: dict, expected: list[str]) -> None:
    options = scsynth.Options(**kwargs)
    actual = list(options)
    actual[0] = "/path/to/executable"  # replace to make it portable
    assert actual == expected
