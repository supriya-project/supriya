import asyncio
import logging
import sys

import pytest

from supriya import exceptions
from supriya.osc import find_free_port
from supriya.realtime import AsyncServer
from supriya.realtime.servers import DEFAULT_HEALTHCHECK
from supriya.scsynth import Options

supernova_skip_win = pytest.param(
    "supernova",
    marks=pytest.mark.skipif(
        sys.platform.startswith("win"), reason="Supernova won't boot on Windows"
    ),
)


@pytest.fixture(autouse=True)
def healthcheck_attempts(monkeypatch):
    # TODO: This should be settable at 1, not 2
    monkeypatch.setattr(DEFAULT_HEALTHCHECK, "max_attempts", 2)


@pytest.fixture(autouse=True)
def setup_logging(caplog):
    caplog.set_level(logging.DEBUG, logger="supriya")


@pytest.mark.asyncio
@pytest.mark.parametrize("executable", [None, "scsynth", supernova_skip_win])
async def test_boot_only(executable):
    server = AsyncServer()
    assert not server.is_running
    assert not server.is_owner
    await server.boot(executable=executable)
    assert server.is_running
    assert server.is_owner


@pytest.mark.asyncio
@pytest.mark.parametrize("executable", [None, supernova_skip_win])
async def test_boot_and_quit(executable):
    server = AsyncServer()
    assert not server.is_running
    assert not server.is_owner
    await server.boot(executable=executable)
    assert server.is_running
    assert server.is_owner
    await server.quit()
    assert not server.is_running
    assert not server.is_owner


@pytest.mark.asyncio
@pytest.mark.parametrize("executable", [None, supernova_skip_win])
async def test_boot_and_boot(executable):
    server = AsyncServer()
    assert not server.is_running
    assert not server.is_owner
    await server.boot(executable=executable)
    assert server.is_running
    assert server.is_owner
    with pytest.raises(exceptions.ServerOnline):
        await server.boot(executable=executable)
    assert server.is_running
    assert server.is_owner


@pytest.mark.asyncio
@pytest.mark.parametrize("executable", [None, supernova_skip_win])
async def test_boot_and_quit_and_quit(executable):
    server = AsyncServer()
    assert not server.is_running
    assert not server.is_owner
    await server.boot(executable=executable)
    assert server.is_running
    assert server.is_owner
    await server.quit()
    assert not server.is_running
    assert not server.is_owner
    await server.quit()
    assert not server.is_running
    assert not server.is_owner


@pytest.mark.asyncio
@pytest.mark.parametrize("executable", [None, supernova_skip_win])
async def test_boot_and_connect(executable):
    server = AsyncServer()
    assert not server.is_running
    assert not server.is_owner
    await server.boot(executable=executable)
    assert server.is_running
    assert server.is_owner
    with pytest.raises(exceptions.ServerOnline):
        await server.connect()
    assert server.is_running
    assert server.is_owner


@pytest.mark.asyncio
@pytest.mark.parametrize("executable", [None, supernova_skip_win])
async def test_boot_a_and_boot_b_cannot_boot(executable):
    server_a, server_b = AsyncServer(), AsyncServer()
    assert not server_a.is_running and not server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner
    await server_a.boot(maximum_logins=4, executable=executable)
    assert server_a.is_running and server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner
    with pytest.raises(exceptions.ServerCannotBoot):
        await server_b.boot(maximum_logins=4, executable=executable)
    assert server_a.is_running and server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner


# scsynth only
@pytest.mark.asyncio
async def test_boot_a_and_connect_b_too_many_clients():
    server_a, server_b = AsyncServer(), AsyncServer()
    assert not server_a.is_running and not server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner
    await server_a.boot(maximum_logins=1)
    assert server_a.is_running and server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner
    with pytest.raises(exceptions.TooManyClients):
        await server_b.connect()
    assert server_a.is_running and server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner


@pytest.mark.asyncio
@pytest.mark.parametrize("executable", [None])
async def test_boot_a_and_connect_b_and_quit_a(executable):
    server_a, server_b = AsyncServer(), AsyncServer()
    assert not server_a.is_running and not server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner
    await server_a.boot(maximum_logins=2, executable=executable)
    await server_b.connect()
    assert server_a.is_running and server_a.is_owner
    assert server_b.is_running and not server_b.is_owner
    await server_a.quit()
    assert not server_a.is_running and not server_a.is_owner
    for _ in range(100):
        await asyncio.sleep(0.1)
        if not server_b.is_running:
            break
    assert not server_b.is_running and not server_b.is_owner


