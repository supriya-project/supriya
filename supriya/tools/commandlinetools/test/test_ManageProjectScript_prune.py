# -*- encoding: utf-8 -*-
import shutil
from abjad.tools import systemtools
from supriya.tools import commandlinetools
from base import ProjectPackageScriptTestCase


class Test(ProjectPackageScriptTestCase):

    def test_prune(self):
        self.create_project()
        self.create_material('material_one')
        self.create_material(
            'material_two',
            definition_contents=self.chained_session_template.render(
                input_material_name='material_one',
                output_material_name='material_two',
                multiplier=0.5,
                ),
            )
        self.create_material(
            'material_three',
            definition_contents=self.chained_session_template.render(
                input_material_name='material_two',
                output_material_name='material_three',
                multiplier=-1.0,
                ),
            )
        material_four_path = self.create_material(
            'material_four',
            definition_contents=self.chained_session_template.render(
                input_material_name='material_two',
                output_material_name='material_four',
                multiplier=0.125,
                ),
            )

        script = commandlinetools.ManageMaterialScript()
        command = ['--render', '*']
        with systemtools.TemporaryDirectoryChange(
            str(self.inner_project_path)):
            try:
                script(command)
            except SystemExit as e:
                raise RuntimeError('SystemExit: {}'.format(e.code))

        self.compare_path_contents(
            self.inner_project_path,
            [
                'test_project/test_project/__init__.py',
                'test_project/test_project/assets/.gitignore',
                'test_project/test_project/composites/.gitignore',
                'test_project/test_project/composites/__init__.py',
                'test_project/test_project/distribution/.gitignore',
                'test_project/test_project/etc/.gitignore',
                'test_project/test_project/materials/.gitignore',
                'test_project/test_project/materials/__init__.py',
                'test_project/test_project/materials/material_four/__init__.py',
                'test_project/test_project/materials/material_four/definition.py',
                'test_project/test_project/materials/material_four/render.aiff',
                'test_project/test_project/materials/material_four/render.yml',
                'test_project/test_project/materials/material_one/__init__.py',
                'test_project/test_project/materials/material_one/definition.py',
                'test_project/test_project/materials/material_one/render.aiff',
                'test_project/test_project/materials/material_one/render.yml',
                'test_project/test_project/materials/material_three/__init__.py',
                'test_project/test_project/materials/material_three/definition.py',
                'test_project/test_project/materials/material_three/render.aiff',
                'test_project/test_project/materials/material_three/render.yml',
                'test_project/test_project/materials/material_two/__init__.py',
                'test_project/test_project/materials/material_two/definition.py',
                'test_project/test_project/materials/material_two/render.aiff',
                'test_project/test_project/materials/material_two/render.yml',
                'test_project/test_project/metadata.json',
                'test_project/test_project/project-settings.yml',
                'test_project/test_project/renders/.gitignore',
                'test_project/test_project/renders/51af72cb1d8801ac035cdd449461c64b.aiff',
                'test_project/test_project/renders/51af72cb1d8801ac035cdd449461c64b.osc',
                'test_project/test_project/renders/76786aa4c87248615c1734dbc29f302e.aiff',
                'test_project/test_project/renders/76786aa4c87248615c1734dbc29f302e.osc',
                'test_project/test_project/renders/91654bbdefccdd74d4f221d2b9f5fe71.aiff',
                'test_project/test_project/renders/91654bbdefccdd74d4f221d2b9f5fe71.osc',
                'test_project/test_project/renders/95cecb2c724619fe502164459560ba5d.aiff',
                'test_project/test_project/renders/95cecb2c724619fe502164459560ba5d.osc',
                'test_project/test_project/synthdefs/.gitignore',
                'test_project/test_project/synthdefs/__init__.py',
                'test_project/test_project/test/.gitignore',
                'test_project/test_project/tools/.gitignore',
                'test_project/test_project/tools/__init__.py'
                ],
            )

        shutil.rmtree(str(material_four_path))

        script = commandlinetools.ManageProjectScript()
        command = ['--prune']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(
                str(self.inner_project_path)):
                try:
                    script(command)
                except SystemExit as e:
                    raise RuntimeError('SystemExit: {}'.format(e.code))

        self.compare_path_contents(
            self.inner_project_path,
            [
                'test_project/test_project/__init__.py',
                'test_project/test_project/assets/.gitignore',
                'test_project/test_project/composites/.gitignore',
                'test_project/test_project/composites/__init__.py',
                'test_project/test_project/distribution/.gitignore',
                'test_project/test_project/etc/.gitignore',
                'test_project/test_project/materials/.gitignore',
                'test_project/test_project/materials/__init__.py',
                'test_project/test_project/materials/material_one/__init__.py',
                'test_project/test_project/materials/material_one/definition.py',
                'test_project/test_project/materials/material_one/render.aiff',
                'test_project/test_project/materials/material_one/render.yml',
                'test_project/test_project/materials/material_three/__init__.py',
                'test_project/test_project/materials/material_three/definition.py',
                'test_project/test_project/materials/material_three/render.aiff',
                'test_project/test_project/materials/material_three/render.yml',
                'test_project/test_project/materials/material_two/__init__.py',
                'test_project/test_project/materials/material_two/definition.py',
                'test_project/test_project/materials/material_two/render.aiff',
                'test_project/test_project/materials/material_two/render.yml',
                'test_project/test_project/metadata.json',
                'test_project/test_project/project-settings.yml',
                'test_project/test_project/renders/.gitignore',
                'test_project/test_project/renders/76786aa4c87248615c1734dbc29f302e.aiff',
                'test_project/test_project/renders/76786aa4c87248615c1734dbc29f302e.osc',
                'test_project/test_project/renders/91654bbdefccdd74d4f221d2b9f5fe71.aiff',
                'test_project/test_project/renders/91654bbdefccdd74d4f221d2b9f5fe71.osc',
                'test_project/test_project/renders/95cecb2c724619fe502164459560ba5d.aiff',
                'test_project/test_project/renders/95cecb2c724619fe502164459560ba5d.osc',
                'test_project/test_project/synthdefs/.gitignore',
                'test_project/test_project/synthdefs/__init__.py',
                'test_project/test_project/test/.gitignore',
                'test_project/test_project/tools/.gitignore',
                'test_project/test_project/tools/__init__.py'
                ],
            )

        self.compare_captured_output(r'''
        Pruning test_project/renders ...
            Pruned test_project/renders/51af72cb1d8801ac035cdd449461c64b.aiff
            Pruned test_project/renders/51af72cb1d8801ac035cdd449461c64b.osc
        ''')
