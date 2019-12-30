import time

import pytest

from supriya.osc import OscBundle, OscMessage
from supriya.synthdefs import SynthDefFactory
from supriya.xdaw import Application, AudioEffect


@pytest.fixture
def synthdef_factory():
    return (
        SynthDefFactory()
        .with_channel_count(2)
        .with_input()
        .with_signal_block(lambda builder, source, state: (source * -2) + 0.25)
        .with_gate(0.01, 0.01)
        .with_output(replacing=True)
    )


def test_1(synthdef_factory):
    """
    Remove one device
    """
    application = Application()
    context = application.add_context()
    track = context.add_track()
    device = track.add_device(AudioEffect, synthdef=synthdef_factory)
    track.remove_devices(device)
    assert list(track.devices) == []
    assert device.application is None
    assert device.graph_order == ()
    assert device.parent is None
    assert device.provider is None


def test_2(synthdef_factory):
    """
    Remove two devices
    """
    application = Application()
    context = application.add_context()
    track = context.add_track()
    device_one = track.add_device(AudioEffect, synthdef=synthdef_factory)
    device_two = track.add_device(AudioEffect, synthdef=synthdef_factory)
    track.remove_devices(device_one, device_two)
    assert list(track.devices) == []
    assert device_one.application is None
    assert device_one.graph_order == ()
    assert device_one.parent is None
    assert device_one.provider is None
    assert device_two.application is None
    assert device_two.graph_order == ()
    assert device_two.parent is None
    assert device_two.provider is None


def test_3(synthdef_factory):
    """
    Remove first device, leaving second untouched
    """
    application = Application()
    context = application.add_context()
    track = context.add_track()
    device_one = track.add_device(AudioEffect, synthdef=synthdef_factory)
    device_two = track.add_device(AudioEffect, synthdef=synthdef_factory)
    track.remove_devices(device_one)
    assert list(track.devices) == [device_two]
    assert device_one.application is None
    assert device_one.graph_order == ()
    assert device_one.parent is None
    assert device_one.provider is None
    assert device_two.application is context.application
    assert device_two.graph_order == (2, 0, 0, 0, 4, 0)
    assert device_two.parent is track.devices
    assert device_two.provider is None


def test_4(synthdef_factory):
    """
    Boot, remove first device, leaving second untouched
    """
    application = Application()
    context = application.add_context()
    track = context.add_track()
    device_one = track.add_device(AudioEffect, synthdef=synthdef_factory)
    device_two = track.add_device(AudioEffect, synthdef=synthdef_factory)
    application.boot()
    with context.provider.server.osc_io.capture() as transcript:
        track.remove_devices(device_one)
    time.sleep(0.1)
    assert list(track.devices) == [device_two]
    assert device_one.application is None
    assert device_one.graph_order == ()
    assert device_one.parent is None
    assert device_one.provider is None
    assert device_two.application is context.application
    assert device_two.graph_order == (2, 0, 0, 0, 4, 0)
    assert device_two.parent is track.devices
    assert device_two.provider is context.provider
    assert len(transcript.sent_messages) == 1
    _, message = transcript.sent_messages[0]
    assert message == OscBundle(contents=(OscMessage(15, 1012, "gate", 0),))
    assert track.peak_levels == dict(
        input=(0.0, 0.0), postfader=(0.25, 0.25), prefader=(0.25, 0.25)
    )
    assert context.master_track.peak_levels == dict(
        input=(0.25, 0.25), postfader=(0.25, 0.25), prefader=(0.25, 0.25)
    )
