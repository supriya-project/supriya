import doctest
import jinja2
import os
import pathlib
import pytest
import re
import shutil
import supriya
import sys
import types
import uqbar.io


pytest_plugins = ['helpers_namespace']


### FIXTURES ###


@pytest.fixture
def cli_paths(tmpdir):
    package_name = 'test_project'
    # test_directory_path = pathlib.Path(__file__).parent
    test_directory_path = pathlib.Path(tmpdir)
    outer_project_path = test_directory_path.joinpath(package_name)
    inner_project_path = outer_project_path.joinpath(package_name)
    cli_paths = types.SimpleNamespace(
        test_directory_path=test_directory_path,
        outer_project_path=outer_project_path,
        inner_project_path=inner_project_path,
        assets_path=inner_project_path.joinpath('assets'),
        sessions_path=inner_project_path.joinpath('sessions'),
        distribution_path=inner_project_path.joinpath('distribution'),
        materials_path=inner_project_path.joinpath('materials'),
        renders_path=inner_project_path.joinpath('renders'),
        synthdefs_path=inner_project_path.joinpath('synthdefs'),
        tools_path=inner_project_path.joinpath('tools'),
        )
    if outer_project_path.exists():
        shutil.rmtree(outer_project_path)
    if sys.path[0] != str(outer_project_path):
        sys.path.insert(0, str(outer_project_path))
    yield cli_paths
    for path, module in tuple(sys.modules.items()):
        if not path or not module:
            continue
        if path.startswith(package_name):
            del(sys.modules[path])


@pytest.fixture
def nonrealtime_paths(tmpdir):
    # test_directory_path = pathlib.Path(__file__).parent
    test_directory_path = pathlib.Path(tmpdir)
    output_directory_path = test_directory_path / 'output'
    render_directory_path = test_directory_path / 'render'
    output_file_path = output_directory_path / 'output.aiff'
    render_yml_file_path = output_directory_path / 'render.yml'
    nonrealtime_paths = types.SimpleNamespace(
        test_directory_path=test_directory_path,
        output_directory_path=output_directory_path,
        render_directory_path=render_directory_path,
        output_file_path=output_file_path,
        render_yml_file_path=render_yml_file_path,
        )
    original_directory = pathlib.Path.cwd()
    for path in [
        output_directory_path,
        render_directory_path,
        ]:
        path.mkdir(parents=True, exist_ok=True)
    os.chdir(test_directory_path)
    yield nonrealtime_paths
    os.chdir(original_directory)
    for path in [
        output_directory_path,
        render_directory_path,
        ]:
        if path.exists():
            shutil.rmtree(path)


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


ansi_escape = re.compile(r'\x1b[^m]*m')


### HELPERS ###


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
def compare_path_contents(path_to_search, expected_files, test_path):
    actual_files = sorted(
        str(path.relative_to(test_path))
        for path in sorted(path_to_search.glob('**/*.*'))
        if '__pycache__' not in path.parts and
        path.suffix != '.pyc'
        )
    pytest.helpers.compare_strings(
        '\n'.join(str(_) for _ in actual_files),
        '\n'.join(str(_) for _ in expected_files),
        )


@pytest.helpers.register
def compare_strings(expected, actual):
    actual = uqbar.strings.normalize(ansi_escape.sub('', actual))
    expected = uqbar.strings.normalize(ansi_escape.sub('', expected))
    example = types.SimpleNamespace()
    example.want = expected
    output_checker = doctest.OutputChecker()
    flags = (
        doctest.NORMALIZE_WHITESPACE |
        doctest.ELLIPSIS |
        doctest.REPORT_NDIFF
        )
    success = output_checker.check_output(expected, actual, flags)
    if not success:
        diff = output_checker.output_difference(example, actual, flags)
        raise Exception(diff)


@pytest.helpers.register
def create_cli_material(
    path,
    material_name='test_material',
    force=False,
    expect_error=False,
    definition_contents=None,
    ):
    path = pathlib.Path(path)
    inner_project_path = path / 'test_project' / 'test_project'
    script = supriya.cli.ManageMaterialScript()
    command = ['--new', material_name]
    if force:
        command.insert(0, '-f')
    with uqbar.io.DirectoryChange(str(inner_project_path)):
        if expect_error:
            with pytest.raises(SystemExit) as exception_info:
                script(command)
            assert exception_info.value.code == 1
        else:
            try:
                script(command)
            except SystemExit:
                raise RuntimeError('SystemExit')
    material_path = inner_project_path / 'materials' / material_name
    if definition_contents:
        definition_contents = uqbar.strings.normalize(definition_contents)
        definition_file_path = material_path / 'definition.py'
        with open(str(definition_file_path), 'w') as file_pointer:
            file_pointer.write(definition_contents)
    return material_path


