import os
import platform

import pytest
from pytest import MonkeyPatch

import supriya
from supriya.ugens import system

pytest_plugins = ["sphinx.testing.fixtures"]


@pytest.fixture
def server():
    server = supriya.Server()
    server.set_latency(0.0)
    server.boot()
    server.add_synthdefs(supriya.default)
    server.sync()
    yield server
    server.quit()


@pytest.fixture(scope="module")
def persistent_server():
    server = supriya.Server()
    server.set_latency(0.0)
    server.boot()
    yield server
    server.quit()


@pytest.fixture(autouse=True)
def system_synthdefs_lru_cache() -> None:
    for name in dir(system):
        object_ = getattr(system, name)
        if hasattr(object_, "cache_clear"):
            object_.cache_clear()


@pytest.fixture(autouse=True)
def system_synthdefs_lag_time(monkeypatch: MonkeyPatch) -> None:
    if platform.system() == "Windows" and os.environ.get("CI"):
        monkeypatch.setattr(system, "LAG_TIME", 0.25)
