import pathlib
import supriya


class TestCase(supriya.systemtools.TestCase):

    def setUp(self):
        super(supriya.systemtools.TestCase, self).setUp()
        self.server = supriya.Server.get_default_server()
        self.manifest_path = (
            pathlib.Path(supriya.__path__[0]) /
            'assets' /
            'applications' /
            'Test.yml'
            )

    def tearDown(self):
        self.server.quit()
        super(supriya.systemtools.TestCase, self).tearDown()

    def test_01(self):
        application = supriya.livetools.Application(self.manifest_path)
        # Buffers
        assert len(application.buffers) == 1
        assert 'birds' in application.buffers
        assert len(application.buffers['birds']) == 9
        # MIDI devices
        assert application.devices is not None
        assert application.devices['test'] is not None
        # Mixer
        assert application.mixer is not None
        assert application.mixer.channel_count == 2
        assert application.mixer.cue_channel_count == 2
        assert len(application.mixer) == 4
        assert 'track-a' in application.mixer
        assert 'slot-one' in application.mixer['track-a']
        assert 'track-b' in application.mixer
        assert 'slot-two' in application.mixer['track-b']

    def test_02(self):
        try:
            application = supriya.livetools.Application(self.manifest_path)
            application.boot()
        finally:
            application.quit()

    def test_03(self):
        application = supriya.Application('supriya:applications/Test2.yml')
        # MIDI devices
        assert application.devices is not None
        assert isinstance(application.devices['nano_a'], supriya.Device)
        assert isinstance(application.devices['nano_b'], supriya.Device)
        # Mixer
        mixer = application.mixer
        assert mixer is not None
        assert mixer.channel_count == 2
        assert mixer.cue_channel_count == 2
        # Tracks
        assert len(mixer) == 6
        assert 'track-a' in mixer
        assert 'track-b' in mixer
        assert 'track-c' in mixer
        assert 'track-d' in mixer
        # Sends
        assert sorted(mixer['track-a'].send) == ['master', 'track-c', 'track-d']
        assert sorted(mixer['track-b'].send) == ['master', 'track-c', 'track-d']
        assert sorted(mixer['track-c'].send) == ['master']
        assert sorted(mixer['track-d'].send) == ['master']
        # Binding
        assert len(application.bindings) == 5
