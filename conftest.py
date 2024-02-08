import asyncio

import pytest
import pytest_asyncio

import supriya
from supriya import scsynth
from supriya.contexts.realtime import BaseServer


@pytest.fixture(autouse=True)
def add_libraries(doctest_namespace):
    doctest_namespace["supriya"] = supriya


@pytest.fixture(autouse=True, scope="session")
def shutdown_scsynth():
    scsynth.kill()
    yield
    scsynth.kill()


@pytest_asyncio.fixture(autouse=True)
async def shutdown_realtime_contexts(shutdown_scsynth):
    for context in tuple(BaseServer._contexts):
        result = context._shutdown()
        if asyncio.iscoroutine(result):
            await result
    yield
    for context in tuple(BaseServer._contexts):
        result = context._shutdown()
        if asyncio.iscoroutine(result):
            await result
