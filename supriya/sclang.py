import os
import pathlib
import platform

import uqbar.io

import supriya


def find(sclang_path=None):
    """Find the ``sclang`` executable.

    The following paths, if defined, will be searched (prioritised as ordered):
    1. The absolute path ``sclang_path``
    2. The environment variable ``SCLANG_PATH``
    3. ``sclang_path`` if defined in Supriya's configuration file
    4. The user's ``PATH``
    5. Common installation directories of the SuperCollider application.

    Returns a path to the ``sclang`` executable.
    Raises ``RuntimeError`` if no path is found.
    """
    sclang_path = pathlib.Path(
        sclang_path
        or os.environ.get("SCLANG_PATH")
        or supriya.config.get("core", "sclang_path", fallback=None)
        or "sclang"
    )
    if sclang_path.is_absolute() and uqbar.io.find_executable(sclang_path):
        return sclang_path
    sclang_path_candidates = uqbar.io.find_executable(sclang_path.name)
    if sclang_path_candidates:
        return pathlib.Path(sclang_path_candidates[0])
    if platform.system() == "Darwin":
        for path in [
            pathlib.Path("/Applications/SuperCollider.app/Contents/MacOS/sclang"),
            pathlib.Path(
                "/Applications/SuperCollider/SuperCollider.app/Contents/MacOS/sclang"
            ),
        ]:
            if path.exists():
                return path
    elif platform.system() == "Linux":
        for path in [
            pathlib.Path("/usr/bin/sclang"),
            pathlib.Path("/usr/local/bin/sclang"),
        ]:
            if path.exists():
                return path
    raise RuntimeError("Failed to locate sclang")
