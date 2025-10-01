import pytest

from supriya.sessions import Session


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.asyncio
async def test_Rack_set_name(online: bool) -> None:
    session = Session()
    mixer = await session.add_mixer()
    rack = await mixer.add_rack()
    if online:
        await session.boot()
    assert rack.name is None
    for name in ("Foo", "Bar", "Baz"):
        rack.set_name(name=name)
        assert rack.name == name
    rack.set_name(name=None)
    assert rack.name is None
