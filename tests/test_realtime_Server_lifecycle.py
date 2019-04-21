import time

import pytest

import supriya


def test_boot_and_quit():
    server = supriya.Server()
    assert not server.is_running
    assert not server.is_owner
    server.boot()
    assert server.is_running
    assert server.is_owner
    server.quit()
    assert not server.is_running
    assert not server.is_owner


def test_boot_and_boot():
    server = supriya.Server()
    assert not server.is_running
    assert not server.is_owner
    server.boot()
    assert server.is_running
    assert server.is_owner
    server.boot()
    assert server.is_running
    assert server.is_owner


def test_boot_and_quit_and_quit():
    server = supriya.Server()
    assert not server.is_running
    assert not server.is_owner
    server.boot()
    assert server.is_running
    assert server.is_owner
    server.quit()
    assert not server.is_running
    assert not server.is_owner
    server.quit()
    assert not server.is_running
    assert not server.is_owner


def test_boot_and_connect():
    server = supriya.Server()
    assert not server.is_running
    assert not server.is_owner
    server.boot()
    assert server.is_running
    assert server.is_owner
    server.connect()
    assert server.is_running
    assert server.is_owner


def test_boot_a_and_connect_b():
    server_a, server_b = supriya.Server(), supriya.Server()
    assert not server_a.is_running and not server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner
    server_a.boot(maximum_logins=4)
    assert server_a.is_running and server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner
    server_b.connect()
    assert server_a.is_running and server_a.is_owner
    assert server_b.is_running and not server_b.is_owner
    assert server_a.query_remote_nodes() == server_b.query_remote_nodes()
    assert server_a.client_id == 0 and server_b.client_id == 1
    assert server_a.default_group.node_id == 1 and server_b.default_group.node_id == 2
    group = supriya.Group()
    group.allocate(target_node=server_a)
    assert server_a.root_node[0][0] is group
    assert server_b.root_node[0][0] is not group
    assert server_a.query_remote_nodes() == server_b.query_remote_nodes()


def test_boot_a_and_boot_b_cannot_boot():
    server_a, server_b = supriya.Server(), supriya.Server()
    assert not server_a.is_running and not server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner
    server_a.boot(maximum_logins=4)
    assert server_a.is_running and server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner
    with pytest.raises(supriya.exceptions.ServerCannotBoot):
        server_b.boot(maximum_logins=4)
    assert server_a.is_running and server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner


def test_boot_a_and_connect_b_too_many_clients():
    server_a, server_b = supriya.Server(), supriya.Server()
    assert not server_a.is_running and not server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner
    server_a.boot(maximum_logins=1)
    assert server_a.is_running and server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner
    with pytest.raises(supriya.exceptions.TooManyClients):
        server_b.connect()
    assert server_a.is_running and server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner


def test_boot_a_and_connect_b_and_quit_a():
    server_a, server_b = supriya.Server(), supriya.Server()
    assert not server_a.is_running and not server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner
    server_a.boot(maximum_logins=2)
    server_b.connect()
    assert server_a.is_running and server_a.is_owner
    assert server_b.is_running and not server_b.is_owner
    server_a.quit()
    assert not server_a.is_running and not server_a.is_owner
    time.sleep(2)  # wait for status watcher
    assert not server_b.is_running and not server_b.is_owner


def test_boot_a_and_connect_b_and_disconnect_b():
    server_a, server_b = supriya.Server(), supriya.Server()
    assert not server_a.is_running and not server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner
    server_a.boot(maximum_logins=2)
    server_b.connect()
    assert server_a.is_running and server_a.is_owner
    assert server_b.is_running and not server_b.is_owner
    server_b.disconnect()
    assert server_a.is_running and server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner


def test_boot_a_and_connect_b_and_disconnect_a():
    server_a, server_b = supriya.Server(), supriya.Server()
    assert not server_a.is_running and not server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner
    server_a.boot(maximum_logins=2)
    server_b.connect()
    assert server_a.is_running and server_a.is_owner
    assert server_b.is_running and not server_b.is_owner
    with pytest.raises(supriya.exceptions.OwnedServerShutdown):
        server_a.disconnect()
    assert server_a.is_running and server_a.is_owner
    assert server_b.is_running and not server_b.is_owner


def test_boot_a_and_connect_b_and_force_disconnect_a():
    server_a, server_b = supriya.Server(), supriya.Server()
    assert not server_a.is_running and not server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner
    server_a.boot(maximum_logins=2)
    server_b.connect()
    assert server_a.is_running and server_a.is_owner
    assert server_b.is_running and not server_b.is_owner
    server_a.disconnect(force=True)
    assert not server_a.is_running and not server_a.is_owner
    assert server_b.is_running and not server_b.is_owner


def test_boot_a_and_connect_b_and_quit_b():
    server_a, server_b = supriya.Server(), supriya.Server()
    assert not server_a.is_running and not server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner
    server_a.boot(maximum_logins=2)
    server_b.connect()
    assert server_a.is_running and server_a.is_owner
    assert server_b.is_running and not server_b.is_owner
    with pytest.raises(supriya.exceptions.UnownedServerShutdown):
        server_b.quit()
    assert server_a.is_running and server_a.is_owner
    assert server_b.is_running and not server_b.is_owner


def test_boot_a_and_connect_b_and_force_quit_b():
    server_a, server_b = supriya.Server(), supriya.Server()
    assert not server_a.is_running and not server_a.is_owner
    assert not server_b.is_running and not server_b.is_owner
    server_a.boot(maximum_logins=2)
    server_b.connect()
    assert server_a.is_running and server_a.is_owner
    assert server_b.is_running and not server_b.is_owner
    server_b.quit(force=True)
    assert not server_b.is_running and not server_b.is_owner
    time.sleep(2)  # wait for status watcher
    assert not server_a.is_running and not server_a.is_owner
