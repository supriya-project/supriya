import logging
import time

import pytest

from supriya.clock import Moment
from supriya.midi import NoteOffMessage, NoteOnMessage
from supriya.xdaw import Application, Instrument, Note


@pytest.fixture(autouse=True)
def logger(caplog):
    caplog.set_level(logging.DEBUG, logger="supriya.clock")
    caplog.set_level(logging.DEBUG, logger="supriya.xdaw")


@pytest.fixture
def application():
    application = Application.new(1, 1, 1).boot()
    track = application.contexts[0].tracks[0]
    track.add_device(Instrument)
    track.slots[0].add_clip()
    yield application
    application.quit()


def test_1(mocker, application):
    """
    Delete a note.
    """
    time_mock = mocker.patch.object(application.transport._clock, "get_current_time")
    time_mock.return_value = 0.0
    track = application.contexts[0].tracks[0]
    track.slots[0].clip.add_notes([Note(0, 1, pitch=60)])
    with track.devices[0].capture() as transcript:
        track.slots[0].fire()
        time.sleep(0.01)
    assert list(transcript) == [
        Instrument.CaptureEntry(
            moment=Moment(
                beats_per_minute=120.0,
                measure=1,
                measure_offset=0.0,
                offset=0.0,
                seconds=0.0,
                time_signature=(4, 4),
            ),
            label="I",
            message=NoteOnMessage(pitch=60, velocity=100.0),
        )
    ]
    with track.devices[0].capture() as transcript:
        time_mock.return_value = 0.5
        time.sleep(0.01)
    assert list(transcript) == []
    with track.devices[0].capture() as transcript:
        track.slots[0].clip.remove_notes(track.slots[0].clip.notes)
        time.sleep(0.1)
    assert list(transcript) == [
        Instrument.CaptureEntry(
            moment=Moment(
                beats_per_minute=120.0,
                measure=1,
                measure_offset=0.25,
                offset=0.25,
                seconds=0.5,
                time_signature=(4, 4),
            ),
            label="I",
            message=NoteOffMessage(pitch=60),
        )
    ]


def test_2(mocker, application):
    """
    Add a note.
    """
    time_mock = mocker.patch.object(application.transport._clock, "get_current_time")
    time_mock.return_value = 0.0
    track = application.contexts[0].tracks[0]
    with track.devices[0].capture() as transcript:
        track.slots[0].fire()
        time.sleep(0.01)
        assert list(transcript) == []
    with track.devices[0].capture() as transcript:
        track.slots[0].clip.add_notes([Note(0.75, 1, pitch=60)])
        time.sleep(0.01)
        assert list(transcript) == []
    with track.devices[0].capture() as transcript:
        time_mock.return_value = 2.0
        time.sleep(0.01)
        assert list(transcript) == [
            Instrument.CaptureEntry(
                moment=Moment(
                    beats_per_minute=120.0,
                    measure=1,
                    measure_offset=0.75,
                    offset=0.75,
                    seconds=1.5,
                    time_signature=(4, 4),
                ),
                label="I",
                message=NoteOnMessage(pitch=60, velocity=100.0),
            ),
            Instrument.CaptureEntry(
                moment=Moment(
                    beats_per_minute=120.0,
                    measure=2,
                    measure_offset=0.0,
                    offset=1.0,
                    seconds=2.0,
                    time_signature=(4, 4),
                ),
                label="I",
                message=NoteOffMessage(pitch=60, velocity=100.0),
            ),
        ]
