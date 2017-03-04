# -*- encoding: utf-8 -*-
import pathlib
import shutil
import sys
from abjad.tools import systemtools
from supriya.tools import commandlinetools
from supriya.tools import soundfiletools


class ProjectPackageScriptTestCase(systemtools.TestCase):

    package_name = 'test_project'
    test_path = pathlib.Path(__file__).parent
    outer_project_path = test_path.joinpath(package_name)
    inner_project_path = outer_project_path.joinpath(package_name)
    assets_path = inner_project_path.joinpath('assets')
    composites_path = inner_project_path.joinpath('composites')
    distribution_path = inner_project_path.joinpath('distribution')
    materials_path = inner_project_path.joinpath('materials')
    renders_path = inner_project_path.joinpath('renders')
    synthdefs_path = inner_project_path.joinpath('synthdefs')
    tools_path = inner_project_path.joinpath('tools')

    ### TEST LIFECYCLE ###

    def setUp(self):
        super(ProjectPackageScriptTestCase, self).setUp()
        if self.outer_project_path.exists():
            shutil.rmtree(str(self.outer_project_path))
        self.directory_items = set(self.test_path.iterdir())
        sys.path.insert(0, str(self.outer_project_path))

    def tearDown(self):
        super(ProjectPackageScriptTestCase, self).tearDown()
        for path in sorted(self.test_path.iterdir()):
            if path in self.directory_items:
                continue
            if path.is_file():
                path.unlink()
            else:
                shutil.rmtree(str(path))
        sys.path.remove(str(self.outer_project_path))
        for path, module in tuple(sys.modules.items()):
            if not path or not module:
                continue
            if path.startswith(self.package_name):
                del(sys.modules[path])

    ### UTILITY METHODS ###

    def create_material(
        self,
        material_name='test_material',
        force=False,
        expect_error=False,
        ):
        script = commandlinetools.ManageMaterialScript()
        command = ['--new', material_name]
        if force:
            command.insert(0, '-f')
        with systemtools.TemporaryDirectoryChange(str(self.inner_project_path)):
            if expect_error:
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
                assert context_manager.exception.code == 1
            else:
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')
        return self.inner_project_path.joinpath(
            'materials',
            material_name,
            )

    def create_project(self, force=False, expect_error=False):
        script = commandlinetools.ManageProjectScript()
        command = [
            '--new',
            'Test Project',
            '-n', 'Josiah Wolf Oberholtzer',
            '-e', 'josiah.oberholtzer@gmail.com',
            '-g', 'josiah-wolf-oberholtzer',
            '-w', 'www.josiahwolfoberholtzer.com',
            '-l', 'amazing_library',
            ]
        if force:
            command.insert(0, '-f')
        with systemtools.TemporaryDirectoryChange(str(self.test_path)):
            if expect_error:
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
                assert context_manager.exception.code == 1
            else:
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')

    def sample(self, file_path):
        soundfile = soundfiletools.SoundFile(file_path)
        return {
            0.0: [round(x, 6) for x in soundfile.at_percent(0)],
            0.21: [round(x, 6) for x in soundfile.at_percent(0.21)],
            0.41: [round(x, 6) for x in soundfile.at_percent(0.41)],
            0.61: [round(x, 6) for x in soundfile.at_percent(0.61)],
            0.81: [round(x, 6) for x in soundfile.at_percent(0.81)],
            0.99: [round(x, 6) for x in soundfile.at_percent(0.99)],
            }

