import uqbar.io
from supriya.tools import commandlinetools
from commandlinetools_testbase import ProjectPackageScriptTestCase


class Test(ProjectPackageScriptTestCase):

    def test_list_sessions(self):
        self.create_project()
        self.create_session('foo')
        self.create_session('bar')
        self.create_session('baz')
        self.create_session('quux')
        script = commandlinetools.ManageSessionScript()
        command = ['--list']
        with uqbar.io.RedirectedStreams(stdout=self.string_io):
            with uqbar.io.DirectoryChange(
                str(self.inner_project_path)):
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
                assert context_manager.exception.code == 1
        self.compare_captured_output(r'''
        Available sessions:
            Session:
                bar [Session]
                baz [Session]
                foo [Session]
                quux [Session]
        ''')

    def test_list_sessions_no_sessions(self):
        self.create_project()
        script = commandlinetools.ManageSessionScript()
        command = ['--list']
        with uqbar.io.RedirectedStreams(stdout=self.string_io):
            with uqbar.io.DirectoryChange(
                str(self.inner_project_path)):
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
                assert context_manager.exception.code == 1
        self.compare_captured_output(r'''
        Available sessions:
            No sessions available.
        ''')
