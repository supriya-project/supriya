import pytest

from supriya.patterns import (
    CompositeEvent,
    EventPattern,
    GroupAllocateEvent,
    GroupPattern,
    NodeFreeEvent,
    NoteEvent,
    NullEvent,
    ParallelPattern,
    SequencePattern,
)
from supriya.patterns.testutils import MockUUID as M
from supriya.patterns.testutils import run_pattern_test


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
                        NoteEvent(M("A"), delta=0.0, frequency=440),
                        NoteEvent(M("B"), delta=0.0, frequency=777),
                    ],
                    delta=1.0,
                ),
                CompositeEvent(
                    [
                        NoteEvent(M("C"), delta=0.0, frequency=550),
                        NoteEvent(M("D"), delta=0.0, frequency=888),
                    ],
                    delta=1.0,
                ),
                CompositeEvent(
                    [
                        NoteEvent(M("E"), delta=0.0, frequency=660),
                        NoteEvent(M("F"), delta=0.0, frequency=999),
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
                        NoteEvent(M("A"), delta=0.0, x=1),
                        NoteEvent(M("B"), delta=0.0, y=1),
                    ],
                    delta=1.0,
                ),
                NoteEvent(M("C"), delta=0.5, x=2),
                NoteEvent(M("D"), delta=0.5, y=2),
                NoteEvent(M("E"), delta=1.0, x=3),
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
                        NoteEvent(M("A"), delta=0.0, x=1),
                        NoteEvent(M("B"), delta=0.0, y=1),
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
                        CompositeEvent([GroupAllocateEvent(M("A"))]),
                        NoteEvent(M("B"), delta=0.0, target_node=M("A"), x=1),
                        CompositeEvent([GroupAllocateEvent(M("C"))]),
                        NoteEvent(M("D"), delta=0.0, target_node=M("C"), y=1),
                    ],
                    delta=1.0,
                ),
                NoteEvent(M("E"), delta=0.5, target_node=M("A"), x=2),
                NoteEvent(M("F"), delta=0.5, target_node=M("C"), y=2),
                NoteEvent(M("G"), delta=1.0, target_node=M("A"), x=3),
                CompositeEvent(
                    [
                        CompositeEvent([NullEvent(delta=0.25), NodeFreeEvent(M("A"))]),
                        CompositeEvent([NullEvent(delta=0.25), NodeFreeEvent(M("C"))]),
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
                        CompositeEvent([GroupAllocateEvent(M("A"))]),
                        NoteEvent(M("B"), delta=0.0, target_node=M("A"), x=1),
                        CompositeEvent([GroupAllocateEvent(M("C"))]),
                        NoteEvent(M("D"), delta=0.0, target_node=M("C"), y=1),
                    ],
                    delta=1.0,
                ),
                CompositeEvent(
                    [NullEvent(delta=0.25), NodeFreeEvent(M("A"))], delta=0.5
                ),
                CompositeEvent([NullEvent(delta=0.25), NodeFreeEvent(M("C"))]),
            ],
            False,
        ),
    ],
)
def test(stop_at, patterns, expected, is_infinite):
    pattern = ParallelPattern(patterns)
    run_pattern_test(pattern, expected, is_infinite, stop_at)
