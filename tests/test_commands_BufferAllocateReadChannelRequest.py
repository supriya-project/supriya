import unittest
import supriya.nonrealtime
import supriya.commands
import supriya.soundfiles


class TestCase(unittest.TestCase):

    def test_Session(self):
        session = supriya.nonrealtime.Session()
        request = supriya.commands.BufferAllocateReadChannelRequest(
            buffer_id=1,
            channel_indices=[4, 5],
            file_path=session,
            frame_count=512,
            starting_frame=128,
            )
        assert request.file_path is session
        osc_message = request.to_osc_message(with_textual_osc_command=True)
        assert osc_message.address == '/b_allocReadChannel'
        assert osc_message.contents == (1, session, 128, 512, 4, 5)

    def test_Say(self):
        say = supriya.soundfiles.Say('Some text.')
        request = supriya.commands.BufferAllocateReadChannelRequest(
            buffer_id=1,
            channel_indices=[4, 5],
            file_path=say,
            frame_count=512,
            starting_frame=128,
            )
        assert request.file_path is say
        osc_message = request.to_osc_message(with_textual_osc_command=True)
        assert osc_message.address == '/b_allocReadChannel'
        assert osc_message.contents == (1, say, 128, 512, 4, 5)
