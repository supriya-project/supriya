from typing import Callable

import pytest

from supriya.sessions import Device, DeviceContainer, Session, SignalTesterDevice

from .conftest import does_not_raise, run_test


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "commands, target, expected_components_diff, expected_tree_diff, expected_messages",
    [
        (
            [
                (None, "add_mixer", {"name": "Mixer"}),
                (
                    "mixers[0]",
                    "add_device",
                    {"device_class": SignalTesterDevice, "name": "Self"},
                ),
            ],
            "mixers[0].devices[0]",
            lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,4 +1,3 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
            -            <SignalTesterDevice 2 'Self'>
            """,
            """
            --- initial
            +++ mutation
            @@ -4,9 +4,9 @@
                     1004 supriya:meters:2 (mixers[1]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (mixers[1]:devices)
            -            1007 group (devices[2]:group)
            -                1008 supriya:device-dc-tester:2 (devices[2]:synth)
            -                    active: 1.0, dc: 1.0, done_action: 2.0, gate: 1.0, out: 16.0
            +            1007 group
            +                1008 supriya:device-dc-tester:2
            +                    active: 1.0, dc: 1.0, done_action: 14.0, gate: 0.0, out: 16.0
                     1003 supriya:channel-strip:2 (mixers[1]:channel-strip)
                         active: 1.0, done_action: 2.0, gain: c0, gate: 1.0, out: 16.0
                     1005 supriya:meters:2 (mixers[1]:output-levels)
            """,
            """
            - [None, [['/n_set', 1007, 'gate', 0.0], ['/n_set', 1008, 'done_action', 14.0]]]
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_Device_delete(
    commands: list[tuple[str | None, str, dict | None]],
    expected_components_diff: Callable[[Session], str] | str,
    expected_messages: str,
    expected_tree_diff: str,
    online: bool,
    target: str,
) -> None:
    async with run_test(
        annotation="numeric",
        commands=commands,
        expected_components_diff=expected_components_diff,
        expected_messages=expected_messages,
        expected_tree_diff=expected_tree_diff,
        online=online,
    ) as session:
        target_ = session[target]
        assert isinstance(target_, Device)
        parent = target_.parent
        await target_.delete()
    assert parent
    assert target_ not in parent.devices
    assert target_.address == "devices[?]"
    assert target_.context is None
    assert target_.mixer is None
    assert target_.parent is None
    assert target_.session is None


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "commands, target, parent, index, maybe_raises, expected_graph_order, expected_components_diff, expected_tree_diff, expected_messages",
    [
        # 0
        # move to other mixer: raises
        (
            [
                (None, "add_mixer", {"name": "Mixer One"}),
                (None, "add_mixer", {"name": "Mixer Two"}),
                (
                    "mixers[0]",
                    "add_device",
                    {"device_class": SignalTesterDevice, "name": "Self"},
                ),
            ],
            "mixers[0].devices[0]",
            "mixers[1]",
            0,
            pytest.raises(RuntimeError),
            (0, 0),
            "",
            "",
            "",
        ),
        # 1
        # move to same parent, same index: no-op
        (
            [
                (None, "add_mixer", {"name": "Mixer One"}),
                (
                    "mixers[0]",
                    "add_device",
                    {"device_class": SignalTesterDevice, "name": "Self"},
                ),
            ],
            "mixers[0].devices[0]",
            "mixers[0]",
            0,
            does_not_raise,
            (0, 0),
            "",
            "",
            "",
        ),
        # 2
        # move to same parent, index too low: raises
        (
            [
                (None, "add_mixer", {"name": "Mixer One"}),
                (
                    "mixers[0]",
                    "add_device",
                    {"device_class": SignalTesterDevice, "name": "Self"},
                ),
            ],
            "mixers[0].devices[0]",
            "mixers[0]",
            -1,
            pytest.raises(RuntimeError),
            (0, 0),
            "",
            "",
            "",
        ),
        # 3
        # move to same parent, index too high: raises
        (
            [
                (None, "add_mixer", {"name": "Mixer One"}),
                (
                    "mixers[0]",
                    "add_device",
                    {"device_class": SignalTesterDevice, "name": "Self"},
                ),
            ],
            "mixers[0].devices[0]",
            "mixers[0]",
            2,
            pytest.raises(RuntimeError),
            (0, 0),
            "",
            "",
            "",
        ),
        # 4
        # move to other device container
        (
            [
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Track"}),
                (
                    "mixers[0]",
                    "add_device",
                    {"device_class": SignalTesterDevice, "name": "Self"},
                ),
            ],
            "mixers[0].devices[0]",
            "mixers[0].tracks[0]",
            0,
            does_not_raise,
            (0, 0, 0),
            """
            --- initial
            +++ mutation
            @@ -2,4 +2,4 @@
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
                         <Track 2 'Track'>
            -            <SignalTesterDevice 3 'Self'>
            +                <SignalTesterDevice 3 'Self'>
            """,
            """
            --- initial
            +++ mutation
            @@ -6,6 +6,11 @@
                             1011 supriya:meters:2 (tracks[2]:input-levels)
                                 in_: 18.0, out: 7.0
                             1009 group (tracks[2]:devices)
            +                    1014 group (devices[3]:group)
            +                        1015 supriya:device-dc-tester:2
            +                            active: 1.0, dc: 1.0, done_action: 2.0, gate: 0.0, out: 16.0
            +                        1016 supriya:device-dc-tester:2 (devices[3]:synth)
            +                            active: 1.0, dc: 1.0, done_action: 2.0, gate: 1.0, out: 18.0
                             1010 supriya:channel-strip:2 (tracks[2]:channel-strip)
                                 active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
                             1012 supriya:meters:2 (tracks[2]:output-levels)
            @@ -15,9 +20,6 @@
                     1004 supriya:meters:2 (mixers[1]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (mixers[1]:devices)
            -            1014 group (devices[3]:group)
            -                1015 supriya:device-dc-tester:2 (devices[3]:synth)
            -                    active: 1.0, dc: 1.0, done_action: 2.0, gate: 1.0, out: 16.0
                     1003 supriya:channel-strip:2 (mixers[1]:channel-strip)
                         active: 1.0, done_action: 2.0, gain: c0, gate: 1.0, out: 16.0
                     1005 supriya:meters:2 (mixers[1]:output-levels)
            """,
            """
            - ['/s_new', 'supriya:device-dc-tester:2', 1016, 1, 1014, 'out', 18.0]
            - ['/g_head', 1009, 1014]
            - ['/n_set', 1015, 'done_action', 2.0, 'gate', 0.0]
            """,
        ),
        # 5
        # move before sibling
        (
            [
                (None, "add_mixer", {"name": "Mixer"}),
                (
                    "mixers[0]",
                    "add_device",
                    {"device_class": SignalTesterDevice, "name": "Older Sibling"},
                ),
                (
                    "mixers[0]",
                    "add_device",
                    {"device_class": SignalTesterDevice, "name": "Self"},
                ),
            ],
            "mixers[0].devices[1]",
            "mixers[0]",
            0,
            does_not_raise,
            (0, 0),
            lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,5 +1,5 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
            +            <SignalTesterDevice 3 'Self'>
                         <SignalTesterDevice 2 'Older Sibling'>
            -            <SignalTesterDevice 3 'Self'>
            """,
            """
            --- initial
            +++ mutation
            @@ -4,11 +4,11 @@
                     1004 supriya:meters:2 (mixers[1]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (mixers[1]:devices)
            +            1009 group (devices[3]:group)
            +                1010 supriya:device-dc-tester:2 (devices[3]:synth)
            +                    active: 1.0, dc: 1.0, done_action: 2.0, gate: 1.0, out: 16.0
                         1007 group (devices[2]:group)
                             1008 supriya:device-dc-tester:2 (devices[2]:synth)
            -                    active: 1.0, dc: 1.0, done_action: 2.0, gate: 1.0, out: 16.0
            -            1009 group (devices[3]:group)
            -                1010 supriya:device-dc-tester:2 (devices[3]:synth)
                                 active: 1.0, dc: 1.0, done_action: 2.0, gate: 1.0, out: 16.0
                     1003 supriya:channel-strip:2 (mixers[1]:channel-strip)
                         active: 1.0, done_action: 2.0, gain: c0, gate: 1.0, out: 16.0
            """,
            """
            - ['/g_head', 1002, 1009]
            """,
        ),
        # 6
        # move after sibling
        (
            [
                (None, "add_mixer", {"name": "Mixer"}),
                (
                    "mixers[0]",
                    "add_device",
                    {"device_class": SignalTesterDevice, "name": "Self"},
                ),
                (
                    "mixers[0]",
                    "add_device",
                    {"device_class": SignalTesterDevice, "name": "Younger Sibling"},
                ),
            ],
            "mixers[0].devices[0]",
            "mixers[0]",
            1,
            does_not_raise,
            (0, 1),
            lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,5 +1,5 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
            +            <SignalTesterDevice 3 'Younger Sibling'>
                         <SignalTesterDevice 2 'Self'>
            -            <SignalTesterDevice 3 'Younger Sibling'>
            """,
            """
            --- initial
            +++ mutation
            @@ -4,11 +4,11 @@
                     1004 supriya:meters:2 (mixers[1]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (mixers[1]:devices)
            +            1009 group (devices[3]:group)
            +                1010 supriya:device-dc-tester:2 (devices[3]:synth)
            +                    active: 1.0, dc: 1.0, done_action: 2.0, gate: 1.0, out: 16.0
                         1007 group (devices[2]:group)
                             1008 supriya:device-dc-tester:2 (devices[2]:synth)
            -                    active: 1.0, dc: 1.0, done_action: 2.0, gate: 1.0, out: 16.0
            -            1009 group (devices[3]:group)
            -                1010 supriya:device-dc-tester:2 (devices[3]:synth)
                                 active: 1.0, dc: 1.0, done_action: 2.0, gate: 1.0, out: 16.0
                     1003 supriya:channel-strip:2 (mixers[1]:channel-strip)
                         active: 1.0, done_action: 2.0, gain: c0, gate: 1.0, out: 16.0
            """,
            """
            - ['/n_after', 1007, 1009]
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_Device_move(
    commands: list[tuple[str | None, str, dict | None]],
    expected_components_diff: Callable[[Session], str] | str,
    expected_graph_order: list[int],
    expected_messages: str,
    expected_tree_diff: str,
    index: int,
    maybe_raises,
    online: bool,
    parent: str,
    target: str,
) -> None:
    async with run_test(
        annotation="numeric",
        commands=commands,
        expected_components_diff=expected_components_diff,
        expected_messages=expected_messages,
        expected_tree_diff=expected_tree_diff,
        online=online,
    ) as session:
        target_ = session[target]
        parent_ = session[parent]
        old_parent = target_.parent
        assert isinstance(old_parent, DeviceContainer)
        assert isinstance(parent_, DeviceContainer)
        assert isinstance(target_, Device)
        raised = True
        with maybe_raises:
            await target_.move(index=index, parent=parent_)
            raised = False
    assert target_.graph_order == expected_graph_order
    if not raised:
        assert target_.parent is parent_
        assert target_ in parent_.devices
        if parent_ is not old_parent:
            assert target_ not in old_parent.devices


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.asyncio
async def test_Device_set_name(online: bool) -> None:
    session = Session()
    mixer = await session.add_mixer()
    device = await mixer.add_device(device_class=SignalTesterDevice)
    if online:
        await session.boot()
    assert device.name is None
    for name in ("Foo", "Bar", "Baz"):
        device.set_name(name=name)
        assert device.name == name
    device.set_name(name=None)
    assert device.name is None
