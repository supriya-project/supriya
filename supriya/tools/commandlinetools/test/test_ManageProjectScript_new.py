# -*- encoding: utf-8 -*-
import json
import os
from abjad.tools import stringtools
from abjad.tools import systemtools
from commandlinetools_testbase import ProjectPackageScriptTestCase


class Test(ProjectPackageScriptTestCase):

    expected_files = [
        'test_project/.gitignore',
        'test_project/README.md',
        'test_project/requirements.txt',
        'test_project/setup.cfg',
        'test_project/setup.py',
        'test_project/test_project/__init__.py',
        'test_project/test_project/assets/.gitignore',
        'test_project/test_project/composites/.gitignore',
        'test_project/test_project/composites/__init__.py',
        'test_project/test_project/distribution/.gitignore',
        'test_project/test_project/etc/.gitignore',
        'test_project/test_project/materials/.gitignore',
        'test_project/test_project/materials/__init__.py',
        'test_project/test_project/metadata.json',
        'test_project/test_project/project-settings.yml',
        'test_project/test_project/renders/.gitignore',
        'test_project/test_project/synthdefs/.gitignore',
        'test_project/test_project/synthdefs/__init__.py',
        'test_project/test_project/test/.gitignore',
        'test_project/test_project/tools/.gitignore',
        'test_project/test_project/tools/__init__.py',
        ]

    expected_readme_contents = stringtools.normalize('''
    TEST PROJECT
    ############
    ''')

    expected_project_settings_contents = stringtools.normalize('''
    composer:
        email: josiah.oberholtzer@gmail.com
        github: josiah-wolf-oberholtzer
        library: amazing_library
        name: Josiah Wolf Oberholtzer
        website: www.josiahwolfoberholtzer.com
    server_options:
        audio_bus_channel_count: 128
        block_size: 64
        buffer_count: 1024
        control_bus_channel_count: 4096
        hardware_buffer_size: null
        initial_node_id: 1000
        input_bus_channel_count: 8
        input_device: null
        input_stream_mask: false
        load_synthdefs: true
        maximum_node_count: 1024
        maximum_synthdef_count: 1024
        memory_locking: false
        memory_size: 8192
        output_bus_channel_count: 8
        output_device: null
        output_stream_mask: false
        protocol: udp
        random_number_generator_count: 64
        remote_control_volume: false
        restricted_path: null
        sample_rate: null
        verbosity: 0
        wire_buffer_count: 64
        zero_configuration: false
    title: Test Project
    ''')

    def test_exists(self):
        with systemtools.RedirectedStreams(stdout=self.string_io):
            self.create_project()
        assert self.outer_project_path.exists()
        with systemtools.RedirectedStreams(stdout=self.string_io):
            self.create_project(expect_error=True)
        assert self.outer_project_path.exists()
        self.compare_captured_output(r'''
            Creating project package 'Test Project'...
                Writing test_project/metadata.json
                Created test_project/
            Creating project package 'Test Project'...
                Directory test_project already exists.
        '''.replace('/', os.path.sep))

    def test_force_replace(self):
        with systemtools.RedirectedStreams(stdout=self.string_io):
            self.create_project()
        assert self.outer_project_path.exists()
        with systemtools.RedirectedStreams(stdout=self.string_io):
            self.create_project(force=True)
        assert self.outer_project_path.exists()
        self.compare_captured_output(r'''
            Creating project package 'Test Project'...
                Writing test_project/metadata.json
                Created test_project/
            Creating project package 'Test Project'...
                Writing test_project/metadata.json
                Created test_project/
        '''.replace('/', os.path.sep))

    def test_success(self):
        with systemtools.RedirectedStreams(stdout=self.string_io):
            self.create_project()
        assert self.outer_project_path.exists()
        self.compare_path_contents(
            self.outer_project_path,
            self.expected_files,
            )
        project_metadata_path = self.inner_project_path.joinpath('metadata.json')
        assert project_metadata_path.exists()
        with open(str(project_metadata_path), 'r') as file_pointer:
            metadata = json.loads(file_pointer.read())
        assert metadata == {
            'composer_email': 'josiah.oberholtzer@gmail.com',
            'composer_github': 'josiah-wolf-oberholtzer',
            'composer_library': 'amazing_library',
            'composer_name': 'Josiah Wolf Oberholtzer',
            'composer_website': 'www.josiahwolfoberholtzer.com',
            'title': 'Test Project',
            }
        self.compare_captured_output(r'''
            Creating project package 'Test Project'...
                Writing test_project/metadata.json
                Created test_project/
        '''.replace('/', os.path.sep))
        self.compare_file_contents(
            self.outer_project_path.joinpath('README.md'),
            self.expected_readme_contents,
            )
        self.compare_file_contents(
            self.inner_project_path.joinpath('project-settings.yml'),
            self.expected_project_settings_contents
            )
