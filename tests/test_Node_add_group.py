from nonrealtimetools_testbase import TestCase
from supriya.tools import nonrealtimetools


class TestCase(TestCase):

    def test_01(self):
        """
        With Session.at(...) context manager.
        """
        session = nonrealtimetools.Session()
        with session.at(5):
            node = session.add_group(duration=10)
        assert isinstance(node, nonrealtimetools.Group)
        assert node in session.nodes
        assert node.start_offset == 5
        assert node.stop_offset == 15

    def test_02(self):
        """
        With offset=... keyword.
        """
        session = nonrealtimetools.Session()
        node = session.add_group(duration=10, offset=5)
        assert isinstance(node, nonrealtimetools.Group)
        assert node in session.nodes
        assert node.start_offset == 5
        assert node.stop_offset == 15

    def test_03(self):
        """
        Without Session.at(...) context manager or offset keyword.
        """
        session = nonrealtimetools.Session()
        with self.assertRaises(ValueError):
            session.add_group(duration=10)

    def test_04(self):
        """
        With both Session.at(...) context manager and offset keyword.
        """
        session = nonrealtimetools.Session()
        with session.at(5):
            node = session.add_group(duration=10, offset=13)
        assert isinstance(node, nonrealtimetools.Group)
        assert node in session.nodes
        assert node.start_offset == 13
        assert node.stop_offset == 23

    def test_05(self):
        """
        Mismatch.
        """
        session = nonrealtimetools.Session()
        with session.at(5):
            node = session.add_group(duration=10, offset=13)
            with self.assertRaises(ValueError):
                node.add_group(duration=1)
