import time

import pytest
from uqbar.strings import normalize

from supriya.assets.synthdefs import default
from supriya.midi import NoteOnMessage
from supriya.xdaw import Application, Instrument


@pytest.fixture
def application():
    application = Application()
    context = application.add_context(name="Context")
    context.add_track(name="Track")
    application.boot()
    yield application
    application.quit()


def test_1(application):
    application.boot()
    track = application.primary_context["Track"]
    instrument = track.add_device(Instrument, synthdef=default)
    time.sleep(0.01)
    with instrument.lock(instrument, 0.0), instrument.capture() as transcript:
        instrument.perform([NoteOnMessage(note_number=57, velocity=100)])
    time.sleep(0.01)
    assert list(transcript) == [
        instrument.CaptureEntry(
            moment=None, label="I", message=NoteOnMessage(note_number=57, velocity=100)
        )
    ]
    assert str(instrument.query()) == normalize(
        """
        NODE TREE 1044 group (Instrument)
            1047 mixer/patch[replace]/2x2 (DeviceIn)
                active: 1.0, gate: 1.0, in_: 18.0, lag: 0.01, out: 28.0
            1045 group (Parameters)
            1046 group (Body)
                1049 default
                    out: 28.0, amplitude: 0.620001, frequency: 220.0, gate: 1.0, pan: 0.5
            1048 mixer/patch[hard,mix]/2x2 (DeviceOut)
                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 28.0, lag: 0.01, mix: 1.0, out: 18.0
        """
    )
    with instrument.lock(instrument, 0.0), instrument.capture() as transcript:
        instrument.perform([NoteOnMessage(note_number=57, velocity=127)])
    time.sleep(0.01)
    assert list(transcript) == [
        instrument.CaptureEntry(
            moment=None, label="I", message=NoteOnMessage(note_number=57, velocity=127)
        )
    ]
    assert str(instrument.query()) == normalize(
        """
        NODE TREE 1044 group (Instrument)
            1047 mixer/patch[replace]/2x2 (DeviceIn)
                active: 1.0, gate: 1.0, in_: 18.0, lag: 0.01, out: 28.0
            1045 group (Parameters)
            1046 group (Body)
                1050 default
                    out: 28.0, amplitude: 1.0, frequency: 220.0, gate: 1.0, pan: 0.5
                1049 default
                    out: 28.0, amplitude: 0.620001, frequency: 220.0, gate: 0.0, pan: 0.5
            1048 mixer/patch[hard,mix]/2x2 (DeviceOut)
                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 28.0, lag: 0.01, mix: 1.0, out: 18.0
        """
    )
