import asyncio
from typing import Callable

import pytest

from supriya.sessions import (
    Component,
    Mixer,
    Session,
    SignalTesterDevice,
    Track,
    TrackSend,
)
from supriya.ugens import system  # lookup system.LAG_TIME to support monkeypatching

from .conftest import run_test


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "commands, target, expected_components_diff, expected_tree_diff, expected_messages",
    [
        (
            [
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Track One"}),
                ("mixers[0]", "add_track", {"name": "Track Two"}),
                (
                    "mixers[0].tracks[0]",
                    "add_send",
                    {"name": "Self", "target": "mixers[0].tracks[1]"},
                ),
            ],
            "mixers[0].tracks[0].sends[0]",
            """
            --- initial
            +++ mutation
            @@ -2,5 +2,4 @@
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
                         <Track 2 'Track One'>
            -                <TrackSend 4 'Self' postfader target=<Track 3 'Track Two'>>
                         <Track 3 'Track Two'>
            """,
            """
            --- initial
            +++ mutation
            @@ -8,8 +8,8 @@
                             1009 group (session.mixers[0].tracks[0]:devices)
                             1010 supriya:channel-strip:2 (session.mixers[0].tracks[0]:channel-strip)
                                 active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
            -                1014 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].sends[0]:synth)
            -                    active: c5, done_action: 2.0, gain: c11, gate: 1.0, in_: 18.0, out: 20.0
            +                1014 supriya:patch-cable:2x2
            +                    active: c5, done_action: 2.0, gain: c11, gate: 0.0, in_: 18.0, out: 20.0
                             1012 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
                                 in_: 18.0, out: 9.0
                             1013 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:output)
            """,
            """
            - ['/n_set', 1014, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        (
            [
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Track One"}),
                ("mixers[0]", "add_track", {"name": "Track Two"}),
                (
                    "mixers[0].tracks[1]",
                    "add_send",
                    {"name": "Self", "target": "mixers[0].tracks[0]"},
                ),
            ],
            "mixers[0].tracks[1].sends[0]",
            """
            --- initial
            +++ mutation
            @@ -3,4 +3,3 @@
                     <Mixer 1 'Mixer'>
                         <Track 2 'Track One'>
                         <Track 3 'Track Two'>
            -                <TrackSend 4 'Self' postfader target=<Track 2 'Track One'>>
            """,
            """
            --- initial
            +++ mutation
            @@ -2,8 +2,8 @@
                 NODE TREE 1000 group (session.mixers[0]:group)
                     1001 group (session.mixers[0]:tracks)
                         1007 group (session.mixers[0].tracks[0]:group)
            -                1014 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0]:feedback)
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            +                1014 supriya:fb-patch-cable:2x2
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 20.0
                             1008 group (session.mixers[0].tracks[0]:tracks)
                             1011 supriya:meters:2 (session.mixers[0].tracks[0]:input-levels)
                                 in_: 20.0, out: 7.0
            @@ -21,8 +21,8 @@
                             1017 group (session.mixers[0].tracks[1]:devices)
                             1018 supriya:channel-strip:2 (session.mixers[0].tracks[1]:channel-strip)
                                 active: c11, done_action: 2.0, gain: c12, gate: 1.0, out: 22.0
            -                1022 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].sends[0]:synth)
            -                    active: c11, done_action: 2.0, gain: c17, gate: 1.0, in_: 22.0, out: 18.0
            +                1022 supriya:patch-cable:2x2
            +                    active: c11, done_action: 2.0, gain: c17, gate: 0.0, in_: 22.0, out: 18.0
                             1020 supriya:meters:2 (session.mixers[0].tracks[1]:output-levels)
                                 in_: 22.0, out: 15.0
                             1021 supriya:patch-cable:2x2 (session.mixers[0].tracks[1]:output)
            """,
            """
            - ['/n_set', 1022, 'done_action', 2.0, 'gate', 0.0]
            - ['/n_set', 1014, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_TrackSend_delete(
    commands: list[tuple[str | None, str, dict | None]],
    expected_components_diff: Callable[[Session], str] | str,
    expected_messages: str,
    expected_tree_diff: str,
    online: bool,
    target: str,
) -> None:
    async with run_test(
        commands=commands,
        expected_components_diff=expected_components_diff,
        expected_messages=expected_messages,
        expected_tree_diff=expected_tree_diff,
        online=online,
    ) as session:
        target_ = session[target]
        assert isinstance(target_, TrackSend)
        parent = target_.parent
        await target_.delete()
    # Post-conditions
    assert parent
    assert target_ not in parent.sends
    assert target_.address == "sends[?]"
    assert target_.context is None
    assert target_.parent is None
    assert target_.mixer is None
    assert target_.session is None


@pytest.mark.parametrize(
    "commands, target, gain, expected_levels",
    [
        (
            [
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Track One"}),
                ("mixers[0]", "add_track", {"name": "Track Two"}),
                (
                    "mixers[0].tracks[0]",
                    "add_device",
                    {"device_class": SignalTesterDevice},
                ),
                ("mixers[0].tracks[0]", "add_send", {"target": "mixers[0].tracks[1]"}),
            ],
            "mixers[0].tracks[0].sends[0]",
            -6,
            [
                ("Mixer", [1.5, 1.5], [1.5, 1.5]),
                ("Track One", [0.0, 0.0], [1.0, 1.0]),
                ("Track Two", [0.5, 0.5], [0.5, 0.5]),
            ],
        ),
        (
            [
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Track One"}),
                ("mixers[0]", "add_track", {"name": "Track Two"}),
                (
                    "mixers[0].tracks[1]",
                    "add_device",
                    {"device_class": SignalTesterDevice},
                ),
                ("mixers[0].tracks[1]", "add_send", {"target": "mixers[0].tracks[0]"}),
            ],
            "mixers[0].tracks[1].sends[0]",
            -6,
            [
                ("Mixer", [1.5, 1.5], [1.5, 1.5]),
                ("Track One", [0.5, 0.5], [0.5, 0.5]),
                ("Track Two", [0.0, 0.0], [1.0, 1.0]),
            ],
        ),
    ],
)
@pytest.mark.asyncio
async def test_TrackSend_gain(
    commands: list[tuple[str | None, str, dict | None]],
    expected_levels: list[tuple[str, list[float], list[float]]],
    gain: float,
    target: str,
) -> None:
    async with run_test(
        annotation=None,
        commands=commands,
        online=True,
    ) as session:
        target_ = session[target]
        assert isinstance(target_, TrackSend)
        target_.parameters["gain"].set(gain)
    await asyncio.sleep(system.LAG_TIME * 2)
    actual_levels = [
        (
            component.name,
            [round(x, 2) for x in component.input_levels],
            [round(x, 2) for x in component.output_levels],
        )
        for component in session.walk(Component)
        if isinstance(component, (Mixer, Track))
    ]
    assert actual_levels == expected_levels
