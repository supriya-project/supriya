import pytest

from supriya.assets.synthdefs import default
from supriya.nonrealtime import Session
from supriya.realtime import Server


@pytest.fixture
def server():
    server = Server()
    server.boot()
    default.allocate(server=server)
    yield server
    server.quit()


@pytest.fixture
def session():
    yield Session()
