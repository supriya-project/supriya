import time

import pytest
from uqbar.strings import normalize

from supriya.synthdefs import SynthDefCompiler, SynthDefFactory
from supriya.xdaw import (
    Application,
    AudioEffect,
    DeviceIn,
    DeviceOut,
    Instrument,
)


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


def test_AudioEffect_1(synthdef_factory):
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
    assert device.graph_order == (3, 0, 0, 0, 5, 0)
    assert device.parent is track.devices
    assert device.provider is context.provider


def test_AudioEffect_2(synthdef_factory):
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
    assert device_one.graph_order == (3, 0, 0, 0, 5, 0)
    assert device_one.parent is track.devices
    assert device_one.provider is context.provider
    assert device_two.application is context.application
    assert device_two.graph_order == (3, 0, 0, 0, 5, 1)
    assert device_two.parent is track.devices
    assert device_two.provider is context.provider


def test_AudioEffect_3(synthdef_factory):
    """
    Boot, add one device
    """
    synthdef = synthdef_factory.build(channel_count=2)
    application = Application()
    context = application.add_context()
    track = context.add_track()
    application.boot()
    with context.provider.server.osc_protocol.capture() as transcript:
        device = track.add_device(AudioEffect, synthdef=synthdef_factory)
    assert list(track.devices) == [device]
    assert device.application is context.application
    assert device.graph_order == (3, 0, 0, 0, 5, 0)
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
        [21, 1044, 1, 1013],
        [21, 1045, 0, 1044],
        [21, 1046, 1, 1044],
        [9, synthdef.anonymous_name, 1047, 0, 1046, "out", 28.0],
        [9, "mixer/patch[replace]/2x2", 1048, 0, 1044, "in_", 18.0, "out", 28.0],
        [9, "mixer/patch[hard,mix]/2x2", 1049, 1, 1044, "in_", 28.0, "out", 18.0],
    ]
    assert message.to_list() == [
        None,
        [[5, compiled_synthdefs, [None, bundle_contents]]],
    ]
    time.sleep(0.1)
    assert track.peak_levels == dict(
        input=(0.0, 0.0), postfader=(0.25, 0.25), prefader=(0.25, 0.25)
    )
    assert context.master_track.peak_levels == dict(
        input=(0.25, 0.25), postfader=(0.25, 0.25), prefader=(0.25, 0.25)
    )


def test_AudioEffect_4(synthdef_factory):
    """
    Add one device, boot, add second device
    """
    synthdef = synthdef_factory.build(channel_count=2)
    application = Application()
    context = application.add_context()
    track = context.add_track()
    device_one = track.add_device(AudioEffect, synthdef=synthdef_factory)
    application.boot()
    with context.provider.server.osc_protocol.capture() as transcript:
        device_two = track.add_device(AudioEffect, synthdef=synthdef_factory)
    assert list(track.devices) == [device_one, device_two]
    assert device_one.application is context.application
    assert device_one.graph_order == (3, 0, 0, 0, 5, 0)
    assert device_one.parent is track.devices
    assert device_one.provider is context.provider
    assert device_two.application is context.application
    assert device_two.graph_order == (3, 0, 0, 0, 5, 1)
    assert device_two.parent is track.devices
    assert device_two.provider is context.provider
    assert len(transcript.sent_messages) == 1
    _, message = transcript.sent_messages[0]
    assert message.to_list() == [
        None,
        [
            [21, 1050, 1, 1013],
            [21, 1051, 0, 1050],
            [21, 1052, 1, 1050],
            [9, synthdef.anonymous_name, 1053, 0, 1052, "out", 30.0],
            [9, "mixer/patch[replace]/2x2", 1054, 0, 1050, "in_", 18.0, "out", 30.0],
            [9, "mixer/patch[hard,mix]/2x2", 1055, 1, 1050, "in_", 30.0, "out", 18.0],
        ],
    ]
    time.sleep(0.1)
    assert track.peak_levels == dict(
        input=(0.0, 0.0), postfader=(0.5, 0.5), prefader=(0.5, 0.5)
    )
    assert context.master_track.peak_levels == dict(
        input=(0.5, 0.5), postfader=(0.5, 0.5), prefader=(0.5, 0.5)
    )


