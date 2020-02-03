import pytest

import supriya
from supriya import scsynth
from supriya.realtime.servers import AsyncServer, Server


@pytest.fixture(autouse=True)
def add_libraries(doctest_namespace):
    doctest_namespace["supriya"] = supriya


@pytest.fixture(autouse=True)
def shutdown_scsynth():
    scsynth.kill()
    yield
    scsynth.kill()


@pytest.fixture(autouse=True)
def shutdown_sync_servers(shutdown_scsynth):
    for server in tuple(Server._servers):
        server._shutdown()
    yield
    for server in tuple(Server._servers):
        server._shutdown()


@pytest.fixture(autouse=True)
async def shutdown_async_servers(shutdown_scsynth, event_loop):
    for server in tuple(AsyncServer._servers):
        server._shutdown()
    yield
    for server in tuple(AsyncServer._servers):
        server._shutdown()
        if server.osc_protocol.healthcheck_task is not None:
            await server.osc_protocol.healthcheck_task
