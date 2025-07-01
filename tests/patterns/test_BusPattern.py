import pytest

from supriya import AddAction, CalculationRate
from supriya.patterns import (
    BusAllocateEvent,
    BusFreeEvent,
    BusPattern,
    CompositeEvent,
    Event,
    EventPattern,
    GroupAllocateEvent,
    NodeFreeEvent,
    NoteEvent,
    NullEvent,
    ParallelPattern,
    SequencePattern,
    SynthAllocateEvent,
)
from supriya.patterns.testutils import MockUUID as M
from supriya.patterns.testutils import run_pattern_test
from supriya.typing import CalculationRateLike
from supriya.ugens import system


@pytest.mark.parametrize(
    "stop_at, inner_pattern, calculation_rate, channel_count, release_time, expected, is_infinite",
    [
        (
            None,
            EventPattern(a=SequencePattern([1, 2])),
            "audio",
            2,
            0.0,
            [
                CompositeEvent(
                    [
                        BusAllocateEvent(
                            M("A"),
                            calculation_rate=CalculationRate.AUDIO,
                            channel_count=2,
                        ),
                        GroupAllocateEvent(M("B")),
                        SynthAllocateEvent(
                            M("C"),
                            add_action=AddAction.ADD_AFTER,
                            amplitude=1.0,
                            fade_time=0.0,
                            in_=M("A"),
                            synthdef=system.system_link_audio_2,
                            target_node=M("B"),
                        ),
                    ]
                ),
                NoteEvent(M("D"), a=1, out=M("A"), target_node=M("B")),
                NoteEvent(M("E"), a=2, out=M("A"), target_node=M("B")),
                CompositeEvent(
                    [NodeFreeEvent(M("C")), NodeFreeEvent(M("B")), BusFreeEvent(M("A"))]
                ),
            ],
            False,
        ),
        (
            None,
            EventPattern(a=SequencePattern([1, 2])),
            "audio",
            2,
            0.25,
            [
                CompositeEvent(
                    [
                        BusAllocateEvent(
                            M("A"),
                            calculation_rate=CalculationRate.AUDIO,
                            channel_count=2,
                        ),
                        GroupAllocateEvent(M("B")),
                        SynthAllocateEvent(
                            M("C"),
                            add_action=AddAction.ADD_AFTER,
                            amplitude=1.0,
                            fade_time=0.25,
                            in_=M("A"),
                            synthdef=system.system_link_audio_2,
                            target_node=M("B"),
                        ),
                    ]
                ),
                NoteEvent(M("D"), a=1, out=M("A"), target_node=M("B")),
                NoteEvent(M("E"), a=2, out=M("A"), target_node=M("B")),
                CompositeEvent(
                    [
                        NodeFreeEvent(M("C")),
                        NullEvent(delta=0.25),
                        NodeFreeEvent(M("B")),
                        BusFreeEvent(M("A")),
                    ]
                ),
            ],
            False,
        ),
        (
            None,
            BusPattern(EventPattern(a=SequencePattern([1, 2])), channel_count=2),
            "audio",
            2,
            0.25,
            [
                CompositeEvent(
                    [
                        BusAllocateEvent(
                            M("A"),
                            calculation_rate=CalculationRate.AUDIO,
                            channel_count=2,
                        ),
                        GroupAllocateEvent(M("B")),
                        SynthAllocateEvent(
                            M("C"),
                            add_action=AddAction.ADD_AFTER,
                            amplitude=1.0,
                            fade_time=0.25,
                            in_=M("A"),
                            synthdef=system.system_link_audio_2,
                            target_node=M("B"),
                        ),
                    ]
                ),
                CompositeEvent(
                    [
                        BusAllocateEvent(
                            M("D"),
                            calculation_rate=CalculationRate.AUDIO,
                            channel_count=2,
                        ),
                        GroupAllocateEvent(M("E"), target_node=M("B")),
                        SynthAllocateEvent(
                            M("F"),
                            add_action=AddAction.ADD_AFTER,
                            amplitude=1.0,
                            fade_time=0.25,
                            in_=M("D"),
                            out=M("A"),
                            synthdef=system.system_link_audio_2,
                            target_node=M("E"),
                        ),
                    ]
                ),
                NoteEvent(M("G"), a=1, out=M("D"), target_node=M("E")),
                NoteEvent(M("H"), a=2, out=M("D"), target_node=M("E")),
                CompositeEvent(
                    [
                        NodeFreeEvent(M("F")),
                        NullEvent(delta=0.25),
                        NodeFreeEvent(M("E")),
                        BusFreeEvent(M("D")),
                    ]
                ),
                CompositeEvent(
                    [
                        NodeFreeEvent(M("C")),
                        NullEvent(delta=0.25),
                        NodeFreeEvent(M("B")),
                        BusFreeEvent(M("A")),
                    ]
                ),
            ],
            False,
        ),
        (
            None,
            ParallelPattern(
                [
                    BusPattern(
                        EventPattern(a=SequencePattern([1, 2])), channel_count=2
                    ),
                    BusPattern(
                        EventPattern(a=SequencePattern([1, 2])), channel_count=2
                    ),
                ]
            ),
            "audio",
            2,
            0.25,
            [
                CompositeEvent(
                    [
                        BusAllocateEvent(
                            M("A"),
                            calculation_rate=CalculationRate.AUDIO,
                            channel_count=2,
                        ),
                        GroupAllocateEvent(M("B")),
                        SynthAllocateEvent(
                            M("C"),
                            system.system_link_audio_2,
                            add_action=AddAction.ADD_AFTER,
                            amplitude=1.0,
                            fade_time=0.25,
                            in_=M("A"),
                            target_node=M("B"),
                        ),
                    ]
                ),
                CompositeEvent(
                    [
                        CompositeEvent(
                            [
                                BusAllocateEvent(
                                    M("D"),
                                    calculation_rate=CalculationRate.AUDIO,
                                    channel_count=2,
                                ),
                                GroupAllocateEvent(M("E"), target_node=M("B")),
                                SynthAllocateEvent(
                                    M("F"),
                                    system.system_link_audio_2,
                                    add_action=AddAction.ADD_AFTER,
                                    amplitude=1.0,
                                    fade_time=0.25,
                                    in_=M("D"),
                                    out=M("A"),
                                    target_node=M("E"),
                                ),
                            ]
                        ),
                        NoteEvent(
                            M("G"),
                            a=1,
                            delta=0.0,
                            out=M("D"),
                            target_node=M("E"),
                        ),
                        CompositeEvent(
                            [
                                BusAllocateEvent(
                                    M("H"),
                                    calculation_rate=CalculationRate.AUDIO,
                                    channel_count=2,
                                ),
                                GroupAllocateEvent(M("I"), target_node=M("B")),
                                SynthAllocateEvent(
                                    M("J"),
                                    system.system_link_audio_2,
                                    add_action=AddAction.ADD_AFTER,
                                    amplitude=1.0,
                                    fade_time=0.25,
                                    in_=M("H"),
                                    out=M("A"),
                                    target_node=M("I"),
                                ),
                            ]
                        ),
                        NoteEvent(
                            M("K"),
                            a=1,
                            delta=0.0,
                            out=M("H"),
                            target_node=M("I"),
                        ),
                    ],
                    delta=1.0,
                ),
                CompositeEvent(
                    [
                        NoteEvent(
                            M("L"),
                            a=2,
                            delta=0.0,
                            out=M("D"),
                            target_node=M("E"),
                        ),
                        NoteEvent(
                            M("M"),
                            a=2,
                            delta=0.0,
                            out=M("H"),
                            target_node=M("I"),
                        ),
                    ],
                    delta=1.0,
                ),
                CompositeEvent(
                    [
                        CompositeEvent(
                            [
                                NodeFreeEvent(M("F")),
                                NullEvent(delta=0.25),
                                NodeFreeEvent(M("E")),
                                BusFreeEvent(M("D")),
                            ]
                        ),
                        CompositeEvent(
                            [
                                NodeFreeEvent(M("J")),
                                NullEvent(delta=0.25),
                                NodeFreeEvent(M("I")),
                                BusFreeEvent(M("H")),
                            ]
                        ),
                    ]
                ),
                CompositeEvent(
                    [
                        NodeFreeEvent(M("C")),
                        NullEvent(delta=0.25),
                        NodeFreeEvent(M("B")),
                        BusFreeEvent(M("A")),
                    ]
                ),
            ],
            False,
        ),
    ],
)
def test_pattern(
    stop_at: float | None,
    inner_pattern,
    calculation_rate: CalculationRateLike,
    channel_count: int,
    release_time: float,
    expected: list[Event],
    is_infinite: bool,
) -> None:
    pattern = BusPattern(
        inner_pattern,
        calculation_rate=calculation_rate,
        channel_count=channel_count,
        release_time=release_time,
    )
    run_pattern_test(pattern, expected, is_infinite, stop_at)
