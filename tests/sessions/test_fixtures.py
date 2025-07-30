import pytest
from uqbar.strings import normalize

from supriya.sessions import Session

from .conftest import debug_components, debug_tree


@pytest.mark.asyncio
async def test_bare_session(bare_session: tuple[Session, str, str]) -> None:
    session, initial_components, initial_tree = bare_session
    assert isinstance(session, Session)
    await session.boot()
    actual_components = debug_components(session)
    actual_tree = await debug_tree(session)
    assert initial_components == actual_components
    assert initial_tree == actual_tree
    assert actual_tree == "<empty>"


@pytest.mark.asyncio
async def test_basic_session(basic_session: tuple[Session, str, str]) -> None:
    session, initial_components, initial_tree = basic_session
    assert isinstance(session, Session)
    await session.boot()
    actual_components = debug_components(session)
    actual_tree = await debug_tree(session)
    assert initial_components == actual_components
    assert initial_tree == actual_tree
    assert actual_tree == normalize(
        """
        <session.contexts[0]>
            NODE TREE 1000 group (session.mixers[0]:group)
                1001 group (session.mixers[0]:tracks)
                    1007 group (session.mixers[0].tracks[0]:group)
                        1008 group (session.mixers[0].tracks[0]:tracks)
                        1011 supriya:meters:2 (session.mixers[0].tracks[0]:input-levels)
                            in_: 18.0, out: 7.0
                        1009 group (session.mixers[0].tracks[0]:devices)
                        1010 supriya:channel-strip:2 (session.mixers[0].tracks[0]:channel-strip)
                            active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
                        1012 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
                            in_: 18.0, out: 9.0
                        1013 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:output)
                            active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
                1004 supriya:meters:2 (session.mixers[0]:input-levels)
                    in_: 16.0, out: 1.0
                1002 group (session.mixers[0]:devices)
                1003 supriya:channel-strip:2 (session.mixers[0]:channel-strip)
                    active: 1.0, done_action: 2.0, gain: c0, gate: 1.0, out: 16.0
                1005 supriya:meters:2 (session.mixers[0]:output-levels)
                    in_: 16.0, out: 3.0
                1006 supriya:patch-cable:2x2 (session.mixers[0]:output)
                    active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 0.0
        """
    )
