import pytest

import supriya
from supriya.osc import OscBundle, OscMessage


@pytest.fixture(autouse=True)
def shutdown_sync_servers(shutdown_scsynth):
    pass


@pytest.fixture
def server(persistent_server):
    persistent_server.reset()
    persistent_server.add_synthdef(supriya.assets.synthdefs.default)
    yield persistent_server


def test_synth_pause_unpause(server):
    synth = supriya.realtime.Synth().allocate(server)
    assert not synth.is_paused
    with server.osc_protocol.capture() as transcript:
        synth.pause()
    assert [(_.label, _.message) for _ in transcript] == [
        ("S", OscMessage("/n_run", 1000, 0))
    ]
    assert synth.is_paused
    with server.osc_protocol.capture() as transcript:
        synth.pause()
    assert list(transcript) == []
    assert synth.is_paused
    with server.osc_protocol.capture() as transcript:
        synth.unpause()
    assert [(_.label, _.message) for _ in transcript] == [
        ("S", OscMessage("/n_run", 1000, 1))
    ]
    assert not synth.is_paused
    with server.osc_protocol.capture() as transcript:
        synth.unpause()
    assert list(transcript) == []
    assert not synth.is_paused


def test_group_pause_unpause(server):
    group = supriya.realtime.Group().allocate(server)
    assert not group.is_paused
    with server.osc_protocol.capture() as transcript:
        group.pause()
    assert [(_.label, _.message) for _ in transcript] == [
        ("S", OscMessage("/n_run", 1000, 0))
    ]
    assert group.is_paused
    with server.osc_protocol.capture() as transcript:
        group.pause()
    assert list(transcript) == []
    assert group.is_paused
    with server.osc_protocol.capture() as transcript:
        group.unpause()
    assert [(_.label, _.message) for _ in transcript] == [
        ("S", OscMessage("/n_run", 1000, 1))
    ]
    assert not group.is_paused
    with server.osc_protocol.capture() as transcript:
        group.unpause()
    assert list(transcript) == []
    assert not group.is_paused


def test_synth_allocate_free_paused(server):
    synth = supriya.realtime.Synth(synthdef=supriya.assets.synthdefs.test)
    synth.pause()
    assert synth.is_paused
    with server.osc_protocol.capture() as transcript:
        synth.allocate(server)
    bundle = OscBundle(
        contents=(
            OscMessage("/s_new", "test", 1000, 0, 1),
            OscMessage("/n_run", 1000, 0),
        )
    )
    assert [(_.label, _.message) for _ in transcript] == [
        ("S", OscMessage("/d_recv", supriya.assets.synthdefs.test.compile(), bundle)),
        ("R", OscMessage("/n_go", 1000, 1, -1, -1, 0)),
        ("R", OscMessage("/n_off", 1000, 1, -1, -1, 0)),
        ("R", OscMessage("/done", "/d_recv")),
    ]
    assert synth.is_paused
    with server.osc_protocol.capture() as transcript:
        synth.free()
    assert [(_.label, _.message) for _ in transcript] == [
        ("S", OscMessage("/n_free", 1000))
    ]
    assert synth.is_paused
    synth.unpause()
    assert not synth.is_paused


def test_group_allocate_paused(server):
    group = supriya.realtime.Group()
    group.pause()
    assert group.is_paused
    with server.osc_protocol.capture() as transcript:
        group.allocate(server)
    assert [(_.label, _.message) for _ in transcript] == [
        (
            "S",
            OscBundle(
                contents=(
                    OscMessage("/g_new", 1000, 0, 1),
                    OscMessage("/n_run", 1000, 0),
                    OscMessage("/sync", 0),
                )
            ),
        ),
        ("R", OscMessage("/n_go", 1000, 1, -1, -1, 1, -1, -1)),
        ("R", OscMessage("/n_off", 1000, 1, -1, -1, 1, -1, -1)),
        ("R", OscMessage("/synced", 0)),
    ]
    assert group.is_paused
    with server.osc_protocol.capture() as transcript:
        group.free()
    assert [(_.label, _.message) for _ in transcript] == [
        ("S", OscMessage("/n_free", 1000))
    ]
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
    with server.osc_protocol.capture() as transcript:
        group.allocate(server)
    assert [(_.label, _.message) for _ in transcript] == [
        (
            "S",
            OscBundle(
                contents=(
                    OscMessage("/g_new", 1000, 0, 1),
                    OscMessage("/s_new", "default", 1001, 0, 1000),
                    OscMessage("/g_new", 1002, 3, 1001),
                    OscMessage("/s_new", "default", 1003, 0, 1002),
                    OscMessage("/n_run", 1001, 0, 1003, 0),
                    OscMessage("/sync", 0),
                )
            ),
        ),
        ("R", OscMessage("/n_go", 1000, 1, -1, -1, 1, -1, -1)),
        ("R", OscMessage("/n_go", 1001, 1000, -1, -1, 0)),
        ("R", OscMessage("/n_go", 1002, 1000, 1001, -1, 1, -1, -1)),
        ("R", OscMessage("/n_go", 1003, 1002, -1, -1, 0)),
        ("R", OscMessage("/n_off", 1001, 1000, -1, 1002, 0)),
        ("R", OscMessage("/n_off", 1003, 1002, -1, -1, 0)),
        ("R", OscMessage("/synced", 0)),
    ]
    assert not group.is_paused
    assert group[0].is_paused
    assert not group[1].is_paused
    assert group[1][0].is_paused
    with server.osc_protocol.capture() as transcript:
        group.free()
    assert [(_.label, _.message) for _ in transcript] == [
        ("S", OscMessage("/n_free", 1000))
    ]
    assert not group.is_paused
    assert group[0].is_paused
    assert not group[1].is_paused
    assert group[1][0].is_paused
