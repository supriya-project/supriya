from supriya.xdaw import Application


def test_repeat():
    """
    Unmuting more than once is a no-op
    """
    application = Application()
    context = application.add_context()
    context.add_track(name="a")
    application.boot()
    context["a"].mute()
    context["a"].unmute()
    with context.provider.server.osc_io.capture() as transcript:
        context["a"].unmute()
    assert not len(transcript.sent_messages)


def test_stacked():
    """
    Unmuting while a parent is muted is a no-op
    """
    application = Application()
    context = application.add_context()
    context.add_track(name="a").add_track(name="b").add_track(name="c")
    application.boot()
    context["a"].mute()
    context["b"].mute()
    context["c"].mute()
    with context.provider.server.osc_io.capture() as transcript:
        context["c"].unmute()
        context["b"].unmute()
    assert not len(transcript.sent_messages)
    with context.provider.server.osc_io.capture() as transcript:
        context["a"].unmute()
    assert len(transcript.sent_messages) == 1
    _, message = transcript.sent_messages[0]
    # Unmuting the root-most parent unmutes all children at once
    assert message.to_list() == [
        None,
        [
            [15, track.node_proxies["output"].identifier, "active", 1]
            for track in [context["a"], context["b"], context["c"]]
        ],
    ]
