import pytest

from supriya.mixers.devices import Device, DeviceContainer

from .conftest import run_test


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "commands, target, expected_components_diff, expected_tree_diff, expected_messages",
    [
        (
            [
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_device", {"device_class": Device, "name": "Self"}),
            ],
            "mixers[0].devices[0]",
            """
            --- initial
            +++ mutation
            @@ -1,4 +1,3 @@
             <Session 0>
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
            -            <Device 2 'Self'>
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
    expected_components_diff: str,
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
    assert target_.parent is None


@pytest.mark.parametrize(
    "commands, target, parent, index, maybe_raises, expected_graph_order, expected_components_diff, expected_tree_diff, expected_messages",
    [],
)
@pytest.mark.asyncio
async def test_Device_move(
    commands: list[tuple[str | None, str, dict | None]],
    expected_components_diff: str,
    expected_graph_order: list[int],
    expected_messages: str,
    expected_tree_diff: str,
    index: int,
    maybe_raises,
    parent: str,
    target: str,
    online: bool = True,
) -> None:
    async with run_test(
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
