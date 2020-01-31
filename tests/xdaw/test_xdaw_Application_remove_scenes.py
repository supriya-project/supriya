from supriya.xdaw import Application


def test_1():
    application = Application()
    context_one = application.add_context()
    context_two = application.add_context()
    scenes = [application.add_scene() for _ in range(3)]
    all_slots = []
    for context in context_one, context_two:
        track_a = context.add_track()
        track_b = context.add_track()
        track_c = track_a.add_track()
        for track in [track_a, track_b, track_c]:
            all_slots.append((track, tuple(track.slots)))
    application.remove_scenes(scenes[2], scenes[0])
    assert len(application.scenes) == 1
    assert scenes[1] in application.scenes
    for track, slots in all_slots:
        assert len(track.slots) == 1
        assert slots[0].parent is None
        assert slots[2].parent is None
        assert slots[1] in track.slots
