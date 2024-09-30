from typing import Union

import pytest

from supriya.mixers.mixers import Mixer
from supriya.mixers.tracks import Track
from supriya.typing import DEFAULT


@pytest.fixture
def track(mixer: Mixer) -> Track:
    return mixer.tracks[0]


@pytest.mark.asyncio
async def test_Track_activate(track: Track) -> None:
    await track.activate()


@pytest.mark.asyncio
async def test_Track_add_track(track: Track) -> None:
    await track.add_track()


@pytest.mark.asyncio
async def test_Track_deactivate(track: Track) -> None:
    await track.deactivate()


@pytest.mark.asyncio
async def test_Track_delete(track: Track) -> None:
    await track.delete()


@pytest.mark.parametrize(
    "index, parent",
    [
        (..., ...),
    ],
)
@pytest.mark.asyncio
async def test_Track_move(
    index: int, parent: Union[Mixer, Track], track: Track
) -> None:
    await track.move(index=index, parent=parent)


@pytest.mark.parametrize("output", [None, DEFAULT])
@pytest.mark.asyncio
async def test_Track_set_output(output, track: Track) -> None:
    await track.set_output(output)


@pytest.mark.asyncio
async def test_Track_solo(track: Track) -> None:
    await track.solo()


@pytest.mark.asyncio
async def test_Track_ungroup(track: Track) -> None:
    await track.ungroup()


@pytest.mark.asyncio
async def test_Track_unsolo(track: Track) -> None:
    await track.unsolo()
