import unittest
import supriya.nonrealtime
import supriya.commands
import supriya.soundfiles


class TestCase(unittest.TestCase):

    def test_Session(self):
        session = supriya.nonrealtime.Session()
        request = supriya.commands.BufferReadRequest(
            buffer_id=1,
            file_path=session,
            frame_count=512,
            leave_open=True,
            starting_frame_in_buffer=0,
            starting_frame_in_file=0,
            )
        assert request.file_path is session
        osc_message = request.to_osc_message(with_textual_osc_command=True)
        assert osc_message.address == '/b_read'
        assert osc_message.contents == (1, session, 0, 512, 0, 1)

    def test_Say(self):
        say = supriya.soundfiles.Say('Some text.')
        request = supriya.commands.BufferReadRequest(
            buffer_id=1,
            file_path=say,
            frame_count=512,
            leave_open=True,
            starting_frame_in_buffer=0,
            starting_frame_in_file=0,
            )
        assert request.file_path is say
        osc_message = request.to_osc_message(with_textual_osc_command=True)
        assert osc_message.address == '/b_read'
        assert osc_message.contents == (1, say, 0, 512, 0, 1)
