import asyncio
import concurrent.futures
import logging
import random
import warnings
from pathlib import Path
from typing import AsyncGenerator

import pytest
import pytest_asyncio

import supriya
from supriya import default
from supriya.contexts.errors import MomentClosed
from supriya.contexts.realtime import AsyncServer, Server
from supriya.contexts.responses import BufferInfo
from supriya.osc import OscBundle, OscMessage


async def get(x):
    if asyncio.iscoroutine(x):
        return await x
    return x


@pytest.fixture
def audio_paths() -> list[Path]:
    return sorted((Path(supriya.__path__[0]) / "samples").glob("bird*.wav"))


@pytest.fixture(autouse=True)
def use_caplog(caplog) -> None:
    caplog.set_level(logging.INFO)


@pytest_asyncio.fixture(autouse=True, params=[AsyncServer, Server])
async def context(request) -> AsyncGenerator[AsyncServer | Server, None]:
    context = request.param()
    await get(context.boot())
    context.add_synthdefs(default)
    await get(context.sync())
    yield context


@pytest.mark.asyncio
async def test_Buffer_allocated(context: AsyncServer | Server) -> None:
    # buffers can be allocated
    buffer_a = context.add_buffer(channel_count=1, frame_count=512)
    buffer_b = context.add_buffer(channel_count=1, frame_count=512)
    assert not buffer_a.allocated  # waiting for the /done /b_alloc response
    assert not buffer_b.allocated  # waiting for the /done /b_alloc response
    await get(context.sync())
    assert buffer_a.allocated
    assert buffer_b.allocated
    # freed buffers are unallocated
    buffer_a.free()
    assert buffer_a.allocated  # waiting for the /done /b_free response
    assert buffer_b.allocated
    await get(context.sync())
    assert not buffer_a.allocated  # waiting for the /done /b_free response
    assert buffer_b.allocated
    # nothing is allocated on an unbooted context
    await get(context.quit())
    assert not buffer_a.allocated
    assert not buffer_b.allocated
    # allocation state is stored in the context, not the node
    await get(context.boot())
    assert not buffer_a.allocated
    assert not buffer_b.allocated


@pytest.mark.asyncio
async def test_add_buffer(
    audio_paths: list[Path], context: AsyncServer | Server
) -> None:
    with context.osc_protocol.capture() as transcript:
        # neither frame count nor file path provided
        with pytest.raises(ValueError):
            context.add_buffer()
        # both channel count and file path provided
        with pytest.raises(ValueError):
            context.add_buffer(file_path=audio_paths[0], channel_count=1)
        # both channel count and channel indices provided
        with pytest.raises(ValueError):
            context.add_buffer(
                file_path=audio_paths[0], channel_count=1, channel_indices=[0]
            )
        # /b_alloc
        buffer_a = context.add_buffer(channel_count=1, frame_count=23)
        # /b_allocRead
        buffer_b = context.add_buffer(frame_count=19, file_path=audio_paths[0])
        # /b_allocReadChannel
        buffer_c = context.add_buffer(
            frame_count=17, file_path=audio_paths[1], channel_indices=[0, 0]
        )
        # completion without moment errors
        with pytest.raises(MomentClosed):
            buffer_d = context.add_buffer(channel_count=3, frame_count=31)
            with buffer_d:
                ...
        # completion without moment via on_completion lambda succeeds
        buffer_e = context.add_buffer(
            channel_count=1, frame_count=47, on_completion=lambda ctx: ctx.add_group()
        )
        # completion inside moment succeeds
        with context.at(1.23):
            buffer_f = context.add_buffer(channel_count=3, frame_count=31)
            with buffer_f:
                context.add_group()
    buffers = [buffer_a, buffer_b, buffer_c, buffer_d, buffer_e, buffer_f]
    assert all(buffer.context is context for buffer in buffers)
    assert [buffer.id_ for buffer in buffers] == [0, 1, 2, 3, 4, 5]
    assert transcript.filtered(received=False, status=False) == [
        OscMessage("/b_alloc", 0, 23, 1),
        OscMessage("/b_allocRead", 1, str(audio_paths[0]), 0, 19),
        OscMessage("/b_allocReadChannel", 2, str(audio_paths[1]), 0, 17, 0, 0),
        OscMessage("/b_alloc", 3, 31, 3),
        OscMessage("/b_alloc", 4, 47, 1, OscMessage("/g_new", 1000, 0, 1)),
        OscBundle(
            contents=(
                OscMessage("/b_alloc", 5, 31, 3, OscMessage("/g_new", 1001, 0, 1)),
            ),
            timestamp=1.23 + context.latency,
        ),
    ]


