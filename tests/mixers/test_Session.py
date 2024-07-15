from contextlib import nullcontext as does_not_raise

import pytest
from uqbar.strings import normalize

from supriya.enums import BootStatus
from supriya.mixers import Session


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.asyncio
async def test_Session_boot(online: bool, session: Session) -> None:
    # Pre-conditions
    assert session.status == BootStatus.OFFLINE
    if online:
        await session.boot()
        assert session.status == BootStatus.ONLINE
    # Operation
    await session.boot()  # idempotent
    # Post-conditions
    assert session.status == BootStatus.ONLINE
    assert await session.dump_tree() == normalize(
        f"""
        {session.contexts[0]!r}
            NODE TREE 1000 group (session.mixers[0]:group)
                1001 group (session.mixers[0]:tracks)
                    1004 group (session.mixers[0].tracks[0]:group)
                        1005 group (session.mixers[0].tracks[0]:tracks)
                        1006 channel-strip-2 (session.mixers[0].tracks[0]:channel_strip)
                            active: 1.0, bus: 18.0, gain: 0.0, gate: 1.0
                        1007 patch-cable-2 (session.mixers[0].tracks[0]:output)
                            gate: 1.0, in_: 18.0, out: 18.0
                1002 channel-strip-2 (session.mixers[0]:channel_strip)
                    active: 1.0, bus: 16.0, gain: 0.0, gate: 1.0
                1003 patch-cable-2 (session.mixers[0]:output)
                    gate: 1.0, in_: 16.0, out: 0.0
        """
    )


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.asyncio
async def test_Session_quit(online: bool, session: Session) -> None:
    # Pre-conditions
    assert session.status == BootStatus.OFFLINE
    if online:
        await session.boot()
        assert session.status == BootStatus.ONLINE
    # Operation
    await session.quit()
    # Post-conditions
    assert session.status == BootStatus.OFFLINE
    with pytest.raises(RuntimeError):
        assert await session.dump_tree()


@pytest.mark.parametrize(
    "online, expectation",
    [
        (False, pytest.raises(RuntimeError)),
        (True, does_not_raise()),
    ],
)
@pytest.mark.asyncio
async def test_Session_add_context(expectation, online: bool, session: Session) -> None:
    # Pre-conditions
    if online:
        await session.boot()
    assert len(session.contexts) == 1
    # Operation
    context = await session.add_context()
    # Post-conditions
    assert len(session.contexts) == 2
    assert context in session.contexts
    assert context.boot_status == session.status
    with expectation:
        assert await session.dump_tree() == normalize(
            f"""
            {session.contexts[0]!r}
                NODE TREE 1000 group (session.mixers[0]:group)
                    1001 group (session.mixers[0]:tracks)
                        1004 group (session.mixers[0].tracks[0]:group)
                            1005 group (session.mixers[0].tracks[0]:tracks)
                            1006 channel-strip-2 (session.mixers[0].tracks[0]:channel_strip)
                                active: 1.0, bus: 18.0, gain: 0.0, gate: 1.0
                            1007 patch-cable-2 (session.mixers[0].tracks[0]:output)
                                gate: 1.0, in_: 18.0, out: 18.0
                    1002 channel-strip-2 (session.mixers[0]:channel_strip)
                        active: 1.0, bus: 16.0, gain: 0.0, gate: 1.0
                    1003 patch-cable-2 (session.mixers[0]:output)
                        gate: 1.0, in_: 16.0, out: 0.0
            {session.contexts[1]!r}
            """
        )


