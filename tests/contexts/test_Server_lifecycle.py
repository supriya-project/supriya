import asyncio
import logging
import sys

import pytest

from supriya.contexts.realtime import (
    DEFAULT_HEALTHCHECK,
    AsyncServer,
    BootStatus,
    Server,
)
from supriya.exceptions import (
    OwnedServerShutdown,
    ServerCannotBoot,
    ServerOnline,
    TooManyClients,
    UnownedServerShutdown,
)
from supriya.osc import find_free_port
from supriya.scsynth import Options

supernova = pytest.param(
    "supernova",
    marks=pytest.mark.skipif(
        sys.platform.startswith("win"), reason="Supernova won't boot on Windows"
    ),
)


@pytest.fixture(autouse=True)
def use_caplog(caplog):
    caplog.set_level(logging.INFO)


@pytest.fixture(autouse=True)
def healthcheck_attempts(monkeypatch):
    monkeypatch.setattr(DEFAULT_HEALTHCHECK, "max_attempts", 1)


@pytest.mark.asyncio
@pytest.mark.parametrize("executable", ["scsynth", supernova])
@pytest.mark.parametrize("context_class", [AsyncServer, Server])
async def test_boot_only(executable, context_class):
    context = context_class()
    assert context.boot_status == BootStatus.OFFLINE
    assert not context.is_owner
    result = context.boot(executable=executable)
    if asyncio.iscoroutine(result):
        await result
    assert context.boot_status == BootStatus.ONLINE
    assert context.is_owner


@pytest.mark.asyncio
@pytest.mark.parametrize("executable", ["scsynth", supernova])
@pytest.mark.parametrize("context_class", [AsyncServer, Server])
async def test_boot_and_quit(executable, context_class):
    context = context_class()
    assert context.boot_status == BootStatus.OFFLINE
    assert not context.is_owner
    result = context.boot(executable=executable)
    if asyncio.iscoroutine(result):
        await result
    assert context.boot_status == BootStatus.ONLINE
    assert context.is_owner
    result = context.quit()
    if asyncio.iscoroutine(result):
        await result
    assert context.boot_status == BootStatus.OFFLINE
    assert not context.is_owner


@pytest.mark.asyncio
@pytest.mark.parametrize("executable", ["scsynth", supernova])
@pytest.mark.parametrize("context_class", [AsyncServer, Server])
async def test_boot_and_boot(executable, context_class):
    context = context_class()
    assert context.boot_status == BootStatus.OFFLINE
    assert not context.is_owner
    result = context.boot(executable=executable)
    if asyncio.iscoroutine(result):
        await result
    assert context.boot_status == BootStatus.ONLINE
    assert context.is_owner
    with pytest.raises(ServerOnline):
        result = context.boot(executable=executable)
        if asyncio.iscoroutine(result):
            await result
    assert context.boot_status == BootStatus.ONLINE
    assert context.is_owner


@pytest.mark.asyncio
@pytest.mark.parametrize("executable", ["scsynth", supernova])
@pytest.mark.parametrize("context_class", [AsyncServer, Server])
async def test_boot_and_quit_and_quit(executable, context_class):
    context = context_class()
    assert context.boot_status == BootStatus.OFFLINE
    assert not context.is_owner
    result = context.boot(executable=executable)
    if asyncio.iscoroutine(result):
        await result
    assert context.boot_status == BootStatus.ONLINE
    assert context.is_owner
    result = context.quit()
    if asyncio.iscoroutine(result):
        await result
    assert context.boot_status == BootStatus.OFFLINE
    assert not context.is_owner
    result = context.quit()
    if asyncio.iscoroutine(result):
        await result
    assert context.boot_status == BootStatus.OFFLINE
    assert not context.is_owner


@pytest.mark.asyncio
@pytest.mark.parametrize("executable", ["scsynth", supernova])
@pytest.mark.parametrize("context_class", [AsyncServer, Server])
async def test_boot_and_connect(executable, context_class):
    context = context_class()
    assert context.boot_status == BootStatus.OFFLINE
    assert not context.is_owner
    result = context.boot(executable=executable)
    if asyncio.iscoroutine(result):
        await result
    assert context.boot_status == BootStatus.ONLINE
    assert context.is_owner
    with pytest.raises(ServerOnline):
        result = context.connect()
        if asyncio.iscoroutine(result):
            await result
    assert context.boot_status == BootStatus.ONLINE
    assert context.is_owner