@pytest.mark.asyncio
async def test_add_buffer_group(context: AsyncServer | Server) -> None:
    # neither channel count nor frame count provided
    with pytest.raises(ValueError):
        context.add_buffer_group()
    # count less than 1
    with pytest.raises(ValueError):
        context.add_buffer_group(channel_count=1, count=0, frame_count=512)
    # /b_alloc
    with context.osc_protocol.capture() as transcript:
        buffer_group = context.add_buffer_group(
            channel_count=1, count=5, frame_count=23
        )
    assert len(buffer_group) == 5
    assert all(buffer.context is context for buffer in buffer_group)
    assert [buffer.id_ for buffer in buffer_group] == [0, 1, 2, 3, 4]
    assert transcript.filtered(received=False, status=False) == [
        OscBundle(
            contents=(
                OscMessage("/b_alloc", 0, 23, 1),
                OscMessage("/b_alloc", 1, 23, 1),
                OscMessage("/b_alloc", 2, 23, 1),
                OscMessage("/b_alloc", 3, 23, 1),
                OscMessage("/b_alloc", 4, 23, 1),
            )
        )
    ]


@pytest.mark.asyncio
async def test_close_buffer(context: AsyncServer | Server) -> None:
    buffer_a = context.add_buffer(channel_count=1, frame_count=23)
    buffer_b = context.add_buffer(channel_count=1, frame_count=23)
    buffer_c = context.add_buffer(channel_count=1, frame_count=23)
    with context.osc_protocol.capture() as transcript:
        # completion without moment errors, but initial request succeeds
        with pytest.raises(MomentClosed):
            with buffer_a.close():
                ...
        # completion without moment via on_completion lambda succeeds
        buffer_b.close(on_completion=lambda ctx: buffer_b.free())
        # completion inside moment succeeds
        with context.at():
            with buffer_c.close():
                buffer_c.free()
    assert transcript.filtered(received=False, status=False) == [
        OscMessage("/b_close", 0),
        OscMessage("/b_close", 1, OscMessage("/b_free", 1)),
        OscMessage("/b_close", 2, OscMessage("/b_free", 2)),
    ]


@pytest.mark.asyncio
async def test_copy_buffer(context: AsyncServer | Server) -> None:
    buffer_a = context.add_buffer(channel_count=1, frame_count=23)
    buffer_b = context.add_buffer(channel_count=1, frame_count=23)
    with context.osc_protocol.capture() as transcript:
        buffer_a.copy(
            target_buffer=buffer_b,
            starting_frame=5,
            target_starting_frame=7,
            frame_count=3,
        )
    assert transcript.filtered(received=False, status=False) == [
        OscMessage("/b_gen", 1, "copy", 7, 0, 5, 3)
    ]


@pytest.mark.asyncio
async def test_fill_buffer(context: AsyncServer | Server) -> None:
    buffer_a = context.add_buffer(channel_count=1, frame_count=23)
    buffer_b = context.add_buffer(channel_count=1, frame_count=23)
    with context.osc_protocol.capture() as transcript:
        # one-off
        buffer_a.fill(2, 3, 0.5)
        # with moment, including grouping
        with context.at():
            buffer_a.fill(2, 3, 0.6)
            buffer_b.fill(3, 4, 0.5)
            buffer_a.fill(4, 5, 0.4)
            buffer_a.fill(5, 6, 0.3)
    assert transcript.filtered(received=False, status=False) == [
        OscMessage("/b_fill", 0, 2, 3, 0.5),
        OscBundle(
            contents=(
                OscMessage("/b_fill", 0, 2, 3, 0.6, 4, 5, 0.4, 5, 6, 0.3),
                OscMessage("/b_fill", 1, 3, 4, 0.5),
            )
        ),
    ]