def test_AudioEffect_query(synthdef_factory):
    application = Application()
    context = application.add_context()
    track = context.add_track()
    application.boot()
    track.add_device(AudioEffect, synthdef=synthdef_factory)
    assert str(track.query()) == normalize(
        """
        NODE TREE 1002 group (Track)
            1009 group (Parameters)
                1010 group (gain)
                1011 group (panning)
            1012 group (Receives)
            1003 mixer/patch[fb,gain]/2x2 (Input)
                active: 1.0, gain: 0.0, gate: 1.0, in_: 16.0, lag: 0.01, out: 18.0
            1008 group (SubTracks)
            1004 mixer/levels/2 (InputLevels)
                out: 18.0, gate: 1.0, lag: 0.01
            1013 group (Devices)
                1044 group (AudioEffect)
                    1048 mixer/patch[replace]/2x2 (DeviceIn)
                        active: 1.0, gate: 1.0, in_: 18.0, lag: 0.01, out: 28.0
                    1045 group (Parameters)
                    1046 group (Body)
                        1047 e2f7071cbafa6a2884524e116f015fa9
                            out: 28.0, gate: 1.0
                    1049 mixer/patch[hard,mix]/2x2 (DeviceOut)
                        active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 28.0, lag: 0.01, mix: 1.0, out: 18.0
            1005 mixer/levels/2 (PrefaderLevels)
                out: 18.0, gate: 1.0, lag: 0.01
            1014 group (PreFaderSends)
            1006 mixer/patch[gain,hard,replace]/2x2 (Output)
                active: 1.0, gain: c0, gate: 1.0, hard_gate: 1.0, in_: 18.0, lag: 0.01, out: 18.0
            1015 group (PostFaderSends)
                1029 mixer/patch[gain]/2x2 (Send)
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 18.0, lag: 0.01, out: 22.0
            1007 mixer/levels/2 (PostfaderLevels)
                out: 18.0, gate: 1.0, lag: 0.01
        """
    )


def test_Instrument_query(dc_instrument_synthdef_factory):
    application = Application()
    context = application.add_context()
    track = context.add_track()
    application.boot()
    track.add_device(Instrument, synthdef=dc_instrument_synthdef_factory)
    assert str(track.query()) == normalize(
        """
        NODE TREE 1002 group (Track)
            1009 group (Parameters)
                1010 group (gain)
                1011 group (panning)
            1012 group (Receives)
            1003 mixer/patch[fb,gain]/2x2 (Input)
                active: 1.0, gain: 0.0, gate: 1.0, in_: 16.0, lag: 0.01, out: 18.0
            1008 group (SubTracks)
            1004 mixer/levels/2 (InputLevels)
                out: 18.0, gate: 1.0, lag: 0.01
            1013 group (Devices)
                1044 group (Instrument)
                    1047 mixer/patch[replace]/2x2 (DeviceIn)
                        active: 1.0, gate: 1.0, in_: 18.0, lag: 0.01, out: 28.0
                    1045 group (Parameters)
                    1046 group (Body)
                    1048 mixer/patch[hard,mix]/2x2 (DeviceOut)
                        active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 28.0, lag: 0.01, mix: 1.0, out: 18.0
            1005 mixer/levels/2 (PrefaderLevels)
                out: 18.0, gate: 1.0, lag: 0.01
            1014 group (PreFaderSends)
            1006 mixer/patch[gain,hard,replace]/2x2 (Output)
                active: 1.0, gain: c0, gate: 1.0, hard_gate: 1.0, in_: 18.0, lag: 0.01, out: 18.0
            1015 group (PostFaderSends)
                1029 mixer/patch[gain]/2x2 (Send)
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 18.0, lag: 0.01, out: 22.0
            1007 mixer/levels/2 (PostfaderLevels)
                out: 18.0, gate: 1.0, lag: 0.01
        """
    )