@pytest.helpers.register
def create_cli_project(path, force=False, expect_error=False):
    path = pathlib.Path(path)
    script = supriya.cli.ManageProjectScript()
    command = [
        '--new',
        'Test Project',
        '--composer-name', 'Josiah Wolf Oberholtzer',
        '--composer-email', 'josiah.oberholtzer@gmail.com',
        '--composer-github', 'josiah-wolf-oberholtzer',
        '--composer-website', 'www.josiahwolfoberholtzer.com',
        '--composer-library', 'amazing_library',
        ]
    if force:
        command.insert(0, '-f')
    with uqbar.io.DirectoryChange(str(path)):
        if expect_error:
            with pytest.raises(SystemExit) as exception_info:
                script(command)
            assert exception_info.value.code == 1
        else:
            try:
                script(command)
            except SystemExit:
                raise RuntimeError('SystemExit')


@pytest.helpers.register
def create_cli_session(
    path,
    session_name='test_session',
    force=False,
    expect_error=False,
    definition_contents=None,
    ):
    path = pathlib.Path(path)
    inner_project_path = path / 'test_project' / 'test_project'
    script = supriya.cli.ManageSessionScript()
    command = ['--new', session_name]
    if force:
        command.insert(0, '-f')
    with uqbar.io.DirectoryChange(str(inner_project_path)):
        if expect_error:
            with pytest.raises(SystemExit) as exception_info:
                script(command)
            assert exception_info.value.code == 1
        else:
            try:
                script(command)
            except SystemExit:
                raise RuntimeError('SystemExit')
    session_path = inner_project_path / 'sessions' / session_name
    if definition_contents:
        definition_contents = uqbar.strings.normalize(definition_contents)
        definition_file_path = session_path / 'definition.py'
        with open(str(definition_file_path), 'w') as file_pointer:
            file_pointer.write(definition_contents)
    return session_path


@pytest.helpers.register
def get_basic_session_template():
    return jinja2.Template(uqbar.strings.normalize('''
    import supriya
    from test_project import project_settings


    {{ output_section_singular }} = supriya.Session.from_project_settings(project_settings)

    with supriya.synthdefs.SynthDefBuilder(
        duration=1.,
        out_bus=0,
        ) as builder:
        source = supriya.ugens.Line.ar(
            duration=builder['duration'],
            ) * {{ multiplier | default(1.0) }}
        supriya.ugens.Out.ar(
            bus=builder['out_bus'],
            source=[source] * len({{ output_section_singular }}.audio_output_bus_group),
            )
    ramp_synthdef = builder.build()

    with {{ output_section_singular }}.at(0):
        {{ output_section_singular }}.add_synth(
            duration=1,
            synthdef=ramp_synthdef,
            )
    '''))


@pytest.helpers.register
def get_chained_session_template():
    return jinja2.Template(uqbar.strings.normalize('''
    import supriya
    from test_project import project_settings
    from test_project.{{ input_section_singular }}s.{{ input_name }}.definition \
        import {{ input_section_singular }} as {{ input_name }}


    {{ output_section_singular }} = supriya.Session.from_project_settings(
        project_settings,
        input_={{ input_name }},
        )

    with supriya.SynthDefBuilder(
        in_bus=0,
        out_bus=0,
        multiplier=1,
        ) as builder:
        source = supriya.ugens.In.ar(
            bus=builder['in_bus'],
            channel_count=len({{ output_section_singular }}.audio_output_bus_group),
            )
        supriya.ugens.ReplaceOut.ar(
            bus=builder['out_bus'],
            source=source * builder['multiplier'],
            )
    multiplier_synthdef = builder.build()

    with {{ output_section_singular }}.at(0):
        {{ output_section_singular }}.add_synth(
            duration=1,
            in_bus={{ output_section_singular }}.audio_input_bus_group,
            multiplier={{ multiplier }},
            synthdef=multiplier_synthdef,
            )
    '''))


@pytest.helpers.register
def get_session_factory_template():
    return jinja2.Template(uqbar.strings.normalize('''
    import supriya
    from test_project import project_settings


    class SessionFactory:

        def __init__(self, project_settings):
            self.project_settings = project_settings

        def _build_ramp_synthdef(self):
            server_options = self.project_settings['server_options']
            channel_count = server_options['output_bus_channel_count']
            with supriya.synthdefs.SynthDefBuilder(
                duration=1.,
                out_bus=0,
                ) as builder:
                source = supriya.ugens.Line.ar(
                    duration=builder['duration'],
                    ) * {{ multiplier | default(1.0) }}
                supriya.ugens.Out.ar(
                    bus=builder['out_bus'],
                    source=[source] * channel_count,
                    )
            ramp_synthdef = builder.build()
            return ramp_synthdef

        def __session__(self):
            session = supriya.Session.from_project_settings(self.project_settings)
            ramp_synthdef = self._build_ramp_synthdef()
            with session.at(0):
                session.add_synth(
                    duration=1,
                    synthdef=ramp_synthdef,
                    )
            return session


    {{ output_section_singular }} = SessionFactory(project_settings)
    '''))


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
