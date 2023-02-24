import logging

import pytest

from supriya.contexts.errors import MomentClosed
from supriya.contexts.nonrealtime import Score
from supriya.osc import OscBundle, OscMessage
from supriya.synthdefs import SynthDefBuilder, SynthDefCompiler
from supriya.ugens import Out, SinOsc


@pytest.fixture(autouse=True)
def use_caplog(caplog):
    caplog.set_level(logging.INFO)


@pytest.fixture
def context(request):
    return Score()


@pytest.fixture
def synthdefs():
    with SynthDefBuilder(bus=0, frequency=440) as builder:
        Out.ar(bus=builder["bus"], source=SinOsc.ar(frequency=builder["frequency"]))
    synthdef_a = builder.build(name="synthdef-a")
    synthdef_b = builder.build(name="synthdef-b")
    synthdef_c = builder.build(name="synthdef-c")
    return [synthdef_a, synthdef_b, synthdef_c]


def test_add_synthdefs(context, synthdefs):
    def compiled(x):
        return SynthDefCompiler.compile_synthdefs(x)

    with context.at(0):
        # no synthdefs provided
        with pytest.raises(ValueError):
            context.add_synthdefs()
        # /d_recv
        context.add_synthdefs(synthdefs[0])
        # multiples
        context.add_synthdefs(*synthdefs)
        # completion via on_completion lambda succeeds
        context.add_synthdefs(synthdefs[1], on_completion=lambda ctx: ctx.add_group())
        # completion without moment errors
        completion = context.add_synthdefs(synthdefs[2])
    with pytest.raises(MomentClosed):
        with completion:
            context.add_group()
    with context.at(1.23):
        # completion inside moment succeeds
        with context.add_synthdefs(synthdefs[2]):
            context.add_group()
    assert list(context.iterate_osc_bundles()) == [
        OscBundle(
            contents=(
                OscMessage("/d_recv", compiled([synthdefs[0]])),
                OscMessage("/d_recv", compiled(synthdefs)),
                OscMessage(
                    "/d_recv",
                    compiled([synthdefs[1]]),
                    OscMessage("/g_new", 1000, 0, 0),
                ),
                OscMessage("/d_recv", compiled([synthdefs[2]])),
            ),
            timestamp=0.0,
        ),
        OscBundle(
            contents=[
                OscMessage(
                    "/d_recv",
                    compiled([synthdefs[2]]),
                    OscMessage("/g_new", 1001, 0, 0),
                )
            ],
            timestamp=1.23,
        ),
    ]


def test_free_synthdefs(context, synthdefs):
    with context.at(0):
        # no synthdefs provided
        with pytest.raises(ValueError):
            context.free_synthdefs()
        # /d_free
        context.free_synthdefs(*synthdefs)
    assert list(context.iterate_osc_bundles()) == [
        OscBundle(
            contents=(OscMessage("/d_free", "synthdef-a", "synthdef-b", "synthdef-c"),),
            timestamp=0.0,
        )
    ]


def test_free_all_synthdefs(context):
    with context.at(0):
        context.free_all_synthdefs()
    assert list(context.iterate_osc_bundles()) == [
        OscBundle(contents=(OscMessage("/d_freeAll"),), timestamp=0.0)
    ]


def test_load_synthdefs(context, tmp_path):
    with context.at(0):
        context.load_synthdefs(tmp_path / "a.scsyndef")
        # completion via on_completion lambda succeeds
        context.load_synthdefs(
            tmp_path / "b.scsyndef", on_completion=lambda ctx: ctx.add_group()
        )
        # completion without moment errors
        completion = context.load_synthdefs(tmp_path / "c.scsyndef")
    with pytest.raises(MomentClosed):
        with completion:
            context.add_group()
    with context.at(1.23):
        # completion inside moment succeeds
        with context.load_synthdefs(tmp_path / "c.scsyndef"):
            context.add_group()
    assert list(context.iterate_osc_bundles()) == [
        OscBundle(
            contents=(
                OscMessage("/d_load", str(tmp_path / "a.scsyndef")),
                OscMessage(
                    "/d_load",
                    str(tmp_path / "b.scsyndef"),
                    OscMessage("/g_new", 1000, 0, 0),
                ),
                OscMessage("/d_load", str(tmp_path / "c.scsyndef")),
            ),
            timestamp=0.0,
        ),
        OscBundle(
            contents=(
                OscMessage(
                    "/d_load",
                    str(tmp_path / "c.scsyndef"),
                    OscMessage("/g_new", 1001, 0, 0),
                ),
            ),
            timestamp=1.23,
        ),
    ]


def test_load_synthdefs_directory(context, tmp_path):
    with context.at(0):
        context.load_synthdefs_directory(tmp_path / "a")
        # completion via on_completion lambda succeeds
        context.load_synthdefs_directory(
            tmp_path / "b", on_completion=lambda ctx: ctx.add_group()
        )
        # completion without moment errors
        completion = context.load_synthdefs_directory(tmp_path / "c")
    with pytest.raises(MomentClosed):
        with completion:
            context.add_group()
    with context.at(1.23):
        # completion inside moment succeeds
        with context.load_synthdefs_directory(tmp_path / "c"):
            context.add_group()
    assert list(context.iterate_osc_bundles()) == [
        OscBundle(
            contents=(
                OscMessage("/d_loadDir", str(tmp_path / "a")),
                OscMessage(
                    "/d_loadDir", str(tmp_path / "b"), OscMessage("/g_new", 1000, 0, 0)
                ),
                OscMessage("/d_loadDir", str(tmp_path / "c")),
            ),
            timestamp=0.0,
        ),
        OscBundle(
            contents=(
                OscMessage(
                    "/d_loadDir", str(tmp_path / "c"), OscMessage("/g_new", 1001, 0, 0)
                ),
            ),
            timestamp=1.23,
        ),
    ]
