from uuid import UUID

from supriya.xdaw import MasterTrack, Target


def test_1():
    master_track = MasterTrack()
    assert isinstance(master_track.receive_target, Target)
    assert isinstance(master_track.send_target, Target)
    assert isinstance(master_track.uuid, UUID)
    assert len(master_track.devices) == 0
    assert len(master_track.postfader_sends) == 0
    assert len(master_track.prefader_sends) == 0
    assert master_track.application is None
    assert master_track.channel_count is None
    assert master_track.effective_channel_count == 2
    assert master_track.context is None
    assert master_track.graph_order == ()
    assert master_track.name is None
    assert master_track.parent is None
    assert master_track.provider is None
