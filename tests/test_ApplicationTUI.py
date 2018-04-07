import supriya


class TestCase(supriya.systemtools.TestCase):

    def test_01(self):
        manifest_path = 'supriya:applications/Test.yml'
        application = supriya.livetools.Application(manifest_path)
        tui = application.tui()
        assert tui is not None
