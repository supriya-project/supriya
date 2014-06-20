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


def test_Buffer_01(server):

    buffer_ = servertools.Buffer()

    assert buffer_.buffer_id is None
    assert buffer_.buffer_group is None
    assert buffer_.channel_count == 0
    assert buffer_.frame_count == 0
    assert buffer_.sample_rate == 0
    assert not buffer_.is_allocated
    assert buffer_.server is None

    buffer_.allocate(frame_count=512)
    server.sync()

    assert buffer_.buffer_id == 0
    assert buffer_.buffer_group is None
    assert buffer_.channel_count == 1
    assert buffer_.frame_count == 512
    assert buffer_.sample_rate == server.server_options.sample_rate
    assert buffer_.is_allocated
    assert buffer_.server is server

    buffer_.free()
    server.sync()

    assert buffer_.buffer_id is None
    assert buffer_.buffer_group is None
    assert buffer_.channel_count == 0
    assert buffer_.frame_count == 0
    assert buffer_.sample_rate == 0
    assert not buffer_.is_allocated
    assert buffer_.server is None

