import uuid

from supriya.patterns import NoteEvent


def test___eq__():
    event_one = NoteEvent(uuid.uuid4())
    event_two = NoteEvent(uuid.uuid4())
    non_event = 23
    assert event_one == event_one
    assert event_two == event_two
    assert event_one != event_two
    assert event_one != non_event
    assert event_two != non_event
