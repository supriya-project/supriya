from uuid import UUID

from supriya.xdaw import CueTrack, Target


def test_1():
    cue_track = CueTrack()
    assert cue_track.application is None
    assert cue_track.channel_count == 2
    assert cue_track.effective_channel_count == 2
    assert cue_track.context is None
    assert cue_track.graph_order == ()
    assert cue_track.name is None
    assert cue_track.parent is None
    assert cue_track.provider is None
    assert isinstance(cue_track.receive_target, Target)
    assert isinstance(cue_track.send_target, Target)
    assert isinstance(cue_track.uuid, UUID)
    assert len(cue_track.devices) == 0
    assert len(cue_track.postfader_sends) == 0
    assert len(cue_track.prefader_sends) == 0
