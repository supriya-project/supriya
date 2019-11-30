import time

import pytest

from supriya.osc import OscBundle, OscMessage
from supriya.synthdefs import SynthDefCompiler, SynthDefFactory
from supriya.xdaw import Application, AudioEffect, DeviceIn, DeviceOut


@pytest.fixture
def synthdef_factory():
    factory = (
        SynthDefFactory()
        .with_channel_count(2)
        .with_input()
        .with_signal_block(lambda builder, source, state: (source * -3) + 0.25)
        .with_gate(0.01, 0.01)
        .with_output(replacing=True)
    )
    return factory


def test_1(synthdef_factory):
    """
    Add one device
    """
    application = Application()
    context = application.add_context()
    track = context.add_track()
    device = track.add_device(AudioEffect, synthdef=synthdef_factory)
    assert isinstance(device, AudioEffect)
    assert device.synthdef == synthdef_factory
    assert list(track.devices) == [device]
    assert device.application is context.application
    assert device.graph_order == (1, 0, 0, 0, 3, 0)
    assert device.parent is track.devices
    assert device.provider is context.provider


def test_2(synthdef_factory):
    """
    Add two devices
    """
    application = Application()
    context = application.add_context()
    track = context.add_track()
    device_one = track.add_device(AudioEffect, synthdef=synthdef_factory)
    device_two = track.add_device(AudioEffect, synthdef=synthdef_factory)
    assert list(track.devices) == [device_one, device_two]
    assert device_one.application is context.application
    assert device_one.graph_order == (1, 0, 0, 0, 3, 0)
    assert device_one.parent is track.devices
    assert device_one.provider is context.provider
    assert device_two.application is context.application
    assert device_two.graph_order == (1, 0, 0, 0, 3, 1)
    assert device_two.parent is track.devices
    assert device_two.provider is context.provider


def test_3(synthdef_factory):
    """
    Boot, add one device
    """
    synthdef = synthdef_factory.build(channel_count=2)
    application = Application()
    context = application.add_context()
    track = context.add_track()
    application.boot()
    with context.provider.server.osc_io.capture() as transcript:
        device = track.add_device(AudioEffect, synthdef=synthdef_factory)
    assert list(track.devices) == [device]
    assert device.application is context.application
    assert device.graph_order == (1, 0, 0, 0, 3, 0)
    assert device.parent is track.devices
    assert device.provider is context.provider
    assert len(transcript.sent_messages) == 1
    _, message = transcript.sent_messages[0]
    compiled_synthdefs = bytearray(
        SynthDefCompiler.compile_synthdefs(
            [synthdef, DeviceOut.build_synthdef(2, 2), DeviceIn.build_synthdef(2, 2)]
        )
    )
    bundle_contents = [
        OscMessage(21, 1039, 1, 1011),
        OscMessage(21, 1040, 0, 1039),
        OscMessage(21, 1041, 1, 1039),
        OscMessage(9, synthdef.anonymous_name, 1042, 0, 1041, "out", 28.0),
        OscMessage(
            9, "mixer/patch[replace]/2x2", 1043, 0, 1039, "in_", 18.0, "out", 28.0
        ),
        OscMessage(
            9, "mixer/patch[hard,mix]/2x2", 1044, 1, 1039, "in_", 28.0, "out", 18.0
        ),
    ]
    assert message == OscBundle(
        contents=(
            OscMessage(5, compiled_synthdefs, OscBundle(contents=bundle_contents)),
        )
    )
    time.sleep(0.1)
    assert track.peak_levels == dict(
        input=(0.0, 0.0), postfader=(0.25, 0.25), prefader=(0.25, 0.25)
    )
    assert context.master_track.peak_levels == dict(
        input=(0.25, 0.25), postfader=(0.25, 0.25), prefader=(0.25, 0.25)
    )


def test_4(synthdef_factory):
    """
    Add one device, boot, add second device
    """
    synthdef = synthdef_factory.build(channel_count=2)
    application = Application()
    context = application.add_context()
    track = context.add_track()
    device_one = track.add_device(AudioEffect, synthdef=synthdef_factory)
    application.boot()
    with context.provider.server.osc_io.capture() as transcript:
        device_two = track.add_device(AudioEffect, synthdef=synthdef_factory)
    assert list(track.devices) == [device_one, device_two]
    assert device_one.application is context.application
    assert device_one.graph_order == (1, 0, 0, 0, 3, 0)
    assert device_one.parent is track.devices
    assert device_one.provider is context.provider
    assert device_two.application is context.application
    assert device_two.graph_order == (1, 0, 0, 0, 3, 1)
    assert device_two.parent is track.devices
    assert device_two.provider is context.provider
    assert len(transcript.sent_messages) == 1
    _, message = transcript.sent_messages[0]
    assert message == OscBundle(
        contents=(
            OscMessage(21, 1045, 1, 1011),
            OscMessage(21, 1046, 0, 1045),
            OscMessage(21, 1047, 1, 1045),
            OscMessage(9, synthdef.anonymous_name, 1048, 0, 1047, "out", 30.0),
            OscMessage(
                9, "mixer/patch[replace]/2x2", 1049, 0, 1045, "in_", 18.0, "out", 30.0
            ),
            OscMessage(
                9, "mixer/patch[hard,mix]/2x2", 1050, 1, 1045, "in_", 30.0, "out", 18.0
            ),
        )
    )
    time.sleep(0.1)
    assert track.peak_levels == dict(
        input=(0.0, 0.0), postfader=(0.5, 0.5), prefader=(0.5, 0.5)
    )
    assert context.master_track.peak_levels == dict(
        input=(0.5, 0.5), postfader=(0.5, 0.5), prefader=(0.5, 0.5)
    )
