import pytest
from uqbar.strings import normalize

from supriya.mixers import Session
from supriya.mixers.devices import Device, DeviceContainer

from .conftest import assert_components_diff, assert_tree_diff, capture, format_messages


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "target, expected_components_diff, expected_tree_diff, expected_messages",
    [
        (
            "mixers[0]",
            """
            --- initial
            +++ mutation
            @@ -9,5 +9,6 @@
                         <Track 4 'B' session.mixers[0].tracks[1]>
                             <TrackSend 11 session.mixers[0].tracks[1].sends[0] target=session.mixers[0].tracks[0].tracks[0]>
                         <Track 5 'C' session.mixers[0].tracks[2]>
            +            <Device 12 session.mixers[0].devices[0]>
                     <Mixer 2 'Q' session.mixers[1]>
                         <Track 9 'D' session.mixers[1].tracks[0]>
            """,
            """
            --- initial
            +++ mutation
            @@ -76,6 +76,9 @@
                     1004 supriya:meters:2 (session.mixers[0]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (session.mixers[0]:devices)
            +            1066 group (session.mixers[0].devices[0]:group)
            +                1067 supriya:device-dc-tester:2 (session.mixers[0].devices[0]:synth)
            +                    dc: 1.0, out: 16.0
                     1003 supriya:channel-strip:2 (session.mixers[0]:channel-strip)
                         active: 1.0, done_action: 2.0, gain: c0, gate: 1.0, out: 16.0
                     1005 supriya:meters:2 (session.mixers[0]:output-levels)
            """,
            r"""
            - ['/d_recv', <SynthDef: supriya:device-dc-tester:2>]
            - ['/sync', 2]
            - [None, [['/g_new', 1066, 1, 1002], ['/s_new', 'supriya:device-dc-tester:2', 1067, 1, 1066, 'out', 16.0]]]
            """,
        ),
        (
            "mixers[0].tracks[0]",
            """
            --- initial
            +++ mutation
            @@ -5,6 +5,7 @@
                             <Track 6 'A1' session.mixers[0].tracks[0].tracks[0]>
                                 <Track 8 'A11' session.mixers[0].tracks[0].tracks[0].tracks[0]>
                             <Track 7 'A2' session.mixers[0].tracks[0].tracks[1]>
            +                <Device 12 session.mixers[0].tracks[0].devices[0]>
                             <TrackSend 10 session.mixers[0].tracks[0].sends[0] target=session.mixers[0].tracks[1]>
                         <Track 4 'B' session.mixers[0].tracks[1]>
                             <TrackSend 11 session.mixers[0].tracks[1].sends[0] target=session.mixers[0].tracks[0].tracks[0]>
            """,
            """
            --- initial
            +++ mutation
            @@ -41,6 +41,9 @@
                             1011 supriya:meters:2 (session.mixers[0].tracks[0]:input-levels)
                                 in_: 18.0, out: 7.0
                             1009 group (session.mixers[0].tracks[0]:devices)
            +                    1066 group (session.mixers[0].tracks[0].devices[0]:group)
            +                        1067 supriya:device-dc-tester:2 (session.mixers[0].tracks[0].devices[0]:synth)
            +                            dc: 1.0, out: 18.0
                             1010 supriya:channel-strip:2 (session.mixers[0].tracks[0]:channel-strip)
                                 active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
                             1036 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].sends[0]:synth)
            """,
            r"""
            - ['/d_recv', <SynthDef: supriya:device-dc-tester:2>]
            - ['/sync', 2]
            - [None, [['/g_new', 1066, 1, 1009], ['/s_new', 'supriya:device-dc-tester:2', 1067, 1, 1066, 'out', 18.0]]]
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_Track_add_device(
    complex_session: tuple[Session, str, str],
    expected_components_diff: str,
    expected_messages: str,
    expected_tree_diff: str,
    online: bool,
    target: str,
) -> None:
    # Pre-conditions
    session, initial_components, initial_tree = complex_session
    if online:
        await session.boot()
    target_ = session[target]
    assert isinstance(target_, DeviceContainer)
    # Operation
    with capture(session["mixers[0]"].context) as messages:
        device = await target_.add_device()
    # Post-conditions
    assert isinstance(device, Device)
    assert device in target_.devices
    assert device.parent is target_
    assert target_.devices[0] is device
    assert_components_diff(session, expected_components_diff, initial_components)
    if not online:
        return
    await assert_tree_diff(
        session,
        expected_tree_diff,
        expected_initial_tree=initial_tree,
    )
    assert format_messages(messages) == normalize(expected_messages)
