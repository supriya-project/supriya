import io
import pytest
import supriya.cli
import uqbar.io


def test_clean(cli_paths):
    string_io = io.StringIO()
    pytest.helpers.create_cli_project(cli_paths.test_directory_path)
    pytest.helpers.create_cli_material(
        cli_paths.test_directory_path,
        'material_one',
        definition_contents=pytest.helpers.get_basic_session_template().render(
            output_section_singular='material',
            ),
        )
    pytest.helpers.create_cli_material(
        cli_paths.test_directory_path,
        'material_two',
        definition_contents=pytest.helpers.get_basic_session_template().render(
            multiplier=0.5,
            output_section_singular='material',
            ),
        )
    pytest.helpers.create_cli_material(
        cli_paths.test_directory_path,
        'material_three',
        definition_contents=pytest.helpers.get_basic_session_template().render(
            multiplier=0.25,
            output_section_singular='material',
            ),
        )

    script = supriya.cli.ManageMaterialScript()
    command = ['--render', '*']
    with uqbar.io.DirectoryChange(cli_paths.inner_project_path):
        try:
            script(command)
        except SystemExit as e:
            raise RuntimeError('SystemExit: {}'.format(e.code))

    pytest.helpers.compare_path_contents(
        cli_paths.inner_project_path,
        [
            'test_project/test_project/__init__.py',
            'test_project/test_project/assets/.gitignore',
            'test_project/test_project/distribution/.gitignore',
            'test_project/test_project/etc/.gitignore',
            'test_project/test_project/materials/.gitignore',
            'test_project/test_project/materials/__init__.py',
            'test_project/test_project/materials/material_one/__init__.py',
            'test_project/test_project/materials/material_one/definition.py',
            'test_project/test_project/materials/material_one/render.aiff',
            'test_project/test_project/materials/material_one/render.yml',
            'test_project/test_project/materials/material_three/__init__.py',
            'test_project/test_project/materials/material_three/definition.py',
            'test_project/test_project/materials/material_three/render.aiff',
            'test_project/test_project/materials/material_three/render.yml',
            'test_project/test_project/materials/material_two/__init__.py',
            'test_project/test_project/materials/material_two/definition.py',
            'test_project/test_project/materials/material_two/render.aiff',
            'test_project/test_project/materials/material_two/render.yml',
            'test_project/test_project/project-settings.yml',
            'test_project/test_project/renders/.gitignore',
            'test_project/test_project/renders/session-5ec1eb97cfc0e98291f27464546df568.aiff',
            'test_project/test_project/renders/session-5ec1eb97cfc0e98291f27464546df568.osc',
            'test_project/test_project/renders/session-95cecb2c724619fe502164459560ba5d.aiff',
            'test_project/test_project/renders/session-95cecb2c724619fe502164459560ba5d.osc',
            'test_project/test_project/renders/session-e628a25fe369270f786d60fbbc047365.aiff',
            'test_project/test_project/renders/session-e628a25fe369270f786d60fbbc047365.osc',
            'test_project/test_project/sessions/.gitignore',
            'test_project/test_project/sessions/__init__.py',
            'test_project/test_project/synthdefs/.gitignore',
            'test_project/test_project/synthdefs/__init__.py',
            'test_project/test_project/test/.gitignore',
            'test_project/test_project/tools/.gitignore',
            'test_project/test_project/tools/__init__.py'
            ],
        cli_paths.test_directory_path,
        )

    script = supriya.cli.ManageProjectScript()
    command = ['--clean']
    with uqbar.io.RedirectedStreams(stdout=string_io), \
        uqbar.io.DirectoryChange(cli_paths.inner_project_path):
        try:
            script(command)
        except SystemExit as e:
            raise RuntimeError('SystemExit: {}'.format(e.code))

    pytest.helpers.compare_path_contents(
        cli_paths.inner_project_path,
        [
            'test_project/test_project/__init__.py',
            'test_project/test_project/assets/.gitignore',
            'test_project/test_project/distribution/.gitignore',
            'test_project/test_project/etc/.gitignore',
            'test_project/test_project/materials/.gitignore',
            'test_project/test_project/materials/__init__.py',
            'test_project/test_project/materials/material_one/__init__.py',
            'test_project/test_project/materials/material_one/definition.py',
            'test_project/test_project/materials/material_one/render.aiff',
            'test_project/test_project/materials/material_one/render.yml',
            'test_project/test_project/materials/material_three/__init__.py',
            'test_project/test_project/materials/material_three/definition.py',
            'test_project/test_project/materials/material_three/render.aiff',
            'test_project/test_project/materials/material_three/render.yml',
            'test_project/test_project/materials/material_two/__init__.py',
            'test_project/test_project/materials/material_two/definition.py',
            'test_project/test_project/materials/material_two/render.aiff',
            'test_project/test_project/materials/material_two/render.yml',
            'test_project/test_project/project-settings.yml',
            'test_project/test_project/renders/.gitignore',
            'test_project/test_project/sessions/.gitignore',
            'test_project/test_project/sessions/__init__.py',
            'test_project/test_project/synthdefs/.gitignore',
            'test_project/test_project/synthdefs/__init__.py',
            'test_project/test_project/test/.gitignore',
            'test_project/test_project/tools/.gitignore',
            'test_project/test_project/tools/__init__.py'
            ],
        cli_paths.test_directory_path,
        )

    pytest.helpers.compare_strings(
        r'''
        Cleaning test_project/renders ...
            Cleaned test_project/renders/session-5ec1eb97cfc0e98291f27464546df568.aiff
            Cleaned test_project/renders/session-5ec1eb97cfc0e98291f27464546df568.osc
            Cleaned test_project/renders/session-95cecb2c724619fe502164459560ba5d.aiff
            Cleaned test_project/renders/session-95cecb2c724619fe502164459560ba5d.osc
            Cleaned test_project/renders/session-e628a25fe369270f786d60fbbc047365.aiff
            Cleaned test_project/renders/session-e628a25fe369270f786d60fbbc047365.osc
        ''',
        string_io.getvalue(),
        )
