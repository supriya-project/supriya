from uuid import UUID

from supriya.xdaw import Context, CueTrack, MasterTrack


def test_1():
    context = Context()
    assert context.application is None
    assert context.graph_order == ()
    assert context.name is None
    assert context.provider is None
    assert isinstance(context.cue_track, CueTrack)
    assert isinstance(context.master_track, MasterTrack)
    assert isinstance(context.uuid, UUID)
    assert len(context.tracks) == 0