@pytest.mark.asyncio
async def test_free_buffer(context: AsyncServer | Server) -> None:
    buffer_a = context.add_buffer(channel_count=1, frame_count=23)
    buffer_b = context.add_buffer(channel_count=1, frame_count=23)
    buffer_c = context.add_buffer(channel_count=1, frame_count=23)
    with context.osc_protocol.capture() as transcript:
        # completion without moment errors, but initial request succeeds
        with pytest.raises(MomentClosed):
            with buffer_a.free():
                ...
        # completion without moment via on_completion lambda succeeds
        buffer_b.free(on_completion=lambda ctx: ctx.add_group())
        # completion inside moment succeeds
        with context.at():
            with buffer_c.free():
                context.add_group()
    assert transcript.filtered(received=False, status=False) == [
        OscMessage("/b_free", 0),
        OscMessage("/b_free", 1, OscMessage("/g_new", 1000, 0, 1)),
        OscMessage("/b_free", 2, OscMessage("/g_new", 1001, 0, 1)),
    ]


def test_generate_buffer(context: AsyncServer | Server) -> None:
    buffer = context.add_buffer(channel_count=1, frame_count=1024)
    with context.osc_protocol.capture() as transcript:
        with context.at(0):
            buffer.generate(command_name="sine1", amplitudes=[1, 2, 3])
            buffer.generate(
                command_name="sine2", amplitudes=[1, 2, 3], frequencies=[4, 5, 6]
            )
            buffer.generate(
                command_name="sine3",
                amplitudes=[1, 2, 3],
                frequencies=[4, 5, 6],
                phases=[0.25, 0.0, 0.5],
            )
            buffer.generate(command_name="cheby", amplitudes=[1, 2, 3])
            buffer.generate(
                command_name="sine1", amplitudes=[1, 2, 3], as_wavetable=True
            )
            buffer.generate(
                command_name="sine1", amplitudes=[1, 2, 3], should_clear_first=True
            )
            buffer.generate(
                command_name="sine1",
                amplitudes=[1, 2, 3],
                should_clear_first=True,
                should_normalize=True,
            )
    assert transcript.filtered(received=False, status=False) == [
        OscBundle(
            contents=(
                OscMessage("/b_gen", 0, "sine1", 0, 1.0, 2.0, 3.0),
                OscMessage("/b_gen", 0, "sine2", 0, 4.0, 1.0, 5.0, 2.0, 6.0, 3.0),
                OscMessage(
                    "/b_gen",
                    0,
                    "sine3",
                    0,
                    4.0,
                    1.0,
                    0.25,
                    5.0,
                    2.0,
                    0.0,
                    6.0,
                    3.0,
                    0.5,
                ),
                OscMessage("/b_gen", 0, "cheby", 0, 1.0, 2.0, 3.0),
                OscMessage("/b_gen", 0, "sine1", 2, 1.0, 2.0, 3.0),
                OscMessage("/b_gen", 0, "sine1", 4, 1.0, 2.0, 3.0),
                OscMessage("/b_gen", 0, "sine1", 5, 1.0, 2.0, 3.0),
            ),
            timestamp=0.0 + context.latency,
        ),
    ]


@pytest.mark.asyncio
async def test_get_buffer(context: AsyncServer | Server) -> None:
    buffer = context.add_buffer(channel_count=1, frame_count=512)
    exception_classes = (
        concurrent.futures.TimeoutError,
        asyncio.exceptions.TimeoutError,
    )
    with warnings.catch_warnings(record=True) as w:
        with pytest.raises(exception_classes):
            await get(buffer.get(1024))
        assert len(w) == 1
        assert str(w[-1].message) == "/b_get index out of range"
    await get(context.sync())
    with context.osc_protocol.capture() as transcript:
        assert await get(buffer.get(1, 2, 3)) == {1: 0.0, 2: 0.0, 3: 0.0}  # sync
        assert await get(buffer.get(1, sync=False)) is None  # unsync
    assert transcript.filtered(received=False, status=False) == [
        OscMessage("/b_get", 0, 1, 2, 3),
        OscMessage("/b_get", 0, 1),
    ]


