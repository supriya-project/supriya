import time

import pytest

from supriya.osc import OscBundle, OscMessage
from supriya.xdaw import Application, AudioEffect, Track


@pytest.mark.parametrize(
    "track_names, levels",
    [
        (["a"], [0, 1, 1, 1, 1, 1, 1, 1]),
        (["b"], [1, 0, 0, 0, 1, 1, 1, 1]),
        (["ba"], [1, 1, 0, 1, 1, 1, 1, 1]),
        (["bb"], [1, 1, 1, 0, 1, 1, 1, 1]),
        (["c"], [1, 1, 1, 1, 0, 0, 0, 0]),
        (["ca"], [1, 1, 1, 1, 1, 0, 1, 1]),
        (["cb"], [1, 1, 1, 1, 1, 1, 0, 0]),
        (["cba"], [1, 1, 1, 1, 1, 1, 1, 0]),
    ],
)
def test_levels(track_mute_solo_application, track_names, levels):
    track_mute_solo_application.boot()
    for track_name in track_names:
        track = track_mute_solo_application.primary_context[track_name]
        track.mute()
    time.sleep(0.2)
    assert [
        int(_)
        for _ in track_mute_solo_application.primary_context.master_track.rms_levels[
            "input"
        ]
    ] == levels


@pytest.mark.parametrize(
    "track_names", [["a"], ["b"], ["ba"], ["bb"], ["c"], ["ca"], ["cb"], ["cba"]]
)
def test_transcript(track_mute_solo_application, track_names):
    track_mute_solo_application.boot()
    for track_name in track_names:
        track = track_mute_solo_application.primary_context[track_name]
        with track_mute_solo_application.primary_context.provider.server.osc_io.capture() as transcript:
            track.mute()
        affected_tracks = [track, *track.depth_first(prototype=Track)]
        assert len(transcript.sent_messages) == 1
        _, message = transcript.sent_messages[0]
        assert message == OscBundle(
            contents=[
                OscMessage(15, x.node_proxies["output"].identifier, "active", 0)
                for x in affected_tracks
            ]
        )


@pytest.mark.parametrize("booted", [True, False])
@pytest.mark.parametrize(
    "track_names, expected",
    [
        (["a"], [0, 1, 1, 1, 1, 1, 1, 1]),
        (["b"], [1, 0, 0, 0, 1, 1, 1, 1]),
        (["ba"], [1, 1, 0, 1, 1, 1, 1, 1]),
        (["bb"], [1, 1, 1, 0, 1, 1, 1, 1]),
        (["c"], [1, 1, 1, 1, 0, 0, 0, 0]),
        (["ca"], [1, 1, 1, 1, 1, 0, 1, 1]),
        (["cb"], [1, 1, 1, 1, 1, 1, 0, 0]),
        (["cba"], [1, 1, 1, 1, 1, 1, 1, 0]),
    ],
)
def test_is_active(track_mute_solo_application, booted, track_names, expected):
    if booted:
        track_mute_solo_application.boot()
    for track_name in track_names:
        track = track_mute_solo_application.primary_context[track_name]
        track.mute()
    all_tracks = list(
        track_mute_solo_application.primary_context.depth_first(prototype=Track)
    )
    actual = [bool(track.is_active) for track in all_tracks]
    assert actual == [bool(x) for x in expected]


@pytest.mark.parametrize("booted", [True, False])
@pytest.mark.parametrize(
    "track_names, expected",
    [
        (["a"], [1, 0, 0, 0, 0, 0, 0, 0]),
        (["b"], [0, 1, 0, 0, 0, 0, 0, 0]),
        (["ba"], [0, 0, 1, 0, 0, 0, 0, 0]),
        (["bb"], [0, 0, 0, 1, 0, 0, 0, 0]),
        (["c"], [0, 0, 0, 0, 1, 0, 0, 0]),
        (["ca"], [0, 0, 0, 0, 0, 1, 0, 0]),
        (["cb"], [0, 0, 0, 0, 0, 0, 1, 0]),
        (["cba"], [0, 0, 0, 0, 0, 0, 0, 1]),
    ],
)
def test_is_muted(track_mute_solo_application, booted, track_names, expected):
    if booted:
        track_mute_solo_application.boot()
    for track_name in track_names:
        track = track_mute_solo_application.primary_context[track_name]
        track.mute()
    all_tracks = list(
        track_mute_solo_application.primary_context.depth_first(prototype=Track)
    )
    actual = [bool(track.is_muted) for track in all_tracks]
    assert actual == [bool(x) for x in expected]


def test_stacked():
    application = Application()
    application.add_context().add_track(name="a").add_track(name="b").add_track(
        name="c"
    )
    application.boot()
    application.primary_context["a"].mute()
    with application.primary_context.provider.server.osc_io.capture() as transcript:
        application.primary_context["b"].mute()
        application.primary_context["c"].mute()
    assert not len(transcript.sent_messages)


def test_repeat():
    application = Application()
    application.add_context().add_track(name="a")
    application.boot()
    application.primary_context["a"].mute()
    with application.primary_context.provider.server.osc_io.capture() as transcript:
        application.primary_context["a"].mute()
    assert not len(transcript.sent_messages)


def test_move(dc_index_synthdef_factory):
    application = Application()
    context = application.add_context()
    track_one = context.add_track(name="one")
    track_one.add_device(
        AudioEffect, synthdef=dc_index_synthdef_factory, synthdef_kwargs=dict(index=0)
    )
    application.boot()
    time.sleep(0.2)
    assert context.master_track.rms_levels["input"] == (1.0, 0.0)
    track_two = Track(name="two")
    track_two.add_device(
        AudioEffect, synthdef=dc_index_synthdef_factory, synthdef_kwargs=dict(index=1)
    )
    track_two.mute()
    track_two.move(context, 1)
    time.sleep(0.2)
    assert context.master_track.rms_levels["input"] == (1.0, 0.0)
    track_one.move(track_two, 0)
    time.sleep(0.2)
    assert not track_one.is_active
    assert context.master_track.rms_levels["input"] == (0.0, 0.0)
    track_one.move(context, 0)
    time.sleep(0.2)
    assert track_one.is_active
    assert context.master_track.rms_levels["input"] == (1.0, 0.0)
    track_two.delete()
    time.sleep(0.2)
    assert context.master_track.rms_levels["input"] == (1.0, 0.0)
