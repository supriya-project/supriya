import os
import pathlib
import platform
from pathlib import Path

import uqbar.io

import supriya


def _fallback_sclang_path():
    paths = []
    system = platform.system()
    if system == "Linux":
        paths.extend([Path("/usr/bin/sclang"), Path("/usr/local/bin/sclang")])
    elif system == "Darwin":
        paths.append(Path("/Applications/SuperCollider.app/Contents/MacOS/sclang"))
    elif system == "Windows":
        paths.extend(Path(r"C:\Program Files").glob(r"SuperCollider*\sclang.exe"))
    for path in paths:
        if path.exists():
            return path
    return None


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
    fallback_path = _fallback_sclang_path()
    if fallback_path is not None:
        return fallback_path
    raise RuntimeError("Failed to locate sclang")
