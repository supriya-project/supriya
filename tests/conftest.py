import pytest

import supriya

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
