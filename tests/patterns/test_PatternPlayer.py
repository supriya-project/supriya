from typing import Optional
from unittest.mock import Mock, call

import pytest

from supriya import AddAction, CalculationRate
from supriya.assets.synthdefs import default, system_link_audio_1
from supriya.clocks import AsyncOfflineClock, OfflineClock
from supriya.contexts import AsyncServer, BusGroup, Context, Group, Score, Server, Synth
from supriya.contexts.requests import NewGroup
from supriya.osc import OscBundle, OscMessage
from supriya.patterns import (
    BusPattern,
    EventPattern,
    GroupPattern,
    MonoEventPattern,
    ParallelPattern,
    SequencePattern,
)
from supriya.patterns.events import NoteEvent, Priority, StartEvent, StopEvent


@pytest.mark.parametrize(
    "pattern, until, target_node, expected",
    [
        (
            SequencePattern(
                [
                    EventPattern(frequency=SequencePattern([440, 550, 660])),
                    MonoEventPattern(frequency=SequencePattern([440, 550, 660])),
                ]
            ),
            None,
            None,
            lambda context: [
                call.at(0.0),
                call.add_synth(
                    add_action=AddAction.ADD_TO_HEAD,
                    synthdef=default,
                    target_node=None,
                    frequency=440,
                ),
                call.at(2.0),
                call.add_synth(
                    add_action=AddAction.ADD_TO_HEAD,
                    synthdef=default,
                    target_node=None,
                    frequency=550,
                ),
                call.free_node(
                    Synth(
                        context=context,
                        id_=1000,
                        synthdef=default,
                    )
                ),
                call.at(4.0),
                call.add_synth(
                    add_action=AddAction.ADD_TO_HEAD,
                    synthdef=default,
                    target_node=None,
                    frequency=660,
                ),
                call.free_node(
                    Synth(
                        context=context,
                        id_=1001,
                        synthdef=default,
                    )
                ),
                call.at(6.0),
                call.add_synth(
                    add_action=AddAction.ADD_TO_HEAD,
                    synthdef=default,
                    target_node=None,
                    frequency=440,
                ),
                call.free_node(
                    Synth(
                        context=context,
                        id_=1002,
                        synthdef=default,
                    )
                ),
                call.at(8.0),
                call.set_node(
                    Synth(
                        context=context,
                        id_=1003,
                        synthdef=default,
                    ),
                    frequency=550,
                ),
                call.at(10.0),
                call.set_node(
                    Synth(
                        context=context,
                        id_=1003,
                        synthdef=default,
                    ),
                    frequency=660,
                ),
                call.at(12.0),
                call.free_node(
                    Synth(
                        context=context,
                        id_=1003,
                        synthdef=default,
                    )
                ),
            ],
        ),
        (
            EventPattern(frequency=SequencePattern([440, 550, 660])),
            1.5,
            None,
            lambda context: [
                call.at(0.0),
                call.add_synth(
                    add_action=AddAction.ADD_TO_HEAD,
                    synthdef=default,
                    target_node=None,
                    frequency=440,
                ),
                call.at(2.0),
                call.add_synth(
                    add_action=AddAction.ADD_TO_HEAD,
                    synthdef=default,
                    target_node=None,
                    frequency=550,
                ),
                call.free_node(
                    Synth(
                        context=context,
                        id_=1000,
                        synthdef=default,
                    )
                ),
                call.at(3.0),
                call.free_node(
                    Synth(
                        context=context,
                        id_=1001,
                        synthdef=default,
                    )
                ),
                call.at(3.0),  # 1001 was freed early, nothing to do.
            ],
        ),
        (
            EventPattern(frequency=SequencePattern([440, 550, 660])),
            1.5,
            6666,
            lambda context: [
                call.at(0.0),
                call.add_synth(
                    add_action=AddAction.ADD_TO_HEAD,
                    synthdef=default,
                    target_node=Group(context=context, id_=6666),
                    frequency=440,
                ),
                call.at(2.0),
                call.add_synth(
                    add_action=AddAction.ADD_TO_HEAD,
                    synthdef=default,
                    target_node=Group(context=context, id_=6666),
                    frequency=550,
                ),
                call.free_node(
                    Synth(
                        context=context,
                        id_=1000,
                        synthdef=default,
                    )
                ),
                call.at(3.0),
                call.free_node(
                    Synth(
                        context=context,
                        id_=1001,
                        synthdef=default,
                    )
                ),
                call.at(3.0),  # 1001 was freed early, nothing to do.
            ],
        ),
        (
            GroupPattern(EventPattern(frequency=SequencePattern([440, 550, 660]))),
            1.5,
            6666,
            lambda context: [
                call.at(0.0),
                call.add_group(
                    add_action=AddAction.ADD_TO_HEAD,
                    target_node=Group(context=context, id_=6666),
                ),
                call.add_synth(
                    add_action=AddAction.ADD_TO_HEAD,
                    synthdef=default,
                    target_node=Group(context=context, id_=1000),
                    frequency=440,
                ),
                call.at(2.0),
                call.add_synth(
                    add_action=AddAction.ADD_TO_HEAD,
                    synthdef=default,
                    target_node=Group(context=context, id_=1000),
                    frequency=550,
                ),
                call.free_node(
                    Synth(
                        context=context,
                        id_=1001,
                        synthdef=default,
                    )
                ),
                call.at(3.0),
                call.free_node(
                    Synth(
                        context=context,
                        id_=1002,
                        synthdef=default,
                    )
                ),
                call.at(3.0),  # 1001 was freed early, nothing to do.
                call.at(3.5),
                call.free_node(Group(context=context, id_=1000)),
            ],
        ),
        (
            ParallelPattern(
                [
                    EventPattern(frequency=SequencePattern([440, 550])),
                    EventPattern(frequency=SequencePattern([777, 888])),
                ]
            ),
            None,
            None,
            lambda context: [
                call.at(0.0),
                call.add_synth(
                    add_action=AddAction.ADD_TO_HEAD,
                    synthdef=default,
                    target_node=None,
                    frequency=440,
                ),
                call.add_synth(
                    add_action=AddAction.ADD_TO_HEAD,
                    synthdef=default,
                    target_node=None,
                    frequency=777,
                ),
                call.at(2.0),
                call.add_synth(
                    add_action=AddAction.ADD_TO_HEAD,
                    synthdef=default,
                    target_node=None,
                    frequency=550,
                ),
                call.add_synth(
                    add_action=AddAction.ADD_TO_HEAD,
                    synthdef=default,
                    target_node=None,
                    frequency=888,
                ),
                call.free_node(
                    Synth(
                        context=context,
                        id_=1000,
                        synthdef=default,
                    )
                ),
                call.free_node(
                    Synth(
                        context=context,
                        id_=1001,
                        synthdef=default,
                    )
                ),
                call.at(4.0),
                call.free_node(
                    Synth(
                        context=context,
                        id_=1002,
                        synthdef=default,
                    )
                ),
                call.free_node(
                    Synth(
                        context=context,
                        id_=1003,
                        synthdef=default,
                    )
                ),
            ],
        ),
        (
            GroupPattern(
                BusPattern(MonoEventPattern(frequency=SequencePattern([440, 550, 660])))
            ),
            1.5,
            None,
            lambda context: [
                call.at(0.0),
                call.add_group(add_action=AddAction.ADD_TO_HEAD, target_node=None),
                call.add_bus_group(calculation_rate=CalculationRate.AUDIO, count=1),
                call.add_group(
                    add_action=AddAction.ADD_TO_HEAD,
                    target_node=Group(context=context, id_=1000),
                ),
                call.add_synth(
                    add_action=AddAction.ADD_AFTER,
                    synthdef=system_link_audio_1,
                    target_node=Group(context=context, id_=1001),
                    amplitude=1.0,
                    fade_time=0.25,
                    in_=BusGroup(
                        context=context,
                        calculation_rate=CalculationRate.AUDIO,
                        id_=16,
                        count=1,
                    ),
                ),
                call.add_synth(
                    add_action=AddAction.ADD_TO_HEAD,
                    synthdef=default,
                    target_node=Group(context=context, id_=1001),
                    frequency=440,
                    out=BusGroup(
                        context=context,
                        calculation_rate=CalculationRate.AUDIO,
                        id_=16,
                        count=1,
                    ),
                ),
                call.at(2.0),
                call.set_node(
                    Synth(
                        context=context,
                        id_=1003,
                        synthdef=default,
                    ),
                    frequency=550,
                    out=BusGroup(
                        context=context,
                        calculation_rate=CalculationRate.AUDIO,
                        id_=16,
                        count=1,
                    ),
                ),
                call.at(3.0),
                call.free_node(
                    Synth(
                        context=context,
                        id_=1003,
                        synthdef=default,
                    )
                ),
                call.at(3.0),  # Can we coalesce these moments?
                call.free_node(
                    Synth(
                        context=context,
                        id_=1002,
                        synthdef=system_link_audio_1,
                    )
                ),
                call.at(3.5),
                call.free_node(Group(context=context, id_=1001)),
                call.free_bus_group(
                    BusGroup(
                        context=context,
                        calculation_rate=CalculationRate.AUDIO,
                        id_=16,
                        count=1,
                    )
                ),
                call.free_node(Group(context=context, id_=1000)),
            ],
        ),
    ],
)
def test_context_calls(
    pattern, until: Optional[float], target_node: Optional[int], expected
):
    clock = OfflineClock()
    context = Server().boot()
    target_node_ = None
    if target_node is not None:
        context.send(
            NewGroup(items=[(target_node, "add_to_tail", 1)])
        )  # create an arbitrarily-ID'd group
        target_node_ = Group(context=context, id_=target_node)
    spy = Mock(spec=Context, wraps=context)
    pattern.play(context=spy, clock=clock, target_node=target_node_, until=until)
    expected_mock_calls = expected(context)
    assert spy.mock_calls == expected_mock_calls


