import os
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
        self.create_project()
        self.create_material('test_material')
        with uqbar.io.RedirectedStreams(stdout=self.string_io):
            self.create_material('test_material', expect_error=True)
        self.compare_captured_output(r'''
            Creating material subpackage 'test_material' ...
                Path exists: test_project/materials/test_material
        '''.replace('/', os.path.sep))

    def test_force_replace(self):
        self.create_project()
        self.create_material('test_material')
        with uqbar.io.RedirectedStreams(stdout=self.string_io):
            self.create_material('test_material', force=True)
        self.compare_captured_output(r'''
            Creating material subpackage 'test_material' ...
                Created test_project/materials/test_material/
        '''.replace('/', os.path.sep))

    def test_internal_path(self):
        self.create_project()
        script = supriya.cli.ManageMaterialScript()
        command = ['--new', 'test_material']
        internal_path = self.assets_path
        assert internal_path.exists()
        with uqbar.io.RedirectedStreams(stdout=self.string_io):
            with uqbar.io.DirectoryChange(str(internal_path)):
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')
        self.compare_captured_output(r'''
            Creating material subpackage 'test_material' ...
                Created test_project/materials/test_material/
        '''.replace('/', os.path.sep))

    def test_success(self):
        self.create_project()
        script = supriya.cli.ManageMaterialScript()
        command = ['--new', 'test_material']
        with uqbar.io.RedirectedStreams(stdout=self.string_io):
            with uqbar.io.DirectoryChange(
                str(self.inner_project_path)):
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')
        self.compare_captured_output(r'''
            Creating material subpackage 'test_material' ...
                Created test_project/materials/test_material/
        '''.replace('/', os.path.sep))
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
