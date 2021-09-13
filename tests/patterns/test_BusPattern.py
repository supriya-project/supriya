import pytest

from supriya import AddAction, CalculationRate
from supriya.assets import synthdefs
from supriya.patterns import (
    BusAllocateEvent,
    BusFreeEvent,
    BusPattern,
    CompositeEvent,
    EventPattern,
    GroupAllocateEvent,
    NodeFreeEvent,
    NoteEvent,
    NullEvent,
    SequencePattern,
    SynthAllocateEvent,
)
from supriya.patterns.testutils import MockUUID as M
from supriya.patterns.testutils import run_pattern_test


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
                            synthdef=synthdefs.system_link_audio_2,
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
                            synthdef=synthdefs.system_link_audio_2,
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
                            synthdef=synthdefs.system_link_audio_2,
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
                            synthdef=synthdefs.system_link_audio_2,
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
    ],
)
def test(
    stop_at,
    inner_pattern,
    calculation_rate,
    channel_count,
    release_time,
    expected,
    is_infinite,
):
    pattern = BusPattern(
        inner_pattern,
        calculation_rate=calculation_rate,
        channel_count=channel_count,
        release_time=release_time,
    )
    run_pattern_test(pattern, expected, is_infinite, stop_at)
