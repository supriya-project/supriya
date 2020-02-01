import pytest

import supriya
from supriya import scsynth


@pytest.fixture(autouse=True)
def add_libraries(doctest_namespace):
    doctest_namespace["supriya"] = supriya


@pytest.fixture(autouse=True)
def shutdown():
    scsynth.kill()
    for server in tuple(supriya.Server._servers):
        server._shutdown()
    yield
    for server in tuple(supriya.Server._servers):
        server._shutdown()
    scsynth.kill()
