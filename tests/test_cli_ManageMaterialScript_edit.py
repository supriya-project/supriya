import supriya.cli
import uqbar.io
from cli_testbase import ProjectPackageScriptTestCase
from unittest import mock


class Test(ProjectPackageScriptTestCase):

    @mock.patch('supriya.cli.ProjectPackageScript._call_subprocess')
    def test_success(self, call_subprocess_mock):
        call_subprocess_mock.return_value = 0
        self.create_project()
        material_path = self.create_material('test_material')
        script = supriya.cli.ManageMaterialScript()
        command = ['--edit', 'test_material']
        with uqbar.io.RedirectedStreams(stdout=self.string_io):
            with uqbar.io.DirectoryChange(
                str(self.inner_project_path)):
                try:
                    script(command)
                except SystemExit as e:
                    raise RuntimeError('SystemExit: {}'.format(e.code))
        self.compare_captured_output(r'''
        Edit candidates: 'test_material' ...
        ''')
        definition_path = material_path.joinpath('definition.py')
        command = '{} {!s}'.format(
            supriya.config.get('core', 'editor', fallback='vim'),
            definition_path,
            )
        call_subprocess_mock.assert_called_with(command)
