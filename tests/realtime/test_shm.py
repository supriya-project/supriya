import pytest

pytest.importorskip("supriya.realtime.shm")


def test_shared_memory(server):
    from supriya.realtime import shm

    shared_memory = shm.ServerSHM(server.port, server.options.control_bus_channel_count)
    bus = server.add_bus()
    assert bus.get() == shared_memory[int(bus)] == 0.0
    for value in [1.0, 23.0, 666.0, 0.5]:
        bus.set(value)
        assert bus.get() == shared_memory[int(bus)] == value
    assert shared_memory[:2] == [0.5, 0]
