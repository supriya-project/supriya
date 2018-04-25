import pathlib
import shutil
import sys
import unittest


class ProjectPackageScriptTestCase(unittest.TestCase):

    package_name = 'test_project'
    test_path = pathlib.Path(__file__).parent
    outer_project_path = test_path.joinpath(package_name)
    inner_project_path = outer_project_path.joinpath(package_name)
    assets_path = inner_project_path.joinpath('assets')
    sessions_path = inner_project_path.joinpath('sessions')
    distribution_path = inner_project_path.joinpath('distribution')
    materials_path = inner_project_path.joinpath('materials')
    renders_path = inner_project_path.joinpath('renders')
    synthdefs_path = inner_project_path.joinpath('synthdefs')
    tools_path = inner_project_path.joinpath('tools')

    ### TEST LIFECYCLE ###

    def setUp(self):
        if self.outer_project_path.exists():
            shutil.rmtree(str(self.outer_project_path))
        self.directory_items = set(self.test_path.iterdir())
        sys.path.insert(0, str(self.outer_project_path))

    def tearDown(self):
        for path, module in tuple(sys.modules.items()):
            if not path or not module:
                continue
            if path.startswith(self.package_name):
                del(sys.modules[path])
