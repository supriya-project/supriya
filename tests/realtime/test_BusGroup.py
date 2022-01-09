import supriya.realtime
import supriya.synthdefs


def test_allocate(server):

    bus_group_one = supriya.realtime.BusGroup(
        bus_count=4, calculation_rate=supriya.CalculationRate.CONTROL
    )

    assert not bus_group_one.is_allocated
    assert bus_group_one.bus_id is None
    assert bus_group_one.server is None
    assert len(bus_group_one) == 4
    for bus in bus_group_one:
        assert not bus.is_allocated
        assert bus.bus_group is bus_group_one
        assert bus.bus_id is None
        assert bus.calculation_rate == bus_group_one.calculation_rate

    bus_group_one.allocate(server)
    server.sync()

    assert bus_group_one.is_allocated
    assert bus_group_one.bus_id == 0
    assert bus_group_one.server is server
    assert len(bus_group_one) == 4
    for i, bus in enumerate(bus_group_one):
        assert bus.is_allocated
        assert bus.bus_group is bus_group_one
        assert bus.bus_id == bus_group_one.bus_id + i
        assert bus.calculation_rate == bus_group_one.calculation_rate

    bus_group_two = supriya.realtime.BusGroup(
        bus_count=4, calculation_rate=supriya.CalculationRate.CONTROL
    )
    server.sync()

    assert not bus_group_two.is_allocated
    assert bus_group_two.bus_id is None
    assert bus_group_two.server is None
    assert len(bus_group_two) == 4
    for bus in bus_group_two:
        assert not bus.is_allocated
        assert bus.bus_group is bus_group_two
        assert bus.bus_id is None
        assert bus.calculation_rate == bus_group_two.calculation_rate

    bus_group_two.allocate(server)
    server.sync()

    assert bus_group_two.is_allocated
    assert bus_group_two.bus_id == 4
    assert bus_group_two.server is server
    assert len(bus_group_two) == 4
    for i, bus in enumerate(bus_group_two):
        assert bus.is_allocated
        assert bus.bus_group is bus_group_two
        assert bus.bus_id is bus_group_two.bus_id + i
        assert bus.calculation_rate == bus_group_two.calculation_rate

    bus_group_one.free()
    server.sync()

    assert not bus_group_one.is_allocated
    assert bus_group_one.bus_id is None
    assert bus_group_one.server is None
    assert len(bus_group_one) == 4
    for bus in bus_group_one:
        assert not bus.is_allocated
        assert bus.bus_group is bus_group_one
        assert bus.bus_id is None
        assert bus.calculation_rate == bus_group_one.calculation_rate

    bus_group_two.free()
    server.sync()

    assert not bus_group_two.is_allocated
    assert bus_group_two.bus_id is None
    assert bus_group_two.server is None
    assert len(bus_group_two) == 4
    for bus in bus_group_two:
        assert not bus.is_allocated
        assert bus.bus_group is bus_group_two
        assert bus.bus_id is None
        assert bus.calculation_rate == bus_group_two.calculation_rate
