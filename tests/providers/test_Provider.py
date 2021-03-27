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
