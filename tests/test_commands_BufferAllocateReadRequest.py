import unittest
import supriya.nonrealtime
from supriya.tools import requesttools
from supriya.tools import soundfiletools


class TestCase(unittest.TestCase):

    def test_Session(self):
        session = supriya.nonrealtime.Session()
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

    def test_Say(self):
        say = soundfiletools.Say('Some text.')
        request = requesttools.BufferAllocateReadRequest(
            buffer_id=1,
            file_path=say,
            frame_count=512,
            starting_frame=128,
            )
        assert request.file_path is say
        osc_message = request.to_osc_message(with_textual_osc_command=True)
        assert osc_message.address == '/b_allocRead'
        assert osc_message.contents == (1, say, 128, 512)
