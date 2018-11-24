import pytest

import supriya.nonrealtime
import supriya.synthdefs
import supriya.ugens

with supriya.synthdefs.SynthDefBuilder() as builder:
    source = supriya.ugens.WhiteNoise.ar()
    supriya.ugens.Out.ar(bus=0, source=source)
nonrepeatable_noise_synthdef = builder.build()


with supriya.synthdefs.SynthDefBuilder(rand_id=0, rand_seed=0) as builder:
    supriya.ugens.RandID.ir(rand_id=builder["rand_id"])
    supriya.ugens.RandSeed.ir(seed=builder["rand_seed"], trigger=1)
    source = supriya.ugens.WhiteNoise.ar()
    supriya.ugens.Out.ar(bus=0, source=source)
repeatable_noise_synthdef = builder.build()


with supriya.synthdefs.SynthDefBuilder(rand_id=0, rand_seed=0) as builder:
    supriya.ugens.RandID.ir(rand_id=builder["rand_id"])
    supriya.ugens.RandSeed.ir(seed=builder["rand_seed"], trigger=1)
seed_synthdef = builder.build()


with supriya.synthdefs.SynthDefBuilder(rand_id=0) as builder:
    supriya.ugens.RandID.ir(rand_id=builder["rand_id"])
    source = supriya.ugens.WhiteNoise.ar()
    supriya.ugens.Out.ar(bus=0, source=source)
maybe_repeatable_noise_synthdef = builder.build()


def test_nonrepeatable(nonrealtime_paths):
    session = supriya.nonrealtime.Session(0, 1)
    with session.at(0):
        session.add_synth(duration=1, synthdef=nonrepeatable_noise_synthdef)
    exit_code, output_file_path = session.render()
    pytest.helpers.assert_soundfile_ok(output_file_path, exit_code, 1, 44100, 1)
    sampled_session = pytest.helpers.sample_soundfile(output_file_path)
    for _ in range(10):
        output_file_path.unlink()
        exit_code, output_file_path = session.render()
        pytest.helpers.assert_soundfile_ok(output_file_path, exit_code, 1, 44100, 1)
        assert pytest.helpers.sample_soundfile(output_file_path) != sampled_session


def test_repeatable(nonrealtime_paths):
    session = supriya.nonrealtime.Session(0, 1)
    with session.at(0):
        session.add_synth(duration=1, synthdef=repeatable_noise_synthdef)
    exit_code, output_file_path = session.render()
    pytest.helpers.assert_soundfile_ok(output_file_path, exit_code, 1, 44100, 1)
    sampled_session = pytest.helpers.sample_soundfile(output_file_path)
    for _ in range(10):
        output_file_path.unlink()
        exit_code, output_file_path = session.render()
        pytest.helpers.assert_soundfile_ok(output_file_path, exit_code, 1, 44100, 1)
        assert pytest.helpers.sample_soundfile(output_file_path) == sampled_session


def test_maybe_repeatable_but_wasnt(nonrealtime_paths):
    """
    Setting a RandID isn't enough. The RNG will be initialized randomly.
    """
    session = supriya.nonrealtime.Session(0, 1)
    with session.at(0):
        session.add_synth(duration=1, synthdef=maybe_repeatable_noise_synthdef)
    exit_code, output_file_path = session.render()
    pytest.helpers.assert_soundfile_ok(output_file_path, exit_code, 1, 44100, 1)
    sampled_session = pytest.helpers.sample_soundfile(output_file_path)
    for _ in range(10):
        output_file_path.unlink()
        exit_code, output_file_path = session.render()
        pytest.helpers.assert_soundfile_ok(output_file_path, exit_code, 1, 44100, 1)
        assert pytest.helpers.sample_soundfile(output_file_path) != sampled_session


def test_maybe_repeatable_and_was(nonrealtime_paths):
    """
    Setting a RandID and seeding it in another synth locks us in.
    """
    session = supriya.nonrealtime.Session(0, 1)
    with session.at(0):
        session.add_synth(duration=1, synthdef=maybe_repeatable_noise_synthdef)
        session.add_synth(add_action="ADD_TO_HEAD", duration=0, synthdef=seed_synthdef)
    exit_code, output_file_path = session.render()
    pytest.helpers.assert_soundfile_ok(output_file_path, exit_code, 1, 44100, 1)
    sampled_session = pytest.helpers.sample_soundfile(output_file_path)
    for _ in range(10):
        output_file_path.unlink()
        exit_code, output_file_path = session.render()
        pytest.helpers.assert_soundfile_ok(output_file_path, exit_code, 1, 44100, 1)
        assert pytest.helpers.sample_soundfile(output_file_path) == sampled_session


def test_maybe_repeatable_and_almost_was(nonrealtime_paths):
    """
    Seeding is sensitive to node order.
    """
    session = supriya.nonrealtime.Session(0, 1)
    with session.at(0):
        session.add_synth(duration=1, synthdef=maybe_repeatable_noise_synthdef)
        session.add_synth(add_action="ADD_TO_TAIL", duration=0, synthdef=seed_synthdef)
    exit_code, output_file_path = session.render()
    pytest.helpers.assert_soundfile_ok(output_file_path, exit_code, 1, 44100, 1)
    first_sampled_session = sorted(
        pytest.helpers.sample_soundfile(output_file_path).items()
    )
    for _ in range(10):
        output_file_path.unlink()
        exit_code, output_file_path = session.render()
        pytest.helpers.assert_soundfile_ok(output_file_path, exit_code, 1, 44100, 1)
        sampled_session = sorted(
            pytest.helpers.sample_soundfile(output_file_path).items()
        )
        assert first_sampled_session[0] != sampled_session[0]
        assert first_sampled_session[1:] == sampled_session[1:]


def test_repeatable_via_session_method(nonrealtime_paths):
    session = supriya.nonrealtime.Session(0, 1)
    with session.at(0):
        session.add_synth(
            duration=1, synthdef=maybe_repeatable_noise_synthdef, rand_seed=0
        )
        session.set_rand_seed(rand_id=0, rand_seed=23)
    d_recv_commands = pytest.helpers.build_d_recv_commands(
        [session._build_rand_seed_synthdef(), maybe_repeatable_noise_synthdef]
    )
    assert session.to_lists() == [
        [
            0.0,
            [
                *d_recv_commands,
                [
                    "/s_new",
                    maybe_repeatable_noise_synthdef.anonymous_name,
                    1000,
                    0,
                    0,
                    "rand_seed",
                    0,
                ],
                [
                    "/s_new",
                    session._build_rand_seed_synthdef().anonymous_name,
                    1001,
                    0,
                    0,
                    "rand_id",
                    0,
                    "rand_seed",
                    23,
                ],
            ],
        ],
        [1.0, [["/n_free", 1000], [0]]],
    ]
    exit_code, output_file_path = session.render()
    pytest.helpers.assert_soundfile_ok(output_file_path, exit_code, 1, 44100, 1)
    sampled_session = pytest.helpers.sample_soundfile(output_file_path)
    for _ in range(10):
        output_file_path.unlink()
        exit_code, output_file_path = session.render()
        pytest.helpers.assert_soundfile_ok(output_file_path, exit_code, 1, 44100, 1)
        assert pytest.helpers.sample_soundfile(output_file_path) == sampled_session
