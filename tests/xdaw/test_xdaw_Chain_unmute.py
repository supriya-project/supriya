import time

from supriya.xdaw import Application, AudioEffect, RackDevice


def test_repeat(dc_index_synthdef_factory):
    """
    Unmuting more than once is a no-op
    """
    application = Application(channel_count=1)
    context = application.add_context()
    track = context.add_track()
    rack = track.add_device(RackDevice)
    chain = rack.add_chain()
    chain.add_device(AudioEffect, synthdef=dc_index_synthdef_factory)
    application.boot()
    chain.mute()
    time.sleep(0.2)
    assert [int(_) for _ in context.master_track.rms_levels["input"]] == [0]
    chain.unmute()
    time.sleep(0.2)
    assert [int(_) for _ in context.master_track.rms_levels["input"]] == [1]
    with context.provider.server.osc_io.capture() as transcript:
        chain.unmute()
    assert not len(transcript.sent_messages)
