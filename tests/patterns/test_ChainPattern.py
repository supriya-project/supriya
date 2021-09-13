import pytest

from supriya.patterns import ChainPattern, EventPattern, NoteEvent, SequencePattern
from supriya.patterns.testutils import MockUUID as M
from supriya.patterns.testutils import run_pattern_test


@pytest.mark.parametrize(
    "stop_at, input_a, input_b1, input_b2, input_c, expected, is_infinite",
    [
        (
            None,
            SequencePattern([1, 2, 3]),
            SequencePattern([4, 5]),
            SequencePattern([7, 8, 9]),
            SequencePattern([10, 11]),
            [NoteEvent(M("A"), a=1, b=7, c=10), NoteEvent(M("B"), a=2, b=8, c=11)],
            False,
        ),
        (
            None,
            SequencePattern([1, 2, 3], None),
            SequencePattern([4, 5], None),
            SequencePattern([7, 8, 9]),
            SequencePattern([10, 11]),
            [NoteEvent(M("A"), a=1, b=7, c=10), NoteEvent(M("B"), a=2, b=8, c=11)],
            False,
        ),
        (
            None,
            SequencePattern([1, 2, 3], None),
            SequencePattern([4, 5], None),
            SequencePattern([7, 8, 9], None),
            SequencePattern([10, 11], None),
            [
                NoteEvent(M("A"), a=1, b=7, c=10),
                NoteEvent(M("B"), a=2, b=8, c=11),
                NoteEvent(M("C"), a=3, b=9, c=10),
                NoteEvent(M("D"), a=1, b=7, c=11),
                NoteEvent(M("E"), a=2, b=8, c=10),
                NoteEvent(M("F"), a=3, b=9, c=11),
            ],
            True,
        ),
    ],
)
def test(stop_at, input_a, input_b1, input_b2, input_c, expected, is_infinite):
    pattern = ChainPattern(
        EventPattern(a=input_a, b=input_b1),
        EventPattern(b=input_b2),
        EventPattern(c=input_c),
    )
    run_pattern_test(pattern, expected, is_infinite, stop_at)
