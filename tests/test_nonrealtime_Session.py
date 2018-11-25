import pytest

import supriya.nonrealtime
import supriya.osc
import supriya.soundfiles


def test_01(nonrealtime_paths):
    session = supriya.nonrealtime.Session()
    with session.at(0):
        session.add_synth(duration=1, synthdef=pytest.helpers.build_basic_synthdef())
    exit_code, _ = session.render(nonrealtime_paths.output_file_path)
    pytest.helpers.assert_soundfile_ok(
        nonrealtime_paths.output_file_path, exit_code, 1.0, 44100, 8
    )


def test_02(nonrealtime_paths):
    session = supriya.nonrealtime.Session()
    with session.at(0):
        session.add_synth(duration=300, synthdef=pytest.helpers.build_basic_synthdef())
    exit_code, _ = session.render(
        nonrealtime_paths.output_file_path,
        sample_rate=48000,
        output_bus_channel_count=2,
    )
    pytest.helpers.assert_soundfile_ok(
        nonrealtime_paths.output_file_path, exit_code, 300.0, 48000, 2
    )


def test_03(nonrealtime_paths):
    session = supriya.nonrealtime.Session()
    synthdef = pytest.helpers.build_duration_synthdef()
    with session.at(0):
        session.add_synth(duration=1, synthdef=pytest.helpers.build_duration_synthdef())
    assert session.to_osc_bundles() == [
        supriya.osc.OscBundle(
            timestamp=0.0,
            contents=(
                supriya.osc.OscMessage("/d_recv", bytearray(synthdef.compile())),
                supriya.osc.OscMessage(
                    "/s_new",
                    "448a8d487adfc99ec697033edc2a1227",
                    1000,
                    0,
                    0,
                    "duration",
                    1.0,
                ),
            ),
        ),
        supriya.osc.OscBundle(
            timestamp=1.0,
            contents=(
                supriya.osc.OscMessage("/n_free", 1000),
                supriya.osc.OscMessage(0),
            ),
        ),
    ]
    exit_code, _ = session.render(
        nonrealtime_paths.output_file_path, output_bus_channel_count=1
    )
    pytest.helpers.assert_soundfile_ok(
        nonrealtime_paths.output_file_path, exit_code, 1.0, 44100, 1
    )
    soundfile = supriya.soundfiles.SoundFile(nonrealtime_paths.output_file_path)
    for i in range(1, 100):
        value = round(float(i) / 100, 2)
        assert round(soundfile.at_percent(value)[0], 2) == value


def test_04():
    session = supriya.nonrealtime.Session()
    with session.at(0):
        session.add_synth(duration=1, synthdef=pytest.helpers.build_gate_synthdef())
    assert session.to_osc_bundles(duration=2) == [
        supriya.osc.OscBundle(
            timestamp=0.0,
            contents=(
                supriya.osc.OscMessage(
                    "/d_recv",
                    bytearray(
                        b"SCgf\x00\x00\x00\x02\x00\x01 fc663c6d1f8badaed1bd3e25cf2220f0\x00\x00\x00\x08?\x80\x00\x00\x00\x00\x00\x00@\x00\x00\x00\xc2\xc6\x00\x00<#\xd7\n@\xa0\x00\x00\xc0\x80\x00\x00C\xdc\x00\x00\x00\x00\x00\x01?\x80\x00\x00\x00\x00\x00\x01\x04gate\x00\x00\x00\x00\x00\x00\x00\x05\x07Control\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x01\x06EnvGen\x02\x00\x00\x00\x11\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x01\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x01\xff\xff\xff\xff\x00\x00\x00\x01\xff\xff\xff\xff\x00\x00\x00\x02\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x03\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x04\xff\xff\xff\xff\x00\x00\x00\x05\xff\xff\xff\xff\x00\x00\x00\x06\xff\xff\xff\xff\x00\x00\x00\x01\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x05\xff\xff\xff\xff\x00\x00\x00\x06\x02\x03Saw\x02\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\xff\xff\xff\xff\x00\x00\x00\x07\x02\x0cBinaryOpUGen\x02\x00\x00\x00\x02\x00\x00\x00\x01\x00\x02\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x02\x03Out\x02\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x01\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00"
                    ),
                ),
                supriya.osc.OscMessage(
                    "/s_new", "fc663c6d1f8badaed1bd3e25cf2220f0", 1000, 0, 0
                ),
            ),
        ),
        supriya.osc.OscBundle(
            timestamp=1.0, contents=(supriya.osc.OscMessage("/n_set", 1000, "gate", 0),)
        ),
        supriya.osc.OscBundle(timestamp=2.0, contents=(supriya.osc.OscMessage(0),)),
    ]
