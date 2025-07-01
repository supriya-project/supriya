import asyncio
from typing import Type
from unittest.mock import Mock, call

import pytest
from pytest_mock import MockerFixture
from uqbar.strings import normalize

from supriya import (
    AddAction,
    AsyncServer,
    BusGroup,
    CalculationRate,
    Context,
    Group,
    Score,
    Server,
    Synth,
)
from supriya.clocks import AsyncOfflineClock, OfflineClock
from supriya.contexts.requests import NewGroup
from supriya.osc.utils import format_messages
from supriya.patterns import (
    BusPattern,
    Event,
    EventPattern,
    GroupPattern,
    MonoEventPattern,
    ParallelPattern,
    Pattern,
    PatternPlayer,
    SequencePattern,
)
from supriya.patterns.events import NoteEvent, Priority, StartEvent, StopEvent
from supriya.ugens.system import default, system_link_audio_1


@pytest.mark.parametrize(
    "pattern, until, target_node, expected",
    [
        (
            SequencePattern[Event](
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
                    permanent=False,
                    synthdef=default,
                    target_node=None,
                    frequency=440,
                ),
                call.at(2.0),
                call.add_synth(
                    add_action=AddAction.ADD_TO_HEAD,
                    permanent=False,
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
                    permanent=False,
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
                    permanent=False,
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
                    permanent=False,
                    synthdef=default,
                    target_node=None,
                    frequency=440,
                ),
                call.at(2.0),
                call.add_synth(
                    add_action=AddAction.ADD_TO_HEAD,
                    permanent=False,
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
                    permanent=False,
                    synthdef=default,
                    target_node=Group(context=context, id_=6666),
                    frequency=440,
                ),
                call.at(2.0),
                call.add_synth(
                    add_action=AddAction.ADD_TO_HEAD,
                    permanent=False,
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
                    permanent=False,
                    synthdef=default,
                    target_node=Group(context=context, id_=1000),
                    frequency=440,
                ),
                call.at(2.0),
                call.add_synth(
                    add_action=AddAction.ADD_TO_HEAD,
                    permanent=False,
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
                    permanent=False,
                    synthdef=default,
                    target_node=None,
                    frequency=440,
                ),
                call.add_synth(
                    add_action=AddAction.ADD_TO_HEAD,
                    permanent=False,
                    synthdef=default,
                    target_node=None,
                    frequency=777,
                ),
                call.at(2.0),
                call.add_synth(
                    add_action=AddAction.ADD_TO_HEAD,
                    permanent=False,
                    synthdef=default,
                    target_node=None,
                    frequency=550,
                ),
                call.add_synth(
                    add_action=AddAction.ADD_TO_HEAD,
                    permanent=False,
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
                    permanent=False,
                    synthdef=system_link_audio_1,
                    target_node=Group(context=context, id_=1001),
                    amplitude=1.0,
                    fade_time=0.25,
                    in_=16.0,
                ),
                call.add_synth(
                    add_action=AddAction.ADD_TO_HEAD,
                    permanent=False,
                    synthdef=default,
                    target_node=Group(context=context, id_=1001),
                    frequency=440,
                    out=16.0,
                ),
                call.at(2.0),
                call.set_node(
                    Synth(
                        context=context,
                        id_=1003,
                        synthdef=default,
                    ),
                    frequency=550,
                    out=16.0,
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
    pattern,
    until: float | None,
    target_node: int | None,
    expected,
    mocker: MockerFixture,
) -> None:
    clock = OfflineClock()
    context = Server().boot()
    target_node_ = None
    if target_node is not None:
        context.send(
            NewGroup(items=[(target_node, "add_to_tail", 1)])
        )  # create an arbitrarily-ID'd group
        target_node_ = Group(context=context, id_=target_node)
    spy = Mock(spec=Context, wraps=context)
    mocker.patch.object(context, "send")
    with clock.at():
        pattern.play(context=spy, clock=clock, target_node=target_node_, until=until)
    expected_mock_calls = expected(context)
    assert spy.mock_calls == expected_mock_calls


def test_callback(mocker: MockerFixture) -> None:
    def callback(player, context, event, priority):
        callback_calls.append(
            (player, context.desired_moment.offset, type(event), priority)
        )

    callback_calls: list[tuple[PatternPlayer, float, Type[Event], Priority]] = []
    pattern = EventPattern(frequency=SequencePattern([440, 550, 660]))
    context = Server().boot()
    mocker.patch.object(context, "send")
    with OfflineClock().at() as clock:
        player = pattern.play(context=context, clock=clock, callback=callback)
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
async def test_callback_async(mocker) -> None:
    def callback(player, context, event, priority):
        print("CALLBACK", player, context, event, priority)
        callback_calls.append(
            (player, context.desired_moment.offset, type(event), priority)
        )
        if isinstance(event, StopEvent):
            stop_future.set_result(True)

    event_loop = asyncio.get_running_loop()
    stop_future = event_loop.create_future()
    callback_calls: list[tuple[PatternPlayer, float, Type[Event], Priority]] = []
    pattern = EventPattern(frequency=SequencePattern([440, 550, 660]))
    context = await AsyncServer().boot()
    mocker.patch.object(context, "send")
    async with AsyncOfflineClock().at() as clock:
        player = pattern.play(context=context, clock=clock, callback=callback)
    await stop_future
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


@pytest.mark.parametrize(
    "pattern, at, until, expected",
    [
        (
            EventPattern(
                frequency=SequencePattern([444, 555, 666, 777]),
                rest=SequencePattern([False, True, False, False]),
            ),
            1.0,
            3.5,
            """
            - [1.0, [['/s_new', 'supriya:default', 1000, 0, 0, 'frequency', 444.0]]]
            - [3.0, [['/n_set', 1000, 'gate', 0.0]]]
            - [5.0, [['/s_new', 'supriya:default', 1001, 0, 0, 'frequency', 666.0]]]
            - [7.0, [['/s_new', 'supriya:default', 1002, 0, 0, 'frequency', 777.0], ['/n_set', 1001, 'gate', 0.0]]]
            - [8.0, [['/n_set', 1002, 'gate', 0.0]]]
            """,
        ),
        (
            MonoEventPattern(
                frequency=SequencePattern([444, 555, 666, 777]),
                rest=SequencePattern([False, False, True, False]),
            ),
            1.0,
            3.5,
            """
            - [1.0, [['/s_new', 'supriya:default', 1000, 0, 0, 'frequency', 444.0]]]
            - [3.0, [['/n_set', 1000, 'frequency', 555.0]]]
            - [5.0, [['/n_set', 1000, 'gate', 0.0]]]
            - [7.0, [['/s_new', 'supriya:default', 1001, 0, 0, 'frequency', 777.0]]]
            - [8.0, [['/n_set', 1001, 'gate', 0.0]]]
            """,
        ),
        (
            GroupPattern(
                BusPattern(
                    MonoEventPattern(
                        frequency=SequencePattern([444, 555, 666, 777]),
                        rest=SequencePattern([False, False, True, False]),
                    )
                )
            ),
            1.0,
            3.5,
            """
            - [1.0,
               [['/g_new', 1000, 0, 0, 1001, 0, 1000],
                ['/s_new', 'supriya:link-ar:1', 1002, 3, 1001, 'fade_time', 0.25],
                ['/s_new', 'supriya:default', 1003, 0, 1001, 'frequency', 444.0, 'out', 16.0]]]
            - [3.0, [['/n_set', 1003, 'frequency', 555.0, 'out', 16.0]]]
            - [5.0, [['/n_set', 1003, 'gate', 0.0]]]
            - [7.0, [['/s_new', 'supriya:default', 1004, 0, 1001, 'frequency', 777.0, 'out', 16.0]]]
            - [8.0, [['/n_set', 1004, 'gate', 0.0], ['/n_set', 1002, 'gate', 0.0]]]
            - [8.5, [['/n_free', 1001], ['/n_free', 1000]]]
            """,
        ),
    ],
)
def test_nonrealtime(pattern: Pattern, at: float, until: float, expected: str) -> None:
    context = Score()
    with OfflineClock().at(initial_time=at) as clock:
        pattern.play(context=context, clock=clock, until=until)
    assert format_messages(list(context.iterate_osc_bundles())) == normalize(expected)
