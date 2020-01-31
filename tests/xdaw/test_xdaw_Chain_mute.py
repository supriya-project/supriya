import time

import pytest

from supriya.xdaw import Chain


@pytest.mark.parametrize(
    "chain_names, levels",
    [
        (["outer/a/a"], [0, 1, 1, 1, 1, 1, 1, 1]),
        (["outer/a/b"], [1, 0, 0, 0, 1, 1, 1, 1]),
        (["inner/a/a"], [1, 1, 0, 1, 1, 1, 1, 1]),
        (["inner/a/b"], [1, 1, 1, 0, 1, 1, 1, 1]),
        (["outer/b/a"], [1, 1, 1, 1, 0, 1, 1, 1]),
        (["outer/b/b"], [1, 1, 1, 1, 1, 0, 0, 0]),
        (["inner/b/a"], [1, 1, 1, 1, 1, 1, 0, 1]),
        (["inner/b/b"], [1, 1, 1, 1, 1, 1, 1, 0]),
    ],
)
def test_levels_nested(chain_mute_solo_application, chain_names, levels):
    chain_mute_solo_application.boot()
    for chain_name in chain_names:
        chain = chain_mute_solo_application.primary_context[chain_name]
        chain.mute()
    time.sleep(0.2)
    assert [
        int(_)
        for _ in chain_mute_solo_application.primary_context.master_track.rms_levels[
            "input"
        ]
    ] == levels


@pytest.mark.parametrize(
    "chain_names",
    [
        ["outer/a/a"],
        ["outer/a/b"],
        ["inner/a/a"],
        ["inner/a/b"],
        ["outer/b/a"],
        ["outer/b/b"],
        ["inner/b/a"],
        ["inner/b/b"],
    ],
)
def test_transcript(chain_mute_solo_application, chain_names):
    chain_mute_solo_application.boot()
    context = chain_mute_solo_application.primary_context
    for chain_name in chain_names:
        chain = context[chain_name]
        with context.provider.server.osc_protocol.capture() as transcript:
            chain.mute()
        assert len(transcript.sent_messages) == 1
        _, message = transcript.sent_messages[0]
        assert message.to_list() == [
            None,
            [[15, chain.node_proxies["output"].identifier, "active", 0]],
        ]


@pytest.mark.parametrize("booted", [True, False])
@pytest.mark.parametrize(
    "chain_names, expected",
    [
        (["outer/a/a"], [0, 1, 1, 1, 1, 1, 1, 1]),
        (["outer/a/b"], [1, 0, 1, 1, 1, 1, 1, 1]),
        (["inner/a/a"], [1, 1, 0, 1, 1, 1, 1, 1]),
        (["inner/a/b"], [1, 1, 1, 0, 1, 1, 1, 1]),
        (["outer/b/a"], [1, 1, 1, 1, 0, 1, 1, 1]),
        (["outer/b/b"], [1, 1, 1, 1, 1, 0, 1, 1]),
        (["inner/b/a"], [1, 1, 1, 1, 1, 1, 0, 1]),
        (["inner/b/b"], [1, 1, 1, 1, 1, 1, 1, 0]),
    ],
)
def test_is_active(chain_mute_solo_application, booted, chain_names, expected):
    if booted:
        chain_mute_solo_application.boot()
    for chain_name in chain_names:
        chain = chain_mute_solo_application.primary_context[chain_name]
        chain.mute()
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
def test_is_muted(chain_mute_solo_application, booted, chain_names, expected):
    if booted:
        chain_mute_solo_application.boot()
    for chain_name in chain_names:
        chain = chain_mute_solo_application.primary_context[chain_name]
        chain.mute()
    all_chains = list(
        chain_mute_solo_application.primary_context.depth_first(prototype=Chain)
    )
    actual = [bool(chain.is_muted) for chain in all_chains]
    assert actual == [bool(x) for x in expected]


def test_repeat(chain_mute_solo_application):
    chain_mute_solo_application.boot()
    chain_mute_solo_application.primary_context["outer/a/a"].mute()
    with chain_mute_solo_application.primary_context.provider.server.osc_protocol.capture() as transcript:
        chain_mute_solo_application.primary_context["outer/a/a"].mute()
    assert not len(transcript.sent_messages)
