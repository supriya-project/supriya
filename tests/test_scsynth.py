import pytest
import stat
import os
from supriya import scsynth
from supriya import config
from tempfile import NamedTemporaryFile, TemporaryDirectory
import pathlib


def setup_function():
    os.environ["SCSYNTH_PATH"] = ""

def test_find_argument():

    with NamedTemporaryFile() as tmp:
        got = scsynth.find(tmp.name)
        expected = pathlib.Path(tmp.name).resolve().absolute()
        assert got == expected


def test_find_env_var():

    with NamedTemporaryFile() as tmp:
        os.environ["SCSYNTH_PATH"] = tmp.name
        got = scsynth.find()
        expected = pathlib.Path(tmp.name).resolve().absolute()
        assert got == expected


def test_find_on_path():

    with TemporaryDirectory() as tmp_dir:

        scsynth_path = pathlib.Path(tmp_dir) / "scsynth"

        with open(scsynth_path, "w") as scf:
            scsynth_path.chmod(scsynth_path.stat().st_mode | stat.S_IEXEC)
            os.environ["PATH"] += os.pathsep + tmp_dir
            got = scsynth.find()
            expected = scsynth_path.resolve().absolute()
            assert got == expected


def test_find_from_fallback_paths(mocker):

    with NamedTemporaryFile() as tmp:
        mock = mocker.patch.object(scsynth, "_fallback_scsynth_paths")
        expected = pathlib.Path(tmp.name).resolve().absolute()
        mock.return_value = (expected,)
        got = scsynth.find()
        assert got == expected


def test_find_from_config():

    with NamedTemporaryFile() as tmp:
        config.read_dict({"core": {"scsynth_path": tmp.name}})
        got = scsynth.find()
        expected = pathlib.Path(tmp.name).resolve().absolute()
        assert got == expected
