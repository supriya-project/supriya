# -*- encoding: utf-8 -*-
import pytest
from supriya.tools import servertools
from supriya.tools import synthdeftools


@pytest.fixture(scope='function')
def server(request):
    def server_teardown():
        server.quit()
    server = servertools.Server().boot()
    request.addfinalizer(server_teardown)
    return server


def test_BusGroup_allocate_01(server):

    bus_group_one = servertools.BusGroup(
        bus_count=4,
        calculation_rate=synthdeftools.CalculationRate.CONTROL,
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

    bus_group_one.allocate()
    server.sync()

    assert bus_group_one.is_allocated
    assert bus_group_one.bus_id is 0
    assert bus_group_one.server is server
    assert len(bus_group_one) == 4
    for i, bus in enumerate(bus_group_one):
        assert bus.is_allocated
        assert bus.bus_group is bus_group_one
        assert bus.bus_id == bus_group_one.bus_id + i
        assert bus.calculation_rate == bus_group_one.calculation_rate

    bus_group_two = servertools.BusGroup(
        bus_count=4,
        calculation_rate=synthdeftools.CalculationRate.CONTROL,
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

    bus_group_two.allocate()
    server.sync()

    assert bus_group_two.is_allocated
    assert bus_group_two.bus_id is 4
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

