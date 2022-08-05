import pytest
import pytest_asyncio

import supriya
from supriya import scsynth
from supriya.realtime.servers import AsyncServer, Server


@pytest.fixture(autouse=True)
def add_libraries(doctest_namespace):
    doctest_namespace["supriya"] = supriya


@pytest.fixture(autouse=True, scope="session")
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


@pytest_asyncio.fixture(autouse=True)
async def shutdown_async_servers(shutdown_scsynth, event_loop):
    for server in tuple(AsyncServer._servers):
        await server._shutdown()
    yield
    for server in tuple(AsyncServer._servers):
        await server._shutdown()
