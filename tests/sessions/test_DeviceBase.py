import dataclasses
from typing import Sequence

import pytest

from supriya.sessions import DeviceBase, DeviceContainer, Session, SynthConfig
from supriya.ugens.system import build_dc_synthdef

from .conftest import Scenario


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "scenario",
    [
        Scenario(
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                (
                    "mixers[0]",
                    "add_device",
                    {
                        "synth_configs": [SynthConfig(synthdef=build_dc_synthdef)],
                        "name": "Self",
                    },
                ),
            ],
            subject="mixers[0].devices[0]",
            expected_components_diff=lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,4 +1,3 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
            -            <Device 2 'Self'>
            """,
            expected_messages="""
            - ['/n_set', 1007, 'done_action', 14.0, 'gate', 0.0]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -7,7 +7,7 @@
                         1007 group (devices[2]:group)
                             1008 group (devices[2]:synths)
                                 1009 supriya:dc:2 (devices[2]:synth-0)
            -                        out: 16.0, active: 1.0, dc: 1.0, done_action: 2.0, gate: 1.0
            +                        out: 16.0, active: 1.0, dc: 1.0, done_action: 14.0, gate: 0.0
                             1010 supriya:meters:2 (devices[2]:output-levels)
                                 in_: 16.0, out: 5.0
                     1003 supriya:channel-strip:2 (mixers[1]:channel-strip)
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_DeviceBase_delete(
    scenario: Scenario,
    online: bool,
) -> None:
    async with scenario.run(annotation_style="numeric", online=online) as session:
        subject = session[scenario.subject]
        assert isinstance(subject, DeviceBase)
        parent = subject.parent
        await subject.delete()
    assert parent
    assert subject not in parent.devices
    assert subject.address == "devices[?]"
    assert subject.context is None
    assert subject.mixer is None
    assert subject.parent is None
    assert subject.session is None


@dataclasses.dataclass(frozen=True)
class MoveScenario(Scenario):
    expected_graph_order: Sequence[int]
    index: int
    parent: str


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "scenario",
    [
        # 0
        # move to other mixer: raises
        MoveScenario(
            id="move to other mixer",
            commands=[
                (None, "add_mixer", {"name": "Mixer One"}),
                (None, "add_mixer", {"name": "Mixer Two"}),
                (
                    "mixers[0]",
                    "add_device",
                    {
                        "synth_configs": [SynthConfig(synthdef=build_dc_synthdef)],
                        "name": "Self",
                    },
                ),
            ],
            subject="mixers[0].devices[0]",
            parent="mixers[1]",
            index=0,
            expected_exception=RuntimeError,
            expected_graph_order=(0, 0),
            expected_components_diff="",
            expected_messages="",
            expected_tree_diff="",
        ),
        # 1
        # move to same parent, same index: no-op
        MoveScenario(
            id="move to same parent, same index",
            commands=[
                (None, "add_mixer", {"name": "Mixer One"}),
                (
                    "mixers[0]",
                    "add_device",
                    {
                        "synth_configs": [SynthConfig(synthdef=build_dc_synthdef)],
                        "name": "Self",
                    },
                ),
            ],
            subject="mixers[0].devices[0]",
            parent="mixers[0]",
            index=0,
            expected_graph_order=(0, 0),
            expected_components_diff="",
            expected_messages="",
            expected_tree_diff="",
        ),
        # 2
        # move to same parent, index too low: raises
        MoveScenario(
            id="move to same parent, index too low",
            commands=[
                (None, "add_mixer", {"name": "Mixer One"}),
                (
                    "mixers[0]",
                    "add_device",
                    {
                        "synth_configs": [SynthConfig(synthdef=build_dc_synthdef)],
                        "name": "Self",
                    },
                ),
            ],
            subject="mixers[0].devices[0]",
            parent="mixers[0]",
            index=-1,
            expected_exception=RuntimeError,
            expected_graph_order=(0, 0),
            expected_components_diff="",
            expected_messages="",
            expected_tree_diff="",
        ),
        # 3
        # move to same parent, index too high: raises
        MoveScenario(
            id="move to same parent, index too high",
            commands=[
                (None, "add_mixer", {"name": "Mixer One"}),
                (
                    "mixers[0]",
                    "add_device",
                    {
                        "synth_configs": [SynthConfig(synthdef=build_dc_synthdef)],
                        "name": "Self",
                    },
                ),
            ],
            subject="mixers[0].devices[0]",
            parent="mixers[0]",
            index=2,
            expected_exception=RuntimeError,
            expected_graph_order=(0, 0),
            expected_components_diff="",
            expected_messages="",
            expected_tree_diff="",
        ),
        # 4
        # move to other parent
        MoveScenario(
            id="move to other parent",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_track", {"name": "Track"}),
                (
                    "mixers[0]",
                    "add_device",
                    {
                        "synth_configs": [SynthConfig(synthdef=build_dc_synthdef)],
                        "name": "Self",
                    },
                ),
            ],
            subject="mixers[0].devices[0]",
            parent="mixers[0].tracks[0]",
            index=0,
            expected_graph_order=(0, 0, 0),
            expected_components_diff="""
            --- initial
            +++ mutation
            @@ -2,4 +2,4 @@
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
                         <Track 2 'Track'>
            -            <Device 3 'Self'>
            +                <Device 3 'Self'>
            """,
            expected_messages="""
            - [None,
               [['/s_new', 'supriya:dc:2', 1018, 1, 1015, 'out', 18.0],
                ['/s_new', 'supriya:meters:2', 1019, 1, 1014, 'in_', 18.0, 'out', 11.0]]]
            - ['/g_head', 1009, 1014]
            - [None, [['/n_set', 1016, 'done_action', 2.0, 'gate', 0.0], ['/n_free', 1017]]]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -6,6 +6,14 @@
                             1011 supriya:meters:2 (tracks[2]:input-levels)
                                 in_: 18.0, out: 7.0
                             1009 group (tracks[2]:devices)
            +                    1014 group (devices[3]:group)
            +                        1015 group (devices[3]:synths)
            +                            1016 supriya:dc:2 (devices[3]:synth-0)
            +                                out: 16.0, active: 1.0, dc: 1.0, done_action: 2.0, gate: 0.0
            +                            1018 supriya:dc:2 (devices[3]:synth-0)
            +                                out: 18.0, active: 1.0, dc: 1.0, done_action: 2.0, gate: 1.0
            +                        1019 supriya:meters:2 (devices[3]:output-levels)
            +                            in_: 18.0, out: 11.0
                             1010 supriya:channel-strip:2 (tracks[2]:channel-strip)
                                 active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
                             1012 supriya:meters:2 (tracks[2]:output-levels)
            @@ -15,12 +23,6 @@
                     1004 supriya:meters:2 (mixers[1]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (mixers[1]:devices)
            -            1014 group (devices[3]:group)
            -                1015 group (devices[3]:synths)
            -                    1016 supriya:dc:2 (devices[3]:synth-0)
            -                        out: 16.0, active: 1.0, dc: 1.0, done_action: 2.0, gate: 1.0
            -                1017 supriya:meters:2 (devices[3]:output-levels)
            -                    in_: 16.0, out: 11.0
                     1003 supriya:channel-strip:2 (mixers[1]:channel-strip)
                         active: 1.0, done_action: 2.0, gain: c0, gate: 1.0, out: 16.0
                     1005 supriya:meters:2 (mixers[1]:output-levels)
            """,
        ),
        # 5
        # move before sibling
        MoveScenario(
            id="move before sibling",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                (
                    "mixers[0]",
                    "add_device",
                    {
                        "synth_configs": [SynthConfig(synthdef=build_dc_synthdef)],
                        "name": "Older Sibling",
                    },
                ),
                (
                    "mixers[0]",
                    "add_device",
                    {
                        "synth_configs": [SynthConfig(synthdef=build_dc_synthdef)],
                        "name": "Self",
                    },
                ),
            ],
            subject="mixers[0].devices[1]",
            parent="mixers[0]",
            index=0,
            expected_graph_order=(0, 0),
            expected_components_diff=lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,5 +1,5 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
            +            <Device 3 'Self'>
                         <Device 2 'Older Sibling'>
            -            <Device 3 'Self'>
            """,
            expected_messages="""
            - ['/g_head', 1002, 1011]
            - ['/n_after', 1007, 1011]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -4,18 +4,18 @@
                     1004 supriya:meters:2 (mixers[1]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (mixers[1]:devices)
            +            1011 group (devices[3]:group)
            +                1012 group (devices[3]:synths)
            +                    1013 supriya:dc:2 (devices[3]:synth-0)
            +                        out: 16.0, active: 1.0, dc: 1.0, done_action: 2.0, gate: 1.0
            +                1014 supriya:meters:2 (devices[3]:output-levels)
            +                    in_: 16.0, out: 7.0
                         1007 group (devices[2]:group)
                             1008 group (devices[2]:synths)
                                 1009 supriya:dc:2 (devices[2]:synth-0)
                                     out: 16.0, active: 1.0, dc: 1.0, done_action: 2.0, gate: 1.0
                             1010 supriya:meters:2 (devices[2]:output-levels)
                                 in_: 16.0, out: 5.0
            -            1011 group (devices[3]:group)
            -                1012 group (devices[3]:synths)
            -                    1013 supriya:dc:2 (devices[3]:synth-0)
            -                        out: 16.0, active: 1.0, dc: 1.0, done_action: 2.0, gate: 1.0
            -                1014 supriya:meters:2 (devices[3]:output-levels)
            -                    in_: 16.0, out: 7.0
                     1003 supriya:channel-strip:2 (mixers[1]:channel-strip)
                         active: 1.0, done_action: 2.0, gain: c0, gate: 1.0, out: 16.0
                     1005 supriya:meters:2 (mixers[1]:output-levels)
            """,
        ),
        # 6
        # move after sibling
        MoveScenario(
            id="move after sibling",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                (
                    "mixers[0]",
                    "add_device",
                    {
                        "synth_configs": [SynthConfig(synthdef=build_dc_synthdef)],
                        "name": "Self",
                    },
                ),
                (
                    "mixers[0]",
                    "add_device",
                    {
                        "synth_configs": [SynthConfig(synthdef=build_dc_synthdef)],
                        "name": "Younger Sibling",
                    },
                ),
            ],
            subject="mixers[0].devices[0]",
            parent="mixers[0]",
            index=1,
            expected_graph_order=(0, 1),
            expected_components_diff=lambda session: f"""
            --- initial
            +++ mutation
            @@ -1,5 +1,5 @@
             <Session 0 {session.boot_status.name}>
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
            +            <Device 3 'Younger Sibling'>
                         <Device 2 'Self'>
            -            <Device 3 'Younger Sibling'>
            """,
            expected_messages="""
            - ['/n_after', 1007, 1011]
            - ['/g_head', 1002, 1011]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -4,18 +4,18 @@
                     1004 supriya:meters:2 (mixers[1]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (mixers[1]:devices)
            +            1011 group (devices[3]:group)
            +                1012 group (devices[3]:synths)
            +                    1013 supriya:dc:2 (devices[3]:synth-0)
            +                        out: 16.0, active: 1.0, dc: 1.0, done_action: 2.0, gate: 1.0
            +                1014 supriya:meters:2 (devices[3]:output-levels)
            +                    in_: 16.0, out: 7.0
                         1007 group (devices[2]:group)
                             1008 group (devices[2]:synths)
                                 1009 supriya:dc:2 (devices[2]:synth-0)
                                     out: 16.0, active: 1.0, dc: 1.0, done_action: 2.0, gate: 1.0
                             1010 supriya:meters:2 (devices[2]:output-levels)
                                 in_: 16.0, out: 5.0
            -            1011 group (devices[3]:group)
            -                1012 group (devices[3]:synths)
            -                    1013 supriya:dc:2 (devices[3]:synth-0)
            -                        out: 16.0, active: 1.0, dc: 1.0, done_action: 2.0, gate: 1.0
            -                1014 supriya:meters:2 (devices[3]:output-levels)
            -                    in_: 16.0, out: 7.0
                     1003 supriya:channel-strip:2 (mixers[1]:channel-strip)
                         active: 1.0, done_action: 2.0, gain: c0, gate: 1.0, out: 16.0
                     1005 supriya:meters:2 (mixers[1]:output-levels)
            """,
        ),
    ],
    ids=lambda scenario: scenario.id,
)
@pytest.mark.asyncio
async def test_DeviceBase_move(
    scenario: MoveScenario,
    online: bool,
) -> None:
    async with scenario.run(annotation_style="numeric", online=online) as session:
        subject = session[scenario.subject]
        parent = session[scenario.parent]
        old_parent = subject.parent
        assert isinstance(old_parent, DeviceContainer)
        assert isinstance(parent, DeviceContainer)
        assert isinstance(subject, DeviceBase)
        await subject.move(index=scenario.index, parent=parent)
    assert subject.graph_order == scenario.expected_graph_order
    if scenario.expected_exception:
        return
    assert subject.parent is parent
    assert subject in parent.devices
    if parent is not old_parent:
        assert subject not in old_parent.devices


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.asyncio
async def test_DeviceBase_set_name(online: bool) -> None:
    session = Session()
    mixer = await session.add_mixer()
    device = await mixer.add_device(
        synth_configs=[SynthConfig(synthdef=build_dc_synthdef)]
    )
    if online:
        await session.boot()
    assert device.name is None
    for name in ("Foo", "Bar", "Baz"):
        device.set_name(name=name)
        assert device.name == name
    device.set_name(name=None)
    assert device.name is None
