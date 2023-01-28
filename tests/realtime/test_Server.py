import subprocess
import sys
import time

import pytest
from uqbar.strings import normalize

import supriya
from supriya import exceptions, scsynth
from supriya.assets.synthdefs import default
from supriya.osc import OscMessage, find_free_port
from supriya.realtime import Server
from supriya.realtime.servers import DEFAULT_HEALTHCHECK
from supriya.scsynth import Options, SyncProcessProtocol

supernova_skip_win = pytest.param(
    "supernova",
    marks=pytest.mark.skipif(
        sys.platform.startswith("win"), reason="Supernova won't boot on Windows"
    ),
)


@pytest.fixture(autouse=True)
def healthcheck_attempts(monkeypatch):
    monkeypatch.setattr(DEFAULT_HEALTHCHECK, "max_attempts", 1)


@pytest.mark.parametrize("executable", [None, "scsynth", supernova_skip_win])
def test_boot_options(executable):
    server = supriya.realtime.Server()
    try:
        boot_options = Options(
            memory_size=8192 * 32, buffer_count=2048, executable=executable
        )
        # Default
        server.boot()
        assert isinstance(server.options, type(boot_options))
        assert server.options.buffer_count == 1024
        assert server.options.memory_size == 8192
        server.quit()
        # With Options
        server.boot(options=boot_options)
        assert isinstance(server.options, type(boot_options))
        assert server.options.buffer_count == 2048
        assert server.options.memory_size == 8192 * 32
        server.quit()
        # With **kwargs
        server.boot(buffer_count=2048)
        assert isinstance(server.options, type(boot_options))
        assert server.options.buffer_count == 2048
        # options are sticky now
        assert server.options.memory_size == 8192 * 32
        server.quit()
        # With Options and **kwargs
        server.boot(buffer_count=4096, options=boot_options)
        assert isinstance(server.options, type(boot_options))
        assert server.options.buffer_count == 4096
        assert server.options.memory_size == 8192 * 32
        server.quit()
    finally:
        if server.is_running:
            server.quit()


@pytest.mark.skip("Reimplementing")
def test_server_boot_errors(mocker):
    def check_scsynth():
        process = subprocess.Popen("ps -Af", shell=True, stdout=subprocess.PIPE)
        output, _ = process.communicate()
        return output.decode()

    assert "scsynth" not in check_scsynth()

    server = supriya.realtime.Server()
    server.boot()
    assert "scsynth" in check_scsynth()
    assert server.is_running
    assert server.osc_protocol.is_running

    server.quit()
    assert "scsynth" not in check_scsynth()
    assert not server.is_running
    assert not server.osc_protocol.is_running

    with pytest.raises(supriya.exceptions.ServerCannotBoot), mocker.patch.object(
        supriya.realtime.Server, "_read_scsynth_boot_output"
    ) as patch:
        patch.side_effect = supriya.exceptions.ServerCannotBoot()
        server.boot()

    assert "scsynth" not in check_scsynth()
    assert not server.is_running
    assert not server.osc_protocol.is_running


@pytest.mark.parametrize("executable", [None, supernova_skip_win])
def test_boot_and_quit(executable):
    server = Server()
    assert not server.is_running
    assert not server.is_owner
    server.boot(executable=executable)
    assert server.is_running
    assert server.is_owner
    server.quit()
    assert not server.is_running
    assert not server.is_owner


@pytest.mark.parametrize("executable", [None, supernova_skip_win])
def test_boot_and_quit_with_resources(executable):
    server = Server()
    server.boot(executable=executable)
    server.add_buffer(channel_count=1, frame_count=1024)
    server.add_bus("audio")
    server.add_bus("control")
    server.add_group()
    server.add_synth()
    server.quit()


@pytest.mark.parametrize("executable", [None, supernova_skip_win])
def test_boot_and_boot(executable):
    server = Server()
    assert not server.is_running
    assert not server.is_owner
    server.boot(executable=executable)
    assert server.is_running
    assert server.is_owner
    with pytest.raises(exceptions.ServerOnline):
        server.boot()
    assert server.is_running
    assert server.is_owner


