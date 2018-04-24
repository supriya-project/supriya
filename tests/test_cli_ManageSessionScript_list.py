import io
import pytest
import supriya.cli
import uqbar.io
from cli_testbase import ProjectPackageScriptTestCase


class Test(ProjectPackageScriptTestCase):

    def test_list_sessions(self):
        string_io = io.StringIO()
        pytest.helpers.create_cli_project(self.test_path)
        pytest.helpers.create_cli_session(self.test_path, 'foo')
        pytest.helpers.create_cli_session(self.test_path, 'bar')
        pytest.helpers.create_cli_session(self.test_path, 'baz')
        pytest.helpers.create_cli_session(self.test_path, 'quux')
        script = supriya.cli.ManageSessionScript()
        command = ['--list']
        with uqbar.io.RedirectedStreams(stdout=string_io):
            with uqbar.io.DirectoryChange(
                str(self.inner_project_path)):
                with pytest.raises(SystemExit) as exception_info:
                    script(command)
                assert exception_info.value.code == 1
        pytest.helpers.compare_strings(
            r'''
            Available sessions:
                Session:
                    bar [Session]
                    baz [Session]
                    foo [Session]
                    quux [Session]
            ''',
            string_io.getvalue(),
            )

    def test_list_sessions_no_sessions(self):
        string_io = io.StringIO()
        pytest.helpers.create_cli_project(self.test_path)
        script = supriya.cli.ManageSessionScript()
        command = ['--list']
        with uqbar.io.RedirectedStreams(stdout=string_io):
            with uqbar.io.DirectoryChange(
                str(self.inner_project_path)):
                with pytest.raises(SystemExit) as exception_info:
                    script(command)
                assert exception_info.value.code == 1
        pytest.helpers.compare_strings(
            r'''
            Available sessions:
                No sessions available.
            ''',
            string_io.getvalue(),
            )
