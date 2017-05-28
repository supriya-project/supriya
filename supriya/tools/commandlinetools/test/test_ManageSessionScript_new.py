# -*- encoding: utf-8 -*-
import os
from abjad.tools import systemtools
from supriya.tools import commandlinetools
from commandlinetools_testbase import ProjectPackageScriptTestCase


class Test(ProjectPackageScriptTestCase):

    expected_files = [
        'test_project/test_project/sessions/.gitignore',
        'test_project/test_project/sessions/__init__.py',
        'test_project/test_project/sessions/test_session/__init__.py',
        'test_project/test_project/sessions/test_session/definition.py',
        ]

    def test_exists(self):
        self.create_project()
        self.create_session('test_session')
        with systemtools.RedirectedStreams(stdout=self.string_io):
            self.create_session('test_session', expect_error=True)
        self.compare_captured_output(r'''
            Creating session subpackage 'test_session' ...
                Path exists: test_project/sessions/test_session
        '''.replace('/', os.path.sep))

    def test_force_replace(self):
        self.create_project()
        self.create_session('test_session')
        with systemtools.RedirectedStreams(stdout=self.string_io):
            self.create_session('test_session', force=True)
        self.compare_captured_output(r'''
            Creating session subpackage 'test_session' ...
                Created test_project/sessions/test_session/
        '''.replace('/', os.path.sep))

    def test_internal_path(self):
        self.create_project()
        script = commandlinetools.ManageSessionScript()
        command = ['--new', 'test_session']
        internal_path = self.assets_path
        assert internal_path.exists()
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(str(internal_path)):
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')
        self.compare_captured_output(r'''
            Creating session subpackage 'test_session' ...
                Created test_project/sessions/test_session/
        '''.replace('/', os.path.sep))

    def test_success(self):
        self.create_project()
        script = commandlinetools.ManageSessionScript()
        command = ['--new', 'test_session']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(
                str(self.inner_project_path)):
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')
        self.compare_captured_output(r'''
            Creating session subpackage 'test_session' ...
                Created test_project/sessions/test_session/
        '''.replace('/', os.path.sep))
        assert self.sessions_path.joinpath('test_session').exists()
        self.compare_path_contents(self.sessions_path, self.expected_files)
        definition_path = self.sessions_path.joinpath(
            'test_session', 'definition.py')
        self.compare_file_contents(definition_path, '''
        # -*- encoding: utf-8 -*-
        import supriya
        from test_project import project_settings


        session = supriya.Session.from_project_settings(project_settings)

        with supriya.synthdeftools.SynthDefBuilder(
            duration=1.,
            out_bus=0,
            ) as builder:
            source = supriya.ugentools.Line.ar(
                duration=builder['duration'],
                )
            supriya.ugentools.Out.ar(
                bus=builder['out_bus'],
                source=[source] * len(session.audio_output_bus_group),
                )
        ramp_synthdef = builder.build()

        with session.at(0):
            session.add_synth(
                duration=1,
                synthdef=ramp_synthdef,
                )
        ''')
