import sys

import pytest

from supriya.providers import NonrealtimeProvider, Provider, RealtimeProvider
from supriya.scsynth import Options

supernova_skip_win = pytest.param(
    "supernova",
    marks=pytest.mark.skipif(
        sys.platform.startswith("win"), reason="Supernova won't boot on Windows"
    ),
)


def test_Provider_from_context(session, server):
    realtime_provider = Provider.from_context(server)
    assert isinstance(realtime_provider, RealtimeProvider)
    assert realtime_provider.server is server
    nonrealtime_provider = Provider.from_context(session)
    assert isinstance(nonrealtime_provider, NonrealtimeProvider)
    assert nonrealtime_provider.session is session
    with pytest.raises(ValueError):
        Provider.from_context(23)


@pytest.mark.parametrize("executable", [None, supernova_skip_win])
def test_Provider_realtime(executable):
    options = Options(executable=executable)
    realtime_provider = Provider.realtime(options=options)
    assert isinstance(realtime_provider, RealtimeProvider)
    assert realtime_provider.server.is_running
    assert realtime_provider.server.is_owner
    realtime_provider.server.quit()
    assert not realtime_provider.server.is_running
    assert not realtime_provider.server.is_owner


@pytest.mark.asyncio
@pytest.mark.parametrize("executable", [None, supernova_skip_win])
async def test_Provider_realtime_async(executable):
    options = Options(executable=executable)
    realtime_provider = await Provider.realtime_async(options=options)
    assert isinstance(realtime_provider, RealtimeProvider)
    assert realtime_provider.server.is_running
    assert realtime_provider.server.is_owner
    await realtime_provider.server.quit()
    assert not realtime_provider.server.is_running
    assert not realtime_provider.server.is_owner
