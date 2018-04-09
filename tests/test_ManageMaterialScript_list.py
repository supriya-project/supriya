import uqbar.io
from supriya.tools import commandlinetools
from commandlinetools_testbase import ProjectPackageScriptTestCase


class Test(ProjectPackageScriptTestCase):

    def test_list_materials(self):
        self.create_project()
        self.create_material('foo')
        self.create_material('bar')
        self.create_material('baz')
        self.create_material('quux')
        script = commandlinetools.ManageMaterialScript()
        command = ['--list']
        with uqbar.io.RedirectedStreams(stdout=self.string_io):
            with uqbar.io.DirectoryChange(
                str(self.inner_project_path)):
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
                assert context_manager.exception.code == 1
        self.compare_captured_output(r'''
        Available materials:
            Session:
                bar [Session]
                baz [Session]
                foo [Session]
                quux [Session]
        ''')

    def test_list_materials_no_materials(self):
        self.create_project()
        script = commandlinetools.ManageMaterialScript()
        command = ['--list']
        with uqbar.io.RedirectedStreams(stdout=self.string_io):
            with uqbar.io.DirectoryChange(
                str(self.inner_project_path)):
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
                assert context_manager.exception.code == 1
        self.compare_captured_output(r'''
        Available materials:
            No materials available.
        ''')
