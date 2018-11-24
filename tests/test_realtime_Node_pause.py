import supriya


def test_synth_pause_unpause(server):
    synth = supriya.realtime.Synth().allocate()
    assert not synth.is_paused
    with server.osc_io.capture() as transcript:
        synth.pause()
    assert list(transcript) == [("S", supriya.osc.OscMessage(12, 1000, 0))]
    assert synth.is_paused
    with server.osc_io.capture() as transcript:
        synth.pause()
    assert list(transcript) == []
    assert synth.is_paused
    with server.osc_io.capture() as transcript:
        synth.unpause()
    assert list(transcript) == [("S", supriya.osc.OscMessage(12, 1000, 1))]
    assert not synth.is_paused
    with server.osc_io.capture() as transcript:
        synth.unpause()
    assert list(transcript) == []
    assert not synth.is_paused


def test_group_pause_unpause(server):
    group = supriya.realtime.Group().allocate()
    assert not group.is_paused
    with server.osc_io.capture() as transcript:
        group.pause()
    assert list(transcript) == [("S", supriya.osc.OscMessage(12, 1000, 0))]
    assert group.is_paused
    with server.osc_io.capture() as transcript:
        group.pause()
    assert list(transcript) == []
    assert group.is_paused
    with server.osc_io.capture() as transcript:
        group.unpause()
    assert list(transcript) == [("S", supriya.osc.OscMessage(12, 1000, 1))]
    assert not group.is_paused
    with server.osc_io.capture() as transcript:
        group.unpause()
    assert list(transcript) == []
    assert not group.is_paused


def test_synth_allocate_free_paused(server):
    synth = supriya.realtime.Synth(synthdef=supriya.assets.synthdefs.test)
    synth.pause()
    assert synth.is_paused
    with server.osc_io.capture() as transcript:
        synth.allocate()
    bundle = supriya.osc.OscBundle(
        contents=(
            supriya.osc.OscMessage(9, "test", 1000, 0, 1),
            supriya.osc.OscMessage(12, 1000, 0),
        )
    )
    assert list(transcript) == [
        (
            "S",
            supriya.osc.OscMessage(5, supriya.assets.synthdefs.test.compile(), bundle),
        ),
        ("R", supriya.osc.OscMessage("/n_go", 1000, 1, -1, -1, 0)),
        ("R", supriya.osc.OscMessage("/n_off", 1000, 1, -1, -1, 0)),
        ("R", supriya.osc.OscMessage("/done", "/d_recv")),
    ]
    assert synth.is_paused
    with server.osc_io.capture() as transcript:
        synth.free()
    assert list(transcript) == [("S", supriya.osc.OscMessage(11, 1000))]
    assert synth.is_paused
    synth.unpause()
    assert not synth.is_paused


def test_group_allocate_paused(server):
    group = supriya.realtime.Group()
    group.pause()
    assert group.is_paused
    with server.osc_io.capture() as transcript:
        group.allocate()
    assert list(transcript) == [
        (
            "S",
            supriya.osc.OscBundle(
                contents=(
                    supriya.osc.OscMessage(21, 1000, 0, 1),
                    supriya.osc.OscMessage(12, 1000, 0),
                    supriya.osc.OscMessage(52, 0),
                )
            ),
        ),
        ("R", supriya.osc.OscMessage("/n_go", 1000, 1, -1, -1, 1, -1, -1)),
        ("R", supriya.osc.OscMessage("/n_off", 1000, 1, -1, -1, 1, -1, -1)),
        ("R", supriya.osc.OscMessage("/synced", 0)),
    ]
    assert group.is_paused
    with server.osc_io.capture() as transcript:
        group.free()
    assert list(transcript) == [("S", supriya.osc.OscMessage(11, 1000))]
    assert group.is_paused
    group.unpause()
    assert not group.is_paused


def test_group_allocate_nested_paused(server):
    group = supriya.realtime.Group(
        [supriya.realtime.Synth(), supriya.realtime.Group([supriya.realtime.Synth()])]
    )
    group[0].pause()
    group[1][0].pause()
    assert not group.is_paused
    assert group[0].is_paused
    assert not group[1].is_paused
    assert group[1][0].is_paused
    with server.osc_io.capture() as transcript:
        group.allocate()
    assert list(transcript) == [
        (
            "S",
            supriya.osc.OscBundle(
                contents=(
                    supriya.osc.OscMessage(21, 1000, 0, 1),
                    supriya.osc.OscMessage(9, "default", 1001, 0, 1000),
                    supriya.osc.OscMessage(21, 1002, 3, 1001),
                    supriya.osc.OscMessage(9, "default", 1003, 0, 1002),
                    supriya.osc.OscMessage(12, 1001, 0, 1003, 0),
                    supriya.osc.OscMessage(52, 0),
                )
            ),
        ),
        ("R", supriya.osc.OscMessage("/n_go", 1000, 1, -1, -1, 1, -1, -1)),
        ("R", supriya.osc.OscMessage("/n_go", 1001, 1000, -1, -1, 0)),
        ("R", supriya.osc.OscMessage("/n_go", 1002, 1000, 1001, -1, 1, -1, -1)),
        ("R", supriya.osc.OscMessage("/n_go", 1003, 1002, -1, -1, 0)),
        ("R", supriya.osc.OscMessage("/n_off", 1001, 1000, -1, 1002, 0)),
        ("R", supriya.osc.OscMessage("/n_off", 1003, 1002, -1, -1, 0)),
        ("R", supriya.osc.OscMessage("/synced", 0)),
    ]
    assert not group.is_paused
    assert group[0].is_paused
    assert not group[1].is_paused
    assert group[1][0].is_paused
    with server.osc_io.capture() as transcript:
        group.free()
    assert list(transcript) == [("S", supriya.osc.OscMessage(11, 1000))]
    assert not group.is_paused
    assert group[0].is_paused
    assert not group[1].is_paused
    assert group[1][0].is_paused
