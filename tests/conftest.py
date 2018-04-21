import pathlib
import pytest
import re
import supriya
import types


pytest_plugins = ['helpers_namespace']


### FIXTURES ###


@pytest.fixture
def pseudo_server():
    return types.SimpleNamespace(
        audio_bus_allocator=supriya.realtime.BlockAllocator(),
        control_bus_allocator=supriya.realtime.BlockAllocator(),
        node_id_allocator=supriya.realtime.NodeIdAllocator(),
        )


@pytest.fixture
def server():
    server = supriya.Server()
    server.latency = 0.0
    server.boot()
    supriya.assets.synthdefs.default.allocate(server)
    server.debug_osc = True
    yield server
    server.debug_osc = False
    server.quit()


@pytest.fixture(autouse=True)
def server_shutdown():
    for server in supriya.Server._servers.values():
        server.quit()
    yield
    for server in supriya.Server._servers.values():
        server.quit()


### DATA ###


test_directory_path = pathlib.Path(__file__).parent
output_directory_path = test_directory_path / 'output'
render_directory_path = test_directory_path / 'render'
output_file_path = output_directory_path / 'output.aiff'
render_yml_file_path = output_directory_path / 'render.yml'


class TestSessionFactory:

    def __init__(
        self,
        input_bus_channel_count=None,
        output_bus_channel_count=None,
        multiplier=1.0,
        ):
        options = supriya.realtime.ServerOptions(
            input_bus_channel_count=input_bus_channel_count,
            output_bus_channel_count=output_bus_channel_count,
            )
        self.input_bus_channel_count = options.input_bus_channel_count
        self.output_bus_channel_count = options.output_bus_channel_count
        self.multiplier = multiplier

    def __session__(self):
        session = supriya.nonrealtime.Session(
            input_bus_channel_count=self.input_bus_channel_count,
            output_bus_channel_count=self.output_bus_channel_count,
            name='inner-session',
            )
        output_bus_channel_count = session.options.output_bus_channel_count
        synthdef = build_dc_synthdef(
            channel_count=output_bus_channel_count,
            )
        with session.at(0):
            synth = session.add_synth(
                synthdef=synthdef,
                duration=10,
                source=0,
                )
        with session.at(2):
            synth['source'] = 0.25 * self.multiplier
        with session.at(4):
            synth['source'] = 0.5 * self.multiplier
        with session.at(6):
            synth['source'] = 0.75 * self.multiplier
        with session.at(8):
            synth['source'] = 1.0 * self.multiplier
        assert synthdef.anonymous_name == 'b47278d408f17357f6b260ec30ea213d'
        return session


### HELPERS ###


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
def build_dc_synthdef(channel_count=1):
    with supriya.synthdefs.SynthDefBuilder(
        out_bus=0,
        source=0,
        ) as builder:
        source = supriya.ugens.K2A.ar(source=builder['source'])
        supriya.ugens.Out.ar(
            bus=builder['out_bus'],
            source=[source] * channel_count,
            )
    return builder.build()


@pytest.helpers.register
def build_basic_synthdef(bus=0):
    builder = supriya.synthdefs.SynthDefBuilder()
    with builder:
        supriya.ugens.Out.ar(
            bus=bus,
            source=supriya.ugens.SinOsc.ar(),
            )
    return builder.build()


@pytest.helpers.register
def build_diskin_synthdef(channel_count=1):
    with supriya.synthdefs.SynthDefBuilder(
        out_bus=0,
        buffer_id=0,
        ) as builder:
        source = supriya.ugens.DiskIn.ar(
            buffer_id=builder['buffer_id'],
            channel_count=channel_count,
            )
        supriya.ugens.Out.ar(
            bus=builder['out_bus'],
            source=source,
            )
    return builder.build()


@pytest.helpers.register
def build_duration_synthdef(bus=0):
    builder = supriya.synthdefs.SynthDefBuilder(duration=0)
    with builder:
        supriya.ugens.Out.ar(
            bus=bus,
            source=supriya.ugens.Line.ar(
                duration=builder['duration'],
                ),
            )
    return builder.build()


@pytest.helpers.register
def build_gate_synthdef(bus=0):
    builder = supriya.synthdefs.SynthDefBuilder(gate=1)
    with builder:
        envelope = supriya.synthdefs.Envelope.asr()
        envgen = supriya.ugens.EnvGen.ar(
            envelope=envelope,
            gate=builder['gate'],
            )
        source = supriya.ugens.Saw.ar() * envgen
        supriya.ugens.Out.ar(
            bus=bus,
            source=source,
            )
    return builder.build()


