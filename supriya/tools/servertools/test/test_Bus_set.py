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

    response = control_bus.get()

    control_bus.set(0.5)

    response = control_bus.get()

    control_bus.set(0.25)

    response = control_bus.get()