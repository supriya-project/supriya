import io
import os
import pytest
import supriya.cli
import uqbar.io
from cli_testbase import ProjectPackageScriptTestCase


class Test(ProjectPackageScriptTestCase):

    expected_files = [
        'test_project/test_project/materials/.gitignore',
        'test_project/test_project/materials/__init__.py',
        'test_project/test_project/materials/test_material/__init__.py',
        'test_project/test_project/materials/test_material/definition.py',
        ]

    def test_exists(self):
        string_io = io.StringIO()
        pytest.helpers.create_cli_project(self.test_path)
        pytest.helpers.create_cli_material(self.test_path, 'test_material')
        with uqbar.io.RedirectedStreams(stdout=string_io):
            pytest.helpers.create_cli_material(self.test_path, 'test_material', expect_error=True)
        pytest.helpers.compare_strings(
            r'''
            Creating material subpackage 'test_material' ...
                Path exists: test_project/materials/test_material
            '''.replace('/', os.path.sep),
            string_io.getvalue(),
            )

    def test_force_replace(self):
        string_io = io.StringIO()
        pytest.helpers.create_cli_project(self.test_path)
        pytest.helpers.create_cli_material(self.test_path, 'test_material')
        with uqbar.io.RedirectedStreams(stdout=string_io):
            pytest.helpers.create_cli_material(self.test_path, 'test_material', force=True)
        pytest.helpers.compare_strings(
            r'''
            Creating material subpackage 'test_material' ...
                Created test_project/materials/test_material/
            '''.replace('/', os.path.sep),
            string_io.getvalue(),
            )

    def test_internal_path(self):
        string_io = io.StringIO()
        pytest.helpers.create_cli_project(self.test_path)
        script = supriya.cli.ManageMaterialScript()
        command = ['--new', 'test_material']
        internal_path = self.assets_path
        assert internal_path.exists()
        with uqbar.io.RedirectedStreams(stdout=string_io):
            with uqbar.io.DirectoryChange(str(internal_path)):
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')
        pytest.helpers.compare_strings(
            r'''
            Creating material subpackage 'test_material' ...
                Created test_project/materials/test_material/
            '''.replace('/', os.path.sep),
            string_io.getvalue(),
            )

    def test_success(self):
        string_io = io.StringIO()
        pytest.helpers.create_cli_project(self.test_path)
        script = supriya.cli.ManageMaterialScript()
        command = ['--new', 'test_material']
        with uqbar.io.RedirectedStreams(stdout=string_io):
            with uqbar.io.DirectoryChange(
                str(self.inner_project_path)):
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')
        pytest.helpers.compare_strings(
            r'''
            Creating material subpackage 'test_material' ...
                Created test_project/materials/test_material/
            '''.replace('/', os.path.sep),
            string_io.getvalue(),
            )
        assert self.materials_path.joinpath('test_material').exists()
        self.compare_path_contents(self.materials_path, self.expected_files)
        definition_path = self.materials_path.joinpath(
            'test_material', 'definition.py')
        self.compare_file_contents(definition_path, '''
        import supriya
        from test_project import project_settings


        material = supriya.Session.from_project_settings(project_settings)

        with supriya.synthdefs.SynthDefBuilder(
            duration=1.,
            out_bus=0,
            ) as builder:
            source = supriya.ugens.Line.ar(
                duration=builder['duration'],
                )
            supriya.ugens.Out.ar(
                bus=builder['out_bus'],
                source=[source] * len(material.audio_output_bus_group),
                )
        ramp_synthdef = builder.build()

        with material.at(0):
            material.add_synth(
                duration=1,
                synthdef=ramp_synthdef,
                )
        ''')
