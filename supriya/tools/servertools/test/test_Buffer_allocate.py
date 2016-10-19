# -*- encoding: utf-8 -*-
import os
import unittest
from supriya import servertools


@unittest.skipIf(os.environ.get('TRAVIS') == 'true', 'No Scsynth on Travis-CI')
class Test(unittest.TestCase):

    def setUp(self):
        self.server = servertools.Server().boot()

    def tearDown(self):
        self.server.quit()

    def test_01(self):

        buffer_ = servertools.Buffer()

        assert buffer_.buffer_id is None
        assert buffer_.buffer_group is None
        assert buffer_.channel_count == 0
        assert buffer_.frame_count == 0
        assert buffer_.sample_rate == 0
        assert not buffer_.is_allocated
        assert buffer_.server is None

        buffer_.allocate(frame_count=512)
        self.server.sync()

        assert buffer_.buffer_id == 0
        assert buffer_.buffer_group is None
        assert buffer_.channel_count == 1
        assert buffer_.frame_count == 512
        assert buffer_.sample_rate in (44100, 48000)
        assert buffer_.is_allocated
        assert buffer_.server is self.server

        buffer_.free()
        self.server.sync()

        assert buffer_.buffer_id is None
        assert buffer_.buffer_group is None
        assert buffer_.channel_count == 0
        assert buffer_.frame_count == 0
        assert buffer_.sample_rate == 0
        assert not buffer_.is_allocated
        assert buffer_.server is None

    def test_02(self):

        buffer_ = servertools.Buffer(buffer_group_or_index=23)

        assert buffer_.buffer_id == 23
        assert buffer_.buffer_group is None
        assert buffer_.channel_count == 0
        assert buffer_.frame_count == 0
        assert buffer_.sample_rate == 0
        assert not buffer_.is_allocated
        assert buffer_.server is None

        buffer_.allocate(frame_count=512)
        self.server.sync()

        assert buffer_.buffer_id == 23
        assert buffer_.buffer_group is None
        assert buffer_.channel_count == 1
        assert buffer_.frame_count == 512
        assert buffer_.sample_rate in (44100, 48000)
        assert buffer_.is_allocated
        assert buffer_.server is self.server

        buffer_.free()
        self.server.sync()

        assert buffer_.buffer_id is None
        assert buffer_.buffer_group is None
        assert buffer_.channel_count == 0
        assert buffer_.frame_count == 0
        assert buffer_.sample_rate == 0
        assert not buffer_.is_allocated
        assert buffer_.server is None

    def test_03(self):

        buffer_a = servertools.Buffer()
        buffer_b = servertools.Buffer()
        buffer_c = servertools.Buffer()
        buffer_d = servertools.Buffer()

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

        buffer_a.allocate(frame_count=128, channel_count=1, server=self.server)
        buffer_b.allocate(frame_count=256, channel_count=2, server=self.server)
        buffer_c.allocate(frame_count=512, channel_count=3, server=self.server)
        self.server.sync()

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
        buffer_d.allocate(frame_count=1024, channel_count=4, server=self.server)
        self.server.sync()

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