@pytest.mark.asyncio
@pytest.mark.parametrize("executable", ["scsynth", supernova])
@pytest.mark.parametrize("context_class", [AsyncServer, Server])
async def test_boot_a_and_boot_b_cannot_boot(executable, context_class):
    context_a, context_b = context_class(), context_class()
    assert context_a.boot_status == BootStatus.OFFLINE and not context_a.is_owner
    assert context_b.boot_status == BootStatus.OFFLINE and not context_b.is_owner
    result = context_a.boot(maximum_logins=4, executable=executable)
    if asyncio.iscoroutine(result):
        await result
    assert context_a.boot_status == BootStatus.ONLINE and context_a.is_owner
    assert context_b.boot_status == BootStatus.OFFLINE and not context_b.is_owner
    with pytest.raises(ServerCannotBoot):
        result = context_b.boot(maximum_logins=4, executable=executable)
        if asyncio.iscoroutine(result):
            await result
    assert context_a.boot_status == BootStatus.ONLINE and context_a.is_owner
    assert context_b.boot_status == BootStatus.OFFLINE and not context_b.is_owner


# scsynth only
@pytest.mark.asyncio
@pytest.mark.parametrize("executable", ["scsynth", supernova])
@pytest.mark.parametrize("context_class", [AsyncServer, Server])
async def test_boot_a_and_connect_b_too_many_clients(executable, context_class):
    context_a, context_b = context_class(), context_class()
    assert context_a.boot_status == BootStatus.OFFLINE and not context_a.is_owner
    assert context_b.boot_status == BootStatus.OFFLINE and not context_b.is_owner
    result = context_a.boot(maximum_logins=1)
    if asyncio.iscoroutine(result):
        await result
    assert context_a.boot_status == BootStatus.ONLINE and context_a.is_owner
    assert context_b.boot_status == BootStatus.OFFLINE and not context_b.is_owner
    with pytest.raises(TooManyClients):
        result = context_b.connect()
        if asyncio.iscoroutine(result):
            await result
    assert context_a.boot_status == BootStatus.ONLINE and context_a.is_owner
    assert context_b.boot_status == BootStatus.OFFLINE and not context_b.is_owner


@pytest.mark.asyncio
@pytest.mark.parametrize("executable", ["scsynth", supernova])
@pytest.mark.parametrize("context_class", [AsyncServer, Server])
async def test_boot_a_and_connect_b_and_quit_a(executable, context_class):
    context_a, context_b = context_class(), context_class()
    assert context_a.boot_status == BootStatus.OFFLINE and not context_a.is_owner
    assert context_b.boot_status == BootStatus.OFFLINE and not context_b.is_owner
    result = context_a.boot(maximum_logins=2, executable=executable)
    if asyncio.iscoroutine(result):
        await result
    result = context_b.connect()
    if asyncio.iscoroutine(result):
        await result
    assert context_a.boot_status == BootStatus.ONLINE and context_a.is_owner
    assert context_b.boot_status == BootStatus.ONLINE and not context_b.is_owner
    result = context_a.quit()
    if asyncio.iscoroutine(result):
        await result
    assert context_a.boot_status == BootStatus.OFFLINE and not context_a.is_owner
    for _ in range(100):
        await asyncio.sleep(0.1)
        if context_b.boot_status == BootStatus.OFFLINE:
            break
    assert context_b.boot_status == BootStatus.OFFLINE and not context_b.is_owner


@pytest.mark.asyncio
@pytest.mark.parametrize("executable", ["scsynth", supernova])
@pytest.mark.parametrize("context_class", [AsyncServer, Server])
async def test_boot_a_and_connect_b_and_disconnect_b(executable, context_class):
    context_a, context_b = context_class(), context_class()
    assert context_a.boot_status == BootStatus.OFFLINE and not context_a.is_owner
    assert context_b.boot_status == BootStatus.OFFLINE and not context_b.is_owner
    result = context_a.boot(maximum_logins=2, executable=executable)
    if asyncio.iscoroutine(result):
        await result
    result = context_b.connect()
    if asyncio.iscoroutine(result):
        await result
    assert context_a.boot_status == BootStatus.ONLINE and context_a.is_owner
    assert context_b.boot_status == BootStatus.ONLINE and not context_b.is_owner
    result = context_b.disconnect()
    if asyncio.iscoroutine(result):
        await result
    assert context_a.boot_status == BootStatus.ONLINE and context_a.is_owner
    assert context_b.boot_status == BootStatus.OFFLINE and not context_b.is_owner


@pytest.mark.asyncio
@pytest.mark.parametrize("executable", ["scsynth", supernova])
@pytest.mark.parametrize("context_class", [AsyncServer, Server])
async def test_boot_a_and_connect_b_and_disconnect_a(executable, context_class):
    context_a, context_b = context_class(), context_class()
    assert context_a.boot_status == BootStatus.OFFLINE and not context_a.is_owner
    assert context_b.boot_status == BootStatus.OFFLINE and not context_b.is_owner
    result = context_a.boot(maximum_logins=2, executable=executable)
    if asyncio.iscoroutine(result):
        await result
    result = context_b.connect()
    if asyncio.iscoroutine(result):
        await result
    assert context_a.boot_status == BootStatus.ONLINE and context_a.is_owner
    assert context_b.boot_status == BootStatus.ONLINE and not context_b.is_owner
    with pytest.raises(OwnedServerShutdown):
        result = context_a.disconnect()
        if asyncio.iscoroutine(result):
            await result
    assert context_a.boot_status == BootStatus.ONLINE and context_a.is_owner
    assert context_b.boot_status == BootStatus.ONLINE and not context_b.is_owner


