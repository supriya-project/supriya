from unittest.mock import Mock, call

import pytest

from supriya import AddAction
from supriya.assets.synthdefs import default
from supriya.clocks import OfflineTempoClock
from supriya.newpatterns import (
    EventPattern,
    MonoEventPattern,
    ParallelPattern,
    SequencePattern,
)
from supriya.providers import Provider, SynthProxy


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
                call.at(1.0),
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
                call.at(2.0),
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
                call.at(3.0),
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
                call.at(4.0),
                call.set_node(
                    SynthProxy(
                        provider=provider,
                        identifier=1003,
                        synthdef=default,
                        settings={"frequency": 440},
                    ),
                    frequency=550,
                ),
                call.at(5.0),
                call.set_node(
                    SynthProxy(
                        provider=provider,
                        identifier=1003,
                        synthdef=default,
                        settings={"frequency": 440},
                    ),
                    frequency=660,
                ),
                call.at(6.0),
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
                call.at(1.0),
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
                call.at(1.5),
                call.free_node(
                    SynthProxy(
                        provider=provider,
                        identifier=1001,
                        synthdef=default,
                        settings={"frequency": 550},
                    )
                ),
                call.at(1.5),  # 1001 was freed early, nothing to do.
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
                call.at(1.0),
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
                call.at(2.0),
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
    ],
)
def test(pattern, until, expected):
    clock = OfflineTempoClock()
    provider = Provider.realtime()
    spy = Mock(spec=Provider, wraps=provider)
    pattern.play(provider=spy, clock=clock, until=until)
    expected_mock_calls = expected(provider)
    assert spy.mock_calls == expected_mock_calls
