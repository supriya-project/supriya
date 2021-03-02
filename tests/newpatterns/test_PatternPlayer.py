from unittest.mock import Mock, call

from supriya import AddAction
from supriya.assets.synthdefs import default
from supriya.clocks import OfflineTempoClock
from supriya.newpatterns import EventPattern, MonoEventPattern, SequencePattern
from supriya.provider import Provider, SynthProxy


def test_play():
    pattern = SequencePattern(
        [
            EventPattern(frequency=SequencePattern([440, 550, 660])),
            MonoEventPattern(frequency=SequencePattern([440, 550, 660])),
        ]
    )
    clock = OfflineTempoClock()
    provider = Provider.realtime()
    spy = Mock(spec=Provider, wraps=provider)
    pattern.play(provider=spy, clock=clock)
    assert spy.mock_calls == [
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
    ]
