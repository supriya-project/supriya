import pytest
from uqbar.strings import normalize

from supriya.mixers import Session
from supriya.mixers.mixers import Mixer


@pytest.mark.asyncio
async def test_Mixer_add_track(mixer: Mixer, session: Session) -> None:
    # Pre-conditions
    await session.boot()
    # Operation
    await mixer.add_track()
    # Post-conditions
    assert str(await mixer.dump_tree()) == normalize(
        """
        NODE TREE 1000 group (session.mixers[0]:group)
            1001 group (session.mixers[0]:tracks)
                1004 group (session.mixers[0].tracks[0]:group)
                    1005 group (session.mixers[0].tracks[0]:tracks)
                    1006 channel-strip-2 (session.mixers[0].tracks[0]:channel_strip)
                        active: 1.0, bus: 18.0, gain: 0.0, gate: 1.0
                    1007 patch-cable-2 (session.mixers[0].tracks[0]:output)
                        gate: 1.0, in_: 18.0, out: 18.0
                1008 group (session.mixers[0].tracks[1]:group)
                    1009 group (session.mixers[0].tracks[1]:tracks)
                    1010 channel-strip-2 (session.mixers[0].tracks[1]:channel_strip)
                        active: 1.0, bus: 20.0, gain: 0.0, gate: 1.0
                    1011 patch-cable-2 (session.mixers[0].tracks[1]:output)
                        gate: 1.0, in_: 20.0, out: 20.0
            1002 channel-strip-2 (session.mixers[0]:channel_strip)
                active: 1.0, bus: 16.0, gain: 0.0, gate: 1.0
            1003 patch-cable-2 (session.mixers[0]:output)
                gate: 1.0, in_: 16.0, out: 0.0
        """
    )


@pytest.mark.asyncio
async def test_Mixer_delete(mixer: Mixer, session: Session) -> None:
    await mixer.delete()
