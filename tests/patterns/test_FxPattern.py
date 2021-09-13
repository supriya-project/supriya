import pytest

from supriya import AddAction
from supriya.patterns import (
    CompositeEvent,
    EventPattern,
    FxPattern,
    NodeFreeEvent,
    NoteEvent,
    NullEvent,
    SequencePattern,
    SynthAllocateEvent,
)
from supriya.patterns.testutils import MockUUID as M
from supriya.patterns.testutils import run_pattern_test
from supriya.synthdefs import SynthDefBuilder
from supriya.ugens import FreeVerb, In, Out

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
                            M("A"), add_action=AddAction.ADD_TO_TAIL, synthdef=synthdef
                        )
                    ]
                ),
                NoteEvent(M("B"), a=1),
                NoteEvent(M("C"), a=2),
                CompositeEvent([NodeFreeEvent(M("A"))]),
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
                            M("A"),
                            add_action=AddAction.ADD_TO_TAIL,
                            mix=0.25,
                            synthdef=synthdef,
                        )
                    ]
                ),
                NoteEvent(M("B"), a=1),
                NoteEvent(M("C"), a=2),
                CompositeEvent([NullEvent(delta=0.5), NodeFreeEvent(M("A"))]),
            ],
            False,
        ),
    ],
)
def test(stop_at, inner_pattern, synthdef, release_time, kwargs, expected, is_infinite):
    pattern = FxPattern(inner_pattern, synthdef, release_time=release_time, **kwargs)
    run_pattern_test(pattern, expected, is_infinite, stop_at)
