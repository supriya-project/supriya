import os
import pathlib
import stat
from tempfile import NamedTemporaryFile, TemporaryDirectory
from typing import Dict, List

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
        (
            {},
            [
                "/path/to/scsynth",
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
                "/path/to/scsynth",
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
                "/path/to/scsynth",
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
                "/path/to/scsynth",
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
                "/path/to/scsynth",
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
    ],
)
def test_Options(kwargs: Dict, expected: List[str]) -> None:
    options = scsynth.Options(**kwargs)
    actual = list(options)
    actual[0] = "/path/to/scsynth"  # replace to make it portable
    assert actual == expected
