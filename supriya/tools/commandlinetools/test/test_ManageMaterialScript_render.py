# -*- encoding: utf-8 -*-
import os
from unittest import mock
from abjad.tools import stringtools
from abjad.tools import systemtools
from supriya.tools import commandlinetools
from supriya.tools import nonrealtimetools
from base import ProjectPackageScriptTestCase


class Test(ProjectPackageScriptTestCase):

    expected_files = [
        'test_project/test_project/__init__.py',
        'test_project/test_project/assets/.gitignore',
        'test_project/test_project/composites/.gitignore',
        'test_project/test_project/composites/__init__.py',
        'test_project/test_project/distribution/.gitignore',
        'test_project/test_project/etc/.gitignore',
        'test_project/test_project/materials/.gitignore',
        'test_project/test_project/materials/__init__.py',
        'test_project/test_project/materials/test_material/__init__.py',
        'test_project/test_project/materials/test_material/definition.py',
        'test_project/test_project/materials/test_material/render.aiff',
        'test_project/test_project/metadata.json',
        'test_project/test_project/project-settings.yml',
        'test_project/test_project/renders/.gitignore',
        'test_project/test_project/renders/95cecb2c724619fe502164459560ba5d.aiff',
        'test_project/test_project/renders/95cecb2c724619fe502164459560ba5d.osc',
        'test_project/test_project/renders/render.yml',
        'test_project/test_project/synthdefs/.gitignore',
        'test_project/test_project/synthdefs/__init__.py',
        'test_project/test_project/test/.gitignore',
        'test_project/test_project/tools/.gitignore',
        'test_project/test_project/tools/__init__.py',
        ]

    def test_missing_material(self):
        """
        Handle missing material.
        """
        self.create_project()
        script = commandlinetools.ManageMaterialScript()
        command = ['--render', 'test_material']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(
                str(self.inner_project_path)):
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
                assert context_manager.exception.code == 1
        self.compare_captured_output(r'''
        Render candidates: 'test_material' ...
            No matching materials.
        Available materials:
            No materials available.
        '''.replace('/', os.path.sep))

    def test_missing_definition(self):
        """
        Handle missing definition.
        """
        self.create_project()
        material_path = self.create_material('test_material')
        definition_path = material_path.joinpath('definition.py')
        definition_path.unlink()
        script = commandlinetools.ManageMaterialScript()
        command = ['--render', 'test_material']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(
                str(self.inner_project_path)):
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
                assert context_manager.exception.code == 1
        self.compare_captured_output(r'''
            Render candidates: 'test_material' ...
            Rendering test_project/materials/test_material/
                Importing test_project.materials.test_material.definition
            Traceback (most recent call last):
              File ".../ProjectPackageScript.py", line ..., in _import_path
                return importlib.import_module(path)
              ...
            ImportError: No module named 'test_project.materials.test_material.definition'
        '''.replace('/', os.path.sep))

    def test_python_cannot_render(self):
        """
        Handle un-renderables.
        """
        self.create_project()
        material_path = self.create_material('test_material')
        definition_path = material_path.joinpath('definition.py')
        with open(str(definition_path), 'w') as file_pointer:
            file_pointer.write(stringtools.normalize(r'''
            # -*- coding: utf-8 -*-

            test_material = None
            '''))
        script = commandlinetools.ManageMaterialScript()
        command = ['--render', 'test_material']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(
                str(self.inner_project_path)):
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
                assert context_manager.exception.code == 1
        self.compare_captured_output(r'''
            Render candidates: 'test_material' ...
            Rendering test_project/materials/test_material/
                Importing test_project.materials.test_material.definition
                Cannot render material of type NoneType.
        '''.replace('/', os.path.sep))

    def test_python_error_on_render(self):
        """
        Handle exceptions inside the Python module on __call__().
        """
        self.create_project()
        material_path = self.create_material('test_material')
        definition_path = material_path.joinpath('definition.py')
        with open(str(definition_path), 'w') as file_pointer:
            file_pointer.write(stringtools.normalize(r'''
            # -*- coding: utf-8 -*-

            class Foo(object):
                def __render__(self):
                    raise TypeError('This is fake.')

            test_material = Foo()
            '''))
        script = commandlinetools.ManageMaterialScript()
        command = ['--render', 'test_material']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(
                str(self.inner_project_path)):
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
                assert context_manager.exception.code == 1
        self.compare_captured_output(r'''
            Render candidates: 'test_material' ...
            Rendering test_project/materials/test_material/
                Importing test_project.materials.test_material.definition
            Traceback (most recent call last):
              File ".../ManageMaterialScript.py", line ..., in _render_one_material
                session = material.__render__()
              File ".../test_material/definition.py", line ..., in __render__
                raise TypeError('This is fake.')
            TypeError: This is fake.
        '''.replace('/', os.path.sep))

    def test_python_error_on_import(self):
        """
        Handle exceptions inside the Python module on import.
        """
        self.create_project()
        material_path = self.create_material('test_material')
        definition_path = material_path.joinpath('definition.py')
        with open(str(definition_path), 'a') as file_pointer:
            file_pointer.write('\n\nfailure = 1 / 0\n')
        script = commandlinetools.ManageMaterialScript()
        command = ['--render', 'test_material']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(
                str(self.inner_project_path)):
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
                assert context_manager.exception.code == 1
        self.compare_captured_output(r'''
        Render candidates: 'test_material' ...
        Rendering test_project/materials/test_material/
            Importing test_project.materials.test_material.definition
        Traceback (most recent call last):
          File ".../commandlinetools/ProjectPackageScript.py", line 183, in _import_path
            return importlib.import_module(path)
          ...
          File ".../test_project/test_project/materials/__init__.py", line 6, in <module>
            globals(),
          File ".../ImportManager.py", line 120, in import_material_packages
            output_module = __import__(output_module_path, fromlist=['*'])
          File ".../test_project/test_project/materials/test_material/definition.py", line 27, in <module>
            failure = 1 / 0
        ZeroDivisionError: division by zero
        '''.replace('/', os.path.sep))

    def test_supercollider_error(self):
        self.create_project()
        self.create_material('test_material')
        script = commandlinetools.ManageMaterialScript()
        command = ['--render', 'test_material']
        mock_path = nonrealtimetools.SessionRenderer.__module__
        mock_path += '._call_subprocess'
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(
                str(self.inner_project_path)):
                with self.assertRaises(SystemExit) as context_manager:
                    with mock.patch(mock_path) as call_mock:
                        call_mock.return_value = 1
                        script(command)
                assert context_manager.exception.code == 1
        self.compare_captured_output(r'''
        Render candidates: 'test_material' ...
        Rendering test_project/materials/test_material/
            Importing test_project.materials.test_material.definition
            Writing 95cecb2c724619fe502164459560ba5d.osc.
                Wrote 95cecb2c724619fe502164459560ba5d.osc.
            Rendering 95cecb2c724619fe502164459560ba5d.osc.
                Command: scsynth -N 95cecb2c724619fe502164459560ba5d.osc _ 95cecb2c724619fe502164459560ba5d.aiff 44100 aiff int24
                Rendered 95cecb2c724619fe502164459560ba5d.osc with exit code 1.
                SuperCollider errored!
            Python/SC runtime: 0 seconds
            Render failed. Exiting.
        '''.replace('/', os.path.sep))

    def test_supercollider_no_output(self):
        self.create_project()
        self.create_material('test_material')
        script = commandlinetools.ManageMaterialScript()
        command = ['--render', 'test_material']
        mock_path = nonrealtimetools.SessionRenderer.__module__
        mock_path += '._call_subprocess'
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(
                str(self.inner_project_path)):
                with self.assertRaises(SystemExit) as context_manager:
                    with mock.patch(mock_path) as call_mock:
                        call_mock.return_value = 0  # no output, but no error
                        script(command)
                assert context_manager.exception.code == 1
        self.compare_captured_output(r'''
        Render candidates: 'test_material' ...
        Rendering test_project/materials/test_material/
            Importing test_project.materials.test_material.definition
            Writing 95cecb2c724619fe502164459560ba5d.osc.
                Wrote 95cecb2c724619fe502164459560ba5d.osc.
            Rendering 95cecb2c724619fe502164459560ba5d.osc.
                Command: scsynth -N 95cecb2c724619fe502164459560ba5d.osc _ 95cecb2c724619fe502164459560ba5d.aiff 44100 aiff int24
                Rendered 95cecb2c724619fe502164459560ba5d.osc with exit code 0.
                Output file is missing!
            Python/SC runtime: 0 seconds
            Render failed. Exiting.
        '''.replace('/', os.path.sep))

    def test_success_all_materials(self):
        self.create_project()
        self.create_material('material_one')
        self.create_material('material_two')
        self.create_material('material_three')
        script = commandlinetools.ManageMaterialScript()
        command = ['--render', '*']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(
                str(self.inner_project_path)):
                try:
                    script(command)
                except SystemExit as e:
                    raise RuntimeError('SystemExit: {}'.format(e.code))
        self.compare_captured_output(r'''
        Render candidates: '*' ...
        Rendering test_project/materials/material_one/
            Importing test_project.materials.material_one.definition
            Writing 95cecb2c724619fe502164459560ba5d.osc.
                Wrote 95cecb2c724619fe502164459560ba5d.osc.
            Rendering 95cecb2c724619fe502164459560ba5d.osc.
                Command: scsynth -N 95cecb2c724619fe502164459560ba5d.osc _ 95cecb2c724619fe502164459560ba5d.aiff 44100 aiff int24
                Rendered 95cecb2c724619fe502164459560ba5d.osc with exit code 0.
            Writing renders/render.yml.
                Wrote renders/render.yml.
            Python/SC runtime: 0 seconds
            Rendered test_project/materials/material_one/
        Rendering test_project/materials/material_three/
            Importing test_project.materials.material_three.definition
            Writing 95cecb2c724619fe502164459560ba5d.osc.
                Skipped 95cecb2c724619fe502164459560ba5d.osc. File already exists.
            Rendering 95cecb2c724619fe502164459560ba5d.osc.
                Skipped 95cecb2c724619fe502164459560ba5d.osc. Output already exists.
            Writing renders/render.yml.
                Skipped renders/render.yml. File already exists.
            Python/SC runtime: 0 seconds
            Rendered test_project/materials/material_three/
        Rendering test_project/materials/material_two/
            Importing test_project.materials.material_two.definition
            Writing 95cecb2c724619fe502164459560ba5d.osc.
                Skipped 95cecb2c724619fe502164459560ba5d.osc. File already exists.
            Rendering 95cecb2c724619fe502164459560ba5d.osc.
                Skipped 95cecb2c724619fe502164459560ba5d.osc. Output already exists.
            Writing renders/render.yml.
                Skipped renders/render.yml. File already exists.
            Python/SC runtime: 0 seconds
            Rendered test_project/materials/material_two/
        '''.replace('/', os.path.sep))
        assert self.materials_path.joinpath(
            'material_one',
            'render.aiff',
            ).exists()
        assert self.materials_path.joinpath(
            'material_two',
            'render.aiff',
            ).exists()
        assert self.materials_path.joinpath(
            'material_three',
            'render.aiff',
            ).exists()
        assert self.sample(
            str(self.materials_path.joinpath('material_one', 'render.aiff'))
            ) == {
            0.0:  [2.3e-05] * 8,
            0.21: [0.210295] * 8,
            0.41: [0.410567] * 8,
            0.61: [0.610839] * 8,
            0.81: [0.811111] * 8,
            0.99: [0.991361] * 8,
            }
        assert self.sample(
            str(self.materials_path.joinpath('material_two', 'render.aiff'))
            ) == {
            0.0:  [2.3e-05] * 8,
            0.21: [0.210295] * 8,
            0.41: [0.410567] * 8,
            0.61: [0.610839] * 8,
            0.81: [0.811111] * 8,
            0.99: [0.991361] * 8,
            }
        assert self.sample(
            str(self.materials_path.joinpath('material_three', 'render.aiff'))
            ) == {
            0.0:  [2.3e-05] * 8,
            0.21: [0.210295] * 8,
            0.41: [0.410567] * 8,
            0.61: [0.610839] * 8,
            0.81: [0.811111] * 8,
            0.99: [0.991361] * 8,
            }

    def test_success_filtered_materials(self):
        self.create_project()
        self.create_material('material_one')
        self.create_material('material_two')
        self.create_material('material_three')
        script = commandlinetools.ManageMaterialScript()
        command = ['--render', 'material_t*']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(
                str(self.inner_project_path)):
                try:
                    script(command)
                except SystemExit as e:
                    raise RuntimeError('SystemExit: {}'.format(e.code))
        self.compare_captured_output(r'''
        Render candidates: 'material_t*' ...
        Rendering test_project/materials/material_three/
            Importing test_project.materials.material_three.definition
            Writing 95cecb2c724619fe502164459560ba5d.osc.
                Wrote 95cecb2c724619fe502164459560ba5d.osc.
            Rendering 95cecb2c724619fe502164459560ba5d.osc.
                Command: scsynth -N 95cecb2c724619fe502164459560ba5d.osc _ 95cecb2c724619fe502164459560ba5d.aiff 44100 aiff int24
                Rendered 95cecb2c724619fe502164459560ba5d.osc with exit code 0.
            Writing renders/render.yml.
                Wrote renders/render.yml.
            Python/SC runtime: 0 seconds
            Rendered test_project/materials/material_three/
        Rendering test_project/materials/material_two/
            Importing test_project.materials.material_two.definition
            Writing 95cecb2c724619fe502164459560ba5d.osc.
                Skipped 95cecb2c724619fe502164459560ba5d.osc. File already exists.
            Rendering 95cecb2c724619fe502164459560ba5d.osc.
                Skipped 95cecb2c724619fe502164459560ba5d.osc. Output already exists.
            Writing renders/render.yml.
                Skipped renders/render.yml. File already exists.
            Python/SC runtime: 0 seconds
            Rendered test_project/materials/material_two/
        '''.replace('/', os.path.sep))
        assert not self.materials_path.joinpath(
            'material_one',
            'render.aiff',
            ).exists()
        assert self.materials_path.joinpath(
            'material_two',
            'render.aiff',
            ).exists()
        assert self.materials_path.joinpath(
            'material_three',
            'render.aiff',
            ).exists()
        assert self.sample(
            str(self.materials_path.joinpath('material_two', 'render.aiff'))
            ) == {
            0.0:  [2.3e-05] * 8,
            0.21: [0.210295] * 8,
            0.41: [0.410567] * 8,
            0.61: [0.610839] * 8,
            0.81: [0.811111] * 8,
            0.99: [0.991361] * 8,
            }
        assert self.sample(
            str(self.materials_path.joinpath('material_three', 'render.aiff'))
            ) == {
            0.0:  [2.3e-05] * 8,
            0.21: [0.210295] * 8,
            0.41: [0.410567] * 8,
            0.61: [0.610839] * 8,
            0.81: [0.811111] * 8,
            0.99: [0.991361] * 8,
            }

    def test_success_one_material(self):
        self.create_project()
        self.create_material('test_material')
        script = commandlinetools.ManageMaterialScript()
        command = ['--render', 'test_material']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(
                str(self.inner_project_path)):
                try:
                    script(command)
                except SystemExit as e:
                    raise RuntimeError('SystemExit: {}'.format(e.code))
        self.compare_captured_output(r'''
        Render candidates: 'test_material' ...
        Rendering test_project/materials/test_material/
            Importing test_project.materials.test_material.definition
            Writing 95cecb2c724619fe502164459560ba5d.osc.
                Wrote 95cecb2c724619fe502164459560ba5d.osc.
            Rendering 95cecb2c724619fe502164459560ba5d.osc.
                Command: scsynth -N 95cecb2c724619fe502164459560ba5d.osc _ 95cecb2c724619fe502164459560ba5d.aiff 44100 aiff int24
                Rendered 95cecb2c724619fe502164459560ba5d.osc with exit code 0.
            Writing renders/render.yml.
                Wrote renders/render.yml.
            Python/SC runtime: 0 seconds
            Rendered test_project/materials/test_material/
        '''.replace('/', os.path.sep))
        self.compare_path_contents(
            self.inner_project_path,
            self.expected_files,
            )
        assert self.sample(
            str(self.materials_path.joinpath('test_material', 'render.aiff'))
            ) == {
            0.0:  [2.3e-05] * 8,
            0.21: [0.210295] * 8,
            0.41: [0.410567] * 8,
            0.61: [0.610839] * 8,
            0.81: [0.811111] * 8,
            0.99: [0.991361] * 8,
            }
