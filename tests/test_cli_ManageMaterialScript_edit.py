import pytest
import supriya.cli
import uqbar.io
from cli_testbase import ProjectPackageScriptTestCase
from unittest import mock


class Test(ProjectPackageScriptTestCase):

    @mock.patch('supriya.cli.ProjectPackageScript._call_subprocess')
    def test_success(self, call_subprocess_mock):
        call_subprocess_mock.return_value = 0
        pytest.helpers.create_cli_project(self.test_path)
        material_path = pytest.helpers.create_cli_material(self.test_path, 'test_material')
        script = supriya.cli.ManageMaterialScript()
        command = ['--edit', 'test_material']
        with uqbar.io.RedirectedStreams(stdout=self.string_io):
            with uqbar.io.DirectoryChange(
                str(self.inner_project_path)):
                try:
                    script(command)
                except SystemExit as e:
                    raise RuntimeError('SystemExit: {}'.format(e.code))
        pytest.helpers.compare_strings(
            r'''
            Edit candidates: 'test_material' ...
            ''',
            self.string_io.getvalue(),
            )
        definition_path = material_path.joinpath('definition.py')
        command = '{} {!s}'.format(
            supriya.config.get('core', 'editor', fallback='vim'),
            definition_path,
            )
        call_subprocess_mock.assert_called_with(command)
