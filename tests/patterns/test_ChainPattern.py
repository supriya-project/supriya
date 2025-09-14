from uuid import UUID

import pytest

from supriya.patterns import (
    ChainPattern,
    Event,
    EventPattern,
    NoteEvent,
    SequencePattern,
)

from .conftest import run_pattern_test


@pytest.mark.parametrize(
    "stop_at, input_a, input_b1, input_b2, input_c, expected, is_infinite",
    [
        (
            None,
            SequencePattern([1, 2, 3]),
            SequencePattern([4, 5]),
            SequencePattern([7, 8, 9]),
            SequencePattern([10, 11]),
            [
                NoteEvent(UUID(int=0), a=1, b=7, c=10),
                NoteEvent(UUID(int=1), a=2, b=8, c=11),
            ],
            False,
        ),
        (
            None,
            SequencePattern([1, 2, 3], None),
            SequencePattern([4, 5], None),
            SequencePattern([7, 8, 9]),
            SequencePattern([10, 11]),
            [
                NoteEvent(UUID(int=0), a=1, b=7, c=10),
                NoteEvent(UUID(int=1), a=2, b=8, c=11),
            ],
            False,
        ),
        (
            None,
            SequencePattern([1, 2, 3], None),
            SequencePattern([4, 5], None),
            SequencePattern([7, 8, 9], None),
            SequencePattern([10, 11], None),
            [
                NoteEvent(UUID(int=0), a=1, b=7, c=10),
                NoteEvent(UUID(int=1), a=2, b=8, c=11),
                NoteEvent(UUID(int=2), a=3, b=9, c=10),
                NoteEvent(UUID(int=3), a=1, b=7, c=11),
                NoteEvent(UUID(int=4), a=2, b=8, c=10),
                NoteEvent(UUID(int=5), a=3, b=9, c=11),
            ],
            True,
        ),
    ],
)
def test_pattern(
    stop_at: float | None,
    input_a: SequencePattern,
    input_b1: SequencePattern,
    input_b2: SequencePattern,
    input_c: SequencePattern,
    expected: list[Event],
    is_infinite: bool,
) -> None:
    pattern = ChainPattern(
        EventPattern(a=input_a, b=input_b1),
        EventPattern(b=input_b2),
        EventPattern(c=input_c),
    )
    run_pattern_test(pattern, expected, is_infinite, stop_at)
