# -*- encoding: utf-8 -*-
from abjad.tools import systemtools
from supriya.tools import commandlinetools
from base import ProjectPackageScriptTestCase


class Test(ProjectPackageScriptTestCase):

    def test_clean(self):
        self.create_project()
        self.create_material(
            'material_one',
            definition_contents=self.basic_session_template.render(
                material_name='material_one',
                ),
            )
        self.create_material(
            'material_two',
            definition_contents=self.basic_session_template.render(
                material_name='material_two',
                multiplier=0.5,
                ),
            )
        self.create_material(
            'material_three',
            definition_contents=self.basic_session_template.render(
                material_name='material_three',
                multiplier=0.25,
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
                'test_project/test_project/renders/5ec1eb97cfc0e98291f27464546df568.aiff',
                'test_project/test_project/renders/5ec1eb97cfc0e98291f27464546df568.osc',
                'test_project/test_project/renders/95cecb2c724619fe502164459560ba5d.aiff',
                'test_project/test_project/renders/95cecb2c724619fe502164459560ba5d.osc',
                'test_project/test_project/renders/e628a25fe369270f786d60fbbc047365.aiff',
                'test_project/test_project/renders/e628a25fe369270f786d60fbbc047365.osc',
                'test_project/test_project/synthdefs/.gitignore',
                'test_project/test_project/synthdefs/__init__.py',
                'test_project/test_project/test/.gitignore',
                'test_project/test_project/tools/.gitignore',
                'test_project/test_project/tools/__init__.py'
                ],
            )

        script = commandlinetools.ManageProjectScript()
        command = ['--clean']
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
                'test_project/test_project/synthdefs/.gitignore',
                'test_project/test_project/synthdefs/__init__.py',
                'test_project/test_project/test/.gitignore',
                'test_project/test_project/tools/.gitignore',
                'test_project/test_project/tools/__init__.py'
                ],
            )

        self.compare_captured_output(r'''
        Cleaning test_project/renders ...
            Cleaned test_project/renders/5ec1eb97cfc0e98291f27464546df568.aiff
            Cleaned test_project/renders/5ec1eb97cfc0e98291f27464546df568.osc
            Cleaned test_project/renders/95cecb2c724619fe502164459560ba5d.aiff
            Cleaned test_project/renders/95cecb2c724619fe502164459560ba5d.osc
            Cleaned test_project/renders/e628a25fe369270f786d60fbbc047365.aiff
            Cleaned test_project/renders/e628a25fe369270f786d60fbbc047365.osc
        ''')