@pytest.mark.parametrize("executable", [None, supernova_skip_win])
def test_boot_and_quit_and_quit(executable):
    server = Server()
    assert not server.is_running
    assert not server.is_owner
    server.boot(executable=executable)
    assert server.is_running
    assert server.is_owner
    server.quit()
    assert not server.is_running
    assert not server.is_owner
    server.quit()
    assert not server.is_running
    assert not server.is_owner


@pytest.mark.parametrize("executable", [None, supernova_skip_win])
def test_boot_and_connect(executable):
    server = Server()
    assert not server.is_running
    assert not server.is_owner
    server.boot(executable=executable)
    assert server.is_running
    assert server.is_owner
    with pytest.raises(exceptions.ServerOnline):
        server.connect()
    assert server.is_running
    assert server.is_owner


@pytest.mark.parametrize("executable", [None, supernova_skip_win])
def test_boot_a_and_connect_b(executable):
    server_a, server_b = Server(), Server()
    assert not server_a.is_running and not server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner
    server_a.boot(maximum_logins=4, executable=executable)
    assert server_a.is_running and server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner
    server_b.connect()
    assert server_a.is_running and server_a.is_owner
    assert server_b.is_running and not server_b.is_owner
    assert server_a.query(False) == server_b.query(False)
    assert server_a.client_id == 0 and server_b.client_id == 1
    assert server_a.default_group.node_id == 1 and server_b.default_group.node_id == 2
    group = supriya.Group()
    group.allocate(target_node=server_a)
    assert server_a.root_node[0][0] is group
    server_b.sync()
    assert server_b.root_node[0][0] is not group
    assert server_a.query(False) == server_b.query(False)


@pytest.mark.parametrize("executable", [None, supernova_skip_win])
def test_boot_a_and_boot_b_cannot_boot(executable):
    server_a, server_b = Server(), Server()
    assert not server_a.is_running and not server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner
    server_a.boot(maximum_logins=4, executable=executable)
    assert server_a.is_running and server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner
    with pytest.raises(exceptions.ServerCannotBoot):
        server_b.boot(maximum_logins=4, executable=executable)
    assert server_a.is_running and server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner


#  scsynth only
def test_boot_a_and_connect_b_too_many_clients():
    server_a, server_b = Server(), Server()
    assert not server_a.is_running and not server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner
    server_a.boot(maximum_logins=1)
    assert server_a.is_running and server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner
    with pytest.raises(exceptions.TooManyClients):
        server_b.connect()
    assert server_a.is_running and server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner


@pytest.mark.parametrize("executable", [None])
def test_boot_a_and_connect_b_and_quit_a(executable):
    server_a, server_b = Server(), Server()
    assert not server_a.is_running and not server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner
    server_a.boot(maximum_logins=2, executable=executable)
    server_b.connect()
    assert server_a.is_running and server_a.is_owner
    assert server_b.is_running and not server_b.is_owner
    server_a.quit()
    assert not server_a.is_running and not server_a.is_owner
    for _ in range(100):
        time.sleep(0.1)
        if not server_b.is_running:
            break
    assert not server_b.is_running and not server_b.is_owner


@pytest.mark.parametrize("executable", [None, supernova_skip_win])
def test_boot_a_and_connect_b_and_disconnect_b(executable):
    server_a, server_b = Server(), Server()
    assert not server_a.is_running and not server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner
    server_a.boot(maximum_logins=2, executable=executable)
    server_b.connect()
    assert server_a.is_running and server_a.is_owner
    assert server_b.is_running and not server_b.is_owner
    server_b.disconnect()
    assert server_a.is_running and server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner


@pytest.mark.parametrize("executable", [None, supernova_skip_win])
def test_boot_a_and_connect_b_and_disconnect_a(executable):
    server_a, server_b = Server(), Server()
    assert not server_a.is_running and not server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner
    server_a.boot(maximum_logins=2, executable=executable)
    server_b.connect()
    assert server_a.is_running and server_a.is_owner
    assert server_b.is_running and not server_b.is_owner
    with pytest.raises(exceptions.OwnedServerShutdown):
        server_a.disconnect()
    assert server_a.is_running and server_a.is_owner
    assert server_b.is_running and not server_b.is_owner


