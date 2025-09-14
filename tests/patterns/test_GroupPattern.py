from uuid import UUID

import pytest

from supriya.patterns import (
    CompositeEvent,
    Event,
    EventPattern,
    GroupAllocateEvent,
    GroupPattern,
    NodeFreeEvent,
    NoteEvent,
    NullEvent,
    SequencePattern,
)

from .conftest import run_pattern_test


@pytest.mark.parametrize(
    "stop_at, inner_pattern, release_time, expected, is_infinite",
    [
        (
            None,
            EventPattern(a=SequencePattern([1, 2])),
            0.0,
            [
                CompositeEvent([GroupAllocateEvent(UUID(int=0), delta=0.0)]),
                NoteEvent(UUID(int=1), a=1, target_node=UUID(int=0)),
                NoteEvent(UUID(int=2), a=2, target_node=UUID(int=0)),
                CompositeEvent([NodeFreeEvent(UUID(int=0), delta=0.0)]),
            ],
            False,
        ),
        (
            None,
            EventPattern(a=SequencePattern([1, 2])),
            0.25,
            [
                CompositeEvent([GroupAllocateEvent(UUID(int=0), delta=0.0)]),
                NoteEvent(UUID(int=1), a=1, target_node=UUID(int=0)),
                NoteEvent(UUID(int=2), a=2, target_node=UUID(int=0)),
                CompositeEvent(
                    [NullEvent(delta=0.25), NodeFreeEvent(UUID(int=0), delta=0.0)]
                ),
            ],
            False,
        ),
    ],
)
def test_pattern(
    stop_at: float | None,
    inner_pattern: EventPattern,
    release_time: float,
    expected: list[Event],
    is_infinite: bool,
) -> None:
    pattern = GroupPattern(inner_pattern, release_time=release_time)
    run_pattern_test(pattern, expected, is_infinite, stop_at)
