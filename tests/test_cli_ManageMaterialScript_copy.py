import os
import uqbar.io
import supriya.cli
from cli_testbase import ProjectPackageScriptTestCase


class Test(ProjectPackageScriptTestCase):

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

    def test_missing_source(self):
        self.create_project()
        script = supriya.cli.ManageMaterialScript()
        command = ['--copy', 'material_one', 'material_two']
        with uqbar.io.RedirectedStreams(stdout=self.string_io):
            with uqbar.io.DirectoryChange(
                str(self.inner_project_path)):
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
                assert context_manager.exception.code == 1
        self.compare_captured_output(r'''
        Copying material subpackage 'material_one' to 'material_two' ...
            Subpackage test_project/materials/material_one/ does not exist!
        '''.replace('/', os.path.sep))

    def test_no_force_replace(self):
        self.create_project()
        self.create_material('material_one')
        self.create_material('material_two')
        script = supriya.cli.ManageMaterialScript()
        command = ['--copy', 'material_one', 'material_two']
        with uqbar.io.RedirectedStreams(stdout=self.string_io):
            with uqbar.io.DirectoryChange(
                str(self.inner_project_path)):
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
                assert context_manager.exception.code == 1
        self.compare_captured_output(r'''
        Copying material subpackage 'material_one' to 'material_two' ...
            Subpackage test_project/materials/material_two/ exists!
        '''.replace('/', os.path.sep))

    def test_force_replace(self):
        self.create_project()
        self.create_material('material_one')
        self.create_material('material_two')
        script = supriya.cli.ManageMaterialScript()
        command = ['--copy', 'material_one', 'material_two', '-f']
        with uqbar.io.RedirectedStreams(stdout=self.string_io):
            with uqbar.io.DirectoryChange(
                str(self.inner_project_path)):
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')
        self.compare_captured_output(r'''
        Copying material subpackage 'material_one' to 'material_two' ...
            Overwriting test_project/materials/material_two/ ...
            Copied test_project/materials/material_one/ to test_project/materials/material_two/
        '''.replace('/', os.path.sep))
        self.compare_path_contents(
            self.inner_project_path,
            self.expected_files,
            )

    def test_success(self):
        self.create_project()
        self.create_material('material_one')
        script = supriya.cli.ManageMaterialScript()
        command = ['--copy', 'material_one', 'material_two']
        with uqbar.io.RedirectedStreams(stdout=self.string_io):
            with uqbar.io.DirectoryChange(
                str(self.inner_project_path)):
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')
        self.compare_captured_output(r'''
        Copying material subpackage 'material_one' to 'material_two' ...
            Copied test_project/materials/material_one/ to test_project/materials/material_two/
        '''.replace('/', os.path.sep))
        self.compare_path_contents(
            self.inner_project_path,
            self.expected_files,
            )
