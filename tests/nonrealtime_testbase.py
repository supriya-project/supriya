import os
import pathlib
import shutil
import supriya.nonrealtime
import supriya.realtime
import supriya.soundfiles
import supriya.synthdefs
import supriya.system
import supriya.ugens


class TestCase(supriya.system.TestCase):

    test_directory_path = pathlib.Path(__file__).parent
    output_directory_path = test_directory_path / 'output'
    render_directory_path = test_directory_path / 'render'
    output_file_path = output_directory_path / 'output.aiff'
    render_yml_file_path = output_directory_path / 'render.yml'

    @classmethod
    def setUpClass(cls):
        cls.original_curdir = os.path.abspath(os.curdir)
        os.chdir(str(cls.test_directory_path))

    @classmethod
    def tearDownClass(cls):
        os.chdir(cls.original_curdir)

    def setUp(self):
        for path in [
            self.output_directory_path,
            self.render_directory_path,
            ]:
            path.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        for path in [
            self.output_directory_path,
            self.render_directory_path,
            ]:
            if path.exists():
                shutil.rmtree(str(path))
