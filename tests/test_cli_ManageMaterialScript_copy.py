import io
import os
import pytest
import supriya.cli
import uqbar.io


expected_files = [
    'test_project/test_project/__init__.py',
    'test_project/test_project/assets/.gitignore',
    'test_project/test_project/distribution/.gitignore',
    'test_project/test_project/etc/.gitignore',
    'test_project/test_project/materials/.gitignore',
    'test_project/test_project/materials/__init__.py',
    'test_project/test_project/materials/material_one/__init__.py',
    'test_project/test_project/materials/material_one/definition.py',
    'test_project/test_project/materials/material_two/__init__.py',
    'test_project/test_project/materials/material_two/definition.py',
    'test_project/test_project/project-settings.yml',
    'test_project/test_project/renders/.gitignore',
    'test_project/test_project/sessions/.gitignore',
    'test_project/test_project/sessions/__init__.py',
    'test_project/test_project/synthdefs/.gitignore',
    'test_project/test_project/synthdefs/__init__.py',
    'test_project/test_project/test/.gitignore',
    'test_project/test_project/tools/.gitignore',
    'test_project/test_project/tools/__init__.py'
    ]


def test_missing_source(cli_paths):
    string_io = io.StringIO()
    pytest.helpers.create_cli_project(cli_paths.test_directory_path)
    script = supriya.cli.ManageMaterialScript()
    command = ['--copy', 'material_one', 'material_two']
    with uqbar.io.RedirectedStreams(stdout=string_io):
        with uqbar.io.DirectoryChange(cli_paths.inner_project_path):
            with pytest.raises(SystemExit) as exception_info:
                script(command)
            assert exception_info.value.code == 1
    pytest.helpers.compare_strings(
        r'''
        Copying material subpackage 'material_one' to 'material_two' ...
            Subpackage test_project/materials/material_one/ does not exist!
        '''.replace('/', os.path.sep),
        string_io.getvalue(),
        )


def test_no_force_replace(cli_paths):
    string_io = io.StringIO()
    pytest.helpers.create_cli_project(cli_paths.test_directory_path)
    pytest.helpers.create_cli_material(
        cli_paths.test_directory_path,
        'material_one',
        )
    pytest.helpers.create_cli_material(
        cli_paths.test_directory_path,
        'material_two',
        )
    script = supriya.cli.ManageMaterialScript()
    command = ['--copy', 'material_one', 'material_two']
    with uqbar.io.RedirectedStreams(stdout=string_io):
        with uqbar.io.DirectoryChange(cli_paths.inner_project_path):
            with pytest.raises(SystemExit) as exception_info:
                script(command)
            assert exception_info.value.code == 1
    pytest.helpers.compare_strings(
        r'''
        Copying material subpackage 'material_one' to 'material_two' ...
            Subpackage test_project/materials/material_two/ exists!
        '''.replace('/', os.path.sep),
        string_io.getvalue(),
        )


def test_force_replace(cli_paths):
    string_io = io.StringIO()
    pytest.helpers.create_cli_project(cli_paths.test_directory_path)
    pytest.helpers.create_cli_material(
        cli_paths.test_directory_path,
        'material_one',
        )
    pytest.helpers.create_cli_material(
        cli_paths.test_directory_path,
        'material_two',
        )
    script = supriya.cli.ManageMaterialScript()
    command = ['--copy', 'material_one', 'material_two', '-f']
    with uqbar.io.RedirectedStreams(stdout=string_io):
        with uqbar.io.DirectoryChange(cli_paths.inner_project_path):
            try:
                script(command)
            except SystemExit:
                raise RuntimeError('SystemExit')
    pytest.helpers.compare_strings(
        r'''
        Copying material subpackage 'material_one' to 'material_two' ...
            Overwriting test_project/materials/material_two/ ...
            Copied test_project/materials/material_one/ to test_project/materials/material_two/
        '''.replace('/', os.path.sep),
        string_io.getvalue(),
        )
    pytest.helpers.compare_path_contents(
        cli_paths.inner_project_path,
        expected_files,
        cli_paths.test_directory_path,
        )


def test_success(cli_paths):
    string_io = io.StringIO()
    pytest.helpers.create_cli_project(cli_paths.test_directory_path)
    pytest.helpers.create_cli_material(
        cli_paths.test_directory_path,
        'material_one',
        )
    script = supriya.cli.ManageMaterialScript()
    command = ['--copy', 'material_one', 'material_two']
    with uqbar.io.RedirectedStreams(stdout=string_io):
        with uqbar.io.DirectoryChange(cli_paths.inner_project_path):
            try:
                script(command)
            except SystemExit:
                raise RuntimeError('SystemExit')
    pytest.helpers.compare_strings(
        r'''
        Copying material subpackage 'material_one' to 'material_two' ...
            Copied test_project/materials/material_one/ to test_project/materials/material_two/
        '''.replace('/', os.path.sep),
        string_io.getvalue(),
        )
    pytest.helpers.compare_path_contents(
        cli_paths.inner_project_path,
        expected_files,
        cli_paths.test_directory_path,
        )
