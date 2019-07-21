from uuid import UUID

from supriya.xdaw import Target, Track


def test_1():
    track = Track()
    assert isinstance(track.receive_target, Target)
    assert isinstance(track.send_target, Target)
    assert isinstance(track.uuid, UUID)
    assert len(track.devices) == 0
    assert len(track.postfader_sends) == 1
    assert len(track.prefader_sends) == 0
    assert len(track.tracks) == 0
    assert not track.is_cued
    assert not track.is_muted
    assert not track.is_soloed
    assert track.application is None
    assert track.channel_count is None
    assert track.effective_channel_count == 2
    assert track.context is None
    assert track.graph_order == ()
    assert track.is_active
    assert track.name is None
    assert track.parent is None
    assert track.provider is None
