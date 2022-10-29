import pytest

from supriya.providers import NonrealtimeProvider, Provider, RealtimeProvider


def test_Provider_from_context(session, server):
    realtime_provider = Provider.from_context(server)
    assert isinstance(realtime_provider, RealtimeProvider)
    assert realtime_provider.server is server
    nonrealtime_provider = Provider.from_context(session)
    assert isinstance(nonrealtime_provider, NonrealtimeProvider)
    assert nonrealtime_provider.session is session
    with pytest.raises(ValueError):
        Provider.from_context(23)


def test_Provider_realtime():
    realtime_provider = Provider.realtime()
    assert isinstance(realtime_provider, RealtimeProvider)
    assert realtime_provider.server.is_running
    assert realtime_provider.server.is_owner
    realtime_provider.server.quit()
    assert not realtime_provider.server.is_running
    assert not realtime_provider.server.is_owner


def test_Provider_realtime_supernova():
    realtime_provider = Provider.realtime(supernova=True)
    assert isinstance(realtime_provider, RealtimeProvider)
    assert realtime_provider.server.is_running
    assert realtime_provider.server.is_owner
    realtime_provider.server.quit()
    assert not realtime_provider.server.is_running
    assert not realtime_provider.server.is_owner


@pytest.mark.asyncio
async def test_Provider_realtime_async():
    realtime_provider = await Provider.realtime_async()
    assert isinstance(realtime_provider, RealtimeProvider)
    assert realtime_provider.server.is_running
    assert realtime_provider.server.is_owner
    await realtime_provider.server.quit()
    assert not realtime_provider.server.is_running
    assert not realtime_provider.server.is_owner


@pytest.mark.asyncio
async def test_Provider_realtime_async_supernova():
    realtime_provider = await Provider.realtime_async(supernova=True)
    assert isinstance(realtime_provider, RealtimeProvider)
    assert realtime_provider.server.is_running
    assert realtime_provider.server.is_owner
    await realtime_provider.server.quit()
    assert not realtime_provider.server.is_running
    assert not realtime_provider.server.is_owner
