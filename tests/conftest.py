import pathlib
import pytest
import supriya


pytest_plugins = ['helpers_namespace']


test_directory_path = pathlib.Path(__file__).parent
output_directory_path = test_directory_path / 'output'
render_directory_path = test_directory_path / 'render'
output_file_path = output_directory_path / 'output.aiff'
render_yml_file_path = output_directory_path / 'render.yml'


@pytest.helpers.register
def assert_soundfile_ok(
    exit_code,
    expected_duration,
    expected_sample_rate,
    expected_channel_count,
    file_path=None,
    ):
    file_path = pathlib.Path(file_path or output_file_path)
    assert file_path.exists(), file_path
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
        d_recv_commands.append(['/d_recv', compiled_synthdef])
    return d_recv_commands


@pytest.helpers.register
def sample(file_path):
    soundfile = supriya.soundfiles.SoundFile(file_path)
    return {
        0.0: [round(x, 6) for x in soundfile.at_percent(0)],
        0.21: [round(x, 6) for x in soundfile.at_percent(0.21)],
        0.41: [round(x, 6) for x in soundfile.at_percent(0.41)],
        0.61: [round(x, 6) for x in soundfile.at_percent(0.61)],
        0.81: [round(x, 6) for x in soundfile.at_percent(0.81)],
        0.99: [round(x, 6) for x in soundfile.at_percent(0.99)],
        }


@pytest.fixture(autouse=True)
def server_shutdown():
    for server in supriya.Server._servers.values():
        server.quit()
    yield
    for server in supriya.Server._servers.values():
        server.quit()


@pytest.fixture
def server():
    server = supriya.Server()
    server.debug_osc = True
    yield server
    server.quit()
    server.debug_osc = False
