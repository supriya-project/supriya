import pytest

import supriya


@pytest.fixture(autouse=True)
def add_libraries(doctest_namespace):
    doctest_namespace["supriya"] = supriya


@pytest.fixture(autouse=True)
def shutdown():
    supriya.Server.kill()
    for server in tuple(supriya.Server._servers):
        server._shutdown()
    yield
    for server in tuple(supriya.Server._servers):
        server._shutdown()
    supriya.Server.kill()
