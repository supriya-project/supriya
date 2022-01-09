from supriya.realtime.shm import ServerSHM


def test(server):
    shm = ServerSHM(server.port, server.options.control_bus_channel_count)
    bus = server.add_bus()
    assert bus.get() == shm[int(bus)] == 0.0
    for value in [1.0, 23.0, 666.0, 0.5]:
        bus.set(value)
        assert bus.get() == shm[int(bus)] == value
    assert shm[:2] == [0.5, 0]
