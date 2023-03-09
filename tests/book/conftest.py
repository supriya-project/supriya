import os
import pathlib
import shutil

import pytest
from sphinx.testing.path import path

collect_ignore = ["roots"]


@pytest.fixture(scope="session")
def remove_sphinx_projects(sphinx_test_tempdir):
    # Even upon exception, remove any directory from temp area
    # which looks like a Sphinx project. This ONLY runs once.
    roots_path = pathlib.Path(sphinx_test_tempdir)
    for d in roots_path.iterdir():
        if d.is_dir():
            if pathlib.Path(d, "_build").exists():
                # This directory is a Sphinx project, remove it
                shutil.rmtree(str(d))
    yield


@pytest.fixture()
def rootdir(remove_sphinx_projects):
    roots = path(os.path.dirname(__file__) or ".").abspath() / "roots"
    yield roots