@pytest.mark.asyncio
async def test_get_buffer_range(context: AsyncServer | Server) -> None:
    buffer = context.add_buffer(channel_count=1, frame_count=512)
    exception_classes = (
        concurrent.futures.TimeoutError,
        asyncio.exceptions.TimeoutError,
    )
    with warnings.catch_warnings(record=True) as w:
        with pytest.raises(exception_classes):
            await get(context.get_buffer_range(buffer, 1, 3))  # no such buffer exists
        assert len(w) == 1
        assert str(w[-1].message) == "/b_getn index out of range"
    await get(context.sync())
    with context.osc_protocol.capture() as transcript:
        assert await get(buffer.get_range(1, 3)) == (0.0, 0.0, 0.0)  # sync
        assert await get(buffer.get_range(1, 3, sync=False)) is None  # unsync
    assert transcript.filtered(received=False, status=False) == [
        OscMessage("/b_getn", 0, 1, 3),
        OscMessage("/b_getn", 0, 1, 3),
    ]


@pytest.mark.asyncio
async def test_normalize_buffer(context: AsyncServer | Server) -> None:
    buffer = context.add_buffer(channel_count=1, frame_count=23)
    with context.osc_protocol.capture() as transcript:
        buffer.normalize(0.5)
    assert transcript.filtered(received=False, status=False) == [
        OscMessage("/b_gen", 0, "normalize", 0.5)
    ]


@pytest.mark.asyncio
async def test_query_buffer(context: AsyncServer | Server) -> None:
    frame_count = random.randint(128, 256)
    channel_count = random.randint(1, 8)
    buffer = context.add_buffer(channel_count=channel_count, frame_count=frame_count)
    await asyncio.sleep(0.1)
    assert await get(buffer.query()) in [
        BufferInfo(
            items=[
                BufferInfo.Item(
                    buffer_id=0,
                    frame_count=frame_count,
                    channel_count=channel_count,
                    sample_rate=sample_rate,
                )
            ]
        )
        for sample_rate in [48000, 44100]
    ]
    # unsync
    with context.osc_protocol.capture() as transcript:
        assert await get(buffer.query(sync=False)) is None
    assert transcript.filtered(received=False, status=False) == [
        OscMessage("/b_query", 0)
    ]


@pytest.mark.asyncio
async def test_read_buffer(
    audio_paths: list[Path], context: AsyncServer | Server
) -> None:
    buffer_a = context.add_buffer(channel_count=1, frame_count=23)
    buffer_b = context.add_buffer(channel_count=1, frame_count=23)
    buffer_c = context.add_buffer(channel_count=1, frame_count=23)
    with context.osc_protocol.capture() as transcript:
        # completion without moment errors, but initial request succeeds
        with pytest.raises(MomentClosed):
            with buffer_a.read(file_path=audio_paths[0]):
                ...
        # completion without moment via on_completion lambda succeeds
        buffer_b.read(
            file_path=audio_paths[1], on_completion=lambda ctx: ctx.add_group()
        )
        # completion inside moment succeeds
        with context.at():
            with buffer_c.read(file_path=audio_paths[2]):
                context.add_group()
        # parameters
        buffer_a.read(
            buffer_starting_frame=5,
            channel_indices=[0],
            file_path=audio_paths[3],
            frame_count=16,
            leave_open=True,
            starting_frame=3,
        )
    assert transcript.filtered(received=False, status=False) == [
        OscMessage("/b_read", 0, str(audio_paths[0]), 0, -1, 0, 0),
        OscMessage(
            "/b_read",
            1,
            str(audio_paths[1]),
            0,
            -1,
            0,
            0,
            OscMessage("/g_new", 1000, 0, 1),
        ),
        OscMessage(
            "/b_read",
            2,
            str(audio_paths[2]),
            0,
            -1,
            0,
            0,
            OscMessage("/g_new", 1001, 0, 1),
        ),
        OscMessage("/b_readChannel", 0, str(audio_paths[3]), 3, 16, 5, 1, 0),
    ]


