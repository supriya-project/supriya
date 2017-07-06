import pathlib
from supriya.tools import livetools
from supriya.tools import servertools
from abjad.tools import systemtools as abjad_systemtools


class TestCase(abjad_systemtools.TestCase):

    def setUp(self):
        import supriya
        super(abjad_systemtools.TestCase, self).setUp()
        self.server = servertools.Server.get_default_server()
        self.manifest_path = (
            pathlib.Path(supriya.__path__[0]) /
            'assets' /
            'applications' /
            'Test.yml'
            )

    def tearDown(self):
        self.server.quit()
        super(abjad_systemtools.TestCase, self).tearDown()

    def test_01(self):
        application = livetools.Application(self.manifest_path)
