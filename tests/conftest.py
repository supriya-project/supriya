import pathlib
import platform

import pytest

import supriya

pytest_plugins = ["helpers_namespace", "sphinx.testing.fixtures"]


# ### FIXTURES ### #


@pytest.fixture
def server():
    server = supriya.Server()
    server.latency = 0.0
    server.boot()
    server.add_synthdef(supriya.assets.synthdefs.default)
    yield server
    server.quit()


@pytest.fixture(scope="module")
def persistent_server():
    server = supriya.Server()
    server.latency = 0.0
    server.boot()
    yield server
    server.quit()


# ### HELPERS ### #


@pytest.helpers.register
def assert_soundfile_ok(
    file_path,
    exit_code,
    expected_duration,
    expected_sample_rate,
    expected_channel_count,
):
    file_path = pathlib.Path(file_path)
    assert file_path.exists(), file_path
    if platform.system() != "Windows":
        # scsynth.exe renders but exits non-zero
        # https://github.com/supercollider/supercollider/issues/5769
        assert exit_code == 0, exit_code
    soundfile = supriya.soundfiles.SoundFile(file_path)
    assert round(soundfile.seconds, 2) == expected_duration, round(soundfile.seconds, 2)
    assert soundfile.sample_rate == expected_sample_rate, soundfile.sample_rate
    assert soundfile.channel_count == expected_channel_count, soundfile.channel_count


@pytest.helpers.register
def build_d_recv_commands(synthdefs):
    d_recv_commands = []
    synthdefs = sorted(synthdefs, key=lambda x: x.anonymous_name)
    for synthdef in synthdefs:
        compiled_synthdef = synthdef.compile(use_anonymous_name=True)
        compiled_synthdef = bytearray(compiled_synthdef)
        d_recv_commands.append(["/d_recv", compiled_synthdef])
    return d_recv_commands


@pytest.helpers.register
def build_dc_synthdef(channel_count=1):
    with supriya.synthdefs.SynthDefBuilder(out_bus=0, source=0) as builder:
        source = supriya.ugens.K2A.ar(source=builder["source"])
        supriya.ugens.Out.ar(bus=builder["out_bus"], source=[source] * channel_count)
    return builder.build()


@pytest.helpers.register
def build_basic_synthdef(bus=0):
    builder = supriya.synthdefs.SynthDefBuilder()
    with builder:
        supriya.ugens.Out.ar(bus=bus, source=supriya.ugens.SinOsc.ar())
    return builder.build()


@pytest.helpers.register
def build_diskin_synthdef(channel_count=1):
    with supriya.synthdefs.SynthDefBuilder(out_bus=0, buffer_id=0) as builder:
        source = supriya.ugens.DiskIn.ar(
            buffer_id=builder["buffer_id"], channel_count=channel_count
        )
        supriya.ugens.Out.ar(bus=builder["out_bus"], source=source)
    return builder.build()


@pytest.helpers.register
def build_duration_synthdef(bus=0):
    builder = supriya.synthdefs.SynthDefBuilder(duration=0)
    with builder:
        supriya.ugens.Out.ar(
            bus=bus, source=supriya.ugens.Line.ar(duration=builder["duration"])
        )
    return builder.build()


@pytest.helpers.register
def build_gate_synthdef(bus=0):
    builder = supriya.synthdefs.SynthDefBuilder(gate=1)
    with builder:
        envelope = supriya.synthdefs.Envelope.asr()
        envgen = supriya.ugens.EnvGen.ar(envelope=envelope, gate=builder["gate"])
        source = supriya.ugens.Saw.ar() * envgen
        supriya.ugens.Out.ar(bus=bus, source=source)
    return builder.build()


@pytest.helpers.register
def build_multiplier_synthdef(channel_count=1):
    with supriya.synthdefs.SynthDefBuilder(
        in_bus=0, out_bus=0, multiplier=1
    ) as builder:
        source = supriya.ugens.In.ar(bus=builder["in_bus"], channel_count=channel_count)
        supriya.ugens.ReplaceOut.ar(
            bus=builder["out_bus"], source=source * builder["multiplier"]
        )
    return builder.build()


@pytest.helpers.register
def sample_soundfile(file_path, rounding=6):
    soundfile = supriya.soundfiles.SoundFile(file_path)
    return {
        0.0: [round(x, rounding) for x in soundfile.at_percent(0)],
        0.21: [round(x, rounding) for x in soundfile.at_percent(0.21)],
        0.41: [round(x, rounding) for x in soundfile.at_percent(0.41)],
        0.61: [round(x, rounding) for x in soundfile.at_percent(0.61)],
        0.81: [round(x, rounding) for x in soundfile.at_percent(0.81)],
        0.99: [round(x, rounding) for x in soundfile.at_percent(0.99)],
    }
