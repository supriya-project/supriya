from supriya.xdaw import Application


def test_repeat():
    """
    Unsoloing more than once is a no-op
    """
    application = Application()
    context = application.add_context()
    context.add_track(name="a")
    context.add_track(name="b")
    application.boot()
    context["a"].solo()
    context["a"].unsolo()
    with context.provider.server.osc_io.capture() as transcript:
        context["a"].unsolo()
    assert not len(transcript.sent_messages)


def test_stacked():
    """
    Unsoloing while a parent is soloed is a no-op
    """
    application = Application()
    context = application.add_context()
    context.add_track(name="a").add_track(name="b").add_track(name="c")
    context.add_track(name="d")
    application.boot()
    context["a"].solo()
    context["b"].solo(exclusive=False)
    context["c"].solo(exclusive=False)
    with context.provider.server.osc_io.capture() as transcript:
        context["c"].unsolo(exclusive=True)
        context["b"].unsolo(exclusive=True)
    assert not len(transcript.sent_messages)
    with context.provider.server.osc_io.capture() as transcript:
        context["a"].unsolo()
    assert len(transcript.sent_messages) == 1
    _, message = transcript.sent_messages[0]
    # Unsoloing the root-most parent unsoloes muted tracks
    assert message.to_list() == [
        None,
        [
            [15, context["d"].node_proxies["output"].identifier, "active", 1]
        ]
    ]


def test_exclusivity():
    application = Application()
    context = application.add_context()
    track_a = context.add_track(name="a")
    track_b = context.add_track(name="b")
    track_c = context.add_track(name="c")
    track_d = context.add_track(name="d")
    track_a.solo()
    track_b.solo(exclusive=False)
    track_c.solo(exclusive=False)
    assert [track.is_active for track in context.tracks] == [True, True, True, False]
    track_a.unsolo(exclusive=True)
    assert [track.is_active for track in context.tracks] == [False, True, True, False]
    track_d.solo(exclusive=False)
    assert [track.is_active for track in context.tracks] == [False, True, True, True]
    track_b.unsolo()
    assert [track.is_active for track in context.tracks] == [True, True, True, True]
