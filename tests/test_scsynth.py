import os
import pathlib
import stat
from tempfile import NamedTemporaryFile, TemporaryDirectory
import pytest
from supriya import scsynth


@pytest.fixture
def mock_env_scsynth_path(monkeypatch):
    monkeypatch.delenv("SCSYNTH_PATH", raising=False)


def test_find_argument(mock_env_scsynth_path):

    with NamedTemporaryFile() as tmp:
        expected = pathlib.Path(tmp.name).absolute()
        expected.chmod(expected.stat().st_mode | stat.S_IEXEC)
        got = scsynth.find(expected)
        assert got == expected


def test_find_env_var(mock_env_scsynth_path):

    with NamedTemporaryFile() as tmp:
        expected = pathlib.Path(tmp.name).absolute()
        expected.chmod(expected.stat().st_mode | stat.S_IEXEC)
        os.environ["SCSYNTH_PATH"] = str(expected)
        got = scsynth.find()
        assert got == expected


def test_find_on_path(mock_env_scsynth_path):

    with TemporaryDirectory() as tmp_dir:

        scsynth_path = pathlib.Path(tmp_dir) / "scsynth"

        with open(scsynth_path, "w"):
            scsynth_path.chmod(scsynth_path.stat().st_mode | stat.S_IEXEC)
            os.environ["PATH"] += os.pathsep + tmp_dir
            got = scsynth.find()
            expected = scsynth_path.absolute()
            assert got == expected


def test_find_from_fallback_paths(mock_env_scsynth_path, mocker):

    with NamedTemporaryFile() as tmp:
        expected = pathlib.Path(tmp.name).absolute()
        expected.chmod(expected.stat().st_mode | stat.S_IEXEC)
        mock = mocker.patch.object(scsynth, "_fallback_scsynth_path")
        mock.return_value = expected
        got = scsynth.find()
        assert got == expected


def test_find_from_config(mock_env_scsynth_path, mocker):

    with NamedTemporaryFile() as tmp:
        expected = pathlib.Path(tmp.name).absolute()
        mocker.patch.dict(
            scsynth.supriya.config, {"core": {"scsynth_path": str(expected)}}
        )
        expected.chmod(expected.stat().st_mode | stat.S_IEXEC)
        got = scsynth.find()
        assert got == expected
