# -*- encoding: utf-8 -*-
import pytest
from supriya import servertools
from supriya import synthdeftools


@pytest.fixture(scope='function')
def server(request):
    def server_teardown():
        server.quit()
    server = servertools.Server().boot()
    request.addfinalizer(server_teardown)
    return server


def test_Bus_allocate_01(server):

    control_bus = servertools.Bus.control()

    assert control_bus.bus_group is None
    assert control_bus.bus_id is None
    assert control_bus.calculation_rate == synthdeftools.CalculationRate.CONTROL
    assert control_bus.server is None
    assert not control_bus.is_allocated

    control_bus.allocate()

    assert control_bus.bus_group is None
    assert control_bus.bus_id == 0
    assert control_bus.calculation_rate == synthdeftools.CalculationRate.CONTROL
    assert control_bus.server is server
    assert control_bus.is_allocated
    assert control_bus.map_symbol == 'c0'

    control_bus.free()

    assert control_bus.bus_group is None
    assert control_bus.bus_id is None
    assert control_bus.calculation_rate == synthdeftools.CalculationRate.CONTROL
    assert control_bus.server is None
    assert not control_bus.is_allocated


def test_Bus_allocate_02(server):

    audio_bus = servertools.Bus.audio()

    assert audio_bus.bus_group is None
    assert audio_bus.bus_id is None
    assert audio_bus.calculation_rate == synthdeftools.CalculationRate.AUDIO
    assert audio_bus.server is None
    assert not audio_bus.is_allocated

    audio_bus.allocate()

    assert audio_bus.bus_group is None
    assert audio_bus.bus_id == 16
    assert audio_bus.calculation_rate == synthdeftools.CalculationRate.AUDIO
    assert audio_bus.server is server
    assert audio_bus.is_allocated
    assert audio_bus.map_symbol == 'a16'

    audio_bus.free()

    assert audio_bus.bus_group is None
    assert audio_bus.bus_id is None
    assert audio_bus.calculation_rate == synthdeftools.CalculationRate.AUDIO
    assert audio_bus.server is None
    assert not audio_bus.is_allocated


def test_Bus_allocate_03(server):

    bus = servertools.Bus(
        bus_group_or_index=23,
        calculation_rate=synthdeftools.CalculationRate.CONTROL,
        )

    assert bus.bus_id == 23
    assert bus.bus_group is None
    assert not bus.is_allocated
    assert bus.server is None

    bus.allocate()
    server.sync()

    assert bus.bus_id == 23
    assert bus.bus_group is None
    assert bus.is_allocated
    assert bus.server is server

    bus.free()
    server.sync()

    assert bus.bus_id is None
    assert bus.bus_group is None
    assert not bus.is_allocated
    assert bus.server is None


def test_Bus_allocate_04(server):

    bus_a = servertools.Bus.control()
    bus_b = servertools.Bus.control()
    bus_c = servertools.Bus.control()
    bus_d = servertools.Bus.control()

    assert bus_a.bus_id is None
    assert bus_b.bus_id is None
    assert bus_c.bus_id is None
    assert bus_d.bus_id is None
    assert bus_a.server is None
    assert bus_b.server is None
    assert bus_c.server is None
    assert bus_d.server is None

    bus_a.allocate()
    bus_b.allocate()
    bus_c.allocate()
    server.sync()

    assert bus_a.bus_id == 0
    assert bus_b.bus_id == 1
    assert bus_c.bus_id == 2
    assert bus_d.bus_id is None
    assert bus_a.server is server
    assert bus_b.server is server
    assert bus_c.server is server
    assert bus_d.server is None

    bus_c.free()
    bus_a.free()
    bus_d.allocate()
    server.sync()

    assert bus_a.bus_id is None
    assert bus_b.bus_id == 1
    assert bus_c.bus_id is None
    assert bus_d.bus_id == 0
    assert bus_a.server is None
    assert bus_b.server is server
    assert bus_c.server is None
    assert bus_d.server is server