@pytest.mark.parametrize(
    "online, expectation, reuse_context",
    [
        (False, pytest.raises(RuntimeError), False),
        (True, does_not_raise(), False),
        (True, does_not_raise(), True),
    ],
)
@pytest.mark.asyncio
async def test_Session_add_mixer(
    expectation, online: bool, reuse_context, session: Session
) -> None:
    # Pre-conditions
    if online:
        await session.boot()
    await session.add_context()
    assert len(session.mixers) == 1
    # Operation
    await session.add_mixer(context=None if reuse_context else session.contexts[1])
    # Post-conditions
    assert len(session.mixers) == 2
    with expectation:
        if not reuse_context:
            assert await session.dump_tree() == normalize(
                f"""
                {session.contexts[0]!r}
                    NODE TREE 1000 group (session.mixers[0]:group)
                        1001 group (session.mixers[0]:tracks)
                            1004 group (session.mixers[0].tracks[0]:group)
                                1005 group (session.mixers[0].tracks[0]:tracks)
                                1006 channel-strip-2 (session.mixers[0].tracks[0]:channel_strip)
                                    active: 1.0, bus: 18.0, gain: 0.0, gate: 1.0
                                1007 patch-cable-2 (session.mixers[0].tracks[0]:output)
                                    gate: 1.0, in_: 18.0, out: 18.0
                        1002 channel-strip-2 (session.mixers[0]:channel_strip)
                            active: 1.0, bus: 16.0, gain: 0.0, gate: 1.0
                        1003 patch-cable-2 (session.mixers[0]:output)
                            gate: 1.0, in_: 16.0, out: 0.0
                {session.contexts[1]!r}
                    NODE TREE 1000 group (session.mixers[1]:group)
                        1001 group (session.mixers[1]:tracks)
                            1004 group (session.mixers[1].tracks[0]:group)
                                1005 group (session.mixers[1].tracks[0]:tracks)
                                1006 channel-strip-2 (session.mixers[1].tracks[0]:channel_strip)
                                    active: 1.0, bus: 18.0, gain: 0.0, gate: 1.0
                                1007 patch-cable-2 (session.mixers[1].tracks[0]:output)
                                    gate: 1.0, in_: 18.0, out: 18.0
                        1002 channel-strip-2 (session.mixers[1]:channel_strip)
                            active: 1.0, bus: 16.0, gain: 0.0, gate: 1.0
                        1003 patch-cable-2 (session.mixers[1]:output)
                            gate: 1.0, in_: 16.0, out: 0.0
                """
            )
        else:
            assert await session.dump_tree() == normalize(
                f"""
                {session.contexts[0]!r}
                    NODE TREE 1000 group (session.mixers[0]:group)
                        1001 group (session.mixers[0]:tracks)
                            1004 group (session.mixers[0].tracks[0]:group)
                                1005 group (session.mixers[0].tracks[0]:tracks)
                                1006 channel-strip-2 (session.mixers[0].tracks[0]:channel_strip)
                                    active: 1.0, bus: 18.0, gain: 0.0, gate: 1.0
                                1007 patch-cable-2 (session.mixers[0].tracks[0]:output)
                                    gate: 1.0, in_: 18.0, out: 18.0
                        1002 channel-strip-2 (session.mixers[0]:channel_strip)
                            active: 1.0, bus: 16.0, gain: 0.0, gate: 1.0
                        1003 patch-cable-2 (session.mixers[0]:output)
                            gate: 1.0, in_: 16.0, out: 0.0
                    NODE TREE 1008 group (session.mixers[1]:group)
                        1009 group (session.mixers[1]:tracks)
                            1012 group (session.mixers[1].tracks[0]:group)
                                1013 group (session.mixers[1].tracks[0]:tracks)
                                1014 channel-strip-2 (session.mixers[1].tracks[0]:channel_strip)
                                    active: 1.0, bus: 22.0, gain: 0.0, gate: 1.0
                                1015 patch-cable-2 (session.mixers[1].tracks[0]:output)
                                    gate: 1.0, in_: 22.0, out: 22.0
                        1010 channel-strip-2 (session.mixers[1]:channel_strip)
                            active: 1.0, bus: 20.0, gain: 0.0, gate: 1.0
                        1011 patch-cable-2 (session.mixers[1]:output)
                            gate: 1.0, in_: 20.0, out: 0.0
                {session.contexts[1]!r}
                """
            )


@pytest.mark.parametrize(
    "online, expectation",
    [
        (False, pytest.raises(RuntimeError)),
        (True, does_not_raise()),
    ],
)
@pytest.mark.asyncio
async def test_Session_delete_context(
    expectation, online: bool, session: Session
) -> None:
    # Pre-conditions
    if online:
        await session.boot()
    await session.add_context()
    # Operation
    await session.delete_context(session.contexts[0])
    # Post-conditions
    assert len(session.contexts) == 1
    assert len(session.mixers) == 0
    with expectation:
        assert await session.dump_tree() == normalize(
            f"""
            {session.contexts[0]!r}
            """
        )


