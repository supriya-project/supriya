import pytest

from supriya.patterns import EventPattern, NoteEvent, SequencePattern
from supriya.patterns.testutils import MockUUID as M
from supriya.patterns.testutils import run_pattern_test


@pytest.mark.parametrize(
    "stop_at, input_a, input_b, expected, is_infinite",
    [
        (
            None,
            SequencePattern([1, 2, 3], None),
            SequencePattern([4, 5], None),
            [
                NoteEvent(M("A"), a=1, b=4),
                NoteEvent(M("B"), a=2, b=5),
                NoteEvent(M("C"), a=3, b=4),
                NoteEvent(M("D"), a=1, b=5),
                NoteEvent(M("E"), a=2, b=4),
                NoteEvent(M("F"), a=3, b=5),
            ],
            True,
        ),
        (
            None,
            SequencePattern([1, 2, 3], None),
            SequencePattern([4, 5], 1),
            [NoteEvent(M("A"), a=1, b=4), NoteEvent(M("B"), a=2, b=5)],
            False,
        ),
        (
            None,
            SequencePattern([1, 2, 3], None),
            SequencePattern([4, 5], 2),
            [
                NoteEvent(M("A"), a=1, b=4),
                NoteEvent(M("B"), a=2, b=5),
                NoteEvent(M("C"), a=3, b=4),
                NoteEvent(M("D"), a=1, b=5),
            ],
            False,
        ),
        (
            None,
            SequencePattern([1, 2, 3], 1),
            SequencePattern([4, 5], 1),
            [NoteEvent(M("A"), a=1, b=4), NoteEvent(M("B"), a=2, b=5)],
            False,
        ),
        (
            None,
            SequencePattern([1, 2, 3], 1),
            SequencePattern([4, 5], None),
            [
                NoteEvent(M("A"), a=1, b=4),
                NoteEvent(M("B"), a=2, b=5),
                NoteEvent(M("C"), a=3, b=4),
            ],
            False,
        ),
        (
            None,
            SequencePattern([1, 2, 3], 1),
            4,
            [
                NoteEvent(M("A"), a=1, b=4),
                NoteEvent(M("B"), a=2, b=4),
                NoteEvent(M("C"), a=3, b=4),
            ],
            False,
        ),
    ],
)
def test(stop_at, input_a, input_b, expected, is_infinite):
    pattern = EventPattern(a=input_a, b=input_b)
    run_pattern_test(pattern, expected, is_infinite, stop_at)
