import time

from supriya.xdaw import Application, AudioEffect


def test_gain(dc_index_synthdef_factory):
    application = Application(channel_count=1)
    context = application.add_context()
    track = context.add_track()
    track.add_device(AudioEffect, synthdef=dc_index_synthdef_factory)
    application.boot()
    time.sleep(0.1)
    assert track.rms_levels["prefader"] == (1.0,)
    assert track.rms_levels["postfader"] == (1.0,)
    assert context.master_track.rms_levels["input"] == (1.0,)
    with context.provider.server.osc_io.capture() as transcript:
        track.parameters["gain"].set_(-6.0)
    assert len(transcript.sent_messages) == 1
    _, message = transcript.sent_messages[0]
    assert message.to_list() == [None, [[25, 0, -6.0]]]
    time.sleep(0.2)
    assert track.rms_levels["prefader"] == (1.0,)
    assert track.rms_levels["postfader"] == (0.5011872053146362,)
    assert context.master_track.rms_levels["input"] == (0.5011872053146362,)
