import platform
import random

import pytest

from supriya import Server


@pytest.mark.skipif(
    platform.system() == "Windows", reason="SHM not built under Windows"
)
def test_shared_memory(server: Server) -> None:
    from supriya.contexts.shm import ServerSHM

    assert isinstance(server._shm, ServerSHM)

    values = [i / 2 for i in range(20)]
    bus = server.add_bus(calculation_rate="CONTROL")
    bus_group = server.add_bus_group(
        calculation_rate="CONTROL", count=random.randint(4, 16)
    )

    assert server._shm[bus] == 0.0
    assert server._shm[bus_group] == [0.0] * len(bus_group)
    assert server._shm[int(bus)] == 0.0
    assert server._shm[int(bus_group) : int(bus_group) + len(bus_group)] == [0.0] * len(
        bus_group
    )

    random.shuffle(values)
    server._shm[int(bus)] = values[-1]
    server._shm[int(bus_group) : int(bus_group) + len(bus_group)] = values[
        : len(bus_group)
    ]
    assert server._shm[int(bus)] == values[-1]
    assert (
        server._shm[int(bus_group) : int(bus_group) + len(bus_group)]
        == values[: len(bus_group)]
    )

    random.shuffle(values)
    server._shm[bus] = values[-1]
    server._shm[bus_group] = values[: len(bus_group)]
    assert (
        server._shm[int(bus_group) : int(bus_group) + len(bus_group)]
        == values[: len(bus_group)]
    )
    assert server._shm[int(bus)] == values[-1]
    assert server._shm[bus] == values[-1]
    assert server._shm[bus_group] == values[: len(bus_group)]
