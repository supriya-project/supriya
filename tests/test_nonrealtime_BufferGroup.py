import supriya.nonrealtime


def test_01():
    session = supriya.nonrealtime.Session()
    with session.at(0):
        buffer_group_one = session.add_buffer_group()
    with session.at(5):
        buffer_group_two = session.add_buffer_group(buffer_count=2, duration=10)

    # buffer group one
    assert buffer_group_one.duration == float("inf")
    assert buffer_group_one.session is session
    assert buffer_group_one.start_offset == 0
    assert buffer_group_one.stop_offset == float("inf")

    # buffer group one bufferes
    assert len(buffer_group_one) == 1
    buffer_ = buffer_group_one[0]
    assert buffer_ in buffer_group_one
    assert buffer_group_one.index(buffer_) == 0
    assert buffer_.duration == buffer_group_one.duration
    assert buffer_.session is buffer_group_one.session
    assert buffer_.start_offset == buffer_group_one.start_offset
    assert buffer_.stop_offset == buffer_group_one.stop_offset

    # buffer group two
    assert buffer_group_two.duration == 10
    assert buffer_group_two.session is session
    assert buffer_group_two.start_offset == 5
    assert buffer_group_two.stop_offset == 15

    # buffer group two bufferes
    assert len(buffer_group_two) == 2
    buffer_ = buffer_group_two[0]
    assert buffer_ in buffer_group_two
    assert buffer_group_two.index(buffer_) == 0
    assert buffer_.duration == buffer_group_two.duration
    assert buffer_.session is buffer_group_two.session
    assert buffer_.start_offset == buffer_group_two.start_offset
    assert buffer_.stop_offset == buffer_group_two.stop_offset
    buffer_ = buffer_group_two[1]
    assert buffer_ in buffer_group_two
    assert buffer_group_two.index(buffer_) == 1
    assert buffer_.duration == buffer_group_two.duration
    assert buffer_.session is buffer_group_two.session
    assert buffer_.start_offset == buffer_group_two.start_offset
    assert buffer_.stop_offset == buffer_group_two.stop_offset
