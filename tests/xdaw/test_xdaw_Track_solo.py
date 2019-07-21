import time

import pytest

from supriya.osc import OscBundle, OscMessage
from supriya.xdaw import Application, AudioEffect, Track


@pytest.mark.parametrize(
    "track_names, levels",
    [
        (["a"], [1, 0, 0, 0, 0, 0, 0, 0]),
        (["b"], [0, 1, 1, 1, 0, 0, 0, 0]),
        (["ba"], [0, 1, 1, 0, 0, 0, 0, 0]),
        (["bb"], [0, 1, 0, 1, 0, 0, 0, 0]),
        (["c"], [0, 0, 0, 0, 1, 1, 1, 1]),
        (["ca"], [0, 0, 0, 0, 1, 1, 0, 0]),
        (["cb"], [0, 0, 0, 0, 1, 0, 1, 1]),
        (["cba"], [0, 0, 0, 0, 1, 0, 1, 1]),
    ],
)
def test_levels(track_mute_solo_application, track_names, levels):
    track_mute_solo_application.boot()
    for track_name in track_names:
        track = track_mute_solo_application.primary_context[track_name]
        track.solo()
    time.sleep(0.2)
    assert [
        int(_)
        for _ in track_mute_solo_application.primary_context.master_track.rms_levels[
            "input"
        ]
    ] == levels


@pytest.mark.parametrize(
    "soloed_track_names, muted_track_names",
    [
        (["a"], ["b", "ba", "bb", "c", "ca", "cb", "cba"]),
        (["b"], ["a", "c", "ca", "cb", "cba"]),
        (["ba"], ["a", "bb", "c", "ca", "cb", "cba"]),
        (["bb"], ["a", "ba", "c", "ca", "cb", "cba"]),
        (["c"], ["a", "b", "ba", "bb"]),
        (["ca"], ["a", "b", "ba", "bb", "cb", "cba"]),
        (["cb"], ["a", "b", "ba", "bb", "ca"]),
        (["cba"], ["a", "b", "ba", "bb", "ca"]),
    ],
)
def test_transcript(track_mute_solo_application, soloed_track_names, muted_track_names):
    track_mute_solo_application.boot()
    for soloed_track_name in soloed_track_names:
        soloed_track = track_mute_solo_application.primary_context[soloed_track_name]
        with track_mute_solo_application.primary_context.provider.server.osc_io.capture() as transcript:
            soloed_track.solo()
        osc_messages = []
        for muted_track_name in muted_track_names:
            muted_track = track_mute_solo_application.primary_context[muted_track_name]
            osc_messages.append(
                OscMessage(
                    15, muted_track.node_proxies["output"].identifier, "active", 0
                )
            )
        assert len(transcript.sent_messages) == 1
        _, message = transcript.sent_messages[0]
        assert message == OscBundle(contents=osc_messages)


@pytest.mark.parametrize("booted", [True, False])
@pytest.mark.parametrize(
    "track_names, expected",
    [
        (["a"], [1, 0, 0, 0, 0, 0, 0, 0]),
        (["b"], [0, 1, 1, 1, 0, 0, 0, 0]),
        (["ba"], [0, 1, 1, 0, 0, 0, 0, 0]),
        (["bb"], [0, 1, 0, 1, 0, 0, 0, 0]),
        (["c"], [0, 0, 0, 0, 1, 1, 1, 1]),
        (["ca"], [0, 0, 0, 0, 1, 1, 0, 0]),
        (["cb"], [0, 0, 0, 0, 1, 0, 1, 1]),
        (["cba"], [0, 0, 0, 0, 1, 0, 1, 1]),
    ],
)
def test_is_active(track_mute_solo_application, booted, track_names, expected):
    if booted:
        track_mute_solo_application.boot()
    for track_name in track_names:
        track = track_mute_solo_application.primary_context[track_name]
        track.solo()
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
def test_is_soloed(track_mute_solo_application, booted, track_names, expected):
    if booted:
        track_mute_solo_application.boot()
    for track_name in track_names:
        track = track_mute_solo_application.primary_context[track_name]
        track.solo()
    all_tracks = list(
        track_mute_solo_application.primary_context.depth_first(prototype=Track)
    )
    actual = [bool(track.is_soloed) for track in all_tracks]
    assert actual == [bool(x) for x in expected]


def test_stacked():
    application = Application()
    application.add_context().add_track(name="a").add_track(name="b").add_track(
        name="c"
    )
    application.boot()
    application.primary_context["a"].solo()
    with application.primary_context.provider.server.osc_io.capture() as transcript:
        application.primary_context["b"].solo()
        application.primary_context["c"].solo()
    assert not len(transcript.sent_messages)


def test_repeat():
    application = Application()
    application.add_context().add_track(name="a")
    application.boot()
    application.primary_context["a"].solo()
    with application.primary_context.provider.server.osc_io.capture() as transcript:
        application.primary_context["a"].solo()
    assert not len(transcript.sent_messages)


def test_move(dc_synthdef_factory):
    application = Application()
    context = application.add_context()
    track_one = context.add_track(name="one")
    track_one.add_device(
        AudioEffect, synthdef=dc_synthdef_factory, synthdef_kwargs=dict(index=0)
    )
    application.boot()
    time.sleep(0.2)
    assert context.master_track.rms_levels["input"] == (1.0, 0.0)
    track_two = Track(name="two")
    track_two.add_device(
        AudioEffect, synthdef=dc_synthdef_factory, synthdef_kwargs=dict(index=1)
    )
    track_two.solo()
    track_two.move(context, 1)
    time.sleep(0.2)
    assert not track_one.is_active
    assert context.master_track.rms_levels["input"] == (0.0, 1.0)
    track_one.move(track_two, 0)
    time.sleep(0.2)
    assert track_one.is_active
    assert context.master_track.rms_levels["input"] == (1.0, 1.0)
    track_one.move(context, 0)
    time.sleep(0.2)
    assert not track_one.is_active
    assert context.master_track.rms_levels["input"] == (0.0, 1.0)
    track_two.delete()
    time.sleep(0.2)
    assert track_one.is_active
    assert context.master_track.rms_levels["input"] == (1.0, 0.0)


def test_exclusivity():
    application = Application()
    context = application.add_context()
    track_a = context.add_track(name="a")
    track_b = context.add_track(name="b")
    track_c = context.add_track(name="c")
    track_d = context.add_track(name="d")
    track_a.solo()
    assert [track.is_active for track in context.tracks] == [True, False, False, False]
    track_b.solo(exclusive=False)
    assert [track.is_active for track in context.tracks] == [True, True, False, False]
    track_c.solo()
    assert [track.is_active for track in context.tracks] == [False, False, True, False]
    track_d.solo(exclusive=False)
    assert [track.is_active for track in context.tracks] == [False, False, True, True]
