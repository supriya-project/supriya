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



def test_Bus_01(server):

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


def test_Bus_02(server):

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
