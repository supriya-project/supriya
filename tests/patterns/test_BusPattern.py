from uuid import UUID

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
from supriya.typing import CalculationRateLike
from supriya.ugens import system

from .conftest import run_pattern_test


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
                            UUID(int=0),
                            calculation_rate=CalculationRate.AUDIO,
                            channel_count=2,
                        ),
                        GroupAllocateEvent(UUID(int=1)),
                        SynthAllocateEvent(
                            UUID(int=2),
                            add_action=AddAction.ADD_AFTER,
                            amplitude=1.0,
                            fade_time=0.0,
                            in_=UUID(int=0),
                            synthdef=system.system_link_audio_2,
                            target_node=UUID(int=1),
                        ),
                    ]
                ),
                NoteEvent(UUID(int=3), a=1, out=UUID(int=0), target_node=UUID(int=1)),
                NoteEvent(UUID(int=4), a=2, out=UUID(int=0), target_node=UUID(int=1)),
                CompositeEvent(
                    [
                        NodeFreeEvent(UUID(int=2)),
                        NodeFreeEvent(UUID(int=1)),
                        BusFreeEvent(UUID(int=0)),
                    ]
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
                            UUID(int=0),
                            calculation_rate=CalculationRate.AUDIO,
                            channel_count=2,
                        ),
                        GroupAllocateEvent(UUID(int=1)),
                        SynthAllocateEvent(
                            UUID(int=2),
                            add_action=AddAction.ADD_AFTER,
                            amplitude=1.0,
                            fade_time=0.25,
                            in_=UUID(int=0),
                            synthdef=system.system_link_audio_2,
                            target_node=UUID(int=1),
                        ),
                    ]
                ),
                NoteEvent(UUID(int=3), a=1, out=UUID(int=0), target_node=UUID(int=1)),
                NoteEvent(UUID(int=4), a=2, out=UUID(int=0), target_node=UUID(int=1)),
                CompositeEvent(
                    [
                        NodeFreeEvent(UUID(int=2)),
                        NullEvent(delta=0.25),
                        NodeFreeEvent(UUID(int=1)),
                        BusFreeEvent(UUID(int=0)),
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
                            UUID(int=0),
                            calculation_rate=CalculationRate.AUDIO,
                            channel_count=2,
                        ),
                        GroupAllocateEvent(UUID(int=1)),
                        SynthAllocateEvent(
                            UUID(int=2),
                            add_action=AddAction.ADD_AFTER,
                            amplitude=1.0,
                            fade_time=0.25,
                            in_=UUID(int=0),
                            synthdef=system.system_link_audio_2,
                            target_node=UUID(int=1),
                        ),
                    ]
                ),
                CompositeEvent(
                    [
                        BusAllocateEvent(
                            UUID(int=3),
                            calculation_rate=CalculationRate.AUDIO,
                            channel_count=2,
                        ),
                        GroupAllocateEvent(UUID(int=4), target_node=UUID(int=1)),
                        SynthAllocateEvent(
                            UUID(int=5),
                            add_action=AddAction.ADD_AFTER,
                            amplitude=1.0,
                            fade_time=0.25,
                            in_=UUID(int=3),
                            out=UUID(int=0),
                            synthdef=system.system_link_audio_2,
                            target_node=UUID(int=4),
                        ),
                    ]
                ),
                NoteEvent(UUID(int=6), a=1, out=UUID(int=3), target_node=UUID(int=4)),
                NoteEvent(UUID(int=7), a=2, out=UUID(int=3), target_node=UUID(int=4)),
                CompositeEvent(
                    [
                        NodeFreeEvent(UUID(int=5)),
                        NullEvent(delta=0.25),
                        NodeFreeEvent(UUID(int=4)),
                        BusFreeEvent(UUID(int=3)),
                    ]
                ),
                CompositeEvent(
                    [
                        NodeFreeEvent(UUID(int=2)),
                        NullEvent(delta=0.25),
                        NodeFreeEvent(UUID(int=1)),
                        BusFreeEvent(UUID(int=0)),
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
                            UUID(int=0),
                            calculation_rate=CalculationRate.AUDIO,
                            channel_count=2,
                        ),
                        GroupAllocateEvent(UUID(int=1)),
                        SynthAllocateEvent(
                            UUID(int=2),
                            system.system_link_audio_2,
                            add_action=AddAction.ADD_AFTER,
                            amplitude=1.0,
                            fade_time=0.25,
                            in_=UUID(int=0),
                            target_node=UUID(int=1),
                        ),
                    ]
                ),
                CompositeEvent(
                    [
                        CompositeEvent(
                            [
                                BusAllocateEvent(
                                    UUID(int=3),
                                    calculation_rate=CalculationRate.AUDIO,
                                    channel_count=2,
                                ),
                                GroupAllocateEvent(
                                    UUID(int=4), target_node=UUID(int=1)
                                ),
                                SynthAllocateEvent(
                                    UUID(int=5),
                                    system.system_link_audio_2,
                                    add_action=AddAction.ADD_AFTER,
                                    amplitude=1.0,
                                    fade_time=0.25,
                                    in_=UUID(int=3),
                                    out=UUID(int=0),
                                    target_node=UUID(int=4),
                                ),
                            ]
                        ),
                        NoteEvent(
                            UUID(int=6),
                            a=1,
                            delta=0.0,
                            out=UUID(int=3),
                            target_node=UUID(int=4),
                        ),
                        CompositeEvent(
                            [
                                BusAllocateEvent(
                                    UUID(int=7),
                                    calculation_rate=CalculationRate.AUDIO,
                                    channel_count=2,
                                ),
                                GroupAllocateEvent(
                                    UUID(int=8), target_node=UUID(int=1)
                                ),
                                SynthAllocateEvent(
                                    UUID(int=9),
                                    system.system_link_audio_2,
                                    add_action=AddAction.ADD_AFTER,
                                    amplitude=1.0,
                                    fade_time=0.25,
                                    in_=UUID(int=7),
                                    out=UUID(int=0),
                                    target_node=UUID(int=8),
                                ),
                            ]
                        ),
                        NoteEvent(
                            UUID(int=10),
                            a=1,
                            delta=0.0,
                            out=UUID(int=7),
                            target_node=UUID(int=8),
                        ),
                    ],
                    delta=1.0,
                ),
                CompositeEvent(
                    [
                        NoteEvent(
                            UUID(int=11),
                            a=2,
                            delta=0.0,
                            out=UUID(int=3),
                            target_node=UUID(int=4),
                        ),
                        NoteEvent(
                            UUID(int=12),
                            a=2,
                            delta=0.0,
                            out=UUID(int=7),
                            target_node=UUID(int=8),
                        ),
                    ],
                    delta=1.0,
                ),
                CompositeEvent(
                    [
                        CompositeEvent(
                            [
                                NodeFreeEvent(UUID(int=5)),
                                NullEvent(delta=0.25),
                                NodeFreeEvent(UUID(int=4)),
                                BusFreeEvent(UUID(int=3)),
                            ]
                        ),
                        CompositeEvent(
                            [
                                NodeFreeEvent(UUID(int=9)),
                                NullEvent(delta=0.25),
                                NodeFreeEvent(UUID(int=8)),
                                BusFreeEvent(UUID(int=7)),
                            ]
                        ),
                    ]
                ),
                CompositeEvent(
                    [
                        NodeFreeEvent(UUID(int=2)),
                        NullEvent(delta=0.25),
                        NodeFreeEvent(UUID(int=1)),
                        BusFreeEvent(UUID(int=0)),
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
