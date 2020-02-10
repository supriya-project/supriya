import supriya.commands
import supriya.nonrealtime
import supriya.soundfiles


def test_Session():
    session = supriya.nonrealtime.Session()
    request = supriya.commands.BufferAllocateReadRequest(
        buffer_id=1, file_path=session, frame_count=512, starting_frame=128
    )
    assert request.file_path is session
    osc_message = request.to_osc()
    assert osc_message.address == "/b_allocRead"
    assert osc_message.contents == (1, session, 128, 512)


def test_Say():
    say = supriya.soundfiles.Say("Some text.")
    request = supriya.commands.BufferAllocateReadRequest(
        buffer_id=1, file_path=say, frame_count=512, starting_frame=128
    )
    assert request.file_path is say
    osc_message = request.to_osc()
    assert osc_message.address == "/b_allocRead"
    assert osc_message.contents == (1, say, 128, 512)
