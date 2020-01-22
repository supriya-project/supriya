from supriya.xdaw import Application, Track


def test_1():
    application = Application()
    context_one = application.add_context()
    context_two = application.add_context()
    for context in context_one, context_two:
        context.add_track().add_track()
        context.add_track()
    for track in application.recurse(Track):
        assert len(application.scenes) == 0
        assert len(track.slots) == len(application.scenes)
    scene_one = application.add_scene()
    assert scene_one in application.scenes
    assert application.scenes.index(scene_one) == 0
    for track in application.recurse(Track):
        assert len(application.scenes) == 1
        assert len(track.slots) == len(application.scenes)
    scene_two = application.add_scene()
    assert scene_two in application.scenes
    assert application.scenes.index(scene_two) == 1
    for track in application.recurse(Track):
        assert len(application.scenes) == 2
        assert len(track.slots) == len(application.scenes)