def test_callback():
    def callback(player, context, event, priority):
        callback_calls.append(
            (player, context.desired_moment.offset, type(event), priority)
        )

    callback_calls = []
    pattern = EventPattern(frequency=SequencePattern([440, 550, 660]))
    clock = OfflineClock()
    player = pattern.play(context=Server().boot(), clock=clock, callback=callback)
    assert callback_calls == [
        (player, 0.0, StartEvent, Priority.START),
        (player, 0.0, NoteEvent, Priority.START),
        (player, 1.0, NoteEvent, Priority.START),
        (player, 1.0, NoteEvent, Priority.STOP),
        (player, 2.0, NoteEvent, Priority.START),
        (player, 2.0, NoteEvent, Priority.STOP),
        (player, 3.0, NoteEvent, Priority.STOP),
        (player, 3.0, StopEvent, Priority.STOP),
    ]


@pytest.mark.asyncio
async def test_callback_async(event_loop):
    def callback(player, context, event, priority):
        print("CALLBACK", player, context, event, priority)
        callback_calls.append(
            (player, context.desired_moment.offset, type(event), priority)
        )
        if isinstance(event, StopEvent):
            stop_future.set_result(True)

    stop_future = event_loop.create_future()
    callback_calls = []
    pattern = EventPattern(frequency=SequencePattern([440, 550, 660]))
    clock = AsyncOfflineClock()
    player = pattern.play(
        context=await AsyncServer().boot(), clock=clock, callback=callback
    )
    await clock.start()
    await stop_future
    await clock.stop()
    assert callback_calls == [
        (player, 0.0, StartEvent, Priority.START),
        (player, 0.0, NoteEvent, Priority.START),
        (player, 1.0, NoteEvent, Priority.START),
        (player, 1.0, NoteEvent, Priority.STOP),
        (player, 2.0, NoteEvent, Priority.START),
        (player, 2.0, NoteEvent, Priority.STOP),
        (player, 3.0, NoteEvent, Priority.STOP),
        (player, 3.0, StopEvent, Priority.STOP),
    ]