@pytest.mark.parametrize(
    "online, expectation",
    [
        (False, pytest.raises(RuntimeError)),
        (True, does_not_raise()),
    ],
)
@pytest.mark.asyncio
async def test_Session_set_mixer_context(
    expectation, online: bool, session: Session
) -> None:
    # Pre-conditions
    if online:
        await session.boot()
    mixer = await session.add_mixer()
    await session.add_context()
    # Operation
    await session.set_mixer_context(mixer=mixer, context=session.contexts[1])
    # Post-conditions
    assert len(session.contexts) == 2
    assert len(session.mixers) == 2
    with expectation:
        assert await session.dump_tree() == normalize(
            f"""
            {session.contexts[0]!r}
                NODE TREE 1000 group (session.mixers[0]:group)
                    1001 group (session.mixers[0]:tracks)
                        1004 group (session.mixers[0].tracks[0]:group)
                            1005 group (session.mixers[0].tracks[0]:tracks)
                            1006 channel-strip-2 (session.mixers[0].tracks[0]:channel_strip)
                                active: 1.0, bus: 18.0, gain: 0.0, gate: 1.0
                            1007 patch-cable-2 (session.mixers[0].tracks[0]:output)
                                gate: 1.0, in_: 18.0, out: 18.0
                    1002 channel-strip-2 (session.mixers[0]:channel_strip)
                        active: 1.0, bus: 16.0, gain: 0.0, gate: 1.0
                    1003 patch-cable-2 (session.mixers[0]:output)
                        gate: 1.0, in_: 16.0, out: 0.0
            {session.contexts[1]!r}
                NODE TREE 1000 group (session.mixers[1]:group)
                    1001 group (session.mixers[1]:tracks)
                        1004 group (session.mixers[1].tracks[0]:group)
                            1005 group (session.mixers[1].tracks[0]:tracks)
                            1006 channel-strip-2 (session.mixers[1].tracks[0]:channel_strip)
                                active: 1.0, bus: 18.0, gain: 0.0, gate: 1.0
                            1007 patch-cable-2 (session.mixers[1].tracks[0]:output)
                                gate: 1.0, in_: 18.0, out: 18.0
                    1002 channel-strip-2 (session.mixers[1]:channel_strip)
                        active: 1.0, bus: 16.0, gain: 0.0, gate: 1.0
                    1003 patch-cable-2 (session.mixers[1]:output)
                        gate: 1.0, in_: 16.0, out: 0.0
            """
        )
    # Operation
    await session.set_mixer_context(
        mixer=session.mixers[0], context=session.contexts[1]
    )
    # Post-conditions
    with expectation:
        assert await session.dump_tree() == normalize(
            f"""
            {session.contexts[0]!r}
            {session.contexts[1]!r}
                NODE TREE 1000 group (session.mixers[1]:group)
                    1001 group (session.mixers[1]:tracks)
                        1004 group (session.mixers[1].tracks[0]:group)
                            1005 group (session.mixers[1].tracks[0]:tracks)
                            1006 channel-strip-2 (session.mixers[1].tracks[0]:channel_strip)
                                active: 1.0, bus: 18.0, gain: 0.0, gate: 1.0
                            1007 patch-cable-2 (session.mixers[1].tracks[0]:output)
                                gate: 1.0, in_: 18.0, out: 18.0
                    1002 channel-strip-2 (session.mixers[1]:channel_strip)
                        active: 1.0, bus: 16.0, gain: 0.0, gate: 1.0
                    1003 patch-cable-2 (session.mixers[1]:output)
                        gate: 1.0, in_: 16.0, out: 0.0
                NODE TREE 1008 group (session.mixers[0]:group)
                    1009 group (session.mixers[0]:tracks)
                        1012 group (session.mixers[0].tracks[0]:group)
                            1013 group (session.mixers[0].tracks[0]:tracks)
                            1014 channel-strip-2 (session.mixers[0].tracks[0]:channel_strip)
                                active: 1.0, bus: 22.0, gain: 0.0, gate: 1.0
                            1015 patch-cable-2 (session.mixers[0].tracks[0]:output)
                                gate: 1.0, in_: 22.0, out: 22.0
                    1010 channel-strip-2 (session.mixers[0]:channel_strip)
                        active: 1.0, bus: 20.0, gain: 0.0, gate: 1.0
                    1011 patch-cable-2 (session.mixers[0]:output)
                        gate: 1.0, in_: 20.0, out: 0.0
            """
        )
