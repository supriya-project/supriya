import uuid

import pytest

from supriya.newpatterns.events import NoteEvent, Priority

id_ = uuid.uuid4()


@pytest.mark.parametrize(
    "event, offset, expected",
    [
        (
            NoteEvent(id_),
            0.0,
            [
                (0.0, Priority.START, NoteEvent((id_, 0))),
                (1.0, Priority.STOP, NoteEvent((id_, 0))),
            ],
        ),
        (
            NoteEvent(id_, frequency=[440, 550]),
            0.0,
            [
                (0.0, Priority.START, NoteEvent((id_, 0), frequency=440)),
                (0.0, Priority.START, NoteEvent((id_, 1), frequency=550)),
                (1.0, Priority.STOP, NoteEvent((id_, 0), frequency=440)),
                (1.0, Priority.STOP, NoteEvent((id_, 1), frequency=550)),
            ],
        ),
        (
            NoteEvent(id_, frequency=[440, 550], amplitude=[0.5, 0.75, 1.0]),
            2.5,
            [
                (
                    2.5,
                    Priority.START,
                    NoteEvent((id_, 0), amplitude=0.5, frequency=440),
                ),
                (
                    2.5,
                    Priority.START,
                    NoteEvent((id_, 1), amplitude=0.75, frequency=550),
                ),
                (
                    2.5,
                    Priority.START,
                    NoteEvent((id_, 2), amplitude=1.0, frequency=440),
                ),
                (3.5, Priority.STOP, NoteEvent((id_, 0), amplitude=0.5, frequency=440)),
                (
                    3.5,
                    Priority.STOP,
                    NoteEvent((id_, 1), amplitude=0.75, frequency=550),
                ),
                (3.5, Priority.STOP, NoteEvent((id_, 2), amplitude=1.0, frequency=440)),
            ],
        ),
    ],
)
def test_expand(event, offset, expected):
    actual = event.expand(offset)
    assert actual == expected
