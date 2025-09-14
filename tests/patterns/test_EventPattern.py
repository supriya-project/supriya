from uuid import UUID

import pytest

from supriya.patterns import Event, EventPattern, NoteEvent, SequencePattern

from .conftest import run_pattern_test


@pytest.mark.parametrize(
    "stop_at, input_a, input_b, expected, is_infinite",
    [
        (
            None,
            SequencePattern([1, 2, 3], None),
            SequencePattern([4, 5], None),
            [
                NoteEvent(UUID(int=0), a=1, b=4),
                NoteEvent(UUID(int=1), a=2, b=5),
                NoteEvent(UUID(int=2), a=3, b=4),
                NoteEvent(UUID(int=3), a=1, b=5),
                NoteEvent(UUID(int=4), a=2, b=4),
                NoteEvent(UUID(int=5), a=3, b=5),
            ],
            True,
        ),
        (
            None,
            SequencePattern([1, 2, 3], None),
            SequencePattern([4, 5], 1),
            [NoteEvent(UUID(int=0), a=1, b=4), NoteEvent(UUID(int=1), a=2, b=5)],
            False,
        ),
        (
            None,
            SequencePattern([1, 2, 3], None),
            SequencePattern([4, 5], 2),
            [
                NoteEvent(UUID(int=0), a=1, b=4),
                NoteEvent(UUID(int=1), a=2, b=5),
                NoteEvent(UUID(int=2), a=3, b=4),
                NoteEvent(UUID(int=3), a=1, b=5),
            ],
            False,
        ),
        (
            None,
            SequencePattern([1, 2, 3], 1),
            SequencePattern([4, 5], 1),
            [NoteEvent(UUID(int=0), a=1, b=4), NoteEvent(UUID(int=1), a=2, b=5)],
            False,
        ),
        (
            None,
            SequencePattern([1, 2, 3], 1),
            SequencePattern([4, 5], None),
            [
                NoteEvent(UUID(int=0), a=1, b=4),
                NoteEvent(UUID(int=1), a=2, b=5),
                NoteEvent(UUID(int=2), a=3, b=4),
            ],
            False,
        ),
        (
            None,
            SequencePattern([1, 2, 3], 1),
            4,
            [
                NoteEvent(UUID(int=0), a=1, b=4),
                NoteEvent(UUID(int=1), a=2, b=4),
                NoteEvent(UUID(int=2), a=3, b=4),
            ],
            False,
        ),
    ],
)
def test_pattern(
    stop_at: float | None,
    input_a: SequencePattern,
    input_b: SequencePattern | int,
    expected: list[Event],
    is_infinite: bool,
) -> None:
    pattern = EventPattern(a=input_a, b=input_b)
    run_pattern_test(pattern, expected, is_infinite, stop_at)
