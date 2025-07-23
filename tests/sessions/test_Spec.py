import pytest

from supriya.sessions import Component, Session
from supriya.sessions.specs import Spec


@pytest.mark.parametrize(
    "writer_name, reader_name, feedsback",
    [
        ("mixer", "mixer", True),
        ("mixer", "track_one", True),
        ("mixer", "track_two", True),
        ("mixer", "track_one_child", True),
        ("mixer", "track_two_child", True),
        ("track_one", "mixer", False),
        ("track_one", "track_one", True),
        ("track_one", "track_two", False),
        ("track_one", "track_one_child", True),
        ("track_one", "track_two_child", False),
        ("track_two", "mixer", False),
        ("track_two", "track_one", True),
        ("track_two", "track_two", True),
        ("track_two", "track_one_child", True),
        ("track_two", "track_two_child", True),
        ("track_one_child", "mixer", False),
        ("track_one_child", "track_one", False),
        ("track_one_child", "track_two", False),
        ("track_one_child", "track_one_child", True),
        ("track_one_child", "track_two_child", False),
        ("track_two_child", "mixer", False),
        ("track_two_child", "track_one", True),
        ("track_two_child", "track_two", False),
        ("track_two_child", "track_one_child", True),
        ("track_two_child", "track_two_child", True),
    ],
)
@pytest.mark.asyncio
async def test_Spec_feedsback(
    basic_session: tuple[Session, str, str],
    feedsback: bool,
    writer_name: str,
    reader_name: str,
) -> None:
    session, _, _ = basic_session
    components: dict[str, Component] = {
        "mixer": (mixer := session.mixers[0]),
        "track_one": (track_one := mixer.tracks[0]),
        "track_two": (track_two := await mixer.add_track()),
        "track_one_child": await track_one.add_track(),
        "track_two_child": await track_two.add_track(),
    }
    writer = components[writer_name]
    reader = components[reader_name]
    assert Spec.feedsback(writer.graph_order, reader.graph_order) == feedsback, (
        writer_name,
        reader_name,
    )
