import asyncio
import logging

import pytest
import pytest_asyncio

from supriya.contexts.errors import MomentClosed
from supriya.contexts.realtime import AsyncServer, Server
from supriya.osc import OscBundle, OscMessage
from supriya.synthdefs import SynthDefBuilder, SynthDefCompiler
from supriya.ugens import Out, SinOsc


async def get(x):
    if asyncio.iscoroutine(x):
        return await x
    return x


@pytest.fixture(autouse=True)
def use_caplog(caplog):
    caplog.set_level(logging.INFO)


@pytest_asyncio.fixture(autouse=True, params=[AsyncServer, Server])
async def context(request):
    context = request.param()
    await get(context.boot())
    yield context


@pytest.fixture
def synthdefs():
    with SynthDefBuilder(bus=0, frequency=440) as builder:
        Out.ar(bus=builder["bus"], source=SinOsc.ar(frequency=builder["frequency"]))
    synthdef_a = builder.build(name="synthdef-a")
    synthdef_b = builder.build(name="synthdef-b")
    synthdef_c = builder.build(name="synthdef-c")
    return [synthdef_a, synthdef_b, synthdef_c]


@pytest.mark.asyncio
async def test_add_synthdefs(context, synthdefs):
    def compiled(x):
        return SynthDefCompiler.compile_synthdefs(x)

    with context.osc_protocol.capture() as transcript:
        # no synthdefs provided
        with pytest.raises(ValueError):
            context.add_synthdefs()
        # /d_recv
        context.add_synthdefs(synthdefs[0])
        # multiples
        context.add_synthdefs(*synthdefs)
        # completion without moment via on_completion lambda succeeds
        context.add_synthdefs(synthdefs[1], on_completion=lambda ctx: ctx.add_group())
        # completion without moment errors
        with pytest.raises(MomentClosed):
            with context.add_synthdefs(synthdefs[2]):
                context.add_group()
        # completion inside moment succeeds
        with context.at(1.23):
            with context.add_synthdefs(synthdefs[2]):
                context.add_group()
    assert transcript.filtered(received=False, status=False) == [
        OscMessage("/d_recv", compiled([synthdefs[0]])),
        OscMessage("/d_recv", compiled(synthdefs)),
        OscMessage(
            "/d_recv", compiled([synthdefs[1]]), OscMessage("/g_new", 1000, 0, 1)
        ),
        OscMessage("/d_recv", compiled([synthdefs[2]])),
        OscBundle(
            contents=[
                OscMessage(
                    "/d_recv",
                    compiled([synthdefs[2]]),
                    OscMessage("/g_new", 1001, 0, 1),
                )
            ],
            timestamp=1.23 + context.latency,
        ),
    ]


@pytest.mark.asyncio
async def test_free_synthdefs(context, synthdefs):
    with context.osc_protocol.capture() as transcript:
        # no synthdefs provided
        with pytest.raises(ValueError):
            context.free_synthdefs()
        # /d_free
        context.free_synthdefs(*synthdefs)
    assert transcript.filtered(received=False, status=False) == [
        OscMessage("/d_free", "synthdef-a", "synthdef-b", "synthdef-c")
    ]


@pytest.mark.asyncio
async def test_free_all_synthdefs(context):
    with context.osc_protocol.capture() as transcript:
        context.free_all_synthdefs()
    assert transcript.filtered(received=False, status=False) == [
        OscMessage("/d_freeAll")
    ]


@pytest.mark.asyncio
async def test_load_synthdefs(context, tmp_path):
    with context.osc_protocol.capture() as transcript:
        context.load_synthdefs(tmp_path / "a.scsyndef")
        # completion without moment via on_completion lambda succeeds
        context.load_synthdefs(
            tmp_path / "b.scsyndef", on_completion=lambda ctx: ctx.add_group()
        )
        # completion without moment errors
        with pytest.raises(MomentClosed):
            with context.load_synthdefs(tmp_path / "c.scsyndef"):
                context.add_group()
        # completion inside moment succeeds
        with context.at(1.23):
            with context.load_synthdefs(tmp_path / "c.scsyndef"):
                context.add_group()
    assert transcript.filtered(received=False, status=False) == [
        OscMessage("/d_load", str(tmp_path / "a.scsyndef")),
        OscMessage(
            "/d_load", str(tmp_path / "b.scsyndef"), OscMessage("/g_new", 1000, 0, 1)
        ),
        OscMessage("/d_load", str(tmp_path / "c.scsyndef")),
        OscBundle(
            contents=(
                OscMessage(
                    "/d_load",
                    str(tmp_path / "c.scsyndef"),
                    OscMessage("/g_new", 1001, 0, 1),
                ),
            ),
            timestamp=1.23 + context.latency,
        ),
    ]


@pytest.mark.asyncio
async def test_load_synthdefs_directory(context, tmp_path):
    with context.osc_protocol.capture() as transcript:
        context.load_synthdefs_directory(tmp_path / "a")
        # completion without moment via on_completion lambda succeeds
        context.load_synthdefs_directory(
            tmp_path / "b", on_completion=lambda ctx: ctx.add_group()
        )
        # completion without moment errors
        with pytest.raises(MomentClosed):
            with context.load_synthdefs_directory(tmp_path / "c"):
                context.add_group()
        # completion inside moment succeeds
        with context.at(1.23):
            with context.load_synthdefs_directory(tmp_path / "c"):
                context.add_group()
    assert transcript.filtered(received=False, status=False) == [
        OscMessage("/d_loadDir", str(tmp_path / "a")),
        OscMessage("/d_loadDir", str(tmp_path / "b"), OscMessage("/g_new", 1000, 0, 1)),
        OscMessage("/d_loadDir", str(tmp_path / "c")),
        OscBundle(
            contents=(
                OscMessage(
                    "/d_loadDir", str(tmp_path / "c"), OscMessage("/g_new", 1001, 0, 1)
                ),
            ),
            timestamp=1.23 + context.latency,
        ),
    ]
