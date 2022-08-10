import asyncio
import logging

import pytest

from supriya import exceptions
from supriya.realtime import AsyncServer


@pytest.fixture(autouse=True)
def setup_logging(caplog):
    caplog.set_level(logging.INFO, logger="supriya")


@pytest.mark.asyncio
async def test_boot_only():
    server = AsyncServer()
    assert not server.is_running
    assert not server.is_owner
    await server.boot()
    assert server.is_running
    assert server.is_owner


@pytest.mark.asyncio
async def test_boot_and_quit():
    server = AsyncServer()
    assert not server.is_running
    assert not server.is_owner
    await server.boot()
    assert server.is_running
    assert server.is_owner
    await server.quit()
    assert not server.is_running
    assert not server.is_owner


@pytest.mark.asyncio
async def test_boot_and_boot():
    server = AsyncServer()
    assert not server.is_running
    assert not server.is_owner
    await server.boot()
    assert server.is_running
    assert server.is_owner
    with pytest.raises(exceptions.ServerOnline):
        await server.boot()
    assert server.is_running
    assert server.is_owner


@pytest.mark.asyncio
async def test_boot_and_quit_and_quit():
    server = AsyncServer()
    assert not server.is_running
    assert not server.is_owner
    await server.boot()
    assert server.is_running
    assert server.is_owner
    await server.quit()
    assert not server.is_running
    assert not server.is_owner
    await server.quit()
    assert not server.is_running
    assert not server.is_owner


@pytest.mark.asyncio
async def test_boot_and_connect():
    server = AsyncServer()
    assert not server.is_running
    assert not server.is_owner
    await server.boot()
    assert server.is_running
    assert server.is_owner
    with pytest.raises(exceptions.ServerOnline):
        await server.connect()
    assert server.is_running
    assert server.is_owner


@pytest.mark.asyncio
async def test_boot_a_and_boot_b_cannot_boot():
    server_a, server_b = AsyncServer(), AsyncServer()
    assert not server_a.is_running and not server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner
    await server_a.boot(maximum_logins=4)
    assert server_a.is_running and server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner
    with pytest.raises(exceptions.ServerCannotBoot):
        await server_b.boot(maximum_logins=4)
    assert server_a.is_running and server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner


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
async def test_boot_a_and_connect_b_and_quit_a():
    server_a, server_b = AsyncServer(), AsyncServer()
    assert not server_a.is_running and not server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner
    await server_a.boot(maximum_logins=2)
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
async def test_boot_a_and_connect_b_and_disconnect_b():
    server_a, server_b = AsyncServer(), AsyncServer()
    assert not server_a.is_running and not server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner
    await server_a.boot(maximum_logins=2)
    await server_b.connect()
    assert server_a.is_running and server_a.is_owner
    assert server_b.is_running and not server_b.is_owner
    await server_b.disconnect()
    assert server_a.is_running and server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner


@pytest.mark.asyncio
async def test_boot_a_and_connect_b_and_disconnect_a():
    server_a, server_b = AsyncServer(), AsyncServer()
    assert not server_a.is_running and not server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner
    await server_a.boot(maximum_logins=2)
    await server_b.connect()
    assert server_a.is_running and server_a.is_owner
    assert server_b.is_running and not server_b.is_owner
    with pytest.raises(exceptions.OwnedServerShutdown):
        await server_a.disconnect()
    assert server_a.is_running and server_a.is_owner
    assert server_b.is_running and not server_b.is_owner


@pytest.mark.asyncio
async def test_boot_a_and_connect_b_and_quit_b():
    server_a, server_b = AsyncServer(), AsyncServer()
    assert not server_a.is_running and not server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner
    await server_a.boot(maximum_logins=2)
    await server_b.connect()
    assert server_a.is_running and server_a.is_owner
    assert server_b.is_running and not server_b.is_owner
    with pytest.raises(exceptions.UnownedServerShutdown):
        await server_b.quit()
    assert server_a.is_running and server_a.is_owner
    assert server_b.is_running and not server_b.is_owner


@pytest.mark.asyncio
async def test_boot_a_and_connect_b_and_force_quit_b():
    server_a, server_b = AsyncServer(), AsyncServer()
    assert not server_a.is_running and not server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner
    await server_a.boot(maximum_logins=2)
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
