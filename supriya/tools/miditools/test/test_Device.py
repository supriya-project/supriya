from abjad.tools import systemtools
from supriya.tools import miditools


class TestCase(systemtools.TestCase):

    def test_01(self):
        manifest_path = 'APC40'
        device = miditools.Device(manifest_path)
        message = [0x90, 0x35, 0x7F]
        physical_manifest = device.physical_manifest
        physical_control, value = physical_manifest(message, 0.0)
        assert physical_control.name == 'clip_launch_1x1'
        assert value == 1.0
