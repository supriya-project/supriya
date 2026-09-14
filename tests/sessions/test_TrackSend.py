import dataclasses

import pytest

from supriya.sessions import SynthConfig, TrackSend
from supriya.ugens.system import build_dc_synthdef

from .conftest import Scenario


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "scenario",
    [
        Scenario(
            id="send to younger sibling",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Track One"}),
                ("mixers[0]", "add_track", {"name": "Track Two"}),
                (
                    "mixers[0].tracks[0]",
                    "add_send",
                    {"name": "Self", "target": "mixers[0].tracks[1]"},
                ),
            ],
            subject="mixers[0].tracks[0].sends[0]",
            expected_components_diff="""
            --- initial
            +++ mutation
            @@ -2,5 +2,4 @@
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
                         <Track 2 'Track One'>
            -                <TrackSend 4 'Self' postfader target=<Track 3 'Track Two'>>
                         <Track 3 'Track Two'>
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -9,7 +9,7 @@
                             1010 supriya:channel-strip:2 (session.mixers[0].tracks[0]:channel-strip)
                                 active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
                             1014 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].sends[0]:synth)
            -                    active: c5, done_action: 2.0, gain: c11, gate: 1.0, in_: 18.0, out: 20.0
            +                    active: c5, done_action: 2.0, gain: c11, gate: 0.0, in_: 18.0, out: 20.0
                             1012 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
                                 in_: 18.0, out: 9.0
                             1013 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:output)
            """,
            expected_messages="""
            - ['/n_set', 1014, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        Scenario(
            id="send to older sibling",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Track One"}),
                ("mixers[0]", "add_track", {"name": "Track Two"}),
                (
                    "mixers[0].tracks[1]",
                    "add_send",
                    {"name": "Self", "target": "mixers[0].tracks[0]"},
                ),
            ],
            subject="mixers[0].tracks[1].sends[0]",
            expected_components_diff="""
            --- initial
            +++ mutation
            @@ -3,4 +3,3 @@
                     <Mixer 1 'Mixer'>
                         <Track 2 'Track One'>
                         <Track 3 'Track Two'>
            -                <TrackSend 4 'Self' postfader target=<Track 2 'Track One'>>
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -3,7 +3,7 @@
                     1001 group (session.mixers[0]:tracks)
                         1007 group (session.mixers[0].tracks[0]:group)
                             1014 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0]:feedback)
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 20.0
                             1008 group (session.mixers[0].tracks[0]:tracks)
                             1011 supriya:meters:2 (session.mixers[0].tracks[0]:input-levels)
                                 in_: 20.0, out: 7.0
            @@ -22,7 +22,7 @@
                             1018 supriya:channel-strip:2 (session.mixers[0].tracks[1]:channel-strip)
                                 active: c11, done_action: 2.0, gain: c12, gate: 1.0, out: 22.0
                             1022 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].sends[0]:synth)
            -                    active: c11, done_action: 2.0, gain: c17, gate: 1.0, in_: 22.0, out: 18.0
            +                    active: c11, done_action: 2.0, gain: c17, gate: 0.0, in_: 22.0, out: 18.0
                             1020 supriya:meters:2 (session.mixers[0].tracks[1]:output-levels)
                                 in_: 22.0, out: 15.0
                             1021 supriya:patch-cable:2x2 (session.mixers[0].tracks[1]:output)
            """,
            expected_messages="""
            - ['/n_set', 1022, 'done_action', 2.0, 'gate', 0.0]
            - ['/n_set', 1014, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
    ],
    ids=lambda scenario: scenario.id,
)
@pytest.mark.asyncio
async def test_TrackSend_delete(
    scenario: Scenario,
    online: bool,
) -> None:
    async with scenario.run(online=online) as session:
        subject = session[scenario.subject]
        assert isinstance(subject, TrackSend)
        parent = subject.parent
        await subject.delete()
    # Post-conditions
    assert parent
    assert subject not in parent.sends
    assert subject.address == "sends[?]"
    assert subject.context is None
    assert subject.parent is None
    assert subject.mixer is None
    assert subject.session is None


@dataclasses.dataclass(frozen=True)
class GainScenario(Scenario):
    gain: float


@pytest.mark.parametrize(
    "scenario",
    [
        GainScenario(
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Track One"}),
                ("mixers[0]", "add_track", {"name": "Track Two"}),
                (
                    "mixers[0].tracks[0]",
                    "add_device",
                    {
                        "name": "Device",
                        "synth_configs": [SynthConfig(synthdef=build_dc_synthdef)],
                    },
                ),
                ("mixers[0].tracks[0]", "add_send", {"target": "mixers[0].tracks[1]"}),
            ],
            subject="mixers[0].tracks[0].sends[0]",
            gain=-6,
            expected_levels=[
                ("Mixer", [1.5, 1.5], [1.5, 1.5]),
                ("Track One", [0.0, 0.0], [1.0, 1.0]),
                ("Device", [0.0, 0.0], [1.0, 1.0]),
                ("Track Two", [0.5, 0.5], [0.5, 0.5]),
            ],
        ),
        GainScenario(
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Track One"}),
                ("mixers[0]", "add_track", {"name": "Track Two"}),
                (
                    "mixers[0].tracks[1]",
                    "add_device",
                    {
                        "name": "Device",
                        "synth_configs": [SynthConfig(synthdef=build_dc_synthdef)],
                    },
                ),
                ("mixers[0].tracks[1]", "add_send", {"target": "mixers[0].tracks[0]"}),
            ],
            subject="mixers[0].tracks[1].sends[0]",
            gain=-6,
            expected_levels=[
                ("Mixer", [1.5, 1.5], [1.5, 1.5]),
                ("Track One", [0.5, 0.5], [0.5, 0.5]),
                ("Track Two", [0.0, 0.0], [1.0, 1.0]),
                ("Device", [0.0, 0.0], [1.0, 1.0]),
            ],
        ),
    ],
)
@pytest.mark.asyncio
async def test_TrackSend_gain(
    scenario: GainScenario,
) -> None:
    async with scenario.run(online=True) as session:
        subject = session[scenario.subject]
        assert isinstance(subject, TrackSend)
        subject.parameters["gain"].set(scenario.gain)
