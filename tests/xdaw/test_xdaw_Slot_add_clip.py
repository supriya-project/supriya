from supriya.xdaw import Application, Clip


def test_1():
    application = Application()
    application.add_scene()
    context = application.add_context()
    track = context.add_track()
    assert track.slots[0].clip is None
    clip = track.slots[0].add_clip()
    assert isinstance(clip, Clip)
    assert clip.parent is track.slots[0]
    assert track.slots[0].clip is clip


def test_2():
    """
    Replace existing clip
    """
    application = Application()
    application.add_scene()
    context = application.add_context()
    track = context.add_track()
    clip_one = track.slots[0].add_clip()
    clip_two = track.slots[0].add_clip()
    assert clip_two is track.slots[0].clip
    assert clip_one not in track.slots[0]
    assert clip_one.parent is None
