# -*- encoding: utf-8 -*-
import pytest
from supriya import servertools


@pytest.fixture(scope='function')
def server(request):
    def server_teardown():
        server.quit()
    server = servertools.Server().boot()
    request.addfinalizer(server_teardown)
    return server


def test_Bus_set_01(server):

    control_bus = servertools.Bus.control()
    control_bus.allocate()

    result = control_bus.get()
    assert result == 0.0
    assert control_bus.value == result

    control_bus.set(0.5)
    result = control_bus.get()
    assert result == 0.5
    assert control_bus.value == result

    control_bus.set(0.25)
    result = control_bus.get()
    assert result == 0.25
    assert control_bus.value == result