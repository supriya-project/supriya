import pytest
from uqbar.strings import normalize

from supriya.mixers import Session
from supriya.mixers.mixers import Mixer

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
                (None, "add_mixer", {"name": "Mixer One"}),
                ("mixers[0]", "add_track", {"name": "Track"}),
                (None, "add_mixer", {"name": "Mixer Two"}),
            ],
            "mixers[0]",
            """
            --- initial
            +++ mutation
            @@ -1,5 +1,3 @@
             <Session 0>
                 <session.contexts[0]>
            -        <Mixer 1 'Mixer One'>
            -            <Track 2 'Track'>
                     <Mixer 3 'Mixer Two'>
            """,
            """
            --- initial
            +++ mutation
            @@ -1,26 +1,4 @@
             <session.contexts[0]>
            -    NODE TREE 1000 group
            -        1001 group
            -            1007 group
            -                1008 group
            -                1011 supriya:meters:2
            -                    in_: 18.0, out: 7.0
            -                1009 group
            -                1010 supriya:channel-strip:2
            -                    active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
            -                1012 supriya:meters:2
            -                    in_: 18.0, out: 9.0
            -                1013 supriya:patch-cable:2x2
            -                    active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
            -        1004 supriya:meters:2
            -            in_: 16.0, out: 1.0
            -        1002 group
            -        1003 supriya:channel-strip:2
            -            active: 1.0, done_action: 2.0, gain: c0, gate: 1.0, out: 16.0
            -        1005 supriya:meters:2
            -            in_: 16.0, out: 3.0
            -        1006 supriya:patch-cable:2x2
            -            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 0.0
                 NODE TREE 1014 group
                     1015 group
                     1018 supriya:meters:2
            """,
            """
            - [None, [['/n_set', 1000, 'gate', 0.0], ['/n_set', 1003, 'done_action', 14.0]]]
            """,
        ),
        (
            [
                (None, "add_mixer", {"name": "Mixer One"}),
                ("mixers[0]", "add_track", {"name": "Track"}),
                (None, "add_mixer", {"name": "Mixer Two"}),
            ],
            "mixers[1]",
            """
            --- initial
            +++ mutation
            @@ -2,4 +2,3 @@
                 <session.contexts[0]>
                     <Mixer 1 'Mixer One'>
                         <Track 2 'Track'>
            -        <Mixer 3 'Mixer Two'>
            """,
            """
            --- initial
            +++ mutation
            @@ -21,14 +21,3 @@
                         in_: 16.0, out: 3.0
                     1006 supriya:patch-cable:2x2
                         active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 0.0
            -    NODE TREE 1014 group
            -        1015 group
            -        1018 supriya:meters:2
            -            in_: 20.0, out: 12.0
            -        1016 group
            -        1017 supriya:channel-strip:2
            -            active: 1.0, done_action: 2.0, gain: c11, gate: 1.0, out: 20.0
            -        1019 supriya:meters:2
            -            in_: 20.0, out: 14.0
            -        1020 supriya:patch-cable:2x2
            -            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 0.0
            """,
            """
            - [None, [['/n_set', 1014, 'gate', 0.0], ['/n_set', 1017, 'done_action', 14.0]]]
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_Mixer_delete(
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
        initial_tree = await debug_tree(session, annotated=False)
        print(initial_tree)
    target_ = session[target]
    assert isinstance(target_, Mixer)
    # Operation
    print("Operation")
    with capture(target_.context) as messages:
        await target_.delete()
    # Post-conditions
    print("Post-conditions")
    assert target_ not in session.mixers
    assert target_.parent is None
    assert_components_diff(session, expected_components_diff, initial_components)
    if not online:
        return
    # N.B. The diff looks like the mixer immediately disappeared, but it hasn't.
    #      Session.dump_tree() just queries each mixer's group node, and
    #      because the mixer doesn't exist from the session's perspective, it
    #      doesn't query that group anymore.  We do this to save horizontal
    #      space, but querying the underlying context directly would show the
    #      nodes are still there, although about to be released.
    await assert_tree_diff(
        session,
        expected_tree_diff,
        expected_initial_tree=initial_tree,
        annotated=False,
    )
    assert format_messages(messages) == normalize(expected_messages)
