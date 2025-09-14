from uuid import UUID

import pytest

from supriya import AddAction
from supriya.patterns import (
    CompositeEvent,
    Event,
    EventPattern,
    FxPattern,
    NodeFreeEvent,
    NoteEvent,
    NullEvent,
    SequencePattern,
    SynthAllocateEvent,
)
from supriya.ugens import FreeVerb, In, Out, SynthDef, SynthDefBuilder

from .conftest import run_pattern_test

with SynthDefBuilder(in_=0, out=0, mix=0.0) as builder:
    in_ = In.ar(bus=builder["in_"], channel_count=2)
    reverb = FreeVerb.ar(source=in_, mix=builder["mix"])
    _ = Out.ar(bus=builder["out"], source=reverb)

synthdef = builder.build()


@pytest.mark.parametrize(
    "stop_at, inner_pattern, synthdef, release_time, kwargs, expected, is_infinite",
    [
        (
            None,
            EventPattern(a=SequencePattern([1, 2])),
            synthdef,
            0.0,
            {},
            [
                CompositeEvent(
                    [
                        SynthAllocateEvent(
                            UUID(int=0),
                            add_action=AddAction.ADD_TO_TAIL,
                            synthdef=synthdef,
                        )
                    ]
                ),
                NoteEvent(UUID(int=1), a=1),
                NoteEvent(UUID(int=2), a=2),
                CompositeEvent([NodeFreeEvent(UUID(int=0))]),
            ],
            False,
        ),
        (
            None,
            EventPattern(a=SequencePattern([1, 2])),
            synthdef,
            0.5,
            {"mix": 0.25},
            [
                CompositeEvent(
                    [
                        SynthAllocateEvent(
                            UUID(int=0),
                            add_action=AddAction.ADD_TO_TAIL,
                            mix=0.25,
                            synthdef=synthdef,
                        )
                    ]
                ),
                NoteEvent(UUID(int=1), a=1),
                NoteEvent(UUID(int=2), a=2),
                CompositeEvent([NullEvent(delta=0.5), NodeFreeEvent(UUID(int=0))]),
            ],
            False,
        ),
    ],
)
def test_pattern(
    stop_at: float | None,
    inner_pattern: EventPattern,
    synthdef: SynthDef,
    release_time: float,
    kwargs: dict[str, float],
    expected: list[Event],
    is_infinite: bool,
) -> None:
    pattern = FxPattern(inner_pattern, synthdef, release_time=release_time, **kwargs)
    run_pattern_test(pattern, expected, is_infinite, stop_at)
