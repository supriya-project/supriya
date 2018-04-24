import pytest
import supriya
import supriya.cli
import uqbar.io
from cli_testbase import ProjectPackageScriptTestCase
from unittest import mock


class Test(ProjectPackageScriptTestCase):

    @mock.patch('supriya.cli.ProjectPackageScript._call_subprocess')
    def test_success(self, call_subprocess_mock):
        call_subprocess_mock.return_value = 0
        pytest.helpers.create_cli_project(self.test_path)
        session_path = pytest.helpers.create_cli_session(self.test_path, 'test_session')
        script = supriya.cli.ManageSessionScript()
        command = ['--edit', 'test_session']
        with uqbar.io.RedirectedStreams(stdout=self.string_io):
            with uqbar.io.DirectoryChange(
                str(self.inner_project_path)):
                try:
                    script(command)
                except SystemExit as e:
                    raise RuntimeError('SystemExit: {}'.format(e.code))
        pytest.helpers.compare_strings(
            r'''
            Edit candidates: 'test_session' ...
            ''',
            self.string_io.getvalue(),
            )
        definition_path = session_path.joinpath('definition.py')
        command = '{} {!s}'.format(
            supriya.config.get('core', 'editor', fallback='vim'),
            definition_path,
            )
        call_subprocess_mock.assert_called_with(command)
