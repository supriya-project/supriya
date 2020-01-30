import logging
import time

import pytest

from supriya.assets.synthdefs import default
from supriya.midi import NoteOffMessage, NoteOnMessage
from supriya.xdaw import Application, Arpeggiator, Instrument


@pytest.fixture(autouse=True)
def logger(caplog):
    caplog.set_level(logging.DEBUG, logger="supriya.xdaw")
    caplog.set_level(logging.DEBUG, logger="supriya.clock")


@pytest.fixture
def application():
    application = Application()
    context = application.add_context(name="Context")
    context.add_track(name="Track")
    application.boot()
    default.allocate(server=context.provider.server)
    yield application
    application.quit()


@pytest.mark.timeout(3)
def test_timeout(application):
    application["Track"].add_device(Arpeggiator)
    application["Track"].add_device(Instrument, synthdef=default)
    time.sleep(0.1)
    application.transport.perform([NoteOnMessage(pitch=60, velocity=100)])
    time.sleep(1.0)
    application.quit()


def test_query_1(application):
    """
    Arpeggiator does not modify the server node tree.
    """
    before = str(application["Track"].query())
    application["Track"].add_device(Arpeggiator)
    time.sleep(0.1)
    after = str(application["Track"].query())
    assert before == after


def test_osc_transcript(application):
    """
    Arpeggiator instantiation does not send any OSC messages.
    """
    with application["Context"].provider.server.osc_protocol.capture() as transcript:
        application["Track"].add_device(Arpeggiator)
    assert len(transcript.sent_messages) == 0


def test_midi_transcript_1(mocker, application):
    time_mock = mocker.patch.object(application.transport._clock, "get_current_time")
    time_mock.return_value = 0.0
    arpeggiator = application["Track"].add_device(Arpeggiator)
    assert not application.transport.is_running
    with arpeggiator.capture() as transcript:
        application.transport.perform([NoteOnMessage(pitch=60, velocity=100)])
        assert application.transport.is_running
        time.sleep(0.1)
        time_mock.return_value = 0.5
        time.sleep(0.1)
    assert [(_.label, _.moment.offset, _.message) for _ in transcript] == [
        ("I", 0.0, NoteOnMessage(pitch=60, velocity=100)),
        ("O", 0.0, NoteOnMessage(pitch=60, velocity=100)),
        ("O", 0.0625, NoteOffMessage(pitch=60)),
        ("O", 0.0625, NoteOnMessage(pitch=60, velocity=100)),
        ("O", 0.125, NoteOffMessage(pitch=60)),
        ("O", 0.125, NoteOnMessage(pitch=60, velocity=100)),
        ("O", 0.1875, NoteOffMessage(pitch=60)),
        ("O", 0.1875, NoteOnMessage(pitch=60, velocity=100)),
        ("O", 0.25, NoteOffMessage(pitch=60)),
        ("O", 0.25, NoteOnMessage(pitch=60, velocity=100)),
    ]


def test_midi_transcript_2(mocker, application):
    time_mock = mocker.patch.object(application.transport._clock, "get_current_time")
    time_mock.return_value = 0.0
    arpeggiator = application["Track"].add_device(Arpeggiator)
    assert not application.transport.is_running
    with arpeggiator.capture() as transcript:
        application.transport.perform([NoteOnMessage(pitch=60, velocity=100)])
        application.transport.perform([NoteOnMessage(pitch=63, velocity=100)])
        application.transport.perform([NoteOnMessage(pitch=67, velocity=100)])
        assert application.transport.is_running
        time.sleep(0.1)
        time_mock.return_value = 0.5
        time.sleep(0.1)
    assert [(_.label, _.moment.offset, _.message) for _ in transcript] == [
        ("I", 0.0, NoteOnMessage(pitch=60, velocity=100)),
        ("I", 0.0, NoteOnMessage(pitch=63, velocity=100)),
        ("I", 0.0, NoteOnMessage(pitch=67, velocity=100)),
        ("O", 0.0, NoteOnMessage(pitch=60, velocity=100)),
        ("O", 0.0625, NoteOffMessage(pitch=60)),
        ("O", 0.0625, NoteOnMessage(pitch=63, velocity=100)),
        ("O", 0.125, NoteOffMessage(pitch=63)),
        ("O", 0.125, NoteOnMessage(pitch=67, velocity=100)),
        ("O", 0.1875, NoteOffMessage(pitch=67)),
        ("O", 0.1875, NoteOnMessage(pitch=60, velocity=100)),
        ("O", 0.25, NoteOffMessage(pitch=60)),
        ("O", 0.25, NoteOnMessage(pitch=63, velocity=100)),
    ]