@pytest.mark.asyncio
async def test_set_buffer(context: AsyncServer | Server) -> None:
    buffer = context.add_buffer(channel_count=1, frame_count=32)
    await get(context.sync())  # can't set until allocation finishes
    with context.osc_protocol.capture() as transcript:
        buffer.set(2, 0.5)
    assert transcript.filtered(received=False, status=False) == [
        OscMessage("/b_set", 0, 2, 0.5)
    ]


@pytest.mark.asyncio
async def test_set_buffer_range(context: AsyncServer | Server) -> None:
    buffer = context.add_buffer(channel_count=1, frame_count=32)
    await get(context.sync())  # can't set until allocation finishes
    with context.osc_protocol.capture() as transcript:
        buffer.set_range(4, (0.5, 0.75, 0.25))
    assert transcript.filtered(received=False, status=False) == [
        OscMessage("/b_setn", 0, 4, 3, 0.5, 0.75, 0.25)
    ]


@pytest.mark.asyncio
async def test_write_buffer(context: AsyncServer | Server, tmp_path: Path) -> None:
    buffer_a = context.add_buffer(channel_count=1, frame_count=23)
    buffer_b = context.add_buffer(channel_count=1, frame_count=23)
    buffer_c = context.add_buffer(channel_count=1, frame_count=23)
    with context.osc_protocol.capture() as transcript:
        # completion without moment errors, but initial request succeeds
        with pytest.raises(MomentClosed):
            with buffer_a.write(file_path=tmp_path / "foo-1.aiff"):
                ...
        # completion without moment via on_completion lambda succeeds
        buffer_b.write(
            file_path=tmp_path / "foo-2.aiff", on_completion=lambda ctx: ctx.add_group()
        )
        # completion inside moment succeeds
        with context.at():
            with buffer_c.write(file_path=tmp_path / "foo-3.aiff"):
                context.add_group()
        # parameters
        buffer_a.write(
            file_path=tmp_path / "foo-4.wav",
            frame_count=16,
            header_format="WAV",
            leave_open=True,
            sample_format="FLOAT",
            starting_frame=5,
        )
    assert transcript.filtered(received=False, status=False) == [
        OscMessage(
            "/b_write", 0, str(tmp_path / "foo-1.aiff"), "aiff", "int24", -1, 0, 0
        ),
        OscMessage(
            "/b_write",
            1,
            str(tmp_path / "foo-2.aiff"),
            "aiff",
            "int24",
            -1,
            0,
            0,
            OscMessage("/g_new", 1000, 0, 1),
        ),
        OscMessage(
            "/b_write",
            2,
            str(tmp_path / "foo-3.aiff"),
            "aiff",
            "int24",
            -1,
            0,
            0,
            OscMessage("/g_new", 1001, 0, 1),
        ),
        OscMessage(
            "/b_write", 0, str(tmp_path / "foo-4.wav"), "wav", "float", 16, 5, 1
        ),
    ]


@pytest.mark.asyncio
async def test_zero_buffer(context: AsyncServer | Server) -> None:
    buffer_a = context.add_buffer(channel_count=1, frame_count=23)
    buffer_b = context.add_buffer(channel_count=1, frame_count=23)
    buffer_c = context.add_buffer(channel_count=1, frame_count=23)
    with context.osc_protocol.capture() as transcript:
        # completion without moment errors, but initial request succeeds
        with pytest.raises(MomentClosed):
            with buffer_a.zero():
                ...
        # completion without moment via on_completion lambda succeeds
        buffer_b.zero(on_completion=lambda ctx: ctx.add_group())
        # completion inside moment succeeds
        with context.at():
            with buffer_c.zero():
                context.add_group()
    assert transcript.filtered(received=False, status=False) == [
        OscMessage("/b_zero", 0),
        OscMessage("/b_zero", 1, OscMessage("/g_new", 1000, 0, 1)),
        OscMessage("/b_zero", 2, OscMessage("/g_new", 1001, 0, 1)),
    ]
