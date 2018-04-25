import io
import os
import pytest
import supriya.cli
import uqbar.io


expected_files = [
    'test_project/test_project/materials/.gitignore',
    'test_project/test_project/materials/__init__.py',
    'test_project/test_project/materials/test_material/__init__.py',
    'test_project/test_project/materials/test_material/definition.py',
    ]


def test_exists(cli_paths):
    string_io = io.StringIO()
    pytest.helpers.create_cli_project(cli_paths.test_directory_path)
    pytest.helpers.create_cli_material(cli_paths.test_directory_path, 'test_material')
    with uqbar.io.RedirectedStreams(stdout=string_io):
        pytest.helpers.create_cli_material(cli_paths.test_directory_path, 'test_material', expect_error=True)
    pytest.helpers.compare_strings(
        r'''
        Creating material subpackage 'test_material' ...
            Path exists: test_project/materials/test_material
        '''.replace('/', os.path.sep),
        string_io.getvalue(),
        )


def test_force_replace(cli_paths):
    string_io = io.StringIO()
    pytest.helpers.create_cli_project(cli_paths.test_directory_path)
    pytest.helpers.create_cli_material(cli_paths.test_directory_path, 'test_material')
    with uqbar.io.RedirectedStreams(stdout=string_io):
        pytest.helpers.create_cli_material(cli_paths.test_directory_path, 'test_material', force=True)
    pytest.helpers.compare_strings(
        r'''
        Creating material subpackage 'test_material' ...
            Created test_project/materials/test_material/
        '''.replace('/', os.path.sep),
        string_io.getvalue(),
        )


def test_internal_path(cli_paths):
    string_io = io.StringIO()
    pytest.helpers.create_cli_project(cli_paths.test_directory_path)
    script = supriya.cli.ManageMaterialScript()
    command = ['--new', 'test_material']
    internal_path = cli_paths.assets_path
    assert internal_path.exists()
    with uqbar.io.RedirectedStreams(stdout=string_io):
        with uqbar.io.DirectoryChange(internal_path):
            try:
                script(command)
            except SystemExit:
                raise RuntimeError('SystemExit')
    pytest.helpers.compare_strings(
        r'''
        Creating material subpackage 'test_material' ...
            Created test_project/materials/test_material/
        '''.replace('/', os.path.sep),
        string_io.getvalue(),
        )


def test_success(cli_paths):
    string_io = io.StringIO()
    pytest.helpers.create_cli_project(cli_paths.test_directory_path)
    script = supriya.cli.ManageMaterialScript()
    command = ['--new', 'test_material']
    with uqbar.io.RedirectedStreams(stdout=string_io):
        with uqbar.io.DirectoryChange(cli_paths.inner_project_path):
            try:
                script(command)
            except SystemExit:
                raise RuntimeError('SystemExit')
    pytest.helpers.compare_strings(
        r'''
        Creating material subpackage 'test_material' ...
            Created test_project/materials/test_material/
        '''.replace('/', os.path.sep),
        string_io.getvalue(),
        )
    assert cli_paths.materials_path.joinpath('test_material').exists()
    pytest.helpers.compare_path_contents(
        cli_paths.materials_path,
        expected_files,
        cli_paths.test_directory_path,
        )
    definition_path = cli_paths.materials_path.joinpath(
        'test_material', 'definition.py')
    with definition_path.open() as file_pointer:
        actual_contents = uqbar.strings.normalize(file_pointer.read())
    expected_contents = uqbar.strings.normalize('''
    import supriya
    from test_project import project_settings


    material = supriya.Session.from_project_settings(project_settings)

    with supriya.synthdefs.SynthDefBuilder(
        duration=1.,
        out_bus=0,
        ) as builder:
        source = supriya.ugens.Line.ar(
            duration=builder['duration'],
            )
        supriya.ugens.Out.ar(
            bus=builder['out_bus'],
            source=[source] * len(material.audio_output_bus_group),
            )
    ramp_synthdef = builder.build()

    with material.at(0):
        material.add_synth(
            duration=1,
            synthdef=ramp_synthdef,
            )
    ''')
    assert actual_contents == expected_contents
