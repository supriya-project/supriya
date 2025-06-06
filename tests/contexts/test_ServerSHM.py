import random

from supriya import Server
from supriya.contexts.shm import ServerSHM


def test_shared_memory(server: Server) -> None:
    assert isinstance(server.shared_memory, ServerSHM)

    values = [i / 2 for i in range(20)]
    bus = server.add_bus(calculation_rate="CONTROL")
    bus_group = server.add_bus_group(
        calculation_rate="CONTROL", count=random.randint(4, 16)
    )

    assert server.shared_memory[bus] == 0.0
    assert server.shared_memory[bus_group] == [0.0] * len(bus_group)
    assert server.shared_memory[int(bus)] == 0.0
    assert server.shared_memory[int(bus_group) : int(bus_group) + len(bus_group)] == [
        0.0
    ] * len(bus_group)

    random.shuffle(values)
    server.shared_memory[int(bus)] = values[-1]
    server.shared_memory[int(bus_group) : int(bus_group) + len(bus_group)] = values[
        : len(bus_group)
    ]
    assert server.shared_memory[int(bus)] == values[-1]
    assert (
        server.shared_memory[int(bus_group) : int(bus_group) + len(bus_group)]
        == values[: len(bus_group)]
    )

    random.shuffle(values)
    server.shared_memory[bus] = values[-1]
    server.shared_memory[bus_group] = values[: len(bus_group)]
    assert (
        server.shared_memory[int(bus_group) : int(bus_group) + len(bus_group)]
        == values[: len(bus_group)]
    )
    assert server.shared_memory[int(bus)] == values[-1]
    assert server.shared_memory[bus] == values[-1]
    assert server.shared_memory[bus_group] == values[: len(bus_group)]
