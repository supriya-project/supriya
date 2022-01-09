import collections

import pytest

import supriya.realtime


@pytest.fixture(autouse=True)
def shutdown_sync_servers(shutdown_scsynth):
    pass


@pytest.fixture
def server(persistent_server):
    persistent_server.reset()
    persistent_server.add_synthdef(supriya.assets.synthdefs.default)
    yield persistent_server


def test_allocate_01(server):

    buffer_ = supriya.realtime.Buffer()

    assert buffer_.buffer_id is None
    assert buffer_.buffer_group is None
    assert buffer_.channel_count == 0
    assert buffer_.frame_count == 0
    assert buffer_.sample_rate == 0
    assert not buffer_.is_allocated
    assert buffer_.server is None

    buffer_.allocate(server, frame_count=512)
    server.sync()

    assert buffer_.buffer_id == 0
    assert buffer_.buffer_group is None
    assert buffer_.channel_count == 1
    assert buffer_.frame_count == 512
    assert buffer_.sample_rate in (44100, 48000)
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


def test_allocate_02(server):

    buffer_ = supriya.realtime.Buffer(buffer_group_or_index=23)

    assert buffer_.buffer_id == 23
    assert buffer_.buffer_group is None
    assert buffer_.channel_count == 0
    assert buffer_.frame_count == 0
    assert buffer_.sample_rate == 0
    assert not buffer_.is_allocated
    assert buffer_.server is None

    buffer_.allocate(server, frame_count=512)
    server.sync()

    assert buffer_.buffer_id == 23
    assert buffer_.buffer_group is None
    assert buffer_.channel_count == 1
    assert buffer_.frame_count == 512
    assert buffer_.sample_rate in (44100, 48000)
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


def test_allocate_03(server):

    buffer_a = supriya.realtime.Buffer()
    buffer_b = supriya.realtime.Buffer()
    buffer_c = supriya.realtime.Buffer()
    buffer_d = supriya.realtime.Buffer()

    assert buffer_a.buffer_id is None
    assert buffer_b.buffer_id is None
    assert buffer_c.buffer_id is None
    assert buffer_d.buffer_id is None
    assert buffer_a.frame_count == 0
    assert buffer_b.frame_count == 0
    assert buffer_c.frame_count == 0
    assert buffer_d.frame_count == 0
    assert buffer_a.channel_count == 0
    assert buffer_b.channel_count == 0
    assert buffer_c.channel_count == 0
    assert buffer_d.channel_count == 0

    buffer_a.allocate(server, frame_count=128, channel_count=1)
    buffer_b.allocate(server, frame_count=256, channel_count=2)
    buffer_c.allocate(server, frame_count=512, channel_count=3)
    server.sync()

    assert buffer_a.buffer_id == 0
    assert buffer_b.buffer_id == 1
    assert buffer_c.buffer_id == 2
    assert buffer_d.buffer_id is None
    assert buffer_a.frame_count == 128
    assert buffer_b.frame_count == 256
    assert buffer_c.frame_count == 512
    assert buffer_d.frame_count == 0
    assert buffer_a.channel_count == 1
    assert buffer_b.channel_count == 2
    assert buffer_c.channel_count == 3
    assert buffer_d.channel_count == 0

    buffer_c.free()
    buffer_a.free()
    buffer_d.allocate(server, frame_count=1024, channel_count=4)
    server.sync()

    assert buffer_a.buffer_id is None
    assert buffer_b.buffer_id == 1
    assert buffer_c.buffer_id is None
    assert buffer_d.buffer_id == 0
    assert buffer_a.frame_count == 0
    assert buffer_b.frame_count == 256
    assert buffer_c.frame_count == 0
    assert buffer_d.frame_count == 1024
    assert buffer_a.channel_count == 0
    assert buffer_b.channel_count == 2
    assert buffer_c.channel_count == 0
    assert buffer_d.channel_count == 4


def test_get_01(server):
    buffer_ = supriya.realtime.Buffer()
    buffer_.allocate(server, frame_count=8, sync=True)
    response = buffer_.get(0)
    result = response.as_dict()
    assert result == collections.OrderedDict([(0, 0)])
    response = buffer_.get(0, 1, 2, 3)
    result = response.as_dict()
    assert result == collections.OrderedDict([(0, 0), (1, 0), (2, 0), (3, 0)])
    response = buffer_.get(7, 6, 2, 5, 1)
    result = response.as_dict()
    assert result == collections.OrderedDict([(7, 0), (6, 0), (2, 0), (5, 0), (1, 0)])
    buffer_.free()


def test_get_02(server):
    buffer_ = supriya.realtime.Buffer()
    buffer_.allocate(server, frame_count=8, sync=True)
    buffer_.set_contiguous((0, (1, 2, 3, 4, 5, 6, 7, 8)))
    response = buffer_.get(0, 1, 2, 3, 4, 5, 6, 7)
    result = response.as_dict()
    assert result == collections.OrderedDict(
        [(0, 1.0), (1, 2.0), (2, 3.0), (3, 4.0), (4, 5.0), (5, 6.0), (6, 7.0), (7, 8.0)]
    )
    buffer_.set((2, -1.5), (4, -2.125))
    response = buffer_.get(7, 6, 5, 4, 3, 2, 1, 0)
    result = response.as_dict()
    assert result == collections.OrderedDict(
        [
            (7, 8.0),
            (6, 7.0),
            (5, 6.0),
            (4, -2.125),
            (3, 4.0),
            (2, -1.5),
            (1, 2.0),
            (0, 1.0),
        ]
    )
    buffer_.free()
