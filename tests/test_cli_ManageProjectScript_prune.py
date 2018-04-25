import io
import pytest
import shutil
import supriya.cli
import uqbar.io


def test_prune(cli_paths):
    string_io = io.StringIO()
    pytest.helpers.create_cli_project(cli_paths.test_directory_path)
    pytest.helpers.create_cli_material(cli_paths.test_directory_path, 'material_one')
    pytest.helpers.create_cli_material(
        cli_paths.test_directory_path,
        'material_two',
        definition_contents=pytest.helpers.get_chained_session_template().render(
            input_name='material_one',
            input_section_singular='material',
            output_section_singular='material',
            multiplier=0.5,
            ),
        )
    pytest.helpers.create_cli_material(
        cli_paths.test_directory_path,
        'material_three',
        definition_contents=pytest.helpers.get_chained_session_template().render(
            input_name='material_two',
            input_section_singular='material',
            output_section_singular='material',
            multiplier=-1.0,
            ),
        )
    material_four_path = pytest.helpers.create_cli_material(
        cli_paths.test_directory_path,
        'material_four',
        definition_contents=pytest.helpers.get_chained_session_template().render(
            input_name='material_two',
            input_section_singular='material',
            output_section_singular='material',
            multiplier=0.125,
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
            'test_project/test_project/materials/material_four/__init__.py',
            'test_project/test_project/materials/material_four/definition.py',
            'test_project/test_project/materials/material_four/render.aiff',
            'test_project/test_project/materials/material_four/render.yml',
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
            'test_project/test_project/renders/session-1e762e78499929b13e1e74bba37431bc.aiff',
            'test_project/test_project/renders/session-1e762e78499929b13e1e74bba37431bc.osc',
            'test_project/test_project/renders/session-1fa53239afd7268cce27ff05fad76c18.aiff',
            'test_project/test_project/renders/session-1fa53239afd7268cce27ff05fad76c18.osc',
            'test_project/test_project/renders/session-95cecb2c724619fe502164459560ba5d.aiff',
            'test_project/test_project/renders/session-95cecb2c724619fe502164459560ba5d.osc',
            'test_project/test_project/renders/session-ba9c6a9479347975eec14a68dd2f4288.aiff',
            'test_project/test_project/renders/session-ba9c6a9479347975eec14a68dd2f4288.osc',
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

    shutil.rmtree(material_four_path)

    script = supriya.cli.ManageProjectScript()
    command = ['--prune']
    with uqbar.io.RedirectedStreams(stdout=string_io):
        with uqbar.io.DirectoryChange(cli_paths.inner_project_path):
            try:
                script(command)
            except SystemExit as e:
                raise RuntimeError('SystemExit: {}'.format(e.code))

    pytest.helpers.compare_strings(
        r'''
        Pruning test_project/renders ...
            Pruned test_project/renders/session-1fa53239afd7268cce27ff05fad76c18.aiff
            Pruned test_project/renders/session-1fa53239afd7268cce27ff05fad76c18.osc
        ''',
        string_io.getvalue(),
        )

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
            'test_project/test_project/renders/session-1e762e78499929b13e1e74bba37431bc.aiff',
            'test_project/test_project/renders/session-1e762e78499929b13e1e74bba37431bc.osc',
            'test_project/test_project/renders/session-95cecb2c724619fe502164459560ba5d.aiff',
            'test_project/test_project/renders/session-95cecb2c724619fe502164459560ba5d.osc',
            'test_project/test_project/renders/session-ba9c6a9479347975eec14a68dd2f4288.aiff',
            'test_project/test_project/renders/session-ba9c6a9479347975eec14a68dd2f4288.osc',
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
