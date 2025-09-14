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
    ParallelPattern,
    Pattern,
    SequencePattern,
)

from .conftest import run_pattern_test


@pytest.mark.parametrize(
    "stop_at, patterns, expected, is_infinite",
    [
        (
            None,
            [
                EventPattern(frequency=SequencePattern([440, 550, 660])),
                EventPattern(frequency=SequencePattern([777, 888, 999])),
            ],
            [
                CompositeEvent(
                    [
                        NoteEvent(UUID(int=0), delta=0.0, frequency=440),
                        NoteEvent(UUID(int=1), delta=0.0, frequency=777),
                    ],
                    delta=1.0,
                ),
                CompositeEvent(
                    [
                        NoteEvent(UUID(int=2), delta=0.0, frequency=550),
                        NoteEvent(UUID(int=3), delta=0.0, frequency=888),
                    ],
                    delta=1.0,
                ),
                CompositeEvent(
                    [
                        NoteEvent(UUID(int=4), delta=0.0, frequency=660),
                        NoteEvent(UUID(int=5), delta=0.0, frequency=999),
                    ],
                    delta=1.0,
                ),
            ],
            False,
        ),
        (
            None,
            [
                EventPattern(x=SequencePattern([1, 2, 3]), delta=1.0),
                EventPattern(y=SequencePattern([1, 2]), delta=1.5),
            ],
            [
                CompositeEvent(
                    [
                        NoteEvent(UUID(int=0), delta=0.0, x=1),
                        NoteEvent(UUID(int=1), delta=0.0, y=1),
                    ],
                    delta=1.0,
                ),
                NoteEvent(UUID(int=2), delta=0.5, x=2),
                NoteEvent(UUID(int=3), delta=0.5, y=2),
                NoteEvent(UUID(int=4), delta=1.0, x=3),
            ],
            False,
        ),
        (
            1,
            [
                EventPattern(x=SequencePattern([1, 2, 3]), delta=1.0),
                EventPattern(y=SequencePattern([1, 2]), delta=1.5),
            ],
            [
                CompositeEvent(
                    [
                        NoteEvent(UUID(int=0), delta=0.0, x=1),
                        NoteEvent(UUID(int=1), delta=0.0, y=1),
                    ],
                    delta=1.0,
                )
            ],
            False,
        ),
        (
            None,
            [
                GroupPattern(EventPattern(x=SequencePattern([1, 2, 3]), delta=1.0)),
                GroupPattern(EventPattern(y=SequencePattern([1, 2]), delta=1.5)),
            ],
            [
                CompositeEvent(
                    [
                        CompositeEvent([GroupAllocateEvent(UUID(int=0))]),
                        NoteEvent(UUID(int=1), delta=0.0, target_node=UUID(int=0), x=1),
                        CompositeEvent([GroupAllocateEvent(UUID(int=2))]),
                        NoteEvent(UUID(int=3), delta=0.0, target_node=UUID(int=2), y=1),
                    ],
                    delta=1.0,
                ),
                NoteEvent(UUID(int=4), delta=0.5, target_node=UUID(int=0), x=2),
                NoteEvent(UUID(int=5), delta=0.5, target_node=UUID(int=2), y=2),
                NoteEvent(UUID(int=6), delta=1.0, target_node=UUID(int=0), x=3),
                CompositeEvent(
                    [
                        CompositeEvent(
                            [NullEvent(delta=0.25), NodeFreeEvent(UUID(int=0))]
                        ),
                        CompositeEvent(
                            [NullEvent(delta=0.25), NodeFreeEvent(UUID(int=2))]
                        ),
                    ]
                ),
            ],
            False,
        ),
        (
            1,
            [
                GroupPattern(EventPattern(x=SequencePattern([1, 2, 3]), delta=1.0)),
                GroupPattern(EventPattern(y=SequencePattern([1, 2]), delta=1.5)),
            ],
            [
                CompositeEvent(
                    [
                        CompositeEvent([GroupAllocateEvent(UUID(int=0))]),
                        NoteEvent(UUID(int=1), delta=0.0, target_node=UUID(int=0), x=1),
                        CompositeEvent([GroupAllocateEvent(UUID(int=2))]),
                        NoteEvent(UUID(int=3), delta=0.0, target_node=UUID(int=2), y=1),
                    ],
                    delta=1.0,
                ),
                CompositeEvent(
                    [NullEvent(delta=0.25), NodeFreeEvent(UUID(int=0))], delta=0.5
                ),
                CompositeEvent([NullEvent(delta=0.25), NodeFreeEvent(UUID(int=2))]),
            ],
            False,
        ),
    ],
)
def test_pattern(
    stop_at: float | None,
    patterns: list[Pattern[Event]],
    expected: list[Event],
    is_infinite: bool,
) -> None:
    pattern = ParallelPattern(patterns)
    run_pattern_test(pattern, expected, is_infinite, stop_at)
