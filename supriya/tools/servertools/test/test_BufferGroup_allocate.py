import os
import unittest
from supriya.tools import servertools


@unittest.skipIf(os.environ.get('TRAVIS') == 'true', 'No Scsynth on Travis-CI')
class Test(unittest.TestCase):

    def setUp(self):
        self.server = servertools.Server().boot()

    def tearDown(self):
        self.server.quit()

    def test_01(self):

        buffer_group_one = servertools.BufferGroup(buffer_count=4)

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

        buffer_group_one.allocate(frame_count=512)
        self.server.sync()

        assert buffer_group_one.is_allocated
        assert buffer_group_one.buffer_id is 0
        assert buffer_group_one.server is self.server
        assert len(buffer_group_one) == 4
        for i, buffer_ in enumerate(buffer_group_one):
            assert buffer_.is_allocated
            assert buffer_.buffer_group is buffer_group_one
            assert buffer_.buffer_id == buffer_group_one.buffer_id + i
            assert buffer_.frame_count == 512
            assert buffer_.channel_count == 1

        buffer_group_two = servertools.BufferGroup(buffer_count=4)
        self.server.sync()

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

        buffer_group_two.allocate(frame_count=1024, channel_count=2)
        self.server.sync()

        assert buffer_group_two.is_allocated
        assert buffer_group_two.buffer_id is 4
        assert buffer_group_two.server is self.server
        assert len(buffer_group_two) == 4
        for i, buffer_ in enumerate(buffer_group_two):
            assert buffer_.is_allocated
            assert buffer_.buffer_group is buffer_group_two
            assert buffer_.buffer_id is buffer_group_two.buffer_id + i
            assert buffer_.frame_count == 1024
            assert buffer_.channel_count == 2

        buffer_group_one.free()
        self.server.sync()

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
        self.server.sync()

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
