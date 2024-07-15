import pytest


@pytest.mark.asyncio
async def test_Session_boot(session):
    await session.boot()


@pytest.mark.asyncio
async def test_Session_quit(session):
    await session.quit()


@pytest.mark.asyncio
async def test_Session_add_context(session):
    await session.add_context()


@pytest.mark.asyncio
async def test_Session_add_mixer(session):
    await session.add_mixer()


@pytest.mark.asyncio
async def test_Session_delete_context(session):
    context = await session.add_context()
    await session.delete_context(context)


@pytest.mark.asyncio
async def test_Session_set_mixer_context(session):
    mixer = await session.add_mixer()
    context = await session.add_context()
    await session.set_mixer_context(mixer=mixer, context=context)
