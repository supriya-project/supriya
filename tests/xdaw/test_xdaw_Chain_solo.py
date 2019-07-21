import time

import pytest

from supriya.osc import OscBundle, OscMessage
from supriya.xdaw import Application, AudioEffect, Chain, RackDevice


@pytest.mark.parametrize(
    "chain_names, levels",
    [
        (["outer/a/a"], [1, 0, 0, 0, 1, 1, 1, 1]),
        (["outer/a/b"], [0, 1, 1, 1, 1, 1, 1, 1]),
        (["inner/a/a"], [1, 1, 1, 0, 1, 1, 1, 1]),
        (["inner/a/b"], [1, 1, 0, 1, 1, 1, 1, 1]),
        (["outer/b/a"], [1, 1, 1, 1, 1, 0, 0, 0]),
        (["outer/b/b"], [1, 1, 1, 1, 0, 1, 1, 1]),
        (["inner/b/a"], [1, 1, 1, 1, 1, 1, 1, 0]),
        (["inner/b/b"], [1, 1, 1, 1, 1, 1, 0, 1]),
    ],
)
def test_levels(chain_mute_solo_application, chain_names, levels):
    chain_mute_solo_application.boot()
    for chain_name in chain_names:
        chain = chain_mute_solo_application.primary_context[chain_name]
        chain.solo()
    time.sleep(0.2)
    assert [
        int(_)
        for _ in chain_mute_solo_application.primary_context.master_track.rms_levels[
            "input"
        ]
    ] == levels


@pytest.mark.parametrize(
    "soloed_chain_names, muted_chain_names",
    [
        (["outer/a/a"], ["outer/a/b"]),
        (["outer/a/b"], ["outer/a/a"]),
        (["inner/a/a"], ["inner/a/b"]),
        (["inner/a/b"], ["inner/a/a"]),
        (["outer/b/a"], ["outer/b/b"]),
        (["outer/b/b"], ["outer/b/a"]),
        (["inner/b/a"], ["inner/b/b"]),
        (["inner/b/b"], ["inner/b/a"]),
    ],
)
def test_transcript(chain_mute_solo_application, soloed_chain_names, muted_chain_names):
    chain_mute_solo_application.boot()
    for soloed_chain_name in soloed_chain_names:
        soloed_chain = chain_mute_solo_application.primary_context[soloed_chain_name]
        with chain_mute_solo_application.primary_context.provider.server.osc_io.capture() as transcript:
            soloed_chain.solo()
        osc_messages = []
        for muted_chain_name in muted_chain_names:
            muted_chain = chain_mute_solo_application.primary_context[muted_chain_name]
            osc_messages.append(
                OscMessage(
                    15, muted_chain.node_proxies["output"].identifier, "active", 0
                )
            )
        assert len(transcript.sent_messages) == 1
        _, message = transcript.sent_messages[0]
        assert message == OscBundle(contents=osc_messages)


@pytest.mark.parametrize("booted", [True, False])
@pytest.mark.parametrize(
    "chain_names, expected",
    [
        (["outer/a/a"], [1, 0, 1, 1, 1, 1, 1, 1]),
        (["outer/a/b"], [0, 1, 1, 1, 1, 1, 1, 1]),
        (["inner/a/a"], [1, 1, 1, 0, 1, 1, 1, 1]),
        (["inner/a/b"], [1, 1, 0, 1, 1, 1, 1, 1]),
        (["outer/b/a"], [1, 1, 1, 1, 1, 0, 1, 1]),
        (["outer/b/b"], [1, 1, 1, 1, 0, 1, 1, 1]),
        (["inner/b/a"], [1, 1, 1, 1, 1, 1, 1, 0]),
        (["inner/b/b"], [1, 1, 1, 1, 1, 1, 0, 1]),
    ],
)
def test_is_active(chain_mute_solo_application, booted, chain_names, expected):
    if booted:
        chain_mute_solo_application.boot()
    for chain_name in chain_names:
        chain = chain_mute_solo_application.primary_context[chain_name]
        chain.solo()
    all_chains = list(
        chain_mute_solo_application.primary_context.depth_first(prototype=Chain)
    )
    actual = [bool(chain.is_active) for chain in all_chains]
    assert actual == [bool(x) for x in expected]


