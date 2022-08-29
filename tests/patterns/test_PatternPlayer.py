from unittest.mock import Mock, call

import pytest
from uqbar.strings import normalize

from supriya import AddAction, CalculationRate
from supriya.assets.synthdefs import default, system_link_audio_1
from supriya.clocks import AsyncOfflineClock, OfflineClock
from supriya.patterns import (
    BusPattern,
    EventPattern,
    GroupPattern,
    MonoEventPattern,
    ParallelPattern,
    SequencePattern,
)
from supriya.patterns.events import NoteEvent, Priority, StartEvent, StopEvent
from supriya.providers import BusGroupProxy, GroupProxy, Provider, SynthProxy


@pytest.mark.parametrize(
    "pattern, until, expected",
    [
        (
            SequencePattern(
                [
                    EventPattern(frequency=SequencePattern([440, 550, 660])),
                    MonoEventPattern(frequency=SequencePattern([440, 550, 660])),
                ]
            ),
            None,
            lambda provider: [
                call.at(0.0),
                call.add_synth(
                    add_action=AddAction.ADD_TO_HEAD,
                    synthdef=None,
                    target_node=None,
                    frequency=440,
                ),
                call.at(2.0),
                call.add_synth(
                    add_action=AddAction.ADD_TO_HEAD,
                    synthdef=None,
                    target_node=None,
                    frequency=550,
                ),
                call.free_node(
                    SynthProxy(
                        provider=provider,
                        identifier=1000,
                        synthdef=default,
                        settings={"frequency": 440},
                    )
                ),
                call.at(4.0),
                call.add_synth(
                    add_action=AddAction.ADD_TO_HEAD,
                    synthdef=None,
                    target_node=None,
                    frequency=660,
                ),
                call.free_node(
                    SynthProxy(
                        provider=provider,
                        identifier=1001,
                        synthdef=default,
                        settings={"frequency": 550},
                    )
                ),
                call.at(6.0),
                call.add_synth(
                    add_action=AddAction.ADD_TO_HEAD,
                    synthdef=None,
                    target_node=None,
                    frequency=440,
                ),
                call.free_node(
                    SynthProxy(
                        provider=provider,
                        identifier=1002,
                        synthdef=default,
                        settings={"frequency": 660},
                    )
                ),
                call.at(8.0),
                call.set_node(
                    SynthProxy(
                        provider=provider,
                        identifier=1003,
                        synthdef=default,
                        settings={"frequency": 440},
                    ),
                    frequency=550,
                ),
                call.at(10.0),
                call.set_node(
                    SynthProxy(
                        provider=provider,
                        identifier=1003,
                        synthdef=default,
                        settings={"frequency": 440},
                    ),
                    frequency=660,
                ),
                call.at(12.0),
                call.free_node(
                    SynthProxy(
                        provider=provider,
                        identifier=1003,
                        synthdef=default,
                        settings={"frequency": 440},
                    )
                ),
            ],
        ),
        (
            EventPattern(frequency=SequencePattern([440, 550, 660])),
            1.5,
            lambda provider: [
                call.at(0.0),
                call.add_synth(
                    add_action=AddAction.ADD_TO_HEAD,
                    synthdef=None,
                    target_node=None,
                    frequency=440,
                ),
                call.at(2.0),
                call.add_synth(
                    add_action=AddAction.ADD_TO_HEAD,
                    synthdef=None,
                    target_node=None,
                    frequency=550,
                ),
                call.free_node(
                    SynthProxy(
                        provider=provider,
                        identifier=1000,
                        synthdef=default,
                        settings={"frequency": 440},
                    )
                ),
                call.at(3.0),
                call.free_node(
                    SynthProxy(
                        provider=provider,
                        identifier=1001,
                        synthdef=default,
                        settings={"frequency": 550},
                    )
                ),
                call.at(3.0),  # 1001 was freed early, nothing to do.
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
            lambda provider: [
                call.at(0.0),
                call.add_synth(
                    add_action=AddAction.ADD_TO_HEAD,
                    synthdef=None,
                    target_node=None,
                    frequency=440,
                ),
                call.add_synth(
                    add_action=AddAction.ADD_TO_HEAD,
                    synthdef=None,
                    target_node=None,
                    frequency=777,
                ),
                call.at(2.0),
                call.add_synth(
                    add_action=AddAction.ADD_TO_HEAD,
                    synthdef=None,
                    target_node=None,
                    frequency=550,
                ),
                call.add_synth(
                    add_action=AddAction.ADD_TO_HEAD,
                    synthdef=None,
                    target_node=None,
                    frequency=888,
                ),
                call.free_node(
                    SynthProxy(
                        provider=provider,
                        identifier=1000,
                        synthdef=default,
                        settings={"frequency": 440},
                    )
                ),
                call.free_node(
                    SynthProxy(
                        provider=provider,
                        identifier=1001,
                        synthdef=default,
                        settings={"frequency": 777},
                    )
                ),
                call.at(4.0),
                call.free_node(
                    SynthProxy(
                        provider=provider,
                        identifier=1002,
                        synthdef=default,
                        settings={"frequency": 550},
                    )
                ),
                call.free_node(
                    SynthProxy(
                        provider=provider,
                        identifier=1003,
                        synthdef=default,
                        settings={"frequency": 888},
                    )
                ),
            ],
        ),
        (
            GroupPattern(
                BusPattern(MonoEventPattern(frequency=SequencePattern([440, 550, 660])))
            ),
            1.5,
            lambda provider: [
                call.at(0.0),
                call.add_group(add_action=AddAction.ADD_TO_HEAD, target_node=None),
                call.add_bus_group(
                    calculation_rate=CalculationRate.AUDIO, channel_count=1
                ),
                call.add_group(
                    add_action=AddAction.ADD_TO_HEAD,
                    target_node=GroupProxy(provider=provider, identifier=1000),
                ),
                call.add_synth(
                    add_action=AddAction.ADD_AFTER,
                    synthdef=system_link_audio_1,
                    target_node=GroupProxy(provider=provider, identifier=1001),
                    amplitude=1.0,
                    fade_time=0.25,
                    in_=BusGroupProxy(
                        provider=provider,
                        calculation_rate=CalculationRate.AUDIO,
                        channel_count=1,
                        identifier=16,
                    ),
                ),
                call.add_synth(
                    add_action=AddAction.ADD_TO_HEAD,
                    synthdef=None,
                    target_node=GroupProxy(provider=provider, identifier=1001),
                    frequency=440,
                    out=BusGroupProxy(
                        provider=provider,
                        calculation_rate=CalculationRate.AUDIO,
                        channel_count=1,
                        identifier=16,
                    ),
                ),
                call.at(2.0),
                call.set_node(
                    SynthProxy(
                        provider=provider,
                        identifier=1003,
                        synthdef=default,
                        settings={
                            "frequency": 440,
                            "out": BusGroupProxy(
                                provider=provider,
                                calculation_rate=CalculationRate.AUDIO,
                                channel_count=1,
                                identifier=16,
                            ),
                        },
                    ),
                    frequency=550,
                    out=BusGroupProxy(
                        provider=provider,
                        calculation_rate=CalculationRate.AUDIO,
                        channel_count=1,
                        identifier=16,
                    ),
                ),
                call.at(3.0),
                call.free_node(
                    SynthProxy(
                        provider=provider,
                        identifier=1003,
                        synthdef=default,
                        settings={
                            "frequency": 440,
                            "out": BusGroupProxy(
                                provider=provider,
                                calculation_rate=CalculationRate.AUDIO,
                                channel_count=1,
                                identifier=16,
                            ),
                        },
                    )
                ),
                call.at(3.0),  # Can we coalesce these moments?
                call.free_node(
                    SynthProxy(
                        provider=provider,
                        identifier=1002,
                        synthdef=system_link_audio_1,
                        settings={
                            "amplitude": 1.0,
                            "fade_time": 0.25,
                            "in_": BusGroupProxy(
                                provider=provider,
                                calculation_rate=CalculationRate.AUDIO,
                                channel_count=1,
                                identifier=16,
                            ),
                        },
                    )
                ),
                call.at(3.5),
                call.free_node(GroupProxy(provider=provider, identifier=1001)),
                call.free_bus_group(
                    BusGroupProxy(
                        provider=provider,
                        calculation_rate=CalculationRate.AUDIO,
                        channel_count=1,
                        identifier=16,
                    )
                ),
                call.free_node(GroupProxy(provider=provider, identifier=1000)),
            ],
        ),
    ],
)
def test_provider_calls(pattern, until, expected):
    clock = OfflineClock()
    provider = Provider.realtime()
    spy = Mock(spec=Provider, wraps=provider)
    pattern.play(provider=spy, clock=clock, until=until)
    expected_mock_calls = expected(provider)
    assert spy.mock_calls == expected_mock_calls


def test_callback():
    def callback(player, context, event, priority):
        callback_calls.append(
            (player, context.desired_moment.offset, type(event), priority)
        )

    callback_calls = []
    pattern = EventPattern(frequency=SequencePattern([440, 550, 660]))
    clock = OfflineClock()
    player = pattern.play(provider=Provider.realtime(), clock=clock, callback=callback)
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
    async def callback(player, context, event, priority):
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
        provider=await Provider.realtime_async(), clock=clock, callback=callback
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
    provider = Provider.nonrealtime()
    pattern.play(provider=provider, clock=clock, at=at, until=until)
    # Session should not map in_ or out, but use their bus numbers as consts.
    assert provider.session.to_strings(True) == normalize(
        """
        0.0:
            NODE TREE 0 group
        1.0:
            NODE TREE 0 group
                1000 group
                    1001 group
                        1003 default
                            amplitude: 0.1, frequency: 440.0, gate: 1.0, out: 16.0, pan: 0.5
                    1002 system_link_audio_1
                        done_action: 2.0, fade_time: 0.25, gate: 1.0, in_: 16.0, out: 0.0
        3.0:
            NODE TREE 0 group
                1000 group
                    1001 group
                        1003 default
                            amplitude: 0.1, frequency: 550.0, gate: 1.0, out: 16.0, pan: 0.5
                    1002 system_link_audio_1
                        done_action: 2.0, fade_time: 0.25, gate: 1.0, in_: 16.0, out: 0.0
        4.0:
            NODE TREE 0 group
                1000 group
                    1001 group
        4.5:
            NODE TREE 0 group
        """
    )
