import asyncio
import logging

import pytest

import supriya
from supriya import exceptions
from supriya.realtime import AsyncServer
from supriya.realtime.protocols import AsyncProcessProtocol
from supriya.scsynth import Options


@pytest.fixture(autouse=True)
def setup_logging(caplog):
    caplog.set_level(logging.INFO, logger="supriya")


@pytest.mark.asyncio
@pytest.mark.parametrize("executable", [None, "scsynth", "supernova"])
async def test_boot_only(executable):
    server = AsyncServer()
    assert not server.is_running
    assert not server.is_owner
    await server.boot(executable=executable)
    assert server.is_running
    assert server.is_owner


@pytest.mark.asyncio
@pytest.mark.parametrize("executable", [None, "supernova"])
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
@pytest.mark.parametrize("executable", [None, "supernova"])
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
@pytest.mark.parametrize("executable", [None, "supernova"])
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
@pytest.mark.parametrize("executable", [None, "supernova"])
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
@pytest.mark.parametrize("executable", [None, "supernova"])
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
@pytest.mark.parametrize("executable", [None, "supernova"])
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
@pytest.mark.parametrize("executable", [None, "supernova"])
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
@pytest.mark.parametrize("executable", [None, "supernova"])
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
@pytest.mark.parametrize("executable", [None, "supernova"])
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
@pytest.mark.parametrize("executable", [None, "supernova"])
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
@pytest.mark.parametrize(
    "executable,maximum_node_count",
    [
        (serv, opt)
        for serv in ["scsynth", "supernova"]
        for opt in [32, 64, 128, 1204, 8192]
    ],
)
async def test_boot_reboot_sticky_options_1(executable, maximum_node_count):
    server = AsyncServer()
    port = supriya.osc.utils.find_free_port()
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


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "executable,memory_size",
    [(serv, opt) for serv in ["scsynth", "supernova"] for opt in [13131, 21712, 12345]],
)
async def test_boot_reboot_sticky_options_2(executable, memory_size):
    server = AsyncServer()
    port = supriya.osc.utils.find_free_port()
    options = Options(executable=executable, memory_size=memory_size, port=port)
    await server.boot(options=options)
    assert server.is_running
    assert server._options.memory_size == options.memory_size
    assert server.port == options.port
    await server.quit()
    assert not server.is_running
    await server.boot(memory_size=8199)
    assert server.is_running
    assert server._options.memory_size == 8199
    assert server.port == options.port


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "executable,control_bus_channel_count",
    [(serv, opt) for serv in ["scsynth", "supernova"] for opt in [16385, 6388, 12121]],
)
async def test_boot_reboot_sticky_options_3(executable, control_bus_channel_count):
    server = AsyncServer()
    port = supriya.osc.utils.find_free_port()
    options = Options(
        executable=executable,
        control_bus_channel_count=control_bus_channel_count,
        port=port,
    )
    await server.boot(options=options)
    assert server.is_running
    assert (
        server._options.control_bus_channel_count == options.control_bus_channel_count
    )
    assert server.port == options.port
    await server.quit()
    assert not server.is_running
    await server.boot(options=options, control_bus_channel_count=7777)
    assert server.is_running
    assert server._options.control_bus_channel_count == 7777
    assert server.port == options.port
    await server.quit()
    assert not server.is_running
    await server.boot(options=options)
    assert server.is_running
    assert server._options.control_bus_channel_count == control_bus_channel_count
    assert server.port == options.port


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "executable,maximum_node_count",
    [
        (serv, opt)
        for serv in ["scsynth", "supernova"]
        for opt in [32, 64, 128, 1204, 8192]
    ],
)
async def test_connect_and_reconnect_sticky_options_1(executable, maximum_node_count):
    port = supriya.osc.utils.find_free_port()
    options = Options(
        executable=executable,
        maximum_logins=5,
        maximum_node_count=maximum_node_count,
        port=port,
    )
    protocol = AsyncProcessProtocol()
    await protocol.boot(options)
    # We still need to wait for scsynth to boot
    await asyncio.sleep(3.0)
    server = AsyncServer()
    await server.connect(options=options)
    assert server.is_running and not server.is_owner
    assert server._options.maximum_node_count == options.maximum_node_count
    assert server.port == port
    await server.disconnect()
    await server.connect(port=port)
    assert server._options.maximum_node_count == options.maximum_node_count
    assert server.port == port
    await server.disconnect()
    await server.connect(maximum_node_count=1101)
    assert server._options.maximum_node_count == 1101
    assert server.port == port
    await server.disconnect()
    await server.connect(options=options)
    assert server._options.maximum_node_count == options.maximum_node_count
    assert server.port == port
    await server.disconnect()
    new_options = Options(maximum_node_count=1027, port=port)
    await server.connect(options=new_options)
    assert server._options.maximum_node_count == 1027
    assert server.port == port
    protocol.quit()
