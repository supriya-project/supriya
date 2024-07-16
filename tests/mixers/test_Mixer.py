import pytest


@pytest.mark.asyncio
async def test_Mixer_add_device(mixer):
    await mixer.add_device()


@pytest.mark.asyncio
async def test_Mixer_add_track(mixer):
    await mixer.add_track()


@pytest.mark.asyncio
async def test_Mixer_delete(mixer):
    await mixer.delete()


@pytest.mark.asyncio
async def test_Mixer_group_devices(mixer):
    await mixer.group_devices(0, 2)


@pytest.mark.asyncio
async def test_Mixer_set_channel_count(mixer):
    await mixer.set_channel_count(8)


@pytest.mark.asyncio
async def test_Mixer_set_output(mixer):
    await mixer.set_output(4)
