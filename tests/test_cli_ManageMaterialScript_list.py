import io
import pytest
import supriya.cli
import uqbar.io
from cli_testbase import ProjectPackageScriptTestCase


class Test(ProjectPackageScriptTestCase):

    def test_list_materials(self):
        string_io = io.StringIO()
        pytest.helpers.create_cli_project(self.test_path)
        pytest.helpers.create_cli_material(self.test_path, 'foo')
        pytest.helpers.create_cli_material(self.test_path, 'bar')
        pytest.helpers.create_cli_material(self.test_path, 'baz')
        pytest.helpers.create_cli_material(self.test_path, 'quux')
        script = supriya.cli.ManageMaterialScript()
        command = ['--list']
        with uqbar.io.RedirectedStreams(stdout=string_io):
            with uqbar.io.DirectoryChange(
                str(self.inner_project_path)):
                with pytest.raises(SystemExit) as exception_info:
                    script(command)
                assert exception_info.value.code == 1
        pytest.helpers.compare_strings(
            r'''
            Available materials:
                Session:
                    bar [Session]
                    baz [Session]
                    foo [Session]
                    quux [Session]
            ''',
            string_io.getvalue(),
            )

    def test_list_materials_no_materials(self):
        string_io = io.StringIO()
        pytest.helpers.create_cli_project(self.test_path)
        script = supriya.cli.ManageMaterialScript()
        command = ['--list']
        with uqbar.io.RedirectedStreams(stdout=string_io):
            with uqbar.io.DirectoryChange(
                str(self.inner_project_path)):
                with pytest.raises(SystemExit) as exception_info:
                    script(command)
                assert exception_info.value.code == 1
        pytest.helpers.compare_strings(
            r'''
            Available materials:
                No materials available.
            ''',
            string_io.getvalue(),
            )
