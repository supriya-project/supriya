import io
import os
import pytest
import supriya.cli
import uqbar.io


expected_files = [
    'test_project/test_project/sessions/.gitignore',
    'test_project/test_project/sessions/__init__.py',
    'test_project/test_project/sessions/test_session/__init__.py',
    'test_project/test_project/sessions/test_session/definition.py',
]


def test_exists(cli_paths):
    string_io = io.StringIO()
    pytest.helpers.create_cli_project(cli_paths.test_directory_path)
    pytest.helpers.create_cli_session(cli_paths.test_directory_path, 'test_session')
    with uqbar.io.RedirectedStreams(stdout=string_io):
        pytest.helpers.create_cli_session(
            cli_paths.test_directory_path, 'test_session', expect_error=True
        )
    pytest.helpers.compare_strings(
        r'''
        Creating session subpackage 'test_session' ...
            Path exists: test_project/sessions/test_session
        '''.replace(
            '/', os.path.sep
        ),
        string_io.getvalue(),
    )


def test_force_replace(cli_paths):
    string_io = io.StringIO()
    pytest.helpers.create_cli_project(cli_paths.test_directory_path)
    pytest.helpers.create_cli_session(cli_paths.test_directory_path, 'test_session')
    with uqbar.io.RedirectedStreams(stdout=string_io):
        pytest.helpers.create_cli_session(
            cli_paths.test_directory_path, 'test_session', force=True
        )
    pytest.helpers.compare_strings(
        r'''
        Creating session subpackage 'test_session' ...
            Created test_project/sessions/test_session/
        '''.replace(
            '/', os.path.sep
        ),
        string_io.getvalue(),
    )


def test_internal_path(cli_paths):
    string_io = io.StringIO()
    pytest.helpers.create_cli_project(cli_paths.test_directory_path)
    script = supriya.cli.ManageSessionScript()
    command = ['--new', 'test_session']
    internal_path = cli_paths.assets_path
    assert internal_path.exists()
    with uqbar.io.RedirectedStreams(stdout=string_io), uqbar.io.DirectoryChange(
        internal_path
    ):
        try:
            script(command)
        except SystemExit:
            raise RuntimeError('SystemExit')
    pytest.helpers.compare_strings(
        r'''
        Creating session subpackage 'test_session' ...
            Created test_project/sessions/test_session/
        '''.replace(
            '/', os.path.sep
        ),
        string_io.getvalue(),
    )


def test_success(cli_paths):
    string_io = io.StringIO()
    pytest.helpers.create_cli_project(cli_paths.test_directory_path)
    script = supriya.cli.ManageSessionScript()
    command = ['--new', 'test_session']
    with uqbar.io.RedirectedStreams(stdout=string_io), uqbar.io.DirectoryChange(
        cli_paths.inner_project_path
    ):
        try:
            script(command)
        except SystemExit:
            raise RuntimeError('SystemExit')
    pytest.helpers.compare_strings(
        r'''
        Creating session subpackage 'test_session' ...
            Created test_project/sessions/test_session/
        '''.replace(
            '/', os.path.sep
        ),
        string_io.getvalue(),
    )
    assert cli_paths.sessions_path.joinpath('test_session').exists()
    pytest.helpers.compare_path_contents(
        cli_paths.sessions_path, expected_files, cli_paths.test_directory_path
    )
    definition_path = cli_paths.sessions_path.joinpath('test_session', 'definition.py')
    with definition_path.open() as file_pointer:
        actual_contents = uqbar.strings.normalize(file_pointer.read())
    expected_contents = uqbar.strings.normalize(
        '''
    import supriya
    from test_project import project_settings


    session = supriya.Session.from_project_settings(project_settings)

    with supriya.synthdefs.SynthDefBuilder(
        duration=1.,
        out_bus=0,
        ) as builder:
        source = supriya.ugens.Line.ar(
            duration=builder['duration'],
            )
        supriya.ugens.Out.ar(
            bus=builder['out_bus'],
            source=[source] * len(session.audio_output_bus_group),
            )
    ramp_synthdef = builder.build()

    with session.at(0):
        session.add_synth(
            duration=1,
            synthdef=ramp_synthdef,
            )
    '''
    )
    assert actual_contents == expected_contents
