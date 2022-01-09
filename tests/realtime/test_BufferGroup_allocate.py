import supriya.realtime


def test_allocate(server):

    buffer_group_one = supriya.realtime.BufferGroup(buffer_count=4)

    assert not buffer_group_one.is_allocated
    assert buffer_group_one.buffer_id is None
    assert buffer_group_one.server is None
    assert len(buffer_group_one) == 4
    for buffer_ in buffer_group_one:
        assert not buffer_.is_allocated
        assert buffer_.buffer_group is buffer_group_one
        assert buffer_.buffer_id is None
        assert buffer_.frame_count == 0
        assert buffer_.channel_count == 0

    buffer_group_one.allocate(server, frame_count=512)
    server.sync()

    assert buffer_group_one.is_allocated
    assert buffer_group_one.buffer_id == 0
    assert buffer_group_one.server is server
    assert len(buffer_group_one) == 4
    for i, buffer_ in enumerate(buffer_group_one):
        assert buffer_.is_allocated
        assert buffer_.buffer_group is buffer_group_one
        assert buffer_.buffer_id == buffer_group_one.buffer_id + i
        assert buffer_.frame_count == 512
        assert buffer_.channel_count == 1

    buffer_group_two = supriya.realtime.BufferGroup(buffer_count=4)
    server.sync()

    assert not buffer_group_two.is_allocated
    assert buffer_group_two.buffer_id is None
    assert buffer_group_two.server is None
    assert len(buffer_group_two) == 4
    for buffer_ in buffer_group_two:
        assert not buffer_.is_allocated
        assert buffer_.buffer_group is buffer_group_two
        assert buffer_.buffer_id is None
        assert buffer_.frame_count == 0
        assert buffer_.channel_count == 0

    buffer_group_two.allocate(server, frame_count=1024, channel_count=2)
    server.sync()

    assert buffer_group_two.is_allocated
    assert buffer_group_two.buffer_id == 4
    assert buffer_group_two.server is server
    assert len(buffer_group_two) == 4
    for i, buffer_ in enumerate(buffer_group_two):
        assert buffer_.is_allocated
        assert buffer_.buffer_group is buffer_group_two
        assert buffer_.buffer_id is buffer_group_two.buffer_id + i
        assert buffer_.frame_count == 1024
        assert buffer_.channel_count == 2

    buffer_group_one.free()
    server.sync()

    assert not buffer_group_one.is_allocated
    assert buffer_group_one.buffer_id is None
    assert buffer_group_one.server is None
    assert len(buffer_group_one) == 4
    for buffer_ in buffer_group_one:
        assert not buffer_.is_allocated
        assert buffer_.buffer_group is buffer_group_one
        assert buffer_.buffer_id is None
        assert buffer_.frame_count == 0
        assert buffer_.channel_count == 0

    buffer_group_two.free()
    server.sync()

    assert not buffer_group_two.is_allocated
    assert buffer_group_two.buffer_id is None
    assert buffer_group_two.server is None
    assert len(buffer_group_two) == 4
    for buffer_ in buffer_group_two:
        assert not buffer_.is_allocated
        assert buffer_.buffer_group is buffer_group_two
        assert buffer_.buffer_id is None
        assert buffer_.frame_count == 0
        assert buffer_.channel_count == 0