@pytest.mark.parametrize("executable", [None, supernova_skip_win])
def test_boot_a_and_connect_b_and_quit_b(executable):
    server_a, server_b = Server(), Server()
    assert not server_a.is_running and not server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner
    server_a.boot(maximum_logins=2, executable=executable)
    server_b.connect()
    assert server_a.is_running and server_a.is_owner
    assert server_b.is_running and not server_b.is_owner
    with pytest.raises(exceptions.UnownedServerShutdown):
        server_b.quit()
    assert server_a.is_running and server_a.is_owner
    assert server_b.is_running and not server_b.is_owner


@pytest.mark.parametrize("executable", [None])
def test_boot_a_and_connect_b_and_force_quit_b(executable):
    server_a, server_b = Server(), Server()
    assert not server_a.is_running and not server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner
    server_a.boot(maximum_logins=2, executable=executable)
    server_b.connect()
    assert server_a.is_running and server_a.is_owner
    assert server_b.is_running and not server_b.is_owner
    server_b.quit(force=True)
    assert not server_b.is_running and not server_b.is_owner
    for _ in range(100):
        time.sleep(0.1)
        if not server_a.is_running:
            break
    assert not server_a.is_running and not server_a.is_owner


def test_shared_resources():
    server_a, server_b = Server(), Server()
    server_a.boot(maximum_logins=2)
    server_b.connect()
    with supriya.SynthDefBuilder(frequency=440) as builder:
        _ = supriya.ugens.Out.ar(
            bus=0, source=supriya.ugens.SinOsc.ar(frequency=builder["frequency"])
        )
    synthdef = builder.build(name="foo")
    synth = supriya.Synth(synthdef=synthdef)
    transcript_a = server_a.osc_protocol.capture()
    transcript_b = server_b.osc_protocol.capture()
    with transcript_a, transcript_b:
        synth.allocate(target_node=server_b)
        time.sleep(0.1)  # Wait for all clients to receive /n_go
    assert synth not in server_a
    assert synth in server_b
    assert [
        (label, osc_message)
        for _, label, osc_message in transcript_a
        if osc_message.address not in ["/status", "/status.reply"]
    ] == [("R", OscMessage("/n_go", 67109864, 2, -1, -1, 0))]
    assert [
        (label, osc_message)
        for _, label, osc_message in transcript_b
        if osc_message.address not in ["/status", "/status.reply"]
    ] == [
        (
            "S",
            OscMessage(
                "/d_recv",
                synthdef.compile(),
                OscMessage("/s_new", "foo", 67109864, 0, 2),
            ),
        ),
        ("R", OscMessage("/n_go", 67109864, 2, -1, -1, 0)),
        ("R", OscMessage("/done", "/d_recv")),
    ]
    # TODO: Server A doesn't actually know what this SynthDef should be.
    assert str(server_a.root_node) == normalize(
        """
        NODE TREE 0 group
            1 group
            2 group
                67109864 default
                    out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5
    """
    )
    assert str(server_b.root_node) == normalize(
        """
        NODE TREE 0 group
            1 group
            2 group
                67109864 foo
                    frequency: 440.0
    """
    )


def test_connect_and_reconnect():
    try:
        options = scsynth.Options(maximum_logins=4, port=57110)
        protocol = SyncProcessProtocol()
        protocol.boot(options)
        server = Server()
        server.connect(port=57110)
        assert server.is_running and not server.is_owner
        assert server.client_id == 0
        assert str(server.root_node) == normalize(
            """
            NODE TREE 0 group
                1 group
                2 group
                3 group
                4 group
        """
        )
        server.disconnect()
        server.connect(port=57110)
        assert server.is_running and not server.is_owner
        assert server.client_id == 1
        assert str(server.root_node) == normalize(
            """
            NODE TREE 0 group
                1 group
                2 group
                3 group
                4 group
        """
        )
    finally:
        protocol.quit()


