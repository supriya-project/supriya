import pytest
from uqbar.strings import normalize

from supriya.mixers import Session
from supriya.mixers.tracks import TrackSend

from .conftest import (
    apply_commands,
    assert_components_diff,
    assert_tree_diff,
    capture,
    debug_components,
    debug_tree,
    format_messages,
)


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
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            +                1014 supriya:patch-cable:2x2
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 18.0, out: 20.0
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
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 18.0
            +                1014 supriya:fb-patch-cable:2x2
            +                    active: c5, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 20.0, out: 18.0
                             1008 group (session.mixers[0].tracks[0]:tracks)
                             1011 supriya:meters:2 (session.mixers[0].tracks[0]:input-levels)
                                 in_: 18.0, out: 7.0
            @@ -21,8 +21,8 @@
                             1017 group (session.mixers[0].tracks[1]:devices)
                             1018 supriya:channel-strip:2 (session.mixers[0].tracks[1]:channel-strip)
                                 active: c11, done_action: 2.0, gain: c12, gate: 1.0, out: 22.0
            -                1022 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].sends[0]:synth)
            -                    active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 20.0
            +                1022 supriya:patch-cable:2x2
            +                    active: c11, done_action: 2.0, gain: 0.0, gate: 0.0, in_: 22.0, out: 20.0
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
    expected_components_diff: str,
    expected_messages: str,
    expected_tree_diff: str,
    online: bool,
    target: str,
) -> None:
    # Pre-conditions
    print("Pre-conditions")
    session = Session()
    await apply_commands(session, commands)
    initial_components = debug_components(session)
    if online:
        await session.boot()
        await session.sync()
        initial_tree = await debug_tree(session)
        print(initial_tree)
    target_ = session[target]
    assert isinstance(target_, TrackSend)
    parent = target_.parent
    # Operation
    print("Operation")
    with capture(target_.context) as messages:
        await target_.delete()
    # Post-conditions
    print("Post-conditions")
    assert parent
    assert target_ not in parent.sends
    assert target_.parent is None
    assert_components_diff(session, expected_components_diff, initial_components)
    if not online:
        return
    await assert_tree_diff(
        session,
        expected_tree_diff,
        expected_initial_tree=initial_tree,
    )
    assert format_messages(messages) == normalize(expected_messages)
