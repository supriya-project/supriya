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
from supriya.patterns.testutils import MockUUID as M
from supriya.patterns.testutils import run_pattern_test


@pytest.mark.parametrize(
    "stop_at, inner_pattern, release_time, expected, is_infinite",
    [
        (
            None,
            EventPattern(a=SequencePattern([1, 2])),
            0.0,
            [
                CompositeEvent([GroupAllocateEvent(M("A"), delta=0.0)]),
                NoteEvent(M("B"), a=1, target_node=M("A")),
                NoteEvent(M("C"), a=2, target_node=M("A")),
                CompositeEvent([NodeFreeEvent(M("A"), delta=0.0)]),
            ],
            False,
        ),
        (
            None,
            EventPattern(a=SequencePattern([1, 2])),
            0.25,
            [
                CompositeEvent([GroupAllocateEvent(M("A"), delta=0.0)]),
                NoteEvent(M("B"), a=1, target_node=M("A")),
                NoteEvent(M("C"), a=2, target_node=M("A")),
                CompositeEvent(
                    [NullEvent(delta=0.25), NodeFreeEvent(M("A"), delta=0.0)]
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