def test_nonrealtime():
    at = 1.0
    until = 1.5
    pattern = GroupPattern(
        BusPattern(MonoEventPattern(frequency=SequencePattern([440, 550, 660])))
    )
    clock = OfflineClock()
    context = Score()
    pattern.play(context=context, clock=clock, at=at, until=until)
    # Session should not map in_ or out, but use their bus numbers as consts.
    assert list(context.iterate_osc_bundles()) == [
        OscBundle(
            contents=(
                OscMessage("/g_new", 1000, 0, 0, 1001, 0, 1000),
                OscMessage(
                    "/s_new",
                    "system_link_audio_1",
                    1002,
                    3,
                    1001,
                    "fade_time",
                    0.25,
                    "in_",
                    16.0,
                ),
                OscMessage("/s_new", "default", 1003, 0, 1001, "out", 16.0),
            ),
            timestamp=1.0,
        ),
        OscBundle(
            contents=(OscMessage("/n_set", 1003, "frequency", 550.0, "out", 16.0),),
            timestamp=3.0,
        ),
        OscBundle(
            contents=(
                OscMessage("/n_set", 1003, "gate", 0.0),
                OscMessage("/n_set", 1002, "gate", 0.0),
            ),
            timestamp=4.0,
        ),
        OscBundle(
            contents=(
                OscMessage("/n_free", 1001),
                OscMessage("/n_free", 1000),
            ),
            timestamp=4.5,
        ),
    ]
