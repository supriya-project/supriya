import pytest

from supriya import OscBundle, OscMessage, Score, SynthDef, default
from supriya.ugens import compile_synthdefs


@pytest.fixture
def context() -> Score:
    return Score()


def test_add_group(context: Score) -> None:
    with context.at(0):
        # /g_new
        group = context.add_group()
        # /p_new
        context.add_group(parallel=True)
    with context.at(1.23):
        context.add_group(parallel=True, target_node=group)
        context.add_group(parallel=True, target_node=group)
        context.add_group(target_node=group)
        context.add_group(target_node=group)
    assert list(context.iterate_osc_bundles()) == [
        OscBundle(
            contents=(
                OscMessage("/g_new", 1000, 0, 0),
                OscMessage("/p_new", 1001, 0, 0),
            ),
            timestamp=0.0,
        ),
        OscBundle(
            contents=(
                OscMessage("/p_new", 1002, 0, 1000, 1003, 0, 1000),
                OscMessage("/g_new", 1004, 0, 1000, 1005, 0, 1000),
            ),
            timestamp=1.23,
        ),
    ]
    # guard against invalid add-actions
    with context.at(2.34):
        synth = context.add_synth(default)
        with pytest.raises(ValueError):
            synth.add_group(add_action="ADD_TO_HEAD")
        with pytest.raises(ValueError):
            synth.add_group(add_action="ADD_TO_TAIL")


def test_add_synth(context: Score, two_voice_synthdef: SynthDef) -> None:
    def compiled(*synthdefs):
        return compile_synthdefs(*synthdefs)

    with context.at(0):
        context.add_synthdefs(default)
        bus_a = context.add_bus("AUDIO")
        bus_c = context.add_bus("CONTROL")
        synth = context.add_synth(default)
        context.add_synth(default, frequency=bus_a, amplitude="c0", pan=0.25, out=0)
        context.add_synth(two_voice_synthdef, frequencies=(123, 456))
    with context.at(1.23):
        context.add_synth(default, add_action="ADD_AFTER", target_node=synth)
        context.add_synth(
            default, frequency=bus_c.map_symbol(), amplitude="a16", pan=0.25, out=0
        )
    assert list(context.iterate_osc_bundles()) == [
        OscBundle(
            contents=(
                OscMessage("/d_recv", compiled(default)),
                OscMessage("/s_new", "supriya:default", 1000, 0, 0),
                OscMessage(
                    "/s_new",
                    "supriya:default",
                    1001,
                    0,
                    0,
                    "amplitude",
                    "c0",
                    "frequency",
                    16.0,  # cast to an int
                    "pan",
                    0.25,
                ),
                OscMessage(
                    "/s_new",
                    "test:two-voice",
                    1002,
                    0,
                    0,
                    "frequencies",
                    (123.0, 456.0),
                ),
            ),
            timestamp=0.0,
        ),
        OscBundle(
            contents=(
                OscMessage("/s_new", "supriya:default", 1003, 3, 1000),
                OscMessage(
                    "/s_new",
                    "supriya:default",
                    1004,
                    0,
                    0,
                    "amplitude",
                    "a16",
                    "frequency",
                    "c0",
                    "pan",
                    0.25,
                ),
            ),
            timestamp=1.23,
        ),
    ]
    # guard against invalid add-actions
    with context.at(2.34):
        synth = context.add_synth(default)
        with pytest.raises(ValueError):
            synth.add_synth(default, add_action="ADD_TO_HEAD")
        with pytest.raises(ValueError):
            synth.add_synth(default, add_action="ADD_TO_TAIL")


def test_free_group_children(context: Score) -> None:
    with context.at(0):
        grandparent = context.add_group()
        # setup
        parent = grandparent.add_group()
        grandparent.add_synth(default)
        parent.add_synth(default)
        # /g_freeAll
        grandparent.free_children()
        # /g_deepFree
        grandparent.free_children(synths_only=True)
    assert list(context.iterate_osc_bundles()) == [
        OscBundle(
            contents=(
                OscMessage("/g_new", 1000, 0, 0, 1001, 0, 1000),
                OscMessage("/s_new", "supriya:default", 1002, 0, 1000),
                OscMessage("/s_new", "supriya:default", 1003, 0, 1001),
                OscMessage("/g_freeAll", 1000),
                OscMessage("/g_deepFree", 1000),
            ),
            timestamp=0.0,
        )
    ]


