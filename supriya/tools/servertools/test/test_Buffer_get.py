# -*- encoding: utf-8 -*-
import collections
import pytest
from supriya import servertools


@pytest.fixture(scope='function')
def server(request):
    def server_teardown():
        server.quit()
    server = servertools.Server().boot()
    request.addfinalizer(server_teardown)
    return server


def test_Buffer_get_01(server):

    buffer_ = servertools.Buffer()
    buffer_.allocate(frame_count=8)
    server.sync()

    response = buffer_.get((0,))
    result = response.as_dict()
    assert result == collections.OrderedDict([
        (0, 0),
        ])

    response = buffer_.get((0, 1, 2, 3))
    result = response.as_dict()
    assert result == collections.OrderedDict([
        (0, 0),
        (1, 0),
        (2, 0),
        (3, 0),
        ])

    response = buffer_.get((7, 6, 2, 5, 1))
    result = response.as_dict()
    assert result == collections.OrderedDict([
        (7, 0),
        (6, 0),
        (2, 0),
        (5, 0),
        (1, 0),
        ])

    buffer_.free()
