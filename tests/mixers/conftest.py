import pytest
import pytest_asyncio

from supriya.mixers import Session


@pytest_asyncio.fixture(autouse=True, params=["offline", "online"])
async def session(request):
    session = Session()
    if request.param == "online":
        await session.boot()
    yield session


@pytest.fixture
def mixer(session):
    return session.mixers[0]
