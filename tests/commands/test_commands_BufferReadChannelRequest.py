import supriya.commands
import supriya.nonrealtime
import supriya.soundfiles


def test_Session():
    session = supriya.nonrealtime.Session()
    request = supriya.commands.BufferReadChannelRequest(
        buffer_id=1,
        channel_indices=[4, 5],
        file_path=session,
        frame_count=512,
        leave_open=True,
        starting_frame_in_buffer=0,
        starting_frame_in_file=0,
    )
    assert request.file_path is session
    osc_message = request.to_osc()
    assert osc_message.address == "/b_readChannel"
    assert osc_message.contents == (1, session, 0, 512, 0, 1, 4, 5)


def test_Say():
    say = supriya.soundfiles.Say("Some text.")
    request = supriya.commands.BufferReadChannelRequest(
        buffer_id=1,
        channel_indices=[4, 5],
        file_path=say,
        frame_count=512,
        leave_open=True,
        starting_frame_in_buffer=0,
        starting_frame_in_file=0,
    )
    assert request.file_path is say
    osc_message = request.to_osc()
    assert osc_message.address == "/b_readChannel"
    assert osc_message.contents == (1, say, 0, 512, 0, 1, 4, 5)