@pytest.mark.asyncio
@pytest.mark.parametrize("executable", [None, supernova_skip_win])
async def test_boot_a_and_connect_b_and_disconnect_b(executable):
    server_a, server_b = AsyncServer(), AsyncServer()
    assert not server_a.is_running and not server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner
    await server_a.boot(maximum_logins=2, executable=executable)
    await server_b.connect()
    assert server_a.is_running and server_a.is_owner
    assert server_b.is_running and not server_b.is_owner
    await server_b.disconnect()
    assert server_a.is_running and server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner


@pytest.mark.asyncio
@pytest.mark.parametrize("executable", [None, supernova_skip_win])
async def test_boot_a_and_connect_b_and_disconnect_a(executable):
    server_a, server_b = AsyncServer(), AsyncServer()
    assert not server_a.is_running and not server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner
    await server_a.boot(maximum_logins=2, executable=executable)
    await server_b.connect()
    assert server_a.is_running and server_a.is_owner
    assert server_b.is_running and not server_b.is_owner
    with pytest.raises(exceptions.OwnedServerShutdown):
        await server_a.disconnect()
    assert server_a.is_running and server_a.is_owner
    assert server_b.is_running and not server_b.is_owner


@pytest.mark.asyncio
@pytest.mark.parametrize("executable", [None, supernova_skip_win])
async def test_boot_a_and_connect_b_and_quit_b(executable):
    server_a, server_b = AsyncServer(), AsyncServer()
    assert not server_a.is_running and not server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner
    await server_a.boot(maximum_logins=2, executable=executable)
    await server_b.connect()
    assert server_a.is_running and server_a.is_owner
    assert server_b.is_running and not server_b.is_owner
    with pytest.raises(exceptions.UnownedServerShutdown):
        await server_b.quit()
    assert server_a.is_running and server_a.is_owner
    assert server_b.is_running and not server_b.is_owner


@pytest.mark.asyncio
@pytest.mark.parametrize("executable", [None])
async def test_boot_a_and_connect_b_and_force_quit_b(executable):
    server_a, server_b = AsyncServer(), AsyncServer()
    assert not server_a.is_running and not server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner
    await server_a.boot(maximum_logins=2, executable=executable)
    await server_b.connect()
    assert server_a.is_running and server_a.is_owner
    assert server_b.is_running and not server_b.is_owner
    await server_b.quit(force=True)
    assert not server_b.is_running and not server_b.is_owner
    for _ in range(100):
        await asyncio.sleep(0.1)
        if not server_a.is_running:
            break
    assert not server_a.is_running and not server_a.is_owner


@pytest.mark.asyncio
@pytest.mark.parametrize("executable", [None, supernova_skip_win])
@pytest.mark.parametrize("maximum_node_count", [1204, 8192])
async def test_boot_reboot_sticky_options(executable, maximum_node_count):
    server = AsyncServer()
    port = find_free_port()
    options = Options(
        executable=executable, maximum_node_count=maximum_node_count, port=port
    )
    await server.boot(options=options)
    assert server.is_running
    assert server._options.maximum_node_count == options.maximum_node_count
    assert server.port == options.port
    await server.quit()
    assert not server.is_running
    assert server._options.maximum_node_count == options.maximum_node_count
    assert server.port == options.port
    await server.boot()
    assert server.is_running
    assert server._options.maximum_node_count == options.maximum_node_count
    assert server.port == options.port
    await server.quit()
    assert not server.is_running
    await server.boot(memory_size=8199)
    assert server.is_running
    assert server._options.memory_size == 8199
    assert server._options.maximum_node_count == options.maximum_node_count
    assert server.port == options.port
    await server.quit()
    assert not server.is_running
    await server.boot(options=options)
    assert server.is_running
    assert server._options.memory_size == options.memory_size
    assert server._options.maximum_node_count == options.maximum_node_count
    assert server.port == options.port
