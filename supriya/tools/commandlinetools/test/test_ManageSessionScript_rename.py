# -*- encoding: utf-8 -*-
import os
from abjad.tools import systemtools
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
        'test_project/test_project/metadata.json',
        'test_project/test_project/project-settings.yml',
        'test_project/test_project/renders/.gitignore',
        'test_project/test_project/sessions/.gitignore',
        'test_project/test_project/sessions/__init__.py',
        'test_project/test_project/sessions/session_two/__init__.py',
        'test_project/test_project/sessions/session_two/definition.py',
        'test_project/test_project/synthdefs/.gitignore',
        'test_project/test_project/synthdefs/__init__.py',
        'test_project/test_project/test/.gitignore',
        'test_project/test_project/tools/.gitignore',
        'test_project/test_project/tools/__init__.py'
        ]

    def test_missing_source(self):
        self.create_project()
        script = commandlinetools.ManageSessionScript()
        command = ['--rename', 'session_one', 'session_two']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(
                str(self.inner_project_path)):
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
                assert context_manager.exception.code == 1
        self.compare_captured_output(r'''
        Renaming session subpackage 'session_one' to 'session_two' ...
            Subpackage test_project/sessions/session_one/ does not exist!
        '''.replace('/', os.path.sep))

    def test_no_force_replace(self):
        self.create_project()
        self.create_session('session_one')
        self.create_session('session_two')
        script = commandlinetools.ManageSessionScript()
        command = ['--rename', 'session_one', 'session_two']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(
                str(self.inner_project_path)):
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
                assert context_manager.exception.code == 1
        self.compare_captured_output(r'''
        Renaming session subpackage 'session_one' to 'session_two' ...
            Subpackage test_project/sessions/session_two/ exists!
        '''.replace('/', os.path.sep))

    def test_force_replace(self):
        self.create_project()
        self.create_session('session_one')
        self.create_session('session_two')
        script = commandlinetools.ManageSessionScript()
        command = ['--rename', 'session_one', 'session_two', '-f']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(
                str(self.inner_project_path)):
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')
        self.compare_captured_output(r'''
        Renaming session subpackage 'session_one' to 'session_two' ...
            Overwriting test_project/sessions/session_two/ ...
            Renamed test_project/sessions/session_one/ to test_project/sessions/session_two/
        '''.replace('/', os.path.sep))
        self.compare_path_contents(
            self.inner_project_path,
            self.expected_files,
            )

    def test_success(self):
        self.create_project()
        self.create_session('session_one')
        script = commandlinetools.ManageSessionScript()
        command = ['--rename', 'session_one', 'session_two']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(
                str(self.inner_project_path)):
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')
        self.compare_captured_output(r'''
        Renaming session subpackage 'session_one' to 'session_two' ...
            Renamed test_project/sessions/session_one/ to test_project/sessions/session_two/
        '''.replace('/', os.path.sep))
        self.compare_path_contents(
            self.inner_project_path,
            self.expected_files,
            )