@pytest.mark.asyncio
@pytest.mark.parametrize("executable", ["scsynth", supernova])
@pytest.mark.parametrize("context_class", [AsyncServer, Server])
async def test_boot_a_and_connect_b_and_quit_b(executable, context_class):
    context_a, context_b = context_class(), context_class()
    assert context_a.boot_status == BootStatus.OFFLINE and not context_a.is_owner
    assert context_b.boot_status == BootStatus.OFFLINE and not context_b.is_owner
    result = context_a.boot(maximum_logins=2, executable=executable)
    if asyncio.iscoroutine(result):
        await result
    result = context_b.connect()
    if asyncio.iscoroutine(result):
        await result
    assert context_a.boot_status == BootStatus.ONLINE and context_a.is_owner
    assert context_b.boot_status == BootStatus.ONLINE and not context_b.is_owner
    with pytest.raises(UnownedServerShutdown):
        result = context_b.quit()
        if asyncio.iscoroutine(result):
            await result
    assert context_a.boot_status == BootStatus.ONLINE and context_a.is_owner
    assert context_b.boot_status == BootStatus.ONLINE and not context_b.is_owner


@pytest.mark.asyncio
@pytest.mark.parametrize("executable", ["scsynth", supernova])
@pytest.mark.parametrize("context_class", [AsyncServer, Server])
async def test_boot_a_and_connect_b_and_force_quit_b(executable, context_class):
    context_a, context_b = context_class(), context_class()
    assert context_a.boot_status == BootStatus.OFFLINE and not context_a.is_owner
    assert context_b.boot_status == BootStatus.OFFLINE and not context_b.is_owner
    result = context_a.boot(maximum_logins=2, executable=executable)
    if asyncio.iscoroutine(result):
        await result
    result = context_b.connect()
    if asyncio.iscoroutine(result):
        await result
    assert context_a.boot_status == BootStatus.ONLINE and context_a.is_owner
    assert context_b.boot_status == BootStatus.ONLINE and not context_b.is_owner
    result = context_b.quit(force=True)
    if asyncio.iscoroutine(result):
        await result
    assert context_b.boot_status == BootStatus.OFFLINE and not context_b.is_owner
    for _ in range(100):
        await asyncio.sleep(0.1)
        if context_a.boot_status == BootStatus.OFFLINE:
            break
    assert context_a.boot_status == BootStatus.OFFLINE and not context_a.is_owner


@pytest.mark.asyncio
@pytest.mark.parametrize("executable", ["scsynth", supernova])
@pytest.mark.parametrize("context_class", [AsyncServer, Server])
@pytest.mark.parametrize("maximum_node_count", [1204, 8192])
async def test_boot_reboot_sticky_options(
    executable, maximum_node_count, context_class
):
    context = context_class()
    port = find_free_port()
    options = Options(
        executable=executable, maximum_node_count=maximum_node_count, port=port
    )
    result = context.boot(options=options)
    if asyncio.iscoroutine(result):
        await result
    assert context.boot_status == BootStatus.ONLINE
    assert context.options.maximum_node_count == options.maximum_node_count
    assert context.options.port == options.port
    result = context.quit()
    if asyncio.iscoroutine(result):
        await result
    assert context.boot_status == BootStatus.OFFLINE
    assert context.options.maximum_node_count == options.maximum_node_count
    assert context.options.port == options.port
    result = context.boot()
    if asyncio.iscoroutine(result):
        await result
    assert context.boot_status == BootStatus.ONLINE
    assert context.options.maximum_node_count == options.maximum_node_count
    assert context.options.port == options.port
    result = context.quit()
    if asyncio.iscoroutine(result):
        await result
    assert context.boot_status == BootStatus.OFFLINE
    result = context.boot(memory_size=8199)
    if asyncio.iscoroutine(result):
        await result
    assert context.boot_status == BootStatus.ONLINE
    assert context.options.memory_size == 8199
    assert context.options.maximum_node_count == options.maximum_node_count
    assert context.options.port == options.port
    result = context.quit()
    if asyncio.iscoroutine(result):
        await result
    assert context.boot_status == BootStatus.OFFLINE
    result = context.boot(options=options)
    if asyncio.iscoroutine(result):
        await result
    assert context.boot_status == BootStatus.ONLINE
    assert context.options.memory_size == options.memory_size
    assert context.options.maximum_node_count == options.maximum_node_count
    assert context.options.port == options.port
