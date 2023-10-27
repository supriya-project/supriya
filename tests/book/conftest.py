import shutil
from pathlib import Path

import pytest

collect_ignore = ["roots"]


@pytest.fixture(scope="session")
def remove_sphinx_projects(sphinx_test_tempdir) -> None:
    # Even upon exception, remove any directory from temp area
    # which looks like a Sphinx project. This ONLY runs once.
    roots_path = Path(sphinx_test_tempdir)
    for d in roots_path.iterdir():
        if d.is_dir():
            if Path(d, "_build").exists():
                # This directory is a Sphinx project, remove it
                shutil.rmtree(str(d))
    yield


@pytest.fixture()
def rootdir(remove_sphinx_projects: None) -> Path:
    roots = Path(__file__).parent.absolute() / "roots"
    yield roots