def test_free_node(context: Score) -> None:
    with context.at(0):
        group = context.add_group()
        synth = context.add_synth(default)
        group.free()
        synth.free()
    assert list(context.iterate_osc_bundles()) == [
        OscBundle(
            contents=(
                OscMessage("/g_new", 1000, 0, 0),
                OscMessage("/s_new", "supriya:default", 1001, 0, 0),
                OscMessage("/n_free", 1000),
                OscMessage("/n_set", 1001, "gate", 0),
            ),
            timestamp=0.0,
        )
    ]


def test_map_node(context: Score) -> None:
    with context.at(0):
        bus_a = context.add_bus("AUDIO")
        bus_c = context.add_bus("CONTROL")
        synth = context.add_synth(default)
        synth.map(frequency=bus_a, amplitude=bus_c, pan=None)
    assert list(context.iterate_osc_bundles()) == [
        OscBundle(
            contents=(
                OscMessage("/s_new", "supriya:default", 1000, 0, 0),
                OscMessage("/n_map", 1000, "amplitude", 0, "pan", -1),
                OscMessage("/n_mapa", 1000, "frequency", 16),
            ),
            timestamp=0.0,
        )
    ]


def test_move_node(context: Score) -> None:
    with context.at(0):
        group = context.add_group()
        synth = context.add_synth(default)
        group.move(target_node=synth, add_action="ADD_AFTER")
        synth.move(target_node=group, add_action="ADD_BEFORE")
        synth.move(target_node=group, add_action="ADD_TO_TAIL")
        synth.move(target_node=group, add_action="ADD_TO_HEAD")
    assert list(context.iterate_osc_bundles()) == [
        OscBundle(
            contents=(
                OscMessage("/g_new", 1000, 0, 0),
                OscMessage("/s_new", "supriya:default", 1001, 0, 0),
                OscMessage("/n_after", 1000, 1001),
                OscMessage("/n_before", 1001, 1000),
                OscMessage("/g_tail", 1000, 1001),
                OscMessage("/g_head", 1000, 1001),
            ),
            timestamp=0.0,
        )
    ]


def test_order_nodes(context: Score) -> None:
    with context.at(0):
        group_a = context.add_group()
        group_b = context.add_group()
        group_c = context.add_group()
        group_a.order(group_b, group_c, add_action="ADD_TO_TAIL")
    assert list(context.iterate_osc_bundles()) == [
        OscBundle(
            contents=(
                OscMessage("/g_new", 1000, 0, 0, 1001, 0, 0, 1002, 0, 0),
                OscMessage("/n_order", 1, 1000, 1001, 1002),
            ),
            timestamp=0.0,
        )
    ]


def test_pause_node(context: Score) -> None:
    with context.at(0):
        group = context.add_group()
        group.pause()
    assert list(context.iterate_osc_bundles()) == [
        OscBundle(
            contents=(OscMessage("/g_new", 1000, 0, 0), OscMessage("/n_run", 1000, 0)),
            timestamp=0.0,
        )
    ]


def test_set_node(context: Score) -> None:
    with context.at(0):
        group = context.add_group()
        group.set((1, 2.3), (2, [3.4, 4.5]), foo=3.145, bar=4.5, baz=[1.23, 4.56])
    assert list(context.iterate_osc_bundles()) == [
        OscBundle(
            contents=(
                OscMessage("/g_new", 1000, 0, 0),
                OscMessage(
                    "/n_set",
                    1000,
                    1,
                    2.3,
                    2,
                    [3.4, 4.5],
                    "bar",
                    4.5,
                    "baz",
                    [1.23, 4.56],
                    "foo",
                    3.145,
                ),
            ),
            timestamp=0.0,
        )
    ]


def test_set_node_range(context: Score) -> None:
    with context.at(0):
        group = context.add_group()
        group.set_range((2, [3.4, 4.5]), baz=[1.23, 4.56])
    assert list(context.iterate_osc_bundles()) == [
        OscBundle(
            contents=(
                OscMessage("/g_new", 1000, 0, 0),
                OscMessage("/n_setn", 1000, 2, 2, 3.4, 4.5, "baz", 2, 1.23, 4.56),
            ),
            timestamp=0.0,
        )
    ]


def test_unpause_node(context: Score) -> None:
    with context.at(0):
        group_a = context.add_group()
        group_b = context.add_group()
        group_c = context.add_group()
        group_a.unpause()
    with context.at(1.23):
        group_b.unpause()
        group_c.unpause()
    assert list(context.iterate_osc_bundles()) == [
        OscBundle(
            contents=(
                OscMessage("/g_new", 1000, 0, 0, 1001, 0, 0, 1002, 0, 0),
                OscMessage("/n_run", 1000, 1),
            ),
            timestamp=0.0,
        ),
        OscBundle(contents=(OscMessage("/n_run", 1001, 1, 1002, 1),), timestamp=1.23),
    ]
