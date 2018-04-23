import pytest
import supriya.cli
import uqbar.io
from cli_testbase import ProjectPackageScriptTestCase


class Test(ProjectPackageScriptTestCase):

    def test_list_materials(self):
        pytest.helpers.create_cli_project(self.test_path)
        self.create_material('foo')
        self.create_material('bar')
        self.create_material('baz')
        self.create_material('quux')
        script = supriya.cli.ManageMaterialScript()
        command = ['--list']
        with uqbar.io.RedirectedStreams(stdout=self.string_io):
            with uqbar.io.DirectoryChange(
                str(self.inner_project_path)):
                with pytest.raises(SystemExit) as exception_info:
                    script(command)
                assert exception_info.value.code == 1
        self.compare_captured_output(r'''
        Available materials:
            Session:
                bar [Session]
                baz [Session]
                foo [Session]
                quux [Session]
        ''')

    def test_list_materials_no_materials(self):
        pytest.helpers.create_cli_project(self.test_path)
        script = supriya.cli.ManageMaterialScript()
        command = ['--list']
        with uqbar.io.RedirectedStreams(stdout=self.string_io):
            with uqbar.io.DirectoryChange(
                str(self.inner_project_path)):
                with pytest.raises(SystemExit) as exception_info:
                    script(command)
                assert exception_info.value.code == 1
        self.compare_captured_output(r'''
        Available materials:
            No materials available.
        ''')