@pytest.mark.parametrize("booted", [True, False])
@pytest.mark.parametrize(
    "chain_names, expected",
    [
        (["outer/a/a"], [1, 0, 0, 0, 0, 0, 0, 0]),
        (["outer/a/b"], [0, 1, 0, 0, 0, 0, 0, 0]),
        (["inner/a/a"], [0, 0, 1, 0, 0, 0, 0, 0]),
        (["inner/a/b"], [0, 0, 0, 1, 0, 0, 0, 0]),
        (["outer/b/a"], [0, 0, 0, 0, 1, 0, 0, 0]),
        (["outer/b/b"], [0, 0, 0, 0, 0, 1, 0, 0]),
        (["inner/b/a"], [0, 0, 0, 0, 0, 0, 1, 0]),
        (["inner/b/b"], [0, 0, 0, 0, 0, 0, 0, 1]),
    ],
)
def test_is_soloed(chain_mute_solo_application, booted, chain_names, expected):
    if booted:
        chain_mute_solo_application.boot()
    for chain_name in chain_names:
        chain = chain_mute_solo_application.primary_context[chain_name]
        chain.solo()
    all_chains = list(
        chain_mute_solo_application.primary_context.depth_first(prototype=Chain)
    )
    actual = [bool(chain.is_soloed) for chain in all_chains]
    assert actual == [bool(x) for x in expected]


def test_repeat(chain_mute_solo_application):
    chain_mute_solo_application.boot()
    chain_mute_solo_application.primary_context["outer/a/a"].solo()
    with chain_mute_solo_application.primary_context.provider.server.osc_io.capture() as transcript:
        chain_mute_solo_application.primary_context["outer/a/a"].solo()
    assert not len(transcript.sent_messages)


def test_move(dc_synthdef_factory):
    application = Application(channel_count=4)
    context = application.add_context()
    master_track = context.master_track
    track = context.add_track()
    rack_one = track.add_device(RackDevice, name="one")
    rack_two = track.add_device(RackDevice, name="one")
    chain_a = rack_one.add_chain(name="a")
    chain_b = rack_one.add_chain(name="b")
    chain_c = rack_two.add_chain(name="c")
    chain_d = rack_two.add_chain(name="d")
    for i, chain in enumerate([chain_a, chain_b, chain_c, chain_d]):
        chain.add_device(
            AudioEffect, synthdef=dc_synthdef_factory, synthdef_kwargs=dict(index=i)
        )
    application.boot()
    time.sleep(0.2)
    assert [int(_) for _ in master_track.rms_levels["input"]] == [1, 1, 1, 1]
    chain_b.solo()
    time.sleep(0.2)
    assert [int(_) for _ in master_track.rms_levels["input"]] == [0, 1, 1, 1]
    chain_b.move(rack_two, 0)
    time.sleep(0.2)
    assert [int(_) for _ in master_track.rms_levels["input"]] == [1, 1, 0, 0]
    chain_b.move(rack_one, 0)
    time.sleep(0.2)
    assert [int(_) for _ in master_track.rms_levels["input"]] == [0, 1, 1, 1]
    chain_b.delete()
    time.sleep(0.2)
    assert [int(_) for _ in master_track.rms_levels["input"]] == [1, 0, 1, 1]


def test_exclusivity():
    application = Application()
    context = application.add_context()
    track = context.add_track()
    rack = track.add_device(RackDevice)
    chain_a = rack.add_chain(name="a")
    chain_b = rack.add_chain(name="b")
    chain_c = rack.add_chain(name="c")
    chain_d = rack.add_chain(name="d")
    chain_a.solo()
    assert [chain.is_active for chain in rack.chains] == [True, False, False, False]
    chain_b.solo(exclusive=False)
    assert [chain.is_active for chain in rack.chains] == [True, True, False, False]
    chain_c.solo()
    assert [chain.is_active for chain in rack.chains] == [False, False, True, False]
    chain_d.solo(exclusive=False)
    assert [chain.is_active for chain in rack.chains] == [False, False, True, True]
