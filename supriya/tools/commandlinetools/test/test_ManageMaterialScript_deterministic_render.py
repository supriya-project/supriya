# -*- encoding: utf-8 -*-
import os
from abjad.tools import stringtools
from abjad.tools import systemtools
from supriya.tools import commandlinetools
from base import ProjectPackageScriptTestCase


class Test(ProjectPackageScriptTestCase):

    module_contents = stringtools.normalize('''
    # -*- coding: utf-8 -*-
    from supriya import (
        Session,
        patterntools,
        synthdefs,
    )


    test_material = Session(0, 2)

    pattern = patterntools.Pbus(
        patterntools.Pbind(
            synthdef=synthdefs.default,
            amplitude=patterntools.Pwhite(),
            delta=patterntools.Pwhite(0., 2.),
            duration=patterntools.Pwhite(0.1, 0.5),
            frequency=patterntools.Pwhite(minimum=55, maximum=1760),
            pan=patterntools.Pwhite(-1.0, 1.0),
            )
        )

    with test_material.at(0):
        test_material.inscribe(pattern, duration=10, seed={seed!s})
    ''')

    def test_01(self):
        self.create_project()
        material_path = self.create_material('test_material')
        definition_path = material_path.joinpath('definition.py')
        with open(str(definition_path), 'w') as file_pointer:
            file_pointer.write(self.module_contents.format(seed=0))
        script = commandlinetools.ManageMaterialScript()
        command = ['--render', 'test_material']

        aiff_artifacts = list(self.renders_path.glob('*.aiff'))
        osc_artifacts = list(self.renders_path.glob('*.osc'))
        assert len(aiff_artifacts) == 0
        assert len(osc_artifacts) == 0

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
            Writing cc0574461ace85f1fe1798cc15a59575.osc.
                Wrote cc0574461ace85f1fe1798cc15a59575.osc.
            Rendering cc0574461ace85f1fe1798cc15a59575.osc.
                Command: scsynth -N cc0574461ace85f1fe1798cc15a59575.osc _ cc0574461ace85f1fe1798cc15a59575.aiff 44100 aiff int24 -i 0 -o 2
                Rendered cc0574461ace85f1fe1798cc15a59575.osc with exit code 0.
            Writing test_project/materials/test_material/render.yml.
                Wrote test_project/materials/test_material/render.yml.
            Python/SC runtime: 0 seconds
            Rendered test_project/materials/test_material/
        '''.replace('/', os.path.sep))

        self.reset_string_io()

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
            Writing cc0574461ace85f1fe1798cc15a59575.osc.
                Skipped cc0574461ace85f1fe1798cc15a59575.osc. File already exists.
            Rendering cc0574461ace85f1fe1798cc15a59575.osc.
                Skipped cc0574461ace85f1fe1798cc15a59575.osc. Output already exists.
            Writing test_project/materials/test_material/render.yml.
                Skipped test_project/materials/test_material/render.yml. File already exists.
            Python/SC runtime: 0 seconds
            Rendered test_project/materials/test_material/
        '''.replace('/', os.path.sep))

        self.reset_string_io()

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
            Writing cc0574461ace85f1fe1798cc15a59575.osc.
                Skipped cc0574461ace85f1fe1798cc15a59575.osc. File already exists.
            Rendering cc0574461ace85f1fe1798cc15a59575.osc.
                Skipped cc0574461ace85f1fe1798cc15a59575.osc. Output already exists.
            Writing test_project/materials/test_material/render.yml.
                Skipped test_project/materials/test_material/render.yml. File already exists.
            Python/SC runtime: 0 seconds
            Rendered test_project/materials/test_material/
        '''.replace('/', os.path.sep))

        aiff_artifacts = list(self.renders_path.glob('*.aiff'))
        osc_artifacts = list(self.renders_path.glob('*.osc'))
        assert len(aiff_artifacts) == 1
        assert len(osc_artifacts) == 1

    def test_02(self):
        self.create_project()
        material_path = self.create_material('test_material')
        definition_path = material_path.joinpath('definition.py')
        with open(str(definition_path), 'w') as file_pointer:
            file_pointer.write(self.module_contents.format(seed=None))
        script = commandlinetools.ManageMaterialScript()
        command = ['--render', 'test_material']

        aiff_artifacts = list(self.renders_path.glob('*.aiff'))
        osc_artifacts = list(self.renders_path.glob('*.osc'))
        assert len(aiff_artifacts) == 0
        assert len(osc_artifacts) == 0

        count = 10
        for _ in range(count):
            with systemtools.TemporaryDirectoryChange(
                str(self.inner_project_path)):
                try:
                    script(command)
                except SystemExit as e:
                    raise RuntimeError('SystemExit: {}'.format(e.code))

        aiff_artifacts = list(self.renders_path.glob('*.aiff'))
        osc_artifacts = list(self.renders_path.glob('*.osc'))
        assert len(aiff_artifacts) == count
        assert len(osc_artifacts) == count
