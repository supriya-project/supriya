import pytest
from uqbar.strings import normalize

from supriya.mixers import Session
from supriya.mixers.devices import Device, DeviceContainer

from .conftest import assert_diff, capture, format_messages


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "target, expected_diff, expected_commands",
    [
        (
            "mixers[0]",
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
                         active: 1.0, bus: 16.0, gain: c0, gate: 1.0
                     1005 supriya:meters:2 (session.mixers[0]:output-levels)
            """,
            r"""
            - ['/d_recv',
               b'SCgf\x00\x00\x00\x02\x00\x01\x1asupriya:device-dc-tester:2\x00\x00\x00\x00\x00\x00\x00\x02?\x80\x00\x00\x00\x00\x00'
               b'\x00\x00\x00\x00\x02\x02dc\x00\x00\x00\x00\x03out\x00\x00\x00\x01\x00\x00\x00\x03\x07Control\x01\x00\x00\x00'
               b'\x00\x00\x00\x00\x02\x00\x00\x01\x01\x02DC\x02\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00'
               b'\x00\x00\x00\x02\x03Out\x02\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00'
               b'\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00']
            - ['/sync', 2]
            - [None, [['/g_new', 1066, 1, 1002], ['/s_new', 'supriya:device-dc-tester:2', 1067, 1, 1066, 'out', 16.0]]]
            """,
        ),
        (
            "mixers[0].tracks[0]",
            """
            --- initial
            +++ mutation
            @@ -41,6 +41,9 @@
                             1010 supriya:meters:2 (session.mixers[0].tracks[0]:input-levels)
                                 in_: 18.0, out: 7.0
                             1008 group (session.mixers[0].tracks[0]:devices)
            +                    1066 group (session.mixers[0].tracks[0].devices[0]:group)
            +                        1067 supriya:device-dc-tester:2 (session.mixers[0].tracks[0].devices[0]:synth)
            +                            dc: 1.0, out: 18.0
                             1009 supriya:channel-strip:2 (session.mixers[0].tracks[0]:channel-strip)
                                 active: c5, bus: 18.0, gain: c6, gate: 1.0
                             1051 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].sends[0]:synth)
            """,
            r"""
            - ['/d_recv',
               b'SCgf\x00\x00\x00\x02\x00\x01\x1asupriya:device-dc-tester:2\x00\x00\x00\x00\x00\x00\x00\x02?\x80\x00\x00\x00\x00\x00'
               b'\x00\x00\x00\x00\x02\x02dc\x00\x00\x00\x00\x03out\x00\x00\x00\x01\x00\x00\x00\x03\x07Control\x01\x00\x00\x00'
               b'\x00\x00\x00\x00\x02\x00\x00\x01\x01\x02DC\x02\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00'
               b'\x00\x00\x00\x02\x03Out\x02\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00'
               b'\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00']
            - ['/sync', 2]
            - [None, [['/g_new', 1066, 1, 1008], ['/s_new', 'supriya:device-dc-tester:2', 1067, 1, 1066, 'out', 18.0]]]
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_Track_add_device(
    complex_session: tuple[Session, str],
    expected_commands: str,
    expected_diff: str,
    online: bool,
    target: str,
) -> None:
    # Pre-conditions
    session, initial_tree = complex_session
    if online:
        await session.boot()
    target_ = session[target]
    assert isinstance(target_, DeviceContainer)
    # Operation
    with capture(session["mixers[0]"].context) as commands:
        device = await target_.add_device()
    # Post-conditions
    assert isinstance(device, Device)
    assert device in target_.devices
    assert device.parent is target_
    assert target_.devices[0] is device
    if not online:
        return
    await assert_diff(
        session,
        expected_diff,
        expected_initial_tree=initial_tree,
    )
    assert format_messages(commands) == normalize(expected_commands)
