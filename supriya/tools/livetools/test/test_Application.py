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
        # Buffers
        assert len(application.buffers) == 1
        assert 'birds' in application.buffers
        assert len(application.buffers['birds']) == 9
        # MIDI device
        assert application.device is not None
        # Mixer
        assert application.mixer is not None
        assert application.mixer.channel_count == 1
        assert application.mixer.cue_channel_count == 1
        assert len(application.mixer) == 4
        assert 'track-a' in application.mixer
        assert 'slot-one' in application.mixer['track-a']
        assert 'track-b' in application.mixer
        assert 'slot-two' in application.mixer['track-b']

    def test_02(self):
        try:
            application = livetools.Application(self.manifest_path)
            application.boot()
        finally:
            application.quit()
