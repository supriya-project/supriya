# -*- encoding: utf-8 -*-
import unittest
from supriya.tools import nonrealtimetools
from supriya.tools import requesttools


class TestCase(unittest.TestCase):

    def test_Session(self):
        session = nonrealtimetools.Session()
        request = requesttools.BufferAllocateReadRequest(
            buffer_id=1,
            file_path=session,
            frame_count=512,
            starting_frame=128,
            )
        assert request.file_path is session
        osc_message = request.to_osc_message(with_textual_osc_command=True)
        assert osc_message.address == '/b_allocRead'
        assert osc_message.contents == (1, session, 128, 512)
