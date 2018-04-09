import os
import uqbar.io
from supriya import systemtools
from supriya.tools import commandlinetools
from commandlinetools_testbase import ProjectPackageScriptTestCase


class Test(ProjectPackageScriptTestCase):

    expected_files = [
        'test_project/test_project/__init__.py',
        'test_project/test_project/assets/.gitignore',
        'test_project/test_project/distribution/.gitignore',
        'test_project/test_project/etc/.gitignore',
        'test_project/test_project/materials/.gitignore',
        'test_project/test_project/materials/__init__.py',
        'test_project/test_project/project-settings.yml',
        'test_project/test_project/renders/.gitignore',
        'test_project/test_project/sessions/.gitignore',
        'test_project/test_project/sessions/__init__.py',
        'test_project/test_project/synthdefs/.gitignore',
        'test_project/test_project/synthdefs/__init__.py',
        'test_project/test_project/test/.gitignore',
        'test_project/test_project/tools/.gitignore',
        'test_project/test_project/tools/__init__.py',
        ]

    def test_missing(self):
        self.create_project()
        script = commandlinetools.ManageMaterialScript()
        command = ['--delete', 'test_material']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with uqbar.io.DirectoryChange(
                str(self.inner_project_path)):
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
                assert context_manager.exception.code == 1
        self.compare_captured_output(r'''
        Deleting material subpackage 'test_material' ...
            Subpackage test_project/materials/test_material/ does not exist!
        '''.replace('/', os.path.sep))

    def test_success(self):
        self.create_project()
        self.create_material('test_material')
        script = commandlinetools.ManageMaterialScript()
        command = ['--delete', 'test_material']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with uqbar.io.DirectoryChange(
                str(self.inner_project_path)):
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')
        self.compare_captured_output(r'''
        Deleting material subpackage 'test_material' ...
            Deleted test_project/materials/test_material/
        '''.replace('/', os.path.sep))
        self.compare_path_contents(
            self.inner_project_path,
            self.expected_files,
            )