@pytest.helpers.register
def build_multiplier_synthdef(channel_count=1):
    with supriya.synthdefs.SynthDefBuilder(
        in_bus=0,
        out_bus=0,
        multiplier=1,
        ) as builder:
        source = supriya.ugens.In.ar(
            bus=builder['in_bus'],
            channel_count=channel_count,
            )
        supriya.ugens.ReplaceOut.ar(
            bus=builder['out_bus'],
            source=source * builder['multiplier'],
            )
    return builder.build()


@pytest.helpers.register
def get_objects_as_string(objects, replace_uuids=False):
    pattern = re.compile(r"\bUUID\('(.*)'\)")
    objects_string = '\n'.join(format(x) for x in objects)
    if replace_uuids:
        matches = []
        search_offset = 0
        while True:
            match = pattern.search(objects_string, search_offset)
            if not match:
                break
            group = match.groups()[0]
            if group not in matches:
                matches.append(group)
            search_offset = match.end()
        for i, match in enumerate(matches, 65):
            objects_string = objects_string.replace(match, chr(i))
    return objects_string


@pytest.helpers.register
def make_test_session(
    input_=None,
    input_bus_channel_count=None,
    output_bus_channel_count=None,
    multiplier=1.0,
    ):
    session = supriya.nonrealtime.Session(
        input_bus_channel_count=input_bus_channel_count,
        output_bus_channel_count=output_bus_channel_count,
        name='inner-session',
        )
    output_bus_channel_count = session.options.output_bus_channel_count
    synthdef = build_dc_synthdef(
        channel_count=output_bus_channel_count,
        )
    with session.at(0):
        synth = session.add_synth(
            synthdef=synthdef,
            duration=10,
            source=0,
            )
    with session.at(2):
        synth['source'] = 0.25 * multiplier
    with session.at(4):
        synth['source'] = 0.5 * multiplier
    with session.at(6):
        synth['source'] = 0.75 * multiplier
    with session.at(8):
        synth['source'] = 1.0 * multiplier
    assert synthdef.anonymous_name == 'b47278d408f17357f6b260ec30ea213d'
    d_recv_commands = build_d_recv_commands([synthdef])
    assert session.to_lists() == [
        [0.0, [
            *d_recv_commands,
            ['/s_new', 'b47278d408f17357f6b260ec30ea213d', 1000, 0, 0,
                'source', 0]]],
        [2.0, [['/n_set', 1000, 'source', 0.25 * multiplier]]],
        [4.0, [['/n_set', 1000, 'source', 0.5 * multiplier]]],
        [6.0, [['/n_set', 1000, 'source', 0.75 * multiplier]]],
        [8.0, [['/n_set', 1000, 'source', 1.0 * multiplier]]],
        [10.0, [['/n_free', 1000], [0]]]
        ]
    return session


@pytest.helpers.register
def make_test_session_factory(
    input_bus_channel_count=None,
    output_bus_channel_count=None,
    multiplier=1.0,
    ):
    session_factory = TestSessionFactory(
        input_bus_channel_count=input_bus_channel_count,
        output_bus_channel_count=output_bus_channel_count,
        multiplier=multiplier,
        )
    return session_factory


@pytest.helpers.register
def manual_incommunicado(pattern, timestamp=10):
    pseudo_server = types.SimpleNamespace(
        audio_bus_allocator=supriya.realtime.BlockAllocator(),
        control_bus_allocator=supriya.realtime.BlockAllocator(),
        node_id_allocator=supriya.realtime.NodeIdAllocator(),
        )
    player = supriya.patterns.RealtimeEventPlayer(
        pattern,
        server=pseudo_server,
        )
    lists, deltas, delta = [], [], True
    while delta is not None:
        bundle, delta = player(timestamp, timestamp, communicate=False)
        if delta is not None:
            timestamp += delta
        lists.append(bundle.to_list(True))
        deltas.append(delta)
    return lists, deltas


@pytest.helpers.register
def sample_soundfile(file_path):
    soundfile = supriya.soundfiles.SoundFile(file_path)
    return {
        0.0: [round(x, 6) for x in soundfile.at_percent(0)],
        0.21: [round(x, 6) for x in soundfile.at_percent(0.21)],
        0.41: [round(x, 6) for x in soundfile.at_percent(0.41)],
        0.61: [round(x, 6) for x in soundfile.at_percent(0.61)],
        0.81: [round(x, 6) for x in soundfile.at_percent(0.81)],
        0.99: [round(x, 6) for x in soundfile.at_percent(0.99)],
        }


@pytest.helpers.register
def setup_pattern_send(pattern, iterations):
    events, iterator = [], iter(pattern)
    for i in range(iterations):
        event = next(iterator)
        events.append(event)
    try:
        event = iterator.send(True)
        events.append(event)
        events.extend(iterator)
    except StopIteration:
        pass
    return events
