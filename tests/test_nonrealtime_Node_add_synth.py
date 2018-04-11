import supriya.nonrealtime
import supriya.assets.synthdefs
from nonrealtime_testbase import TestCase
import supriya.nonrealtime


class TestCase(TestCase):

    def test_01(self):
        """
        With Session.at(...) context manager.
        """
        session = supriya.nonrealtime.Session()
        with session.at(5):
            node = session.add_synth(duration=10)
        assert isinstance(node, supriya.nonrealtime.Synth)
        assert node in session.nodes
        assert node.start_offset == 5
        assert node.stop_offset == 15

    def test_02(self):
        """
        With offset=... keyword.
        """
        session = supriya.nonrealtime.Session()
        node = session.add_synth(duration=10, offset=5)
        assert isinstance(node, supriya.nonrealtime.Synth)
        assert node in session.nodes
        assert node.start_offset == 5
        assert node.stop_offset == 15

    def test_03(self):
        """
        Without Session.at(...) context manager or offset keyword.
        """
        session = supriya.nonrealtime.Session()
        with self.assertRaises(ValueError):
            session.add_synth(duration=10)

    def test_04(self):
        """
        With both Session.at(...) context manager and offset keyword.
        """
        session = supriya.nonrealtime.Session()
        with session.at(5):
            node = session.add_synth(duration=10, offset=13)
        assert isinstance(node, supriya.nonrealtime.Synth)
        assert node in session.nodes
        assert node.start_offset == 13
        assert node.stop_offset == 23

    def test_05(self):
        """
        Mismatch.
        """
        session = supriya.nonrealtime.Session()
        with session.at(5):
            node = session.add_synth(duration=10, offset=13)
            with self.assertRaises(ValueError):
                node.add_synth(duration=1)

    def test_06(self):
        """
        Defaults.
        """
        session = supriya.nonrealtime.Session()
        with session.at(0):
            synth = session.add_synth()
        assert synth.synthdef == supriya.assets.synthdefs.default
        assert synth.duration == float('inf')
        assert synth.start_offset == 0.