def test_reset():
    server = Server()
    with pytest.raises(exceptions.ServerOffline):
        server.reset()
    server.boot()
    server.add_synthdef(default)
    server.add_synth()
    server.add_group()
    server.add_buffer(channel_count=1, frame_count=1024)
    server.add_bus("audio")
    server.add_bus("control")
    assert default in server
    server.reset()
    assert server.is_running
    assert default not in server
    server.add_synthdef(default)
    assert default in server


@pytest.mark.parametrize("executable", [None, supernova_skip_win])
def test_reboot(executable):
    options = Options(executable=executable)
    server = Server()
    server.reboot(options=options)
    assert server.is_running
    assert server._options == options
    server.reboot()
    assert server.is_running


@pytest.mark.parametrize("executable", [None, supernova_skip_win])
def test_reboot_with_resources(executable):
    server = Server()
    server.boot(executable=executable)
    server.add_buffer(channel_count=1, frame_count=1024)
    server.add_bus("audio")
    server.add_bus("control")
    server.add_group()
    server.add_synth()
    server.reboot()
    assert server.is_running
    assert server._options.executable == executable


@pytest.mark.parametrize("executable", [None, supernova_skip_win])
def test_reset_and_reboot(executable):
    server = Server()
    server.boot(executable=executable)
    server.reset()
    server.reboot()
    assert server.is_running


@pytest.mark.parametrize("executable", [None, supernova_skip_win])
def test_reset_and_reboot_with_resources(executable):
    server = Server()
    server.boot(executable=executable)
    server.add_buffer(channel_count=1, frame_count=1024)
    server.add_bus("audio")
    server.add_bus("control")
    server.add_group()
    server.add_synth()
    server.reset()
    server.reboot()
    assert server.is_running


@pytest.mark.parametrize("executable", [None, supernova_skip_win])
@pytest.mark.parametrize("memory_size", [8192, 12345])
def test_boot_reboot_sticky_options(executable, memory_size):
    server = Server()
    port = find_free_port()
    options = Options(executable=executable, memory_size=memory_size, port=port)
    server.boot(options=options)
    assert server.is_running
    assert server._options.memory_size == options.memory_size
    assert server.port == options.port
    server.quit()
    assert not server.is_running
    server.boot(memory_size=8193)
    assert server.is_running
    assert server._options.memory_size == 8193
    assert server.port == options.port
    server.reboot()
    assert server.is_running
    assert server._options.memory_size == 8193
    assert server.port == options.port
    server.reboot(options=options)
    assert server.is_running
    assert server._options.memory_size == options.memory_size
    assert server.port == options.port


@pytest.mark.parametrize("executable", [None, supernova_skip_win])
@pytest.mark.parametrize("maximum_node_count", [1204, 8192])
def test_connect_and_reconnect_sticky_options(executable, maximum_node_count):
    try:
        port = find_free_port()
        options = scsynth.Options(
            executable=executable,
            maximum_logins=5,
            maximum_node_count=maximum_node_count,
            port=port,
        )
        protocol = SyncProcessProtocol()
        protocol.boot(options)
        server = Server()
        server.connect(options=options)
        assert server.is_running and not server.is_owner
        assert server._options.maximum_node_count == options.maximum_node_count
        assert server.port == port
        server.disconnect()
        server.connect(port=port)
        assert server._options.maximum_node_count == options.maximum_node_count
        assert server.port == port
        server.disconnect()
        server.connect(maximum_node_count=1101)
        assert server._options.maximum_node_count == 1101
        assert server.port == port
        server.disconnect()
        server.connect(options=options)
        assert server._options.maximum_node_count == options.maximum_node_count
        assert server.port == port
        server.disconnect()
        new_options = scsynth.Options(maximum_node_count=1027, port=port)
        server.connect(options=new_options)
        assert server._options.maximum_node_count == 1027
        assert server.port == port

    finally:
        protocol.quit()
