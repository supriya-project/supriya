import uqbar.io
from unittest import mock
from abjad import abjad_configuration
from supriya import systemtools
from supriya.tools import commandlinetools
from commandlinetools_testbase import ProjectPackageScriptTestCase


class Test(ProjectPackageScriptTestCase):

    @mock.patch('supriya.tools.commandlinetools.ProjectPackageScript._call_subprocess')
    def test_success(self, call_subprocess_mock):
        call_subprocess_mock.return_value = 0
        self.create_project()
        material_path = self.create_material('test_material')
        script = commandlinetools.ManageMaterialScript()
        command = ['--edit', 'test_material']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with uqbar.io.DirectoryChange(
                str(self.inner_project_path)):
                try:
                    script(command)
                except SystemExit as e:
                    raise RuntimeError('SystemExit: {}'.format(e.code))
        self.compare_captured_output(r'''
        Edit candidates: 'test_material' ...
        ''')
        definition_path = material_path.joinpath('definition.py')
        command = '{} {!s}'.format(
            abjad_configuration.get_text_editor(),
            definition_path,
            )
        call_subprocess_mock.assert_called_with(command)
