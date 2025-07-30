from typing import Callable

import pytest

from supriya.sessions import DeviceContainer, Session, SignalTesterDevice

from .conftest import run_test


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "commands, target, expected_components_diff, expected_tree_diff, expected_messages",
    [
        (
            [
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Track"}),
            ],
            "mixers[0]",
            """
            --- initial
            +++ mutation
            @@ -2,3 +2,4 @@
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
                         <Track 2 'Track'>
            +            <SignalTesterDevice 3>
            """,
            """
            --- initial
            +++ mutation
            @@ -15,6 +15,9 @@
                     1004 supriya:meters:2 (session.mixers[0]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (session.mixers[0]:devices)
            +            1014 group (session.mixers[0].devices[0]:group)
            +                1015 supriya:device-dc-tester:2 (session.mixers[0].devices[0]:synth)
            +                    active: 1.0, dc: 1.0, done_action: 2.0, gate: 1.0, out: 16.0
                     1003 supriya:channel-strip:2 (session.mixers[0]:channel-strip)
                         active: 1.0, done_action: 2.0, gain: c0, gate: 1.0, out: 16.0
                     1005 supriya:meters:2 (session.mixers[0]:output-levels)
            """,
            """
            - ['/d_recv', <SynthDef: supriya:device-dc-tester:2>]
            - ['/sync', 3]
            - [None, [['/g_new', 1014, 0, 1002], ['/s_new', 'supriya:device-dc-tester:2', 1015, 1, 1014, 'out', 16.0]]]
            """,
        ),
        (
            [
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Track"}),
            ],
            "mixers[0].tracks[0]",
            """
            --- initial
            +++ mutation
            @@ -2,3 +2,4 @@
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
                         <Track 2 'Track'>
            +                <SignalTesterDevice 3>
            """,
            """
            --- initial
            +++ mutation
            @@ -6,6 +6,9 @@
                             1011 supriya:meters:2 (session.mixers[0].tracks[0]:input-levels)
                                 in_: 18.0, out: 7.0
                             1009 group (session.mixers[0].tracks[0]:devices)
            +                    1014 group (session.mixers[0].tracks[0].devices[0]:group)
            +                        1015 supriya:device-dc-tester:2 (session.mixers[0].tracks[0].devices[0]:synth)
            +                            active: 1.0, dc: 1.0, done_action: 2.0, gate: 1.0, out: 18.0
                             1010 supriya:channel-strip:2 (session.mixers[0].tracks[0]:channel-strip)
                                 active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
                             1012 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
            """,
            """
            - ['/d_recv', <SynthDef: supriya:device-dc-tester:2>]
            - ['/sync', 3]
            - [None, [['/g_new', 1014, 0, 1009], ['/s_new', 'supriya:device-dc-tester:2', 1015, 1, 1014, 'out', 18.0]]]
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_Track_add_device(
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
        assert isinstance(target_, DeviceContainer)
        device = await target_.add_device(SignalTesterDevice)
    assert isinstance(device, SignalTesterDevice)
    assert device in target_.devices
    assert device.parent is target_
    assert target_.devices[0] is device
