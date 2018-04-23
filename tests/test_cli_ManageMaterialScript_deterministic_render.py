import os
import pytest
import supriya.cli
import uqbar.io
import uqbar.strings
from cli_testbase import ProjectPackageScriptTestCase


class Test(ProjectPackageScriptTestCase):

    module_contents = uqbar.strings.normalize('''
    import supriya.assets.synthdefs
    import supriya.patterns
    import supriya.nonrealtime


    material = supriya.nonrealtime.Session(0, 2)

    pattern = supriya.patterns.Pbus(
        supriya.patterns.Pbind(
            synthdef=supriya.assets.synthdefs.default,
            amplitude=supriya.patterns.Pwhite(),
            delta=supriya.patterns.Pwhite(0., 2.),
            duration=supriya.patterns.Pwhite(0.1, 0.5),
            frequency=supriya.patterns.Pwhite(minimum=55, maximum=1760),
            pan=supriya.patterns.Pwhite(-1.0, 1.0),
            )
        )

    with material.at(0):
        material.inscribe(pattern, duration=10, seed={seed!s})
    ''')

    def test_01(self):
        pytest.helpers.create_cli_project(self.test_path)
        material_path = self.create_cli_material('test_material')
        definition_path = material_path.joinpath('definition.py')
        with open(str(definition_path), 'w') as file_pointer:
            file_pointer.write(self.module_contents.format(seed=0))
        script = supriya.cli.ManageMaterialScript()
        command = ['--render', 'test_material']

        aiff_artifacts = sorted(self.renders_path.glob('*.aiff'))
        osc_artifacts = sorted(self.renders_path.glob('*.osc'))
        assert len(aiff_artifacts) == 0
        assert len(osc_artifacts) == 0

        with uqbar.io.RedirectedStreams(stdout=self.string_io):
            with uqbar.io.DirectoryChange(
                str(self.inner_project_path)):
                try:
                    script(command)
                except SystemExit as e:
                    raise RuntimeError('SystemExit: {}'.format(e.code))
        self.compare_captured_output(r'''
        Render candidates: 'test_material' ...
        Rendering test_project/materials/test_material/
            Importing test_project.materials.test_material.definition
            Writing session-96b415a72acd2a1835a3270714011314.osc.
                Wrote session-96b415a72acd2a1835a3270714011314.osc.
            Rendering session-96b415a72acd2a1835a3270714011314.osc.
                Command: scsynth -N session-96b415a72acd2a1835a3270714011314.osc _ session-96b415a72acd2a1835a3270714011314.aiff 44100 aiff int24 -i 0 -o 2
                Rendered session-96b415a72acd2a1835a3270714011314.osc with exit code 0.
            Writing test_project/materials/test_material/render.yml.
                Wrote test_project/materials/test_material/render.yml.
            Python/SC runtime: ... seconds
            Rendered test_project/materials/test_material/
        '''.replace('/', os.path.sep))

        self.reset_string_io()

        with uqbar.io.RedirectedStreams(stdout=self.string_io):
            with uqbar.io.DirectoryChange(
                str(self.inner_project_path)):
                try:
                    script(command)
                except SystemExit as e:
                    raise RuntimeError('SystemExit: {}'.format(e.code))
        self.compare_captured_output(r'''
        Render candidates: 'test_material' ...
        Rendering test_project/materials/test_material/
            Importing test_project.materials.test_material.definition
            Writing session-96b415a72acd2a1835a3270714011314.osc.
                Skipped session-96b415a72acd2a1835a3270714011314.osc. File already exists.
            Rendering session-96b415a72acd2a1835a3270714011314.osc.
                Skipped session-96b415a72acd2a1835a3270714011314.osc. Output already exists.
            Writing test_project/materials/test_material/render.yml.
                Skipped test_project/materials/test_material/render.yml. File already exists.
            Python/SC runtime: 0 seconds
            Rendered test_project/materials/test_material/
        '''.replace('/', os.path.sep))

        self.reset_string_io()

        with uqbar.io.RedirectedStreams(stdout=self.string_io):
            with uqbar.io.DirectoryChange(
                str(self.inner_project_path)):
                try:
                    script(command)
                except SystemExit as e:
                    raise RuntimeError('SystemExit: {}'.format(e.code))
        self.compare_captured_output(r'''
        Render candidates: 'test_material' ...
        Rendering test_project/materials/test_material/
            Importing test_project.materials.test_material.definition
            Writing session-96b415a72acd2a1835a3270714011314.osc.
                Skipped session-96b415a72acd2a1835a3270714011314.osc. File already exists.
            Rendering session-96b415a72acd2a1835a3270714011314.osc.
                Skipped session-96b415a72acd2a1835a3270714011314.osc. Output already exists.
            Writing test_project/materials/test_material/render.yml.
                Skipped test_project/materials/test_material/render.yml. File already exists.
            Python/SC runtime: 0 seconds
            Rendered test_project/materials/test_material/
        '''.replace('/', os.path.sep))

        aiff_artifacts = sorted(self.renders_path.glob('*.aiff'))
        osc_artifacts = sorted(self.renders_path.glob('*.osc'))
        assert len(aiff_artifacts) == 1
        assert len(osc_artifacts) == 1

    def test_02(self):
        pytest.helpers.create_cli_project(self.test_path)
        material_path = self.create_cli_material('test_material')
        definition_path = material_path.joinpath('definition.py')
        with open(str(definition_path), 'w') as file_pointer:
            file_pointer.write(self.module_contents.format(seed=None))
        script = supriya.cli.ManageMaterialScript()
        command = ['--render', 'test_material']

        aiff_artifacts = sorted(self.renders_path.glob('*.aiff'))
        osc_artifacts = sorted(self.renders_path.glob('*.osc'))
        assert len(aiff_artifacts) == 0
        assert len(osc_artifacts) == 0

        count = 10
        for _ in range(count):
            with uqbar.io.DirectoryChange(
                str(self.inner_project_path)):
                try:
                    script(command)
                except SystemExit as e:
                    raise RuntimeError('SystemExit: {}'.format(e.code))

        aiff_artifacts = sorted(self.renders_path.glob('*.aiff'))
        osc_artifacts = sorted(self.renders_path.glob('*.osc'))
        assert len(aiff_artifacts) == count
        assert len(osc_artifacts) == count
