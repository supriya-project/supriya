import pytest
from uqbar.strings import normalize

from supriya.mixers import Session

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
                    1006 group (session.mixers[0].tracks[0]:group)
                        1007 group (session.mixers[0].tracks[0]:tracks)
                        1010 supriya:meters:2 (session.mixers[0].tracks[0]:input-levels)
                            in_: 18.0, out: 7.0
                        1008 group (session.mixers[0].tracks[0]:devices)
                        1009 supriya:channel-strip:2 (session.mixers[0].tracks[0]:channel-strip)
                            active: c5, bus: 18.0, done_action: 2.0, gain: c6, gate: 1.0
                        1011 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
                            in_: 18.0, out: 9.0
                        1012 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].output:synth)
                            active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
                1004 supriya:meters:2 (session.mixers[0]:input-levels)
                    in_: 16.0, out: 1.0
                1002 group (session.mixers[0]:devices)
                1003 supriya:channel-strip:2 (session.mixers[0]:channel-strip)
                    active: 1.0, bus: 16.0, done_action: 2.0, gain: c0, gate: 1.0
                1005 supriya:meters:2 (session.mixers[0]:output-levels)
                    in_: 16.0, out: 3.0
                1013 supriya:patch-cable:2x2 (session.mixers[0].output:synth)
                    active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 0.0
        """
    )


@pytest.mark.asyncio
async def test_complex_session(complex_session: tuple[Session, str, str]) -> None:
    session, initial_components, initial_tree = complex_session
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
                    1006 group (session.mixers[0].tracks[0]:group)
                        1007 group (session.mixers[0].tracks[0]:tracks)
                            1012 group (session.mixers[0].tracks[0].tracks[0]:group)
                                1041 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].feedback:synth)
                                    active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 28.0, out: 20.0
                                1013 group (session.mixers[0].tracks[0].tracks[0]:tracks)
                                    1018 group (session.mixers[0].tracks[0].tracks[0].tracks[0]:group)
                                        1019 group (session.mixers[0].tracks[0].tracks[0].tracks[0]:tracks)
                                        1022 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0].tracks[0]:input-levels)
                                            in_: 22.0, out: 19.0
                                        1020 group (session.mixers[0].tracks[0].tracks[0].tracks[0]:devices)
                                        1021 supriya:channel-strip:2 (session.mixers[0].tracks[0].tracks[0].tracks[0]:channel-strip)
                                            active: c17, bus: 22.0, done_action: 2.0, gain: c18, gate: 1.0
                                        1023 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0].tracks[0]:output-levels)
                                            in_: 22.0, out: 21.0
                                        1024 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].tracks[0].output:synth)
                                            active: c17, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 20.0
                                1016 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:input-levels)
                                    in_: 20.0, out: 13.0
                                1014 group (session.mixers[0].tracks[0].tracks[0]:devices)
                                1015 supriya:channel-strip:2 (session.mixers[0].tracks[0].tracks[0]:channel-strip)
                                    active: c11, bus: 20.0, done_action: 2.0, gain: c12, gate: 1.0
                                1017 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:output-levels)
                                    in_: 20.0, out: 15.0
                                1025 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].output:synth)
                                    active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 18.0
                            1026 group (session.mixers[0].tracks[0].tracks[1]:group)
                                1027 group (session.mixers[0].tracks[0].tracks[1]:tracks)
                                1030 supriya:meters:2 (session.mixers[0].tracks[0].tracks[1]:input-levels)
                                    in_: 24.0, out: 25.0
                                1028 group (session.mixers[0].tracks[0].tracks[1]:devices)
                                1029 supriya:channel-strip:2 (session.mixers[0].tracks[0].tracks[1]:channel-strip)
                                    active: c23, bus: 24.0, done_action: 2.0, gain: c24, gate: 1.0
                                1031 supriya:meters:2 (session.mixers[0].tracks[0].tracks[1]:output-levels)
                                    in_: 24.0, out: 27.0
                                1032 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[1].output:synth)
                                    active: c23, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 24.0, out: 18.0
                        1010 supriya:meters:2 (session.mixers[0].tracks[0]:input-levels)
                            in_: 18.0, out: 7.0
                        1008 group (session.mixers[0].tracks[0]:devices)
                        1009 supriya:channel-strip:2 (session.mixers[0].tracks[0]:channel-strip)
                            active: c5, bus: 18.0, done_action: 2.0, gain: c6, gate: 1.0
                        1051 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].sends[0]:synth)
                            active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 26.0
                        1011 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
                            in_: 18.0, out: 9.0
                        1033 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].output:synth)
                            active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
                    1034 group (session.mixers[0].tracks[1]:group)
                        1035 group (session.mixers[0].tracks[1]:tracks)
                        1038 supriya:meters:2 (session.mixers[0].tracks[1]:input-levels)
                            in_: 26.0, out: 31.0
                        1036 group (session.mixers[0].tracks[1]:devices)
                        1037 supriya:channel-strip:2 (session.mixers[0].tracks[1]:channel-strip)
                            active: c29, bus: 26.0, done_action: 2.0, gain: c30, gate: 1.0
                        1042 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].sends[0]:synth)
                            active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 26.0, out: 28.0
                        1039 supriya:meters:2 (session.mixers[0].tracks[1]:output-levels)
                            in_: 26.0, out: 33.0
                        1040 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].output:synth)
                            active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 26.0, out: 16.0
                    1043 group (session.mixers[0].tracks[2]:group)
                        1044 group (session.mixers[0].tracks[2]:tracks)
                        1047 supriya:meters:2 (session.mixers[0].tracks[2]:input-levels)
                            in_: 30.0, out: 37.0
                        1045 group (session.mixers[0].tracks[2]:devices)
                        1046 supriya:channel-strip:2 (session.mixers[0].tracks[2]:channel-strip)
                            active: c35, bus: 30.0, done_action: 2.0, gain: c36, gate: 1.0
                        1048 supriya:meters:2 (session.mixers[0].tracks[2]:output-levels)
                            in_: 30.0, out: 39.0
                        1049 supriya:patch-cable:2x2 (session.mixers[0].tracks[2].output:synth)
                            active: c35, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 30.0, out: 16.0
                1004 supriya:meters:2 (session.mixers[0]:input-levels)
                    in_: 16.0, out: 1.0
                1002 group (session.mixers[0]:devices)
                1003 supriya:channel-strip:2 (session.mixers[0]:channel-strip)
                    active: 1.0, bus: 16.0, done_action: 2.0, gain: c0, gate: 1.0
                1005 supriya:meters:2 (session.mixers[0]:output-levels)
                    in_: 16.0, out: 3.0
                1050 supriya:patch-cable:2x2 (session.mixers[0].output:synth)
                    active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 0.0
            NODE TREE 1052 group (session.mixers[1]:group)
                1053 group (session.mixers[1]:tracks)
                    1058 group (session.mixers[1].tracks[0]:group)
                        1059 group (session.mixers[1].tracks[0]:tracks)
                        1062 supriya:meters:2 (session.mixers[1].tracks[0]:input-levels)
                            in_: 34.0, out: 48.0
                        1060 group (session.mixers[1].tracks[0]:devices)
                        1061 supriya:channel-strip:2 (session.mixers[1].tracks[0]:channel-strip)
                            active: c46, bus: 34.0, done_action: 2.0, gain: c47, gate: 1.0
                        1063 supriya:meters:2 (session.mixers[1].tracks[0]:output-levels)
                            in_: 34.0, out: 50.0
                        1064 supriya:patch-cable:2x2 (session.mixers[1].tracks[0].output:synth)
                            active: c46, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 34.0, out: 32.0
                1056 supriya:meters:2 (session.mixers[1]:input-levels)
                    in_: 32.0, out: 42.0
                1054 group (session.mixers[1]:devices)
                1055 supriya:channel-strip:2 (session.mixers[1]:channel-strip)
                    active: 1.0, bus: 32.0, done_action: 2.0, gain: c41, gate: 1.0
                1057 supriya:meters:2 (session.mixers[1]:output-levels)
                    in_: 32.0, out: 44.0
                1065 supriya:patch-cable:2x2 (session.mixers[1].output:synth)
                    active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 32.0, out: 0.0
        """
    )
