import io
import os
import pytest
import uqbar.io
import uqbar.strings
from cli_testbase import ProjectPackageScriptTestCase


expected_files = [
    'test_project/.gitignore',
    'test_project/README.md',
    'test_project/requirements.txt',
    'test_project/setup.cfg',
    'test_project/setup.py',
    'test_project/test_project/__init__.py',
    'test_project/test_project/assets/.gitignore',
    'test_project/test_project/distribution/.gitignore',
    'test_project/test_project/etc/.gitignore',
    'test_project/test_project/materials/.gitignore',
    'test_project/test_project/materials/__init__.py',
    'test_project/test_project/project-settings.yml',
    'test_project/test_project/renders/.gitignore',
    'test_project/test_project/sessions/.gitignore',
    'test_project/test_project/sessions/__init__.py',
    'test_project/test_project/synthdefs/.gitignore',
    'test_project/test_project/synthdefs/__init__.py',
    'test_project/test_project/test/.gitignore',
    'test_project/test_project/tools/.gitignore',
    'test_project/test_project/tools/__init__.py',
    ]


expected_readme_contents = uqbar.strings.normalize('''
    TEST PROJECT
    ############
    ''')


expected_project_settings_contents = uqbar.strings.normalize('''
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


class Test(ProjectPackageScriptTestCase):

    def test_exists(self):
        string_io = io.StringIO()
        with uqbar.io.RedirectedStreams(stdout=string_io):
            pytest.helpers.create_cli_project(self.test_path)
        assert self.outer_project_path.exists()
        with uqbar.io.RedirectedStreams(stdout=string_io):
            pytest.helpers.create_cli_project(self.test_path, expect_error=True)
        assert self.outer_project_path.exists()
        pytest.helpers.compare_strings(
            r'''
            Creating project package 'Test Project'...
                Created test_project/
            Creating project package 'Test Project'...
                Directory test_project already exists.
            '''.replace('/', os.path.sep),
            string_io.getvalue(),
            )

    def test_force_replace(self):
        string_io = io.StringIO()
        with uqbar.io.RedirectedStreams(stdout=string_io):
            pytest.helpers.create_cli_project(self.test_path)
        assert self.outer_project_path.exists()
        with uqbar.io.RedirectedStreams(stdout=string_io):
            pytest.helpers.create_cli_project(self.test_path, force=True)
        assert self.outer_project_path.exists()
        pytest.helpers.compare_strings(
            r'''
            Creating project package 'Test Project'...
                Created test_project/
            Creating project package 'Test Project'...
                Created test_project/
            '''.replace('/', os.path.sep),
            string_io.getvalue(),
            )

    def test_success(self):
        string_io = io.StringIO()
        with uqbar.io.RedirectedStreams(stdout=string_io):
            pytest.helpers.create_cli_project(self.test_path)
        assert self.outer_project_path.exists()
        pytest.helpers.compare_path_contents(
            self.outer_project_path,
            expected_files,
            self.test_path,
            )
        pytest.helpers.compare_strings(
            r'''
            Creating project package 'Test Project'...
                Created test_project/
            '''.replace('/', os.path.sep),
            string_io.getvalue(),
            )

        readme_path = self.outer_project_path.joinpath('README.md')
        with readme_path.open() as file_pointer:
            actual_readme_contents = uqbar.strings.normalize(
                file_pointer.read())
        assert expected_readme_contents == actual_readme_contents

        project_settings_path = self.inner_project_path.joinpath(
            'project-settings.yml')
        with project_settings_path.open() as file_pointer:
            actual_project_settings_contents = uqbar.strings.normalize(
                file_pointer.read())
        assert expected_project_settings_contents == \
            actual_project_settings_contents
