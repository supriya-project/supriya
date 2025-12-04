import pytest

from supriya.sessions import Session
from supriya.sessions.specs import Spec


@pytest.mark.parametrize(
    "writer_address, reader_address, feedsback",
    [
        ("mixers[0]", "mixers[0]", True),
        ("mixers[0]", "mixers[0].tracks[0]", True),
        ("mixers[0]", "mixers[0].tracks[1]", True),
        ("mixers[0]", "mixers[0].tracks[0].tracks[0]", True),
        ("mixers[0]", "mixers[0].tracks[1].tracks[0]", True),
        ("mixers[0].tracks[0]", "mixers[0]", False),
        ("mixers[0].tracks[0]", "mixers[0].tracks[0]", True),
        ("mixers[0].tracks[0]", "mixers[0].tracks[1]", False),
        ("mixers[0].tracks[0]", "mixers[0].tracks[0].tracks[0]", True),
        ("mixers[0].tracks[0]", "mixers[0].tracks[1].tracks[0]", False),
        ("mixers[0].tracks[1]", "mixers[0]", False),
        ("mixers[0].tracks[1]", "mixers[0].tracks[0]", True),
        ("mixers[0].tracks[1]", "mixers[0].tracks[1]", True),
        ("mixers[0].tracks[1]", "mixers[0].tracks[0].tracks[0]", True),
        ("mixers[0].tracks[1]", "mixers[0].tracks[1].tracks[0]", True),
        ("mixers[0].tracks[0].tracks[0]", "mixers[0]", False),
        ("mixers[0].tracks[0].tracks[0]", "mixers[0].tracks[0]", False),
        ("mixers[0].tracks[0].tracks[0]", "mixers[0].tracks[1]", False),
        ("mixers[0].tracks[0].tracks[0]", "mixers[0].tracks[0].tracks[0]", True),
        ("mixers[0].tracks[0].tracks[0]", "mixers[0].tracks[1].tracks[0]", False),
        ("mixers[0].tracks[1].tracks[0]", "mixers[0]", False),
        ("mixers[0].tracks[1].tracks[0]", "mixers[0].tracks[0]", True),
        ("mixers[0].tracks[1].tracks[0]", "mixers[0].tracks[1]", False),
        ("mixers[0].tracks[1].tracks[0]", "mixers[0].tracks[0].tracks[0]", True),
        ("mixers[0].tracks[1].tracks[0]", "mixers[0].tracks[1].tracks[0]", True),
    ],
)
@pytest.mark.asyncio
async def test_Spec_feedsback(
    feedsback: bool,
    writer_address: str,
    reader_address: str,
) -> None:
    session = Session()
    mixer = await session.add_mixer()
    track_one = await mixer.add_track()
    track_two = await mixer.add_track()
    await track_one.add_track()
    await track_two.add_track()
    writer = session[writer_address]
    reader = session[reader_address]
    assert Spec.feedsback(writer.graph_order, reader.graph_order) == feedsback, (
        writer_address,
        reader_address,
    )
