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
        instrument.perform(None, [NoteOnMessage(note_number=60, velocity=100)])
    time.sleep(0.01)
    assert list(transcript) == [
        instrument.CaptureEntry(
            moment=None, label="I", message=NoteOnMessage(note_number=60, velocity=100)
        )
    ]
    assert str(instrument.query()) == normalize(
        """
        NODE TREE 1039 group (Instrument)
            1042 mixer/patch[replace]/2x2 (DeviceIn)
                active: 1.0, gate: 1.0, in_: 18.0, lag: 0.01, out: 28.0
            1040 group (Parameters)
            1041 group (Body)
                1044 default
                    out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5
            1043 mixer/patch[hard,mix]/2x2 (DeviceOut)
                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 28.0, lag: 0.01, mix: 1.0, out: 18.0
        """
    )
    with instrument.lock(instrument, 0.0), instrument.capture() as transcript:
        instrument.perform(None, [NoteOnMessage(note_number=60, velocity=0)])
    time.sleep(0.01)
    assert list(transcript) == [
        instrument.CaptureEntry(
            moment=None, label="I", message=NoteOnMessage(note_number=60, velocity=0)
        )
    ]
    assert str(instrument.query()) == normalize(
        """
        NODE TREE 1039 group (Instrument)
            1042 mixer/patch[replace]/2x2 (DeviceIn)
                active: 1.0, gate: 1.0, in_: 18.0, lag: 0.01, out: 28.0
            1040 group (Parameters)
            1041 group (Body)
                1045 default
                    out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5
                1044 default
                    out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 0.0, pan: 0.5
            1043 mixer/patch[hard,mix]/2x2 (DeviceOut)
                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 28.0, lag: 0.01, mix: 1.0, out: 18.0
        """
    )